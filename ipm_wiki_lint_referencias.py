#!/usr/bin/env python3
"""
IPM Wiki — Linter de referencias internas (wikilinks + related_*)
===================================================================

Mide la integridad del grafo interno de la wiki: los `[[wikilinks]]` en el cuerpo
de las páginas, y las listas `related_actors/related_countries/related_institutions/
related_commodities/related_themes` del frontmatter. NO consulta `core.*` — es un
chequeo puramente interno (¿esta página apunta a otra página que existe?), no de
correspondencia con la verdad canónica. Eso es `ipm_wiki_audit.py`, que es a quien
se le importa el parser de frontmatter para no duplicar la lógica.

SOLO MEDICIÓN. No escribe nada, en ningún archivo, en ninguna base. No abre conexión
a ninguna base de datos — no la necesita: todo lo que compara vive en el filesystem.
No hay flag de escritura, a propósito: mezclar medición y reparación en el mismo
archivo fue precisamente el motivo por el que `ipm_wiki_puentes.py` se separó de
`ipm_wiki_audit.py`.

Dos categorías de referencia, con un defecto de medición ya conocido en cada una,
corregido aquí desde el diseño:

  1. WIKILINKS DE CUERPO — `[[objetivo]]` o `[[objetivo|alias]]` en el texto
     markdown. Se resuelven como ruta relativa (`../carpeta/Pagina`, con o sin
     `.md`) o como nombre suelto (búsqueda case-insensitive de basename en todo
     `wiki/`). Defecto corregido: un `[[wikilink]]` dentro de comillas invertidas
     es un ejemplo de sintaxis en prosa (ver `wiki/log.md` y
     `wiki/lint-reports/2026-04-09.md`), no un link real — se excluye antes de
     buscar coincidencias, quitando primero cualquier tramo entre backticks de
     cada línea. Esto NO captura los falsos positivos que no están entre
     backticks (los hay — se reportan aparte, sin forzarlos a desaparecer).

  2. LISTAS related_* DEL FRONTMATTER — cada elemento se compara contra el
     conjunto de slugs de página reales (el campo `slug:` de cada .md). LAS
     COMILLAS SE QUITAN DEL TOKEN ANTES DE COMPARAR:
     `related_countries: [china, "united-states"]` no debe reportar a
     `united-states` como roto solo porque alguien lo escribió entre comillas.
     Ese es el defecto que tenía la medición ad-hoc original (ver
     MEDICION_WIKI_CORE_2026-08-05.md §1) — acá se corrige desde el diseño en
     vez de medirse con el defecto y corregirse después.

No procesa `raw/` ni `ipm-agent-stack/`: no son wiki. `wiki/incoming/` SÍ se
procesa como cualquier otra carpeta — es una cola de staging conocida, pero
excluirla a mano envejece mal (el día que se resuelva, el linter debe verlo solo).

Uso:
    python ipm_wiki_lint_referencias.py [--wiki-dir wiki] [--out-md ruta.md] [--out-json ruta.json]
"""

import argparse
import collections
import json
import os
import pathlib
import re
import sys
from datetime import datetime, timezone

from ipm_wiki_audit import parse_frontmatter

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
BACKTICK_SPAN_RE = re.compile(r"`[^`]*`")
RELATED_FIELDS = [
    "related_actors", "related_countries", "related_institutions",
    "related_commodities", "related_themes",
]


# ── Carga ──────────────────────────────────────────────────────────────────

def load_pages(wiki_dir):
    pages = []
    for path in sorted(pathlib.Path(wiki_dir).rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        pages.append({
            "file": str(path).replace("\\", "/"),
            "text": text,
            "fm": fm,
            "slug": fm.get("slug") or None,
        })
    return pages


# ── 1. Wikilinks de cuerpo ───────────────────────────────────────────────────

def _strip_backtick_spans(line):
    return BACKTICK_SPAN_RE.sub("", line)


def _split_flow_list(raw):
    raw = (raw or "").strip()
    if not (raw.startswith("[") and raw.endswith("]")):
        return None
    inner = raw[1:-1]
    if not inner.strip():
        return []
    return [t.strip() for t in inner.split(",")]


def check_wikilinks(pages):
    by_basename = collections.defaultdict(list)
    for p in pages:
        base = os.path.splitext(os.path.basename(p["file"]))[0]
        by_basename[base.lower()].append(p["file"])

    def resolve(target, source_file):
        t = target.strip()
        if t.startswith("../../raw/") or t.startswith("../raw/"):
            d = os.path.dirname(source_file)
            cand = os.path.normpath(os.path.join(d, t)).replace("\\", "/")
            return ("RAW_OK", cand) if os.path.exists(cand) else ("RAW_BROKEN", cand)
        if "/" in t:
            d = os.path.dirname(source_file)
            cand = os.path.normpath(os.path.join(d, t)).replace("\\", "/")
            if os.path.exists(cand):
                return ("RESOLVED_MD_SUFFIX" if t.lower().endswith(".md") else "RESOLVED", cand)
            cand_md = cand + ".md"
            if os.path.exists(cand_md):
                return ("RESOLVED", cand_md)
            return ("BROKEN_PATH", cand)
        matches = by_basename.get(t.lower(), [])
        if len(matches) == 1:
            return ("RESOLVED_BARE", matches[0])
        if len(matches) > 1:
            return ("AMBIGUOUS", matches)
        return ("UNRESOLVED_BARE", None)

    occurrences = []
    for p in pages:
        for lineno, line in enumerate(p["text"].splitlines(), 1):
            clean = _strip_backtick_spans(line)
            for m in WIKILINK_RE.finditer(clean):
                inner = m.group(1)
                target, _, alias = inner.partition("|")
                status, detail = resolve(target, p["file"])
                occurrences.append({
                    "file": p["file"], "line": lineno, "target": target,
                    "alias": alias or None, "status": status, "detail": detail,
                })
    return occurrences


# ── 2. related_* del frontmatter ─────────────────────────────────────────────

def _strip_quotes(tok):
    if len(tok) >= 2 and ((tok[0] == '"' and tok[-1] == '"') or (tok[0] == "'" and tok[-1] == "'")):
        return tok[1:-1]
    return tok


def check_related(pages):
    page_slugs = {p["slug"]: p["file"] for p in pages if p["slug"]}

    refs = []
    for p in pages:
        for field in RELATED_FIELDS:
            raw = p["fm"].get(field)
            toks = _split_flow_list(raw)
            if not toks:
                continue
            for t in toks:
                if not t:
                    continue
                clean = _strip_quotes(t)
                resolved = clean in page_slugs
                refs.append({
                    "file": p["file"], "field": field, "raw_token": t,
                    "clean_token": clean, "had_quotes": t != clean,
                    "resolved": resolved,
                })
    return refs, page_slugs


# ── Informe ──────────────────────────────────────────────────────────────────

BROKEN_LINK_STATUSES = {"BROKEN_PATH", "AMBIGUOUS", "UNRESOLVED_BARE", "RAW_BROKEN"}


def build_report(pages, link_occs, related_refs, page_slugs, ts):
    n_links_total = len(link_occs)
    broken_links = [o for o in link_occs if o["status"] in BROKEN_LINK_STATUSES]
    n_links_broken = len(broken_links)

    n_related_total = len(related_refs)
    broken_related = [r for r in related_refs if not r["resolved"]]
    n_related_broken = len(broken_related)
    n_quote_fixed = sum(1 for r in related_refs if r["had_quotes"] and r["resolved"])

    by_target = collections.defaultdict(int)
    for r in broken_related:
        by_target[r["clean_token"]] += 1

    lines = []
    w = lines.append
    w(f"# Lint de referencias internas — {ts}\n")
    w("Solo medición. Sin conexión a base de datos, sin escritura. Comillas quitadas "
      "del token de `related_*` y tramos entre backticks quitados antes de buscar "
      "`[[wikilinks]]`, ambos antes de comparar — no después.\n")

    w("## Resumen\n")
    w("| Medida | Valor |")
    w("|---|---|")
    w(f"| Páginas analizadas | {len(pages)} |")
    w(f"| Wikilinks de cuerpo — total | {n_links_total} |")
    w(f"| Wikilinks de cuerpo — rotos | **{n_links_broken}** |")
    w(f"| Referencias related_* — total | {n_related_total} |")
    w(f"| Referencias related_* — rotas (token limpio de comillas) | **{n_related_broken}** |")
    w(f"| — de ellas, tenían comillas y por eso rompían antes | {n_quote_fixed} |")
    w("")

    w("## Wikilinks de cuerpo rotos, por estado\n")
    est = collections.Counter(o["status"] for o in broken_links)
    w("| Estado | Ocurrencias |")
    w("|---|---|")
    for k, n in sorted(est.items(), key=lambda kv: -kv[1]):
        w(f"| {k} | {n} |")
    w("")
    if broken_links:
        w("| Archivo:línea | Target | Estado |")
        w("|---|---|---|")
        for o in broken_links[:200]:
            w(f"| `{o['file']}:{o['line']}` | `{o['target']}` | {o['status']} |")
        if len(broken_links) > 200:
            w(f"\n_...y {len(broken_links) - 200} más — lista íntegra en el JSON._")
    w("")

    w("## Referencias related_* rotas, por slug pedido\n")
    w(f"Slugs distintos pedidos-y-ausentes: {len(by_target)}\n")
    w("| Slug pedido | Ocurrencias |")
    w("|---|---|")
    for slug, n in sorted(by_target.items(), key=lambda kv: -kv[1])[:60]:
        w(f"| `{slug}` | {n} |")
    w("")

    w("---\n*Generado sin ejecutar ninguna escritura ni abrir ninguna conexión de base de datos.*")

    summary = {
        "generado": ts,
        "paginas": len(pages),
        "wikilinks_total": n_links_total,
        "wikilinks_rotos": n_links_broken,
        "related_total": n_related_total,
        "related_rotos": n_related_broken,
        "related_rotos_por_comillas_ya_arreglados": n_quote_fixed,
    }
    return "\n".join(lines), summary


def main():
    ap = argparse.ArgumentParser(description="Lint de referencias internas de la wiki (solo lectura)")
    ap.add_argument("--wiki-dir", default="wiki")
    ap.add_argument("--out-md", default=None)
    ap.add_argument("--out-json", default=None)
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    pages = load_pages(args.wiki_dir)
    link_occs = check_wikilinks(pages)
    related_refs, page_slugs = check_related(pages)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    md, summary = build_report(pages, link_occs, related_refs, page_slugs, ts)

    if args.out_md:
        pathlib.Path(args.out_md).write_text(md, encoding="utf-8")
        print("informe  -> " + args.out_md)
    else:
        print(md)

    if args.out_json:
        payload = {
            "resumen": summary,
            "wikilinks": link_occs,
            "related": related_refs,
        }
        pathlib.Path(args.out_json).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("json     -> " + args.out_json)

    print(f"\nwikilinks rotos: {summary['wikilinks_rotos']} / {summary['wikilinks_total']}")
    print(f"related_* rotos: {summary['related_rotos']} / {summary['related_total']} "
          f"({summary['related_rotos_por_comillas_ya_arreglados']} ya no rompen por comillas)")


if __name__ == "__main__":
    main()
