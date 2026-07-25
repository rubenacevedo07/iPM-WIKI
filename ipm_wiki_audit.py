#!/usr/bin/env python3
"""
IPM Wiki ↔ core.* — Auditoría de correspondencia
================================================

Mide la distancia entre el corpus documental (wiki .md) y la verdad canónica
(core.Entity en meridian). Responde dos preguntas simétricas:

    ¿qué hay en la wiki que no está en la base?
    ¿qué hay en la base que no está documentado?

SOLO LECTURA POR CONSTRUCCIÓN. No existe flag de escritura. Además la sesión se
abre como READ ONLY en Postgres, de modo que la garantía es mecánica y no
depende de que este archivo no contenga un INSERT por descuido — que es
exactamente la lección de fn_compute_ledger_hash_v1: una regla que se sostiene
por disciplina acaba incumpliéndose.

Hermano de ipm_wiki_to_graph.py, del que reutiliza el formato de frontmatter.
Aquel apunta al legacy IPMDB y sí escribe (--sync); éste apunta a core.* y no.

Uso:
    python ipm_wiki_audit.py \
        --wiki-dir ./wiki \
        --dsn "host=localhost port=5433 dbname=meridian user=postgres password=..." \
        --out-md   ../iPM_GV/IPM_Backend_AI/docs/AUDIT_WIKI_CORE.md \
        --out-json ../iPM_GV/IPM_Backend_AI/docs/AUDIT_WIKI_CORE.json

Sin --dsn se toma IPM_CANONICAL_DB_PASSWORD sobre el host/puerto por defecto.
"""

import argparse
import collections
import json
import os
import pathlib
import re
import sys
from datetime import datetime, timezone

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    sys.exit("pip install psycopg2-binary")

# Tipos que SÍ son entidades canónicas. El resto de familias documentales
# (temas, escenarios, fuentes…) no son core.Entity y no deberían serlo: su
# ausencia no es un hueco, es una categoría sin destino en el modelo actual.
ENTITY_TYPES = {"actor", "person", "institution", "company", "country", "commodity", "bank"}

# facility no es sujeto de documentación: una planta o un centro de datos no
# tiene doc wiki. Se separa para no falsear el tamaño del hueco.
NOT_DOCUMENTABLE = {"facility"}


# ── Parser (formato compartido con ipm_wiki_to_graph.py) ─────────────────────

def parse_frontmatter(text):
    """Extrae el frontmatter entre delimitadores ---.

    A diferencia del de ipm_wiki_to_graph.py, ignora las líneas indentadas:
    una lista YAML multilínea no debe producir claves espurias.
    """
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def load_wiki(wiki_dir):
    docs = []
    for path in sorted(pathlib.Path(wiki_dir).rglob("*.md")):
        fm = parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        docs.append({
            "file": str(path).replace("\\", "/"),
            "folder": path.parent.name,
            "slug": fm.get("slug") or None,
            "title": fm.get("title") or None,
            "type": fm.get("type") or None,
            "db_id": fm.get("db_id") or None,
            "db_type": fm.get("db_type") or None,
        })
    return docs


# ── Lectura de core.* ────────────────────────────────────────────────────────

def load_core(cur):
    cur.execute("""
        SELECT "Id"::text, "Slug", "CanonicalName", "EntityType",
               "WikiSlug", "LegacyMappings", "AliasNames"
        FROM core."Entity"
        WHERE NOT "IsDeleted"
        ORDER BY "EntityType", "Slug"
    """)
    rows = []
    for r in cur.fetchall():
        lm = r["LegacyMappings"] or {}
        legacy_ids = {k: v for k, v in lm.items() if k.startswith("public.")}
        rows.append({
            "id": r["Id"],
            "slug": r["Slug"],
            "name": r["CanonicalName"],
            "type": r["EntityType"],
            "wiki_slug": r["WikiSlug"],
            "legacy_ids": legacy_ids,
            "aliases": list(r["AliasNames"] or []),
        })
    return rows


# ── Auditoría ────────────────────────────────────────────────────────────────

def _norm(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def _invert(slug):
    """'trump-donald' -> 'donald-trump'.

    La wiki mezcla dos convenciones: actors/ usa nombre-apellido e incoming/ usa
    APELLIDO-nombre. core.Entity usa siempre nombre-apellido. Sin esta vuelta,
    Trump y Musk aparecen como ausentes de la verdad canónica, que es falso.
    """
    parts = (slug or "").split("-")
    return "-".join(reversed(parts)) if len(parts) == 2 else None


def audit(docs, core):
    by_slug = collections.defaultdict(list)
    for e in core:
        by_slug[e["slug"]].append(e)

    # Índice inverso legacy_id -> entidad, para la vía de respaldo por db_id.
    by_legacy = {}
    for e in core:
        for key, val in e["legacy_ids"].items():
            by_legacy[(key.split(".")[1].upper(), str(val))] = e

    # Índices por nombre canónico y por alias, última vía de resolución.
    by_name = {}
    for e in core:
        by_name.setdefault(_norm(e["name"]), e)
        for al in e["aliases"]:
            by_name.setdefault(_norm(al), e)

    matched, absent, no_slug, conflicts = [], [], [], []

    for d in docs:
        if not d["slug"]:
            no_slug.append(d)
            continue

        hits = by_slug.get(d["slug"], [])
        ent = hits[0] if hits else None

        # Vía de respaldo: db_id + db_type contra LegacyMappings.
        via_id = None
        if d["db_id"] and d["db_id"].isdigit() and d["db_type"]:
            table = {"PERSON": "PERSONS", "COMPANY": "COMPANIES",
                     "COUNTRY": "COUNTRIES", "COMMODITY": "COMMODITIES",
                     "BANK": "BANKS", "FACILITY": "FACILITIES"}.get(d["db_type"].upper())
            if table:
                via_id = by_legacy.get((table, d["db_id"]))

        # El slug exacto es la vía principal, pero no la única. Sin las de abajo
        # el informe sobre-reporta huecos por diferencias de convención.
        estrategia = "slug" if ent else None
        if ent is None and via_id is not None:
            ent, estrategia = via_id, "db_id"
        if ent is None:
            inv = _invert(d["slug"])
            if inv and by_slug.get(inv):
                ent, estrategia = by_slug[inv][0], "slug_invertido"
        if ent is None:
            cand = by_name.get(_norm(d["slug"])) or by_name.get(_norm(d["title"]))
            if cand:
                ent, estrategia = cand, "nombre_o_alias"

        if ent is None:
            absent.append({**d, "resuelve_por_db_id": None})
            continue

        rec = {**d, "core_slug": ent["slug"], "core_name": ent["name"],
               "core_type": ent["type"], "core_id": ent["id"],
               "resuelto_por": estrategia}
        matched.append(rec)

        # Conflicto 1 — referencial: las dos vías apuntan a entidades distintas.
        if via_id is not None and via_id["slug"] != ent["slug"]:
            conflicts.append({"clase": "referencial", "doc": d["file"], "slug": d["slug"],
                              "detalle": f"db_id={d['db_id']} resuelve a '{via_id['slug']}' "
                                         f"pero el slug apunta a '{ent['slug']}'"})
        elif d["db_id"] and d["db_id"].isdigit() and via_id is None:
            conflicts.append({"clase": "referencial", "doc": d["file"], "slug": d["slug"],
                              "detalle": f"db_id={d['db_id']} ({d['db_type']}) no existe en "
                                         f"LegacyMappings de ninguna entidad"})

        # Conflicto 3 — deriva de nombre. Solo se evalúa cuando el cruce fue por
        # slug exacto: si resolvió por db_id, inversión o alias, que los nombres
        # difieran es la premisa del cruce, no un hallazgo.
        if estrategia == "slug" and d["title"] and \
                d["title"].lower().replace(",", "").strip() != ent["name"].lower().strip():
            conflicts.append({"clase": "deriva_de_nombre", "doc": d["file"], "slug": d["slug"],
                              "detalle": f"wiki '{d['title']}' vs core '{ent['name']}'"})

    # Conflicto 2 — duplicados internos de la wiki (mismo slug en dos docs).
    dup_wiki = collections.Counter(d["slug"] for d in docs if d["slug"])
    for slug, n in sorted(dup_wiki.items()):
        if n > 1:
            files = [d["file"] for d in docs if d["slug"] == slug]
            conflicts.append({"clase": "duplicado_en_wiki", "doc": " + ".join(files),
                              "slug": slug, "detalle": f"{n} documentos comparten el slug"})

    # Los ausentes se parten en dos cubos: hueco real vs categoría sin destino.
    hueco_real = [a for a in absent if (a["type"] or "").lower() in ENTITY_TYPES]
    sin_destino = [a for a in absent if (a["type"] or "").lower() not in ENTITY_TYPES]

    # Cobertura inversa: cuenta las entidades efectivamente resueltas por
    # cualquiera de las vías, no solo las que comparten slug literal.
    resueltos = {m["core_slug"] for m in matched}
    con_doc = [e for e in core if e["slug"] in resueltos]
    sin_doc = [e for e in core if e["slug"] not in resueltos]
    sin_doc_documentable = [e for e in sin_doc if e["type"] not in NOT_DOCUMENTABLE]
    sin_doc_no_candidata = [e for e in sin_doc if e["type"] in NOT_DOCUMENTABLE]

    # Calidad de core.*
    dup_core = [{"slug": s, "filas": [{"tipo": e["type"], "nombre": e["name"], "id": e["id"]}
                                      for e in v]}
                for s, v in sorted(by_slug.items()) if len(v) > 1]

    return {
        "matched": matched, "absent": absent, "no_slug": no_slug,
        "hueco_real": hueco_real, "sin_destino": sin_destino,
        "conflicts": conflicts,
        "con_doc": con_doc,
        "sin_doc_documentable": sin_doc_documentable,
        "sin_doc_no_candidata": sin_doc_no_candidata,
        "dup_core": dup_core,
    }


# ── Informe ──────────────────────────────────────────────────────────────────

def render_md(a, docs, core, ts):
    L = []
    w = L.append
    n_wikislug = sum(1 for e in core if e["wiki_slug"])
    n_legacymap = sum(1 for e in core if e["legacy_ids"])
    slugs_core = {e["slug"] for e in core}

    w("# Auditoría wiki ↔ core.* — correspondencia y huecos\n")
    w(f"**Fecha:** {ts} · **Naturaleza:** solo lectura, ninguna escritura ejecutada · "
      "**Generado por:** `ipm_wiki_audit.py`\n")
    w("> La wiki es el corpus de evidencia; `core.*` es la verdad canónica. La Constitución\n"
      "> califica la responsabilidad *Evidencia* como **parcial** y nombra la causa:\n"
      "> *\"WikiChunkRef colgante\"*. Este informe mide esa distancia con datos.\n")

    w("## Resumen\n")
    w("| Medida | Valor |")
    w("|---|---|")
    w(f"| Documentos wiki analizados | {len(docs)} |")
    w(f"| Entidades en `core.Entity` | {len(core)} ({len(slugs_core)} slugs distintos) |")
    w(f"| Docs que coinciden con una entidad | **{len(a['matched'])}** |")
    w(f"| Docs sin entidad canónica | {len(a['absent'])} |")
    w(f"| — de ellos, hueco real (son entidades) | **{len(a['hueco_real'])}** |")
    w(f"| — de ellos, categoría sin destino en el modelo | {len(a['sin_destino'])} |")
    w(f"| Docs sin `slug` en el frontmatter | {len(a['no_slug'])} |")
    w(f"| Entidades canónicas con doc wiki | {len(a['con_doc'])} de {len(slugs_core)} "
      f"({100.0*len(a['con_doc'])/max(1,len(slugs_core)):.1f} %) |")
    w(f"| `LegacyMappings` poblado | {n_legacymap}/{len(core)} |")
    w(f"| **`WikiSlug` poblado** | **{n_wikislug}/{len(core)}** |")
    w(f"| Slugs duplicados en `core.Entity` | {len(a['dup_core'])} |")
    w(f"| Conflictos detectados | {len(a['conflicts'])} |")
    w("")

    w("## 1. Los tres puentes\n")
    w("`core.Entity` fue diseñada con dos columnas puente. Una está completa y la otra vacía:\n")
    w("| Puente | Clave | Cobertura |")
    w("|---|---|---|")
    w(f"| `core.Entity` → legacy | `LegacyMappings` | {n_legacymap}/{len(core)} |")
    w(f"| `core.Entity` → wiki | `WikiSlug` | **{n_wikislug}/{len(core)}** |")
    n_dbid = sum(1 for d in docs if d["db_id"] and d["db_id"].isdigit())
    w(f"| wiki → legacy | `db_id` (frontmatter) | {n_dbid}/{len(docs)} |")
    w("\nEl `slug` del frontmatter coincide con `core.Entity.Slug`, y lo tienen más documentos\n"
      "que `db_id`, así que es la vía principal de cruce; `db_id` se usa como respaldo y como\n"
      "control cruzado.\n")

    w("## 2. Cómo se resolvió cada coincidencia\n")
    est = collections.Counter(m.get("resuelto_por") for m in a["matched"])
    w("El slug exacto no es la única vía. Sin las alternativas el informe sobre-reportaría\n"
      "huecos: la wiki mezcla convenciones (`actors/` usa nombre-apellido, `incoming/` usa\n"
      "APELLIDO-nombre) y usa abreviaturas donde core guarda el nombre completo.\n")
    w("| Vía de resolución | Coincidencias |")
    w("|---|---|")
    for k, n in sorted(est.items(), key=lambda kv: -kv[1]):
        w(f"| {k} | {n} |")
    alt = [m for m in a["matched"] if m.get("resuelto_por") != "slug"]
    if alt:
        w(f"\n**{len(alt)} documentos cruzan con core por una vía distinta al slug literal.** "
          "Son los que importan para poblar `WikiSlug`: su slug de wiki NO sirve como clave.\n")
        w("| Slug en wiki | Slug en core | Vía |")
        w("|---|---|---|")
        for m in sorted(alt, key=lambda x: x["slug"] or ""):
            w(f"| `{m['slug']}` | `{m['core_slug']}` | {m['resuelto_por']} |")
    w("")

    w("## 3. Hueco real — documentos que sí son entidades y no están en core\n")
    if a["hueco_real"]:
        w("| Doc | Slug | Tipo | db_id |")
        w("|---|---|---|---|")
        for d in sorted(a["hueco_real"], key=lambda x: (x["folder"], x["slug"] or "")):
            w(f"| `{d['folder']}/` | {d['slug']} | {d['type']} | {d['db_id'] or '—'} |")
    else:
        w("_Ninguno._")
    w("")

    w("## 4. Categorías sin destino en el modelo\n")
    w("Estos documentos **no son entidades y no deberían serlo**: un tema, un escenario o una\n"
      "fuente no es un `core.Entity`. Su ausencia no es un hueco de datos sino una familia\n"
      "documental sin lugar donde aterrizar — que es precisamente lo que `WikiChunkRef` debía\n"
      "cubrir y hoy no cubre, porque no existe schema `wiki`.\n")
    per_type = collections.Counter((d["type"] or "«sin type»") for d in a["sin_destino"])
    w("| Familia (`type`) | Documentos |")
    w("|---|---|")
    for t, n in sorted(per_type.items(), key=lambda kv: -kv[1]):
        w(f"| {t} | {n} |")
    w(f"\n**Total: {len(a['sin_destino'])} documentos.** Dónde deberían vivir es una decisión de\n"
      "diseño del dueño Contexto (ADR-W4-04); este informe solo constata que no la tienen.\n")

    w("## 5. Conflictos\n")
    if a["conflicts"]:
        for clase in ("referencial", "duplicado_en_wiki", "deriva_de_nombre"):
            grupo = [c for c in a["conflicts"] if c["clase"] == clase]
            if not grupo:
                continue
            w(f"### {clase.replace('_', ' ').capitalize()} ({len(grupo)})\n")
            w("| Slug | Detalle |")
            w("|---|---|")
            for c in grupo:
                w(f"| {c['slug']} | {c['detalle']} |")
            w("")
    else:
        w("_Ninguno._\n")

    w("## 6. Higiene del frontmatter\n")
    est = collections.Counter()
    for d in docs:
        v = d["db_id"]
        est["numérico" if (v and v.isdigit()) else ("TBD" if v == "TBD"
            else ("vacío" if v == "" or v is None and "db_id" in d else "ausente"))] += 1
    w("| `db_id` | Documentos |")
    w("|---|---|")
    for k, n in sorted(est.items(), key=lambda kv: -kv[1]):
        w(f"| {k} | {n} |")
    w(f"\nDocumentos sin `slug` (no cruzables por la vía principal): **{len(a['no_slug'])}**\n")
    if a["no_slug"]:
        for d in a["no_slug"][:25]:
            w(f"- `{d['file']}`")
        if len(a["no_slug"]) > 25:
            w(f"- _…y {len(a['no_slug'])-25} más (listado íntegro en el JSON)_")
    w("")

    w("## 7. Calidad de `core.*`\n")
    w("`core.*` está declarado FROZEN, lo que hace estos hallazgos más relevantes, no menos.\n")
    if a["dup_core"]:
        w("| Slug | Filas que lo comparten |")
        w("|---|---|")
        for d in a["dup_core"]:
            det = " · ".join(f"{f['tipo']}:{f['nombre']}" for f in d["filas"])
            w(f"| `{d['slug']}` | {det} |")
    else:
        w("_Sin duplicados._")
    w("")

    w("---\n")
    w("## Anexo — entidades canónicas sin documentación\n")
    w(f"Cola de trabajo: **{len(a['sin_doc_documentable'])}** entidades documentables sin doc "
      f"wiki, agrupadas por tipo.\n")
    por_tipo = collections.defaultdict(list)
    for e in a["sin_doc_documentable"]:
        por_tipo[e["type"]].append(e)
    for t in sorted(por_tipo, key=lambda k: -len(por_tipo[k])):
        w(f"\n### {t} ({len(por_tipo[t])})\n")
        for e in sorted(por_tipo[t], key=lambda x: x["slug"] or ""):
            w(f"- `{e['slug']}` — {e['name']}")
    w(f"\n### No candidatas: {NOT_DOCUMENTABLE} ({len(a['sin_doc_no_candidata'])})\n")
    w("Una planta o un centro de datos no es sujeto de un documento wiki. Se listan aparte\n"
      "para no falsear el tamaño del hueco: incluirlas haría parecer la cobertura mucho peor\n"
      "de lo que es.\n")
    w(f"_{len(a['sin_doc_no_candidata'])} filas, listado íntegro en el JSON._\n")

    w("---")
    w("*Informe generado sin ejecutar ninguna escritura. La sesión de base de datos se abrió\n"
      "como READ ONLY, de modo que la garantía es mecánica y no depende de la ausencia de\n"
      "sentencias de escritura en el código.*")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Auditoría wiki ↔ core.* (solo lectura)")
    ap.add_argument("--wiki-dir", default="wiki")
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--out-md", default=None)
    ap.add_argument("--out-json", default=None)
    args = ap.parse_args()

    dsn = args.dsn or (
        "host=localhost port=5433 dbname=meridian user=postgres password="
        + os.environ.get("IPM_CANONICAL_DB_PASSWORD", "")
    )

    conn = psycopg2.connect(dsn)
    # Garantía mecánica: aunque este archivo contuviera un INSERT, Postgres lo
    # rechazaría. La regla no depende de que el código sea correcto.
    conn.set_session(readonly=True, autocommit=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    docs = load_wiki(args.wiki_dir)
    core = load_core(cur)
    a = audit(docs, core)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    md = render_md(a, docs, core, ts)
    if args.out_md:
        pathlib.Path(args.out_md).write_text(md, encoding="utf-8")
        # ASCII a propósito: la consola de Windows es cp1252 y una flecha
        # unicode aquí aborta el proceso justo antes de escribir el JSON.
        print("informe  -> " + args.out_md)
    else:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        print(md)

    if args.out_json:
        payload = {
            "generado": ts,
            "solo_lectura": True,
            "resumen": {
                "docs_wiki": len(docs),
                "entidades_core": len(core),
                "coinciden": len(a["matched"]),
                "ausentes": len(a["absent"]),
                "hueco_real": len(a["hueco_real"]),
                "sin_destino": len(a["sin_destino"]),
                "docs_sin_slug": len(a["no_slug"]),
                "entidades_con_doc": len(a["con_doc"]),
                "entidades_sin_doc_documentables": len(a["sin_doc_documentable"]),
                "entidades_sin_doc_no_candidatas": len(a["sin_doc_no_candidata"]),
                "wikislug_poblado": sum(1 for e in core if e["wiki_slug"]),
                "legacymappings_poblado": sum(1 for e in core if e["legacy_ids"]),
                "slugs_duplicados_core": len(a["dup_core"]),
                "conflictos": len(a["conflicts"]),
            },
            "coincidencias": a["matched"],
            "hueco_real": a["hueco_real"],
            "sin_destino": a["sin_destino"],
            "docs_sin_slug": a["no_slug"],
            "conflictos": a["conflicts"],
            "slugs_duplicados_core": a["dup_core"],
            "entidades_sin_doc": [
                {"slug": e["slug"], "nombre": e["name"], "tipo": e["type"]}
                for e in a["sin_doc_documentable"]
            ],
            "entidades_sin_doc_no_candidatas": [
                {"slug": e["slug"], "nombre": e["name"], "tipo": e["type"]}
                for e in a["sin_doc_no_candidata"]
            ],
        }
        pathlib.Path(args.out_json).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("json     -> " + args.out_json)

    conn.close()


if __name__ == "__main__":
    main()
