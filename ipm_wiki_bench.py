#!/usr/bin/env python3
"""
Línea base léxica del retrieval — recall@5 y MRR sobre el gold set
==================================================================

Corre las 27 consultas candidatas del gold set contra wiki.buscar_lexico y
publica recall@5, recall@10 y MRR por idioma.

PARA QUÉ SIRVE ESTE NÚMERO
--------------------------
Para hacer decidible ADR-W4-04. La pregunta "¿qué proveedor de embeddings?" no
se puede responder sin saber qué se consigue SIN embeddings: un recall@5 de 0,7
con BGE-M3 es excelente si la búsqueda por palabras da 0,3, y decepcionante si
ya daba 0,65. Hoy esa decisión se tomaría a ciegas.

ADVERTENCIA — ESTOS NÚMEROS SON PROVISIONALES
---------------------------------------------
El gold set NO está firmado. Sus 27 pares consulta→documento son candidatos que
el founder debe ratificar ítem por ítem, y el propio documento lo dice: ninguna
métrica cuenta como "gold" hasta esa firma. Lo que sigue es una línea base
contra etiquetas provisionales — sirve para comparar contra sí misma y contra
una futura pata densa, no para afirmar una calidad absoluta.

SOLO LECTURA. La sesión se abre READ ONLY.

Uso:
    python ipm_wiki_bench.py --goldset ../iPM_GV/IPM_Backend_AI/docs/WAVE4_WIKI_GOLDSET_RATIFICACION_2026-07-24.md
"""

import argparse
import collections
import os
import re
import sys

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    sys.exit("pip install psycopg2-binary")

IDIOMA = {"E": "inglés", "S": "español", "D": "alemán"}


def parse_goldset(path):
    """Extrae (id, consulta, docs esperados) de las tablas markdown del gold set.

    Formato: | E1 | consulta | `ruta/doc.md` | related | ✓ | firma |
    Se toman el documento primario y los related: el propio gold set deja sin
    decidir si los related cuentan, así que se miden las dos variantes.
    """
    filas = []
    for linea in open(path, encoding="utf-8"):
        if not linea.startswith("|"):
            continue
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if len(celdas) < 4:
            continue
        m = re.match(r"^([ESD])(\d+)$", celdas[0])
        if not m:
            continue
        primario = re.findall(r"`([^`]+\.md)`", celdas[2])
        related = re.findall(r"`([^`]+\.md)`", celdas[3]) if len(celdas) > 3 else []
        if not primario:
            continue
        filas.append({
            "id": celdas[0], "idioma": IDIOMA[m.group(1)], "consulta": celdas[1],
            "primario": primario, "related": related,
        })
    return filas


def norm(ruta):
    """'wiki/indicators/USD-Hegemony-Index.md' -> 'usd-hegemony-index.md'.

    El gold set escribe rutas relativas al vault y la base guarda rutas
    relativas al repo; se comparan por nombre de archivo en minúsculas.
    """
    return ruta.replace("\\", "/").split("/")[-1].lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--goldset", required=True)
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--dsn", default=None)
    args = ap.parse_args()

    dsn = args.dsn or (
        "host=localhost port=5433 dbname=meridian user=postgres password="
        + os.environ.get("IPM_CANONICAL_DB_PASSWORD", "")
    )
    consultas = parse_goldset(args.goldset)
    if not consultas:
        sys.exit("no se extrajo ninguna consulta del gold set — ¿cambió el formato?")

    conn = psycopg2.connect(dsn)
    conn.set_session(readonly=True, autocommit=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    resultados = []
    for q in consultas:
        cur.execute(
            'SELECT "DocPath" FROM wiki.buscar_lexico(%s, %s)', (q["consulta"], args.k * 4))
        # Se deduplica a documento: el gold set puntúa por documento, no por chunk.
        vistos, docs = set(), []
        for r in cur.fetchall():
            d = norm(r["DocPath"])
            if d not in vistos:
                vistos.add(d)
                docs.append(d)

        esperados_p = {norm(x) for x in q["primario"]}
        esperados_t = esperados_p | {norm(x) for x in q["related"]}

        def rango_de(objetivo):
            for i, d in enumerate(docs, 1):
                if d in objetivo:
                    return i
            return None

        resultados.append({**q, "rango_primario": rango_de(esperados_p),
                           "rango_amplio": rango_de(esperados_t),
                           "top1": docs[0] if docs else None})

    def agrega(rows, campo):
        n = len(rows)
        if not n:
            return None
        r5 = sum(1 for r in rows if r[campo] and r[campo] <= 5) / n
        r10 = sum(1 for r in rows if r[campo] and r[campo] <= 10) / n
        mrr = sum(1 / r[campo] for r in rows if r[campo]) / n
        return r5, r10, mrr

    # La consola de Windows es cp1252 y los acentos abortarían el proceso.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    print("LÍNEA BASE LÉXICA — sin embeddings")
    print("=" * 78)
    print("ADVERTENCIA: el gold set NO está firmado. Etiquetas provisionales.\n")

    for etiqueta, campo in (("solo documento primario", "rango_primario"),
                            ("primario o related", "rango_amplio")):
        print(f"--- {etiqueta} ---")
        print(f"  {'idioma':10} {'n':>3}  {'recall@5':>9} {'recall@10':>10} {'MRR':>7}")
        for idioma in ("inglés", "español", "alemán"):
            rows = [r for r in resultados if r["idioma"] == idioma]
            a = agrega(rows, campo)
            if a:
                print(f"  {idioma:10} {len(rows):>3}  {a[0]:>9.2f} {a[1]:>10.2f} {a[2]:>7.3f}")
        a = agrega(resultados, campo)
        print(f"  {'TOTAL':10} {len(resultados):>3}  {a[0]:>9.2f} {a[1]:>10.2f} {a[2]:>7.3f}\n")

    print("--- detalle por consulta (rango del documento esperado) ---")
    for r in resultados:
        rp = r["rango_primario"]
        marca = "✓" if rp and rp <= 5 else ("~" if r["rango_amplio"] and r["rango_amplio"] <= 5 else "✗")
        pos = f"#{rp}" if rp else (f"related #{r['rango_amplio']}" if r["rango_amplio"] else "no encontrado")
        print(f"  {marca} {r['id']:4} {r['idioma']:9} {pos:16} {r['consulta'][:52]}")

    conn.close()


if __name__ == "__main__":
    main()
