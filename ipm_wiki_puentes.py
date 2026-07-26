#!/usr/bin/env python3
"""
Poblado de los puentes wiki ↔ core.*
====================================

Escribe las dos columnas que unen el corpus documental con el modelo canónico:

    wiki."Document"."CoreSlug"   ← a qué entidad canónica describe el documento
    core."Entity"."WikiSlug"     ← qué documento describe a la entidad

POR QUÉ ES UN ARCHIVO APARTE Y NO UN FLAG DE ipm_wiki_audit.py
--------------------------------------------------------------
El auditor declara "SOLO LECTURA POR CONSTRUCCIÓN" y abre la sesión READ ONLY
justamente para que la garantía no dependa de la corrección del código. Meterle
un flag de escritura convertiría esa garantía mecánica en una promesa: bastaría
un fallo en el parseo de argumentos para que una auditoría escribiera.

Es el mismo motivo por el que ipm_wiki_ingest.py está separado. La lógica de
resolución NO se duplica: se importa del auditor.

NINGÚN SLUG SE RENOMBRA
-----------------------
Los slugs de la wiki son claves internas de su propio grafo —'ecb' aparece en 20
documentos, 'imf' en 16—, así que renombrarlos para que cuadren con core
rompería decenas de enlaces. core."Entity"."WikiSlug" existe precisamente para
que la base apunte al nombre ajeno. Cada lado conserva el suyo.

ESCRITURA SOBRE TABLA CONGELADA
-------------------------------
core.* está FROZEN. El UPDATE de WikiSlug está autorizado explícitamente por el
dueño y se ejecuta con tres salvaguardas:

  1. Solo sobre filas cuyo WikiSlug es NULL. Nunca sobrescribe un valor previo.
  2. Todo en una transacción, con entrada en agent."AgentActionLedger": sin autor
     no hay aserción (AX2).
  3. El payload del ledger lleva los pares aplicados, así que revertir es
     UPDATE ... SET "WikiSlug" = NULL sobre esa lista. Como el valor previo es
     NULL en las 1505 filas, la reversión no puede perder nada.

Uso:
    python ipm_wiki_puentes.py --dry-run      # informa y no escribe
    python ipm_wiki_puentes.py                # aplica
"""

import argparse
import collections
import json
import os
import sys

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    sys.exit("pip install psycopg2-binary")

import ipm_wiki_audit as auditor

ACTOR_SLUG = "human_ruben_founder"


def resolver(wiki_dir, cur):
    """Reutiliza la resolución del auditor y agrupa por entidad canónica.

    Devuelve (pares, ambiguos): los pares aplicables y los casos en que varios
    documentos reclaman la misma entidad, que NO se aplican.
    """
    docs = auditor.load_wiki(wiki_dir)
    core = auditor.load_core(cur)
    a = auditor.audit(docs, core)

    por_entidad = collections.defaultdict(list)
    for m in a["matched"]:
        por_entidad[m["core_slug"]].append(m)

    pares, ambiguos = [], []
    for core_slug, ms in sorted(por_entidad.items()):
        if len(ms) > 1:
            # Dos documentos que dicen describir la misma entidad. Elegir uno
            # sería inventar una preferencia que nadie declaró: el puente
            # quedaría atado a un documento arbitrario y el otro pasaría a ser
            # invisible sin que nada lo señale.
            ambiguos.append({"core_slug": core_slug,
                             "docs": [m["file"] for m in ms],
                             "slugs": sorted({m["slug"] for m in ms})})
            continue
        m = ms[0]
        pares.append({"core_slug": core_slug, "core_id": m["core_id"],
                      "wiki_slug": m["slug"], "path": m["file"],
                      "via": m["resuelto_por"]})
    return pares, ambiguos, a


def aplicar(conn, pares, dry_run):
    cur = conn.cursor()

    cur.execute('SELECT "Id" FROM agent."AgentActor" WHERE "ActorSlug" = %s AND "RetiredAt" IS NULL',
                (ACTOR_SLUG,))
    fila = cur.fetchone()
    if not fila:
        raise SystemExit(f"no existe el actor '{ACTOR_SLUG}'")
    actor_id = fila[0]

    # Lado wiki: no está congelado, se escribe directo.
    psycopg2.extras.execute_values(cur, """
        UPDATE wiki."Document" d SET "CoreSlug" = v.core_slug
        FROM (VALUES %s) AS v(path, core_slug)
        WHERE d."Path" = v.path AND d."CoreSlug" IS DISTINCT FROM v.core_slug
    """, [(p["path"], p["core_slug"]) for p in pares])
    n_wiki = cur.rowcount

    # Lado core: congelado, autorizado. El filtro por NULL es lo que hace que
    # esta operación no pueda destruir un valor existente, aunque se repita.
    psycopg2.extras.execute_values(cur, """
        UPDATE core."Entity" e SET "WikiSlug" = v.wiki_slug
        FROM (VALUES %s) AS v(core_slug, wiki_slug)
        WHERE e."Slug" = v.core_slug AND e."IsDeleted" = false
          AND e."WikiSlug" IS NULL
    """, [(p["core_slug"], p["wiki_slug"]) for p in pares])
    n_core = cur.rowcount

    cur.execute("""
        INSERT INTO agent."AgentActionLedger" (
            "Id","ActorId","ActionType","ActionPayload",
            "AffectedEntities","AffectedEdges","Outcome","CreatedAt")
        VALUES (gen_random_uuid(), %s, 'poblar_puente_wiki_core', %s::jsonb,
                %s::jsonb, '[]'::jsonb, 'committed', now())
        RETURNING "Hash"
    """, (actor_id,
          json.dumps({"documentos_actualizados": n_wiki,
                      "entidades_actualizadas": n_core,
                      "valor_previo": "NULL en todas las filas afectadas",
                      "reversion": 'UPDATE core."Entity" SET "WikiSlug"=NULL WHERE "Slug" = ANY(...)',
                      "pares": [{"core": p["core_slug"], "wiki": p["wiki_slug"],
                                 "via": p["via"]} for p in pares]}),
          json.dumps([p["core_id"] for p in pares])))
    ledger_hash = cur.fetchone()[0]
    if not ledger_hash:
        raise SystemExit("el ledger devolvió Hash nulo: falta el trigger trg_ledger_seal")

    if dry_run:
        conn.rollback()
    else:
        conn.commit()
    return n_wiki, n_core, ledger_hash


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki-dir", default="wiki")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--dsn", default=None)
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    dsn = args.dsn or (
        "host=localhost port=5433 dbname=meridian user=postgres password="
        + os.environ.get("IPM_CANONICAL_DB_PASSWORD", ""))

    # Resolución en sesión de solo lectura: mientras se decide QUÉ escribir,
    # escribir es imposible.
    lectura = psycopg2.connect(dsn)
    lectura.set_session(readonly=True, autocommit=True)
    pares, ambiguos, a = resolver(
        args.wiki_dir, lectura.cursor(cursor_factory=psycopg2.extras.DictCursor))
    lectura.close()

    vias = collections.Counter(p["via"] for p in pares)
    print(f"Puentes resueltos: {len(pares)}")
    for via, n in sorted(vias.items(), key=lambda kv: -kv[1]):
        print(f"  por {via:18} {n}")
    print(f"Sin destino canonico (no se tocan): {len(a['sin_destino'])}")
    print(f"Hueco real (entidades que faltan):  {len(a['hueco_real'])}")

    if ambiguos:
        print(f"\nAMBIGUOS — no se aplican, {len(ambiguos)} entidad(es) reclamada(s) "
              "por mas de un documento:")
        for x in ambiguos:
            print(f"  {x['core_slug']}: {', '.join(x['docs'])}")

    conn = psycopg2.connect(dsn)
    try:
        n_wiki, n_core, h = aplicar(conn, pares, args.dry_run)
        marca = "[SIMULACRO, revertido] " if args.dry_run else ""
        print(f"\n{marca}wiki.Document.CoreSlug actualizados: {n_wiki}")
        print(f"{marca}core.Entity.WikiSlug   actualizados: {n_core}")
        if not args.dry_run:
            print(f"ledger: {h[:16]}...")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
