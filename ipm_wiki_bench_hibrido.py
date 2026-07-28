#!/usr/bin/env python3
"""
Bench del retrieval híbrido — la medición que cierra ADR-W4-04
==============================================================

Compara cuatro configuraciones sobre el MISMO gold set firmado:

    lexico        FTS + trigram                    (la línea base del 2026-07-26)
    bge           las dos anteriores + BGE-M3
    e5            las dos anteriores + e5-large
    denso_solo    únicamente el vector             (para saber cuánto aporta él solo)

CÓMO SE DECIDE, Y POR QUÉ ASÍ
-----------------------------
La línea base ya dio recall@5 = 1,00 en INGLÉS. Sobre las 11 consultas inglesas
no hay nada que ganar y sí ruido que meter, así que el criterio de ADR-W4-04 es:

  · se compara sobre las 16 consultas ES/DE,
  · el umbral de éxito es 0,85 GLOBAL (no el 0,7 del gate original: ese listón
    lo puso el gold set antes de saber que el léxico solo ya daba 0,85),
  · gana BGE-M3 salvo que e5 saque ≥3 puntos de recall@5 medio o gane en 2 de
    3 idiomas.

Ese criterio se fijó ANTES de ver los números, y está escrito aquí para que no se
pueda ajustar después de mirarlos.

EL PREFIJO DE e5 TAMBIÉN EN LA CONSULTA
---------------------------------------
e5 se entrenó con "query: ..." para consultas y "passage: ..." para pasajes. El
lado pasaje lo pone ipm_wiki_embed.py; el lado consulta lo pone este archivo.
Olvidarlo mediría una desventaja del prefijo, no del modelo.

SOLO LECTURA sobre la base. Por TCP.

Uso:
    python ipm_wiki_bench_hibrido.py --goldset <ruta>
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

CONFIGS = [
    # (etiqueta, modelo, pesos fts/trgm/denso)
    ("lexico",     None,  1.0, 1.0, 0.0),
    ("bge",        "bge", 1.0, 1.0, 1.0),
    ("e5",         "e5",  1.0, 1.0, 1.0),
    ("denso_solo", "bge", 0.0, 0.0, 1.0),
]

PREFIJO_CONSULTA = {"bge": "", "e5": "query: "}


def parse_goldset(path):
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
        filas.append({"id": celdas[0], "idioma": IDIOMA[m.group(1)], "consulta": celdas[1],
                      "primario": primario, "related": related})
    return filas


def norm(ruta):
    return ruta.replace("\\", "/").split("/")[-1].lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--goldset", required=True)
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--dsn", default=None)
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    dsn = args.dsn or ("host=127.0.0.1 port=5433 dbname=meridian user=postgres password="
                       + os.environ.get("IPM_CANONICAL_DB_PASSWORD", ""))
    conn = psycopg2.connect(dsn)
    conn.set_session(readonly=True, autocommit=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM wiki."v_CoberturaEmbeddings"')
    cob = cur.fetchone()
    print(f"cobertura: {cob['ChunksVigentes']} chunks · bge {cob['ConBge']} · e5 {cob['ConE5']}")
    if cob["ConBge"] == 0 and cob["ConE5"] == 0:
        sys.exit("Sin embeddings: correr ipm_wiki_embed.py primero.")

    consultas = parse_goldset(args.goldset)
    print(f"gold set: {len(consultas)} consultas firmadas\n")

    from sentence_transformers import SentenceTransformer
    modelos = {}
    for clave, hf in (("bge", "BAAI/bge-m3"), ("e5", "intfloat/multilingual-e5-large")):
        if any(c[1] == clave for c in CONFIGS):
            modelos[clave] = SentenceTransformer(hf)

    resultados = {}
    for etiqueta, modelo, w_fts, w_trgm, w_denso in CONFIGS:
        filas = []
        for q in consultas:
            vec = None
            if modelo and w_denso > 0:
                texto = PREFIJO_CONSULTA[modelo] + q["consulta"]
                vec = list(map(float, modelos[modelo].encode(texto, normalize_embeddings=True)))
            cur.execute('''
                SELECT "DocPath" FROM wiki.buscar_hibrido(
                    %s, %s::vector, %s, %s, 60, 0.30, %s, %s, %s)
            ''', (q["consulta"], vec, args.k * 4, modelo or "bge", w_fts, w_trgm, w_denso))
            vistos, docs = set(), []
            for r in cur.fetchall():
                d = norm(r["DocPath"])
                if d not in vistos:
                    vistos.add(d)
                    docs.append(d)
            esperados = {norm(x) for x in q["primario"]}
            rango = next((i for i, d in enumerate(docs, 1) if d in esperados), None)
            filas.append({**q, "rango": rango})
        resultados[etiqueta] = filas

    def agrega(filas):
        n = len(filas)
        if not n:
            return 0, 0
        r5 = sum(1 for f in filas if f["rango"] and f["rango"] <= 5) / n
        mrr = sum(1 / f["rango"] for f in filas if f["rango"]) / n
        return r5, mrr

    print(f"{'config':12} {'EN r@5':>8} {'ES r@5':>8} {'DE r@5':>8} {'ES+DE':>8} {'GLOBAL':>8} {'MRR':>7}")
    print("-" * 64)
    resumen = {}
    for etiqueta in resultados:
        f = resultados[etiqueta]
        por = {i: [x for x in f if x["idioma"] == i] for i in ("inglés", "español", "alemán")}
        esde = por["español"] + por["alemán"]
        r5_en, _ = agrega(por["inglés"])
        r5_es, _ = agrega(por["español"])
        r5_de, _ = agrega(por["alemán"])
        r5_esde, _ = agrega(esde)
        r5_g, mrr_g = agrega(f)
        resumen[etiqueta] = {"en": r5_en, "es": r5_es, "de": r5_de,
                             "esde": r5_esde, "global": r5_g, "mrr": mrr_g}
        print(f"{etiqueta:12} {r5_en:>8.2f} {r5_es:>8.2f} {r5_de:>8.2f} {r5_esde:>8.2f} "
              f"{r5_g:>8.2f} {mrr_g:>7.3f}")

    # ── El criterio, aplicado tal como estaba escrito antes de ver los números ──
    lex, bge, e5 = resumen["lexico"], resumen.get("bge"), resumen.get("e5")
    print("\n--- criterio de ADR-W4-04 (fijado antes de medir) ---")
    if bge and e5:
        dif = (e5["esde"] - bge["esde"]) * 100
        gana_e5_idiomas = sum(1 for i in ("en", "es", "de") if e5[i] > bge[i])
        print(f"  ES/DE  · bge {bge['esde']:.2f} vs e5 {e5['esde']:.2f}  (e5 {dif:+.1f} puntos)")
        print(f"  idiomas donde e5 gana: {gana_e5_idiomas} de 3")
        ganador = "e5" if (dif >= 3.0 or gana_e5_idiomas >= 2) else "bge"
        print(f"  → SHIPS: {ganador}")
        mejor = resumen[ganador]
        print(f"\n  vs la línea base léxica: ES/DE {lex['esde']:.2f} → {mejor['esde']:.2f} "
              f"({(mejor['esde']-lex['esde'])*100:+.1f} puntos)")
        print(f"  global {lex['global']:.2f} → {mejor['global']:.2f} "
              f"({(mejor['global']-lex['global'])*100:+.1f} puntos)")
        print(f"  umbral de éxito 0,85 global: {'SUPERADO' if mejor['global'] >= 0.85 else 'NO SUPERADO'}")
        if mejor["esde"] <= lex["esde"]:
            print("  ⚠ El vector NO mejora ES/DE, que era la única razón por la que se "
                  "justificaba. Ver LINEA_BASE_LEXICA_2026-07-26.md.")

    print("\n--- consultas donde el léxico fallaba (r@5) y qué hace el denso ---")
    fallos = [f["id"] for f in resultados["lexico"] if not (f["rango"] and f["rango"] <= 5)]
    for fid in fallos:
        fila = {e: next(x for x in resultados[e] if x["id"] == fid) for e in resultados}
        est = "  ".join(f"{e}:{('#'+str(fila[e]['rango'])) if fila[e]['rango'] else '—'}"
                        for e in ("lexico", "bge", "e5", "denso_solo"))
        print(f"  {fid:4} {fila['lexico']['idioma']:9} {est}")

    conn.close()


if __name__ == "__main__":
    main()
