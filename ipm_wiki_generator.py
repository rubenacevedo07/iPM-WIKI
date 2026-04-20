#!/usr/bin/env python3
"""
IPM Wiki Generator — SQL → Karpathy-style Markdown
Queries IPMDB and generates structured wiki pages per entity.

Usage:
  python3 ipm_wiki_generator.py --host localhost --port 5432 \
    --db IPMDB --user postgres --password <pw> \
    --company-ids 1 2 4 41 68 90 96 \
    --output-dir ./wiki/companies

The script generates one .md file per company following the
Karpathy LLM Wiki pattern: dense facts, structured sections,
machine-readable headers for RAG/embedding ingestion.
"""

import argparse
import os
import sys
from datetime import datetime

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("psycopg2 not installed. Run: pip install psycopg2-binary --break-system-packages")
    sys.exit(1)

# ── Queries ────────────────────────────────────────────────────────────────

SQL_COMPANY = """
SELECT c."Id", c."Name", c."Ticker", c."CountryId", cn."Name" as "CountryName"
FROM public."Companies" c
LEFT JOIN public."Countries" cn ON cn."Id" = c."CountryId"
WHERE c."Id" = %s
"""

SQL_POWER_INDEX = """
SELECT pi."ArchetypeCode", pi."CompositeScore",
       pi."FinancialScore", pi."MilitaryScore", pi."PoliticalScore",
       pi."TechnologicalScore", pi."IndustrialScore", pi."InformationScore",
       pi."PoliticalTier", pi."MilitaryTier", pi."FinancialTier",
       pi."TrendDirection", pi."ComputedAt"
FROM public."CompanyPowerIndex" pi
WHERE pi."CompanyId" = %s
"""

SQL_EDGES = """
SELECT re."SourceType", re."SourceId", re."TargetType", re."TargetId",
       re."EdgeType", re."Strength", re."Label", re."Description",
       re."BaselineRiskScore", re."IsVerified",
       -- Resolve source name
       CASE
         WHEN re."SourceType" = 'Company' THEN sc."Name"
         WHEN re."SourceType" = 'Person'  THEN sp."Name" || ' ' || sp."LastName"
         WHEN re."SourceType" = 'Country' THEN sct."Name"
         ELSE 'Unknown'
       END as "SourceName",
       -- Resolve target name
       CASE
         WHEN re."TargetType" = 'Company' THEN tc."Name"
         WHEN re."TargetType" = 'Person'  THEN tp."Name" || ' ' || tp."LastName"
         WHEN re."TargetType" = 'Country' THEN tct."Name"
         ELSE 'Unknown'
       END as "TargetName"
FROM public."RelationEdge" re
LEFT JOIN public."Companies" sc  ON re."SourceType"='Company' AND sc."Id"=re."SourceId"
LEFT JOIN public."Persons"   sp  ON re."SourceType"='Person'  AND sp."Id"=re."SourceId"
LEFT JOIN public."Countries" sct ON re."SourceType"='Country' AND sct."Id"=re."SourceId"
LEFT JOIN public."Companies" tc  ON re."TargetType"='Company' AND tc."Id"=re."TargetId"
LEFT JOIN public."Persons"   tp  ON re."TargetType"='Person'  AND tp."Id"=re."TargetId"
LEFT JOIN public."Countries" tct ON re."TargetType"='Country' AND tct."Id"=re."TargetId"
WHERE (
    (re."SourceId" = %s AND re."SourceType" = 'Company') OR
    (re."TargetId" = %s AND re."TargetType" = 'Company')
)
AND re."IsDeleted" = false
ORDER BY re."BaselineRiskScore" DESC NULLS LAST, re."Strength"
"""

SQL_PERSON_VISION = """
SELECT p."Name", p."LastName", p."Title",
       pv."VisionArchetype", pv."VisionSummary",
       pv."DeclaredObjectives", pv."VisionStatements", pv."DivergenceFlags",
       pv."StatedTimeHorizon", pv."ConfidenceScore"
FROM public."PersonVision" pv
JOIN public."Persons" p ON p."Id" = pv."PersonId"
WHERE p."CompanyId" = %s
ORDER BY pv."ConfidenceScore" DESC
"""

SQL_KEY_PEOPLE = """
SELECT DISTINCT p."Name", p."LastName", p."Title",
       re."EdgeType", re."Strength"
FROM public."RelationEdge" re
JOIN public."Persons" p ON p."Id" = re."SourceId"
WHERE re."SourceType" = 'Person'
  AND re."TargetId" = %s AND re."TargetType" = 'Company'
  AND re."IsDeleted" = false
ORDER BY re."Strength", p."LastName"
"""

SQL_NEWS = """
SELECT "Headline", "Summary", "PublishedAt", "SourceName",
       "SourceUrl", "Sentiment", "Importance", "IsVerified"
FROM public."NewsEvent"
WHERE "Headline" ILIKE %s
   OR "Headline" ILIKE %s
ORDER BY "PublishedAt" DESC NULLS LAST
LIMIT 10
"""

# ── Strength/Tier helpers ──────────────────────────────────────────────────

STRENGTH_EMOJI = {
    'Critical': '🔴',
    'High':     '🟠',
    'Medium':   '🟡',
    'Low':      '⚪',
}

TIER_LABEL = {1: 'Dominant', 2: 'Significant', 3: 'Minor'}

ARCHETYPE_DESC = {
    'FINANCIAL':    'Financial power hub — capital markets, investment, and monetary influence',
    'MILITARY':     'Military-industrial complex — defense, weapons systems, national security',
    'TECHNOLOGICAL':'Technological platform — AI, software, semiconductor, or cloud dominance',
    'INDUSTRIAL':   'Industrial powerhouse — manufacturing, energy, or physical infrastructure',
    'POLITICAL':    'Political actor — regulatory, governmental, or multilateral power',
    'HYBRID':       'Hybrid power — crosses multiple power dimensions simultaneously',
    'COERCIVE':     'Coercive actor — sanctions, military, or regulatory enforcement power',
}

def tier_bar(score):
    if score is None: return 'N/A'
    filled = int(score / 10)
    return '█' * filled + '░' * (10 - filled) + f' {score:.0f}/100'

def strength_badge(s):
    return STRENGTH_EMOJI.get(s, '⚪') + f' {s}'

# ── Markdown generator ─────────────────────────────────────────────────────

def generate_wiki_page(conn, company_id, company_name_hint=None):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Company basics
    cur.execute(SQL_COMPANY, (company_id,))
    company = cur.fetchone()
    if not company:
        return None, f"Company {company_id} not found"

    name    = company['Name']
    ticker  = company['Ticker'] or 'PRIVATE'
    country = company['CountryName'] or 'Unknown'

    # Power Index
    cur.execute(SQL_POWER_INDEX, (company_id,))
    pi = cur.fetchone()

    # Edges
    cur.execute(SQL_EDGES, (company_id, company_id))
    edges = cur.fetchall()

    # PersonVision (leaders with vision in same company)
    cur.execute(SQL_PERSON_VISION, (company_id,))
    visions = cur.fetchall()

    # Key People edges
    cur.execute(SQL_KEY_PEOPLE, (company_id,))
    key_people = cur.fetchall()

    # News (search by company name)
    search = f'%{name}%'
    search2 = f'%{ticker}%' if ticker != 'PRIVATE' else search
    cur.execute(SQL_NEWS, (search, search2))
    news = cur.fetchall()

    cur.close()

    # ── Build markdown ─────────────────────────────────────────────────────
    lines = []
    now = datetime.utcnow().strftime('%Y-%m-%d')

    slug_name = name.replace(' ', '_').replace('.', '').replace('/', '_')
    lines += [
        f'---',
        f'entity_id: {company_id}',
        f'ticker: {ticker}',
        f'archetype: {pi["ArchetypeCode"] if pi else "UNKNOWN"}',
        f'composite_score: {pi["CompositeScore"] if pi else "N/A"}',
        f'last_updated: {now}',
        f'source: ipm_db_auto_generated',
        f'aliases: [{name}, {ticker}]',
        f'tags: [ipm-entity, {(pi["ArchetypeCode"] or "unknown").lower() if pi else "unknown"}]',
        f'---',
        '',
        f'# {name}',
        '',
    ]

    # One-liner context
    if pi:
        arch_desc = ARCHETYPE_DESC.get(pi['ArchetypeCode'], pi['ArchetypeCode'])
        trend = pi['TrendDirection'] or 'stable'
        lines.append(f'> **{arch_desc}.** Composite power score: **{pi["CompositeScore"]:.0f}/100** ({trend} trend). Country: {country}.')
    else:
        lines.append(f'> Country: {country}. Power index not yet computed.')
    lines.append('')

    # ── Power Index ────────────────────────────────────────────────────────
    if pi:
        lines += [
            '## Power Index',
            '',
            f'**Archetype:** `{pi["ArchetypeCode"]}`  ',
            f'**Composite:** {tier_bar(float(pi["CompositeScore"]))}  ',
            f'**Trend:** {pi["TrendDirection"] or "stable"}',
            '',
            '| Dimension | Score | Bar |',
            '|-----------|------:|-----|',
        ]
        dims = [
            ('Financial',    pi['FinancialScore']),
            ('Military',     pi['MilitaryScore']),
            ('Political',    pi['PoliticalScore']),
            ('Technological',pi['TechnologicalScore']),
            ('Industrial',   pi['IndustrialScore']),
            ('Information',  pi['InformationScore']),
        ]
        for dim_name, dim_val in dims:
            if dim_val is not None:
                bar = '█' * int(float(dim_val) / 10) + '░' * (10 - int(float(dim_val) / 10))
                lines.append(f'| {dim_name} | {float(dim_val):.0f} | `{bar}` |')

        lines.append('')

        tiers = []
        if pi['FinancialTier']:  tiers.append(f'Financial: Tier {pi["FinancialTier"]} ({TIER_LABEL.get(pi["FinancialTier"], "")})')
        if pi['PoliticalTier']:  tiers.append(f'Political: Tier {pi["PoliticalTier"]} ({TIER_LABEL.get(pi["PoliticalTier"], "")})')
        if pi['MilitaryTier']:   tiers.append(f'Military: Tier {pi["MilitaryTier"]} ({TIER_LABEL.get(pi["MilitaryTier"], "")})')
        if tiers:
            lines.append('**Tiers:** ' + ' · '.join(tiers))
            lines.append('')

    # ── Key People ─────────────────────────────────────────────────────────
    if key_people or visions:
        lines += ['## Leadership', '']
        seen = set()
        for kp in key_people:
            full = f"{kp['Name']} {kp['LastName']}"
            if full not in seen:
                seen.add(full)
                lines.append(f'- **{full}** — {kp["Title"] or kp["EdgeType"]} ({strength_badge(kp["Strength"])})')
        lines.append('')

    # ── PersonVision ───────────────────────────────────────────────────────
    for v in visions:
        full = f"{v['Name']} {v['LastName']}"
        lines += [
            f'### {full} — Vision',
            '',
            f'**Archetype:** `{v["VisionArchetype"]}` · **Confidence:** {v["ConfidenceScore"]:.0f}/100  ',
            f'**Horizon:** {v["StatedTimeHorizon"] or "N/A"}',
            '',
            v['VisionSummary'] or '',
            '',
        ]

        # Vision quotes
        if v['VisionStatements']:
            import json
            stmts = v['VisionStatements']
            if isinstance(stmts, str):
                try: stmts = json.loads(stmts)
                except: stmts = []
            for s in stmts[:3]:
                if isinstance(s, dict) and s.get('quote'):
                    src  = s.get('source', '')
                    date = s.get('date', '')
                    lines.append(f'> *"{s["quote"]}"*')
                    lines.append(f'> — {src}{", " + date if date else ""}')
                    lines.append('')

        # Divergence flags
        if v['DivergenceFlags']:
            import json
            flags = v['DivergenceFlags']
            if isinstance(flags, str):
                try: flags = json.loads(flags)
                except: flags = []
            if flags:
                lines.append('**⚠ Divergence flags:**')
                for f in flags:
                    if isinstance(f, dict):
                        sev = f.get('severity', '')
                        lines.append(f'- [{sev}] Stated: *{f.get("stated", "")}*')
                        lines.append(f'  Observed: {f.get("observed", "")}')
                lines.append('')

    # ── Relations ──────────────────────────────────────────────────────────
    if edges:
        lines += ['## Relations', '']

        # Group by direction
        outbound = [e for e in edges if e['SourceId'] == company_id and e['SourceType'] == 'Company']
        inbound  = [e for e in edges if e['TargetId'] == company_id and e['TargetType'] == 'Company']

        if outbound:
            lines.append('### Outbound (this entity → others)')
            lines.append('')
            lines.append('| Strength | Target | Type | Description |')
            lines.append('|----------|--------|------|-------------|')
            for e in outbound:
                strength = STRENGTH_EMOJI.get(e['Strength'], '') + ' ' + (e['Strength'] or '')
                target   = e['TargetName'] or f"ID:{e['TargetId']}"
                etype    = e['EdgeType'] or ''
                desc     = (e['Description'] or '')[:80] + ('...' if len(e['Description'] or '') > 80 else '')
                # Obsidian wikilink: [[Target Name|Display]]
                ob_link = f'[[{target}|{target}]]' if target and not target.startswith('ID:') else target
                lines.append(f'| {strength} | **{ob_link}** | `{etype}` | {desc} |')
            lines.append('')

        if inbound:
            lines.append('### Inbound (others → this entity)')
            lines.append('')
            lines.append('| Strength | Source | Type | Description |')
            lines.append('|----------|--------|------|-------------|')
            for e in inbound:
                strength = STRENGTH_EMOJI.get(e['Strength'], '') + ' ' + (e['Strength'] or '')
                source   = e['SourceName'] or f"ID:{e['SourceId']}"
                etype    = e['EdgeType'] or ''
                desc     = (e['Description'] or '')[:80] + ('...' if len(e['Description'] or '') > 80 else '')
                ob_link = f'[[{source}|{source}]]' if source and not source.startswith('ID:') else source
                lines.append(f'| {strength} | **{ob_link}** | `{etype}` | {desc} |')
            lines.append('')

    # ── News Events ────────────────────────────────────────────────────────
    if news:
        lines += ['## Recent Events', '']
        for n in news:
            date      = str(n['PublishedAt'])[:10] if n['PublishedAt'] else 'N/A'
            sentiment = n['Sentiment'] or ''
            imp       = n['Importance'] or ''
            verified  = '✓' if n['IsVerified'] else '?'
            headline  = n['Headline'] or ''
            summary   = n['Summary'] or ''
            src       = n['SourceName'] or ''
            url       = n['SourceUrl'] or ''

            sent_emoji = {'Positive':'📈','Negative':'📉','Mixed':'📊','Neutral':'📋'}.get(sentiment, '')
            lines.append(f'### {date} — {headline}')
            lines.append(f'`{imp}` {sent_emoji} {sentiment} · Source: {src} {verified}')
            if url:
                lines.append(f'[Source]({url})')
            lines.append('')
            lines.append(summary)
            lines.append('')

    # ── Footer ─────────────────────────────────────────────────────────────
    lines += [
        '---',
        f'*Auto-generated from IPMDB on {now}. Edge count: {len(edges)}.*',
        f'*Composite score: {pi["CompositeScore"]:.0f}/100 | Archetype: {pi["ArchetypeCode"]}*' if pi else '',
    ]

    slug = name.lower().replace(' ', '_').replace('/', '_').replace('.', '')
    return '\n'.join(lines), slug

# ── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='IPM Wiki Generator')
    parser.add_argument('--host',        default='localhost')
    parser.add_argument('--port',        default=5432, type=int)
    parser.add_argument('--db',          default='IPMDB')
    parser.add_argument('--user',        default='postgres')
    parser.add_argument('--password',    default='postgres')
    parser.add_argument('--company-ids', nargs='+', type=int,
                        default=[1, 2, 4, 41, 68, 90, 96],
                        help='Company IDs to generate wiki pages for')
    parser.add_argument('--output-dir',  default='./wiki_output')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    conn = psycopg2.connect(
        host=args.host, port=args.port,
        dbname=args.db, user=args.user, password=args.password
    )

    generated = []
    for cid in args.company_ids:
        print(f'Generating wiki page for CompanyId={cid}...', end=' ')
        content, slug_or_err = generate_wiki_page(conn, cid)
        if content is None:
            print(f'ERROR: {slug_or_err}')
            continue
        filename = f'{args.output_dir}/{cid:03d}_{slug_or_err}.md'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'→ {filename} ({len(content)} chars)')
        generated.append(filename)

    conn.close()

    # Generate index
    index_path = f'{args.output_dir}/_INDEX.md'
    with open(index_path, 'w') as f:
        f.write(f'# IPM Wiki — Company Index\n\n')
        f.write(f'*Auto-generated {datetime.utcnow().strftime("%Y-%m-%d")} · {len(generated)} entities*\n\n')
        for fp in generated:
            fname = os.path.basename(fp)
            name  = fname[4:-3].replace('_', ' ').title()
            f.write(f'- [{name}]({fname})\n')

    print(f'\n✓ Generated {len(generated)} wiki pages + index → {args.output_dir}/')

if __name__ == '__main__':
    main()
