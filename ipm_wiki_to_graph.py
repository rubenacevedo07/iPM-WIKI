#!/usr/bin/env python3
"""
IPM Wiki → Graph Sync
=====================
Reads enriched .md wiki pages and syncs structured data back to IPMDB.

Pipeline:
  wiki .md files (human+LLM enriched)
    → parse frontmatter + sections
    → validate against DB
    → upsert new/updated edges, events, scores
    → report drift (wiki says X, DB has Y)

Usage:
  python3 ipm_wiki_to_graph.py \
    --wiki-dir ./wiki/companies \
    --host localhost --port 5432 \
    --db IPMDB --user postgres --password <pw> \
    --dry-run          # just report, don't write
    --sync             # write changes to DB
"""

import argparse
import os
import re
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("pip install psycopg2-binary --break-system-packages")
    sys.exit(1)

# ── Parser ─────────────────────────────────────────────────────────────────────

def parse_frontmatter(text):
    """Extract YAML-like frontmatter between --- delimiters."""
    m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip()
    return fm

def parse_power_scores(text):
    """Extract dimension scores from the markdown score table."""
    scores = {}
    dim_map = {
        'Financial': 'financial', 'Military': 'military',
        'Political': 'political', 'Technological': 'technological',
        'Industrial': 'industrial', 'Information': 'information',
    }
    for dim, key in dim_map.items():
        m = re.search(rf'\|\s*{dim}\s*\|\s*(\d+)\s*\|', text)
        if m:
            scores[key] = int(m.group(1))
    return scores

def parse_edges(text):
    """Extract outbound edges from the Relations table in wiki."""
    edges = []
    # Find outbound section
    m = re.search(r'### Outbound.*?\n(.*?)(?=###|\Z)', text, re.DOTALL)
    if not m:
        return edges
    table = m.group(1)
    # Parse table rows: | strength_emoji Strength | **Target** | `EdgeType` | Description |
    for row in table.splitlines():
        cells = [c.strip() for c in row.split('|') if c.strip()]
        if len(cells) < 3 or cells[0].startswith('-'):
            continue
        # Skip header row
        if 'Strength' in cells[0] or 'Target' in cells[1]:
            continue
        strength_raw = cells[0]
        target_raw   = cells[1]
        etype_raw    = cells[2] if len(cells) > 2 else ''
        desc_raw     = cells[3] if len(cells) > 3 else ''

        # Extract strength
        strength = re.sub(r'[🔴🟠🟡⚪]', '', strength_raw).strip()

        # Extract target name (remove ** markdown)
        target_name = re.sub(r'\*\*', '', target_raw).strip()

        # Extract edge type (remove backticks)
        edge_type = etype_raw.replace('`', '').strip()

        # Truncate description
        desc = desc_raw[:120]

        if edge_type and target_name and strength:
            edges.append({
                'target_name': target_name,
                'edge_type':   edge_type,
                'strength':    strength,
                'description': desc,
                'from_wiki':   True,
            })
    return edges

def parse_news(text):
    """Extract news events from wiki."""
    events = []
    # Each event is a ### date — headline
    pattern = re.compile(
        r'###\s+(\d{4}-\d{2}-\d{2})\s+—\s+(.+?)\n'
        r'`([^`]+)`[^\n]*\n'
        r'(?:\[[^\]]+\]\([^\)]+\)\n)?'
        r'\n([^\n#]+)',
        re.MULTILINE
    )
    for m in pattern.finditer(text):
        date, headline, importance, summary = m.groups()
        events.append({
            'date':      date,
            'headline':  headline.strip(),
            'importance': importance.strip(),
            'summary':   summary.strip()[:300],
        })
    return events

# ── DB helpers ──────────────────────────────────────────────────────────────────

def get_company_db(cur, company_id):
    cur.execute('''
        SELECT pi."CompositeScore", pi."FinancialScore", pi."MilitaryScore",
               pi."PoliticalScore", pi."TechnologicalScore",
               pi."IndustrialScore", pi."InformationScore",
               pi."ArchetypeCode", pi."TrendDirection"
        FROM public."CompanyPowerIndex" pi
        WHERE pi."CompanyId" = %s
    ''', (company_id,))
    return cur.fetchone()

def get_company_edges(cur, company_id):
    cur.execute('''
        SELECT re."EdgeType", re."Strength", re."Label",
               CASE
                 WHEN re."TargetType"='Company' THEN tc."Name"
                 WHEN re."TargetType"='Country' THEN tct."Name"
                 WHEN re."TargetType"='Person'  THEN tp."Name" || ' ' || tp."LastName"
               END as "TargetName"
        FROM public."RelationEdge" re
        LEFT JOIN public."Companies" tc  ON re."TargetType"='Company'  AND tc."Id"=re."TargetId"
        LEFT JOIN public."Countries" tct ON re."TargetType"='Country'  AND tct."Id"=re."TargetId"
        LEFT JOIN public."Persons"   tp  ON re."TargetType"='Person'   AND tp."Id"=re."TargetId"
        WHERE re."SourceId"=%s AND re."SourceType"='Company'
          AND re."IsDeleted"=false
    ''', (company_id,))
    return {(r['TargetName'], r['EdgeType']): r for r in cur.fetchall()}

def resolve_company_id(cur, name):
    cur.execute('SELECT "Id" FROM public."Companies" WHERE "Name" ILIKE %s LIMIT 1', (f'%{name}%',))
    r = cur.fetchone()
    return r['Id'] if r else None

# ── Sync logic ──────────────────────────────────────────────────────────────────

STRENGTH_ORDER = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
DIM_COL = {
    'financial': 'FinancialScore', 'military': 'MilitaryScore',
    'political': 'PoliticalScore', 'technological': 'TechnologicalScore',
    'industrial': 'IndustrialScore', 'information': 'InformationScore',
}

def sync_wiki_page(conn, wiki_file, dry_run=True):
    text = Path(wiki_file).read_text(encoding='utf-8')
    fm   = parse_frontmatter(text)

    entity_id = fm.get('entity_id')
    if not entity_id:
        return {'file': wiki_file, 'status': 'SKIP', 'reason': 'no entity_id in frontmatter'}

    try:
        entity_id = int(entity_id)
    except ValueError:
        return {'file': wiki_file, 'status': 'SKIP', 'reason': f'invalid entity_id: {entity_id}'}

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    report = {
        'entity_id': entity_id,
        'file': os.path.basename(wiki_file),
        'score_drift': [],
        'missing_edges': [],
        'missing_news': [],
        'synced': [],
        'errors': [],
    }

    # ── 1. Score drift detection ────────────────────────────────────────────
    wiki_scores = parse_power_scores(text)
    db_pi = get_company_db(cur, entity_id)

    if db_pi and wiki_scores:
        for dim, col in DIM_COL.items():
            wiki_val = wiki_scores.get(dim)
            db_val   = float(db_pi[col]) if db_pi[col] is not None else None
            if wiki_val is not None and db_val is not None and abs(wiki_val - db_val) > 0.5:
                report['score_drift'].append({
                    'dim': dim, 'wiki': wiki_val, 'db': round(db_val, 1)
                })

        # Composite from frontmatter
        wiki_composite = fm.get('composite_score')
        if wiki_composite:
            try:
                wiki_composite = float(wiki_composite)
                db_composite   = float(db_pi['CompositeScore'])
                if abs(wiki_composite - db_composite) > 0.5:
                    report['score_drift'].append({
                        'dim': 'composite', 'wiki': wiki_composite, 'db': round(db_composite, 1)
                    })
            except (ValueError, TypeError):
                pass

    # ── 2. Edge gap detection ───────────────────────────────────────────────
    wiki_edges = parse_edges(text)
    db_edges   = get_company_edges(cur, entity_id)

    for we in wiki_edges:
        key = (we['target_name'], we['edge_type'])
        tname = we['target_name']
        if tname.startswith('[') or tname == 'Unknown': continue  # non-standard TargetType
        if not any((tn is not None) and (tn in tname or tname in tn)
                   for tn, _ in db_edges.keys()):
            # Target not found in DB edges at all
            report['missing_edges'].append(we)
        else:
            # Check if strength differs
            matching = [(tn, et) for tn, et in db_edges
                        if tn is not None and (we['target_name'].lower() in tn.lower() or tn.lower() in we['target_name'].lower())]
            for mkey in matching:
                db_e = db_edges[mkey]
                wiki_s = STRENGTH_ORDER.get(we['strength'], 0)
                db_s   = STRENGTH_ORDER.get(db_e['Strength'], 0)
                if wiki_s != db_s and wiki_s > 0 and db_s > 0:
                    report['score_drift'].append({
                        'dim': f'edge_strength:{we["target_name"]}:{we["edge_type"]}',
                        'wiki': we['strength'], 'db': db_e['Strength']
                    })

    # ── 3. News gap detection ───────────────────────────────────────────────
    wiki_events = parse_news(text)
    for ev in wiki_events:
        cur.execute(
            'SELECT 1 FROM public."NewsEvent" WHERE "Headline" ILIKE %s LIMIT 1',
            (f'%{ev["headline"][:40]}%',)
        )
        if not cur.fetchone():
            report['missing_news'].append(ev)

    # ── 4. Sync missing edges (if not dry_run) ──────────────────────────────
    if not dry_run and report['missing_edges']:
        for we in report['missing_edges']:
            target_id = resolve_company_id(cur, we['target_name'])
            if not target_id:
                report['errors'].append(f"Cannot resolve target: {we['target_name']}")
                continue
            # Check if exists
            cur.execute(
                'SELECT 1 FROM public."RelationEdge" WHERE "SourceId"=%s AND "TargetId"=%s AND "EdgeType"=%s AND "IsDeleted"=false',
                (entity_id, target_id, we['edge_type'])
            )
            if cur.fetchone():
                continue
            cur.execute('SELECT COALESCE(MAX("Id"),0)+1 FROM public."RelationEdge"')
            new_id = cur.fetchone()[0]
            cur.execute('''
                INSERT INTO public."RelationEdge"
                    ("Id","SourceType","SourceId","TargetType","TargetId",
                     "EdgeType","Strength","Label","Description","IsVerified")
                VALUES (%s,'Company',%s,'Company',%s,%s,%s,%s,%s,false)
            ''', (new_id, entity_id, target_id,
                  we['edge_type'], we['strength'],
                  f'[wiki-sync] {we["target_name"]} ({we["edge_type"]})',
                  we['description'][:500]))
            report['synced'].append(f"edge→{we['target_name']}:{we['edge_type']}")

    if not dry_run and report['synced']:
        conn.commit()

    cur.close()
    report['status'] = 'DRIFT' if (report['score_drift'] or report['missing_edges'] or report['missing_news']) else 'OK'
    return report

# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='IPM Wiki → Graph Sync')
    parser.add_argument('--wiki-dir',  required=True)
    parser.add_argument('--host',      default='localhost')
    parser.add_argument('--port',      default=5432, type=int)
    parser.add_argument('--db',        default='IPMDB')
    parser.add_argument('--user',      default='postgres')
    parser.add_argument('--password',  default='postgres')
    parser.add_argument('--dry-run',   action='store_true', default=True)
    parser.add_argument('--sync',      action='store_true')
    args = parser.parse_args()

    dry_run = not args.sync

    conn = psycopg2.connect(
        host=args.host, port=args.port,
        dbname=args.db, user=args.user, password=args.password
    )

    wiki_files = sorted(Path(args.wiki_dir).glob('*.md'))
    wiki_files = [f for f in wiki_files if not f.name.startswith('_')]

    print(f'\n{"="*60}')
    print(f'IPM Wiki → Graph Sync | {"DRY RUN" if dry_run else "WRITE MODE"}')
    print(f'Wiki dir: {args.wiki_dir} | Files: {len(wiki_files)}')
    print(f'{"="*60}\n')

    all_reports = []
    total_drift = 0
    total_missing_edges = 0
    total_missing_news  = 0
    total_synced = 0

    for wiki_file in wiki_files:
        report = sync_wiki_page(conn, wiki_file, dry_run=dry_run)
        all_reports.append(report)

        status = report.get('status', '?')
        eid    = report.get('entity_id', '?')
        fname  = report.get('file', str(wiki_file))

        print(f'[{status:6}] {fname} (entity={eid})')

        if report.get('score_drift'):
            total_drift += len(report['score_drift'])
            for d in report['score_drift']:
                print(f'         ⚠ DRIFT  {d["dim"]}: wiki={d["wiki"]} db={d["db"]}')

        if report.get('missing_edges'):
            total_missing_edges += len(report['missing_edges'])
            for e in report['missing_edges']:
                print(f'         ✗ EDGE   {e["target_name"]} ({e["edge_type"]}/{e["strength"]})')

        if report.get('missing_news'):
            total_missing_news += len(report['missing_news'])
            for n in report['missing_news']:
                print(f'         ✗ NEWS   {n["date"]} — {n["headline"][:50]}')

        if report.get('synced'):
            total_synced += len(report['synced'])
            for s in report['synced']:
                print(f'         ✓ SYNCED {s}')

        if report.get('errors'):
            for e in report['errors']:
                print(f'         ⛔ ERROR  {e}')

    print(f'\n{"="*60}')
    print(f'SUMMARY: {len(wiki_files)} pages')
    print(f'  Score drifts:    {total_drift}')
    print(f'  Missing edges:   {total_missing_edges}')
    print(f'  Missing news:    {total_missing_news}')
    print(f'  Synced items:    {total_synced}')
    if dry_run:
        print(f'\n  → Re-run with --sync to apply missing edges to DB')
    print(f'{"="*60}\n')

    # Save JSON report
    report_path = Path(args.wiki_dir) / '_sync_report.json'
    with open(report_path, 'w') as f:
        json.dump({
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'dry_run': dry_run,
            'wiki_dir': args.wiki_dir,
            'reports': all_reports,
            'summary': {
                'pages': len(wiki_files),
                'score_drifts': total_drift,
                'missing_edges': total_missing_edges,
                'missing_news': total_missing_news,
                'synced': total_synced,
            }
        }, f, indent=2, default=str)
    print(f'JSON report saved: {report_path}')

    conn.close()

if __name__ == '__main__':
    main()
