#!/usr/bin/env python3
"""
Verificación del alcance del corpus indexado — reejecución del verifiedBy de `vault-wiki`
==========================================================================================

POR QUÉ EXISTE ESTE FICHERO
---------------------------
El 2026-07-28 se verificó la arista `vault-wiki` del mapa de arquitectura
(`iPM_GV/IPM_Infra/arquitectura_w4_componentes.json`, `state: "verified-absent"`). Su
campo `verifiedBy` dice:

    "SELECT sobre wiki.Document por ruta e ILIKE '%prediction%'; DISTINCT de la raiz de Path"

**El SQL nunca se persistió — sólo esa frase.** Reejecutarlo obligó a reconstruirlo de cero.
Lo que faltó aquel día no fue la medición: fue que nadie pudiera re-correrla. Este fichero
es la mitad del entregable; el informe es la otra mitad, y ninguna sirve sin la otra.

QUÉ MIDE — seis comprobaciones
------------------------------
  1. DISTINCT de la raíz de `Path`            → ¿es `wiki` para todos?
  2. `Path ILIKE '%prediction%'`              → ¿hay algo del vault?
  3. Deriva `Path`+`ContentHash` DB vs disco  → ¿el 164 de hoy es el 164 del ADR?
  4. Targets `raw/` del gold set (E9/S4/D2/D3) por basename
  5. Colisión D3 por `Path` EXACTO            → convierte inferencia en medición
  6. Censo de colisiones por basename (0-bis) + barrido de identidad por nombre en el
     tooling, con CONTROL POSITIVO: si el barrido no encuentra la línea que sabemos que
     existe, aborta. Un cero sin calibrar no prueba nada.

Las comprobaciones 1-5 leen la base. La 6 es sólo de disco y corre igual sin DB.

SOLO LECTURA — tres barreras, declaradas también en la cabecera del informe
--------------------------------------------------------------------------
  · `set_session(readonly=True)`  — la sesión rechaza cualquier escritura
  · `SET statement_timeout='25s'` — ninguna consulta puede colgar la base
  · TCP a 127.0.0.1:5433          — JAMÁS `docker exec psql`

Va como `postgres` porque `ipm_analytics` no tiene privilegio sobre `wiki.*` (42501).

LA CREDENCIAL — de dónde sale, para que la próxima sesión no lo pregunte
-----------------------------------------------------------------------
Por orden de precedencia:
  1. `--dsn` explícito
  2. `$IPM_CANONICAL_DB_PASSWORD`
  3. **`iPM_GV/IPM_Infra/env/.env.prod`, clave `IPM_CANONICAL_DB_PASSWORD`** ← la vía normal

No se crea una copia más del secreto: se lee de donde ya vive. **El valor no se imprime
nunca** — ni en el log, ni en el informe, ni en el DSN de un mensaje de error.

Uso:
    python ops/verificar_alcance_corpus.py [--out ops/VERIFICACION_ALCANCE_<fecha>.md]
    python ops/verificar_alcance_corpus.py --solo-disco      # 0-bis + barrido, sin DB
"""

import argparse
import collections
import hashlib
import os
import pathlib
import re
import sys

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    sys.exit("pip install psycopg2-binary")


# ── Credencial ────────────────────────────────────────────────────────────────

RUTA_ENV_PROD = pathlib.Path("../iPM_GV/IPM_Infra/env/.env.prod")


def leer_password():
    """Devuelve (password, procedencia). NUNCA imprime el valor."""
    pw = os.environ.get("IPM_CANONICAL_DB_PASSWORD")
    if pw:
        return pw, "$IPM_CANONICAL_DB_PASSWORD"
    if RUTA_ENV_PROD.exists():
        for linea in RUTA_ENV_PROD.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"\s*(?:export\s+)?IPM_CANONICAL_DB_PASSWORD\s*=\s*(.*)$", linea)
            if m:
                val = m.group(1).strip().strip('"').strip("'")
                if val:
                    return val, "iPM_GV/IPM_Infra/env/.env.prod"
    return None, None


# ── 0-bis · censo de colisiones por basename (sólo disco) ─────────────────────

def censo_colisiones(wiki_dir, raw_dir):
    grupos = collections.defaultdict(list)
    for raiz in (wiki_dir, raw_dir):
        base = pathlib.Path(raiz)
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.md")):
            grupos[p.name.lower()].append(str(p).replace("\\", "/"))
    colisiones = {k: v for k, v in grupos.items() if len(v) > 1}
    dentro_indice = {}
    for k, v in colisiones.items():
        solo_w = [r for r in v if r.startswith(wiki_dir + "/")]
        if len(solo_w) > 1:
            dentro_indice[k] = solo_w
    return grupos, colisiones, dentro_indice


# ── Comprobación 6 · barrido de identidad por nombre en el tooling ────────────

PATRONES = [
    ("split-ultimo", re.compile(r"""split\s*\(\s*["'][/\\]+["']\s*\)\s*\[\s*-?1\s*\]""")),
    ("basename",     re.compile(r"os\.path\.basename")),
    (".stem",        re.compile(r"\.stem\b")),
    ("GetFileName",  re.compile(r"Path\.GetFileName(WithoutExtension)?")),
]

# CONTROL POSITIVO: línea que SABEMOS que existe. Si el barrido no la encuentra, el
# barrido está roto y sus ceros no valen. Un barrido por regex ya dio "cero lectores"
# sobre el camino del producto porque el SQL en C# llevaba comillas dobladas.
CONTROL = ("ipm_wiki_bench.py", 79, "split-ultimo")

RAICES_BARRIDO = [".", "../iPM_GV/IPM_Backend_AI/tools", "../iPM_GV/IPM_Infra"]
EXT_BARRIDO = {".py", ".sql", ".cs", ".ps1", ".sh"}
SALTAR = {".git", "__pycache__", "node_modules", "bin", "obj", ".obsidian", "wiki", "raw"}


def barrido_identidad():
    hits = []
    for raiz in RAICES_BARRIDO:
        base = pathlib.Path(raiz)
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.suffix.lower() not in EXT_BARRIDO:
                continue
            if any(s in p.parts for s in SALTAR):
                continue
            try:
                texto = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for i, ln in enumerate(texto.splitlines(), 1):
                for etq, rx in PATRONES:
                    if rx.search(ln):
                        hits.append((str(p).replace("\\", "/"), i, etq, ln.strip()[:110]))
                        break
    ok = any(h[0].endswith(CONTROL[0]) and h[1] == CONTROL[1] and h[2] == CONTROL[2] for h in hits)
    return hits, ok


# ── Consultas contra la base ──────────────────────────────────────────────────

# Los únicos targets del gold set que viven fuera de wiki/. Ver
# WAVE4_WIKI_GOLDSET_RATIFICACION_2026-07-24.md, filas E9 / S4 / D2 / D3.
TARGETS_RAW = [
    ("E9 primario", "raw/internal-notes/palantir-manifesto-2025.md"),
    ("E9 related",  "raw/internal-notes/palantir-wars-ice-programs.md"),
    ("E9 related",  "raw/internal-notes/karp-alex-research-2026-04-22.md"),
    ("S4 primario", "raw/sanctions/russia-oil-2026-04.md"),
    ("D2 primario", "raw/internal-notes/musk-afd-research-2025.md"),
    ("D3 primario", "raw/central-banks/lagarde-ecb-2026-04.md"),
]

D3_RESUMEN = "wiki/sources/Lagarde-ECB-2026-04.md"
D3_FUENTE = "raw/central-banks/lagarde-ecb-2026-04.md"


def sha256_hex(s):
    return hashlib.sha256((s or "").encode("utf-8")).hexdigest()


def medir_db(cur, wiki_dir):
    r = {}

    cur.execute('SELECT DISTINCT split_part("Path", \'/\', 1) AS raiz '
                'FROM wiki."Document" WHERE "RetiredAt" IS NULL ORDER BY 1')
    r["raices"] = [x["raiz"] for x in cur.fetchall()]

    cur.execute('SELECT "Path" FROM wiki."Document" '
                'WHERE "RetiredAt" IS NULL AND "Path" ILIKE %s ORDER BY 1', ("%prediction%",))
    r["predictions"] = [x["Path"] for x in cur.fetchall()]

    cur.execute('SELECT count(*) AS n FROM wiki."Document" WHERE "RetiredAt" IS NULL')
    r["docs_vigentes"] = cur.fetchone()["n"]
    cur.execute('SELECT count(*) AS n FROM wiki."Chunk" WHERE "RetiredAt" IS NULL')
    r["chunks_vigentes"] = cur.fetchone()["n"]
    cur.execute('SELECT max("IngestedAt") AS t FROM wiki."Document"')
    r["ultima_ingesta"] = cur.fetchone()["t"]

    # ── 3 · deriva Path + ContentHash ──
    cur.execute('SELECT "Path", "ContentHash" FROM wiki."Document" WHERE "RetiredAt" IS NULL')
    en_db = {x["Path"]: x["ContentHash"] for x in cur.fetchall()}
    en_disco = {}
    for p in sorted(pathlib.Path(wiki_dir).rglob("*.md")):
        rel = str(p).replace("\\", "/")
        en_disco[rel] = sha256_hex(p.read_text(encoding="utf-8", errors="replace"))
    r["solo_db"] = sorted(set(en_db) - set(en_disco))
    r["solo_disco"] = sorted(set(en_disco) - set(en_db))
    r["hash_distinto"] = sorted(k for k in set(en_db) & set(en_disco) if en_db[k] != en_disco[k])
    r["n_db"], r["n_disco"] = len(en_db), len(en_disco)

    # ── 4 · targets raw/ del gold set, por basename ──
    por_basename = collections.defaultdict(list)
    for ruta in en_db:
        por_basename[ruta.split("/")[-1].lower()].append(ruta)
    r["targets"] = []
    for etq, t in TARGETS_RAW:
        bn = t.split("/")[-1].lower()
        r["targets"].append((etq, t, por_basename.get(bn, [])))

    # ── 5 · colisión D3 por Path EXACTO ──
    cur.execute('SELECT "Path" FROM wiki."Document" WHERE "Path" = %s AND "RetiredAt" IS NULL',
                (D3_RESUMEN,))
    r["d3_resumen_indexado"] = cur.fetchone() is not None
    cur.execute('SELECT "Path" FROM wiki."Document" WHERE "Path" = %s AND "RetiredAt" IS NULL',
                (D3_FUENTE,))
    r["d3_fuente_indexada"] = cur.fetchone() is not None

    return r


# ── Informe ───────────────────────────────────────────────────────────────────

def escribir_informe(ruta, db, procedencia, grupos, colisiones, dentro, hits, ctrl_ok, wiki_dir):
    L = []
    A = L.append
    A("# Verificación del alcance del corpus indexado")
    A("")
    A("Reejecución del `verifiedBy` de la arista `vault-wiki`")
    A("(`iPM_GV/IPM_Infra/arquitectura_w4_componentes.json`), cuyo SQL original no se persistió.")
    A("")
    A("**Generado por** `ops/verificar_alcance_corpus.py`. Ese script es la mitad del entregable:")
    A("lo que faltó el 2026-07-28 no fue la medición, fue que nadie pudiera re-correrla.")
    A("")
    A("## Barreras declaradas")
    A("")
    A("| Barrera | Valor |")
    A("|---|---|")
    A("| sesión | `set_session(readonly=True, autocommit=True)` — rechaza toda escritura |")
    A("| timeout | `SET statement_timeout='25s'` |")
    A("| transporte | TCP `127.0.0.1:5433` — **jamás `docker exec psql`** |")
    A("| usuario | `postgres`, porque `ipm_analytics` no tiene privilegio sobre `wiki.*` (42501) |")
    A("| credencial | leída de `%s` — **valor nunca impreso** |" % (procedencia or "n/d"))
    A("")

    if db:
        # ── Veredicto, calculado. Lo primero que lee quien no estuvo. ──
        raiz_ok = db["raices"] == ["wiki"]
        vault_ok = not db["predictions"]
        d3_ok = db["d3_resumen_indexado"] and not db["d3_fuente_indexada"]
        deriva = len(db["solo_db"]) + len(db["solo_disco"]) + len(db["hash_distinto"])
        A("## Veredicto")
        A("")
        A("| Afirmación verificada | Resultado |")
        A("|---|---|")
        A("| La raíz de **todos** los `Path` es `wiki` | %s |"
          % ("CONFIRMADA" if raiz_ok else "**CONTRADICHA**"))
        A("| **Cero** documentos del vault (`Predictions`) en el índice | %s |"
          % ("CONFIRMADA" if vault_ok else "**CONTRADICHA**"))
        A("| El primario de **D3** no está indexado; lo que casa es el resumen | %s |"
          % ("CONFIRMADA" if d3_ok else "**CONTRADICHA**"))
        A("| El primario de **S4** no está indexado | %s |"
          % ("CONFIRMADA" if not [e for e in db["targets"]
                                  if e[0] == "S4 primario" and e[2]] else "**CONTRADICHA**"))
        A("| Índice y disco son el mismo conjunto | %s |"
          % ("CONFIRMADA" if deriva == 0 else "**%d documento(s) con deriva** — ver §3" % deriva))
        A("")
        if db["hash_distinto"] == ["%s/log.md" % wiki_dir] and not db["solo_db"] and not db["solo_disco"]:
            A("> **Sobre la única deriva.** Es `%s/log.md`, el registro de actividad append-only."
              % wiki_dir)
            A("> Está dentro del corpus indexado, así que **cada entrada que se le añade cambia su**")
            A("> **hash y lo desincroniza del índice hasta la siguiente ingesta**. Es esperado y")
            A("> benigno para este análisis —ningún target del gold set apunta a él— pero significa")
            A("> que el corpus nunca está exactamente sincronizado si alguien loggea. Se anota; no")
            A("> se corrige aquí.")
            A("")

        A("## Estado del índice")
        A("")
        A("| | |")
        A("|---|---|")
        A("| `wiki.\"Document\"` vigentes | **%d** |" % db["docs_vigentes"])
        A("| `wiki.\"Chunk\"` vigentes | **%d** |" % db["chunks_vigentes"])
        A("| última ingesta | %s |" % db["ultima_ingesta"])
        A("")

        A("## 1 · Raíz de `Path` — `SELECT DISTINCT split_part(\"Path\",'/',1)`")
        A("")
        A("Raíces distintas: **%s**" % ", ".join("`%s`" % x for x in db["raices"]))
        A("")
        veredicto = "CONFIRMA" if db["raices"] == ["wiki"] else "**CONTRADICE**"
        A("→ %s la afirmación «la raíz de TODOS es `wiki`»." % veredicto)
        A("")

        A("## 2 · Documentos del vault — `Path ILIKE '%prediction%'`")
        A("")
        if db["predictions"]:
            A("**%d filas** — el vault SÍ aparece:" % len(db["predictions"]))
            for x in db["predictions"]:
                A("- `%s`" % x)
            A("")
            A("→ **CONTRADICE** «cero documentos del vault».")
        else:
            A("**0 filas.** → CONFIRMA «cero documentos del vault».")
        A("")

        A("## 3 · Deriva `Path` + `ContentHash` — índice vs disco")
        A("")
        A("Indexados: **%d** · en disco bajo `%s/`: **%d**" % (db["n_db"], wiki_dir, db["n_disco"]))
        A("")
        A("| clase | n |")
        A("|---|---|")
        A("| sólo en DB (indexado, ya no en disco) | **%d** |" % len(db["solo_db"]))
        A("| sólo en disco (no indexado) | **%d** |" % len(db["solo_disco"]))
        A("| mismo `Path`, **hash distinto** | **%d** |" % len(db["hash_distinto"]))
        A("")
        for etq, lista in (("sólo en DB", db["solo_db"]),
                           ("sólo en disco", db["solo_disco"]),
                           ("hash distinto", db["hash_distinto"])):
            if lista:
                A("**%s:**" % etq)
                for x in lista:
                    A("- `%s`" % x)
                A("")
        if not (db["solo_db"] or db["solo_disco"] or db["hash_distinto"]):
            A("**Sin deriva.** El índice y el disco son el mismo conjunto, hash a hash.")
            A("")

        A("## 4 · Targets `raw/` del gold set, por basename")
        A("")
        A("El bench identifica documentos por basename en minúsculas, así que un target `raw/`")
        A("«acierta» si existe CUALQUIER documento indexado con ese nombre de fichero.")
        A("")
        A("| Etiqueta | Target declarado | Qué hay en el índice con ese basename |")
        A("|---|---|---|")
        for etq, t, encontrados in db["targets"]:
            if not encontrados:
                celda = "**AUSENTE — nada que casar**"
            elif len(encontrados) == 1:
                celda = "`%s`%s" % (encontrados[0], "" if encontrados[0] == t else " ← **otro `Path`**")
            else:
                celda = "**AMBIGUO** — " + ", ".join("`%s`" % x for x in encontrados)
            A("| %s | `%s` | %s |" % (etq, t, celda))
        A("")

        A("## 5 · Colisión D3, por `Path` EXACTO")
        A("")
        A("| `Path` | ¿indexado? |")
        A("|---|---|")
        A("| `%s` (el resumen) | **%s** |" % (D3_RESUMEN, "SÍ" if db["d3_resumen_indexado"] else "NO"))
        A("| `%s` (la fuente) | **%s** |" % (D3_FUENTE, "SÍ" if db["d3_fuente_indexada"] else "NO"))
        A("")
        if db["d3_resumen_indexado"] and not db["d3_fuente_indexada"]:
            A("→ **CONFIRMADO como medición, no como inferencia de código:** el primario declarado")
            A("de D3 no está en el índice. Lo que el bench encuentra es el resumen — **otro")
            A("documento** que colapsa al mismo basename en minúsculas.")
        A("")

    A("## 6 · Censo de colisiones por basename (0-bis) — sólo disco")
    A("")
    A("Corpus declarado (`%s/` + `raw/`): **%d** basenames únicos, **%d grupos colisionan**,"
      % (wiki_dir, len(grupos), len(colisiones)))
    A("**%d dentro del índice** (`%s/` es lo único que `ipm_wiki_ingest.py` recorre)."
      % (len(dentro), wiki_dir))
    A("")
    A("### Dentro del índice — un documento puede contar como acierto de otro")
    A("")
    for k in sorted(dentro):
        A("- `%s`" % k)
        for r in dentro[k]:
            A("  - `%s`" % r)
    A("")
    A("### Generador estructural — `wiki/sources/` nombra igual que su fuente cruda")
    A("")
    A("`CLAUDE.md §4.11` define la página de resumen con `source-path: raw/folder/filename.md`,")
    A("y la práctica la nombra igual. **Cada `raw/` que se resuma añade una colisión más.**")
    A("")
    n_gen = 0
    for k in sorted(colisiones):
        rutas = colisiones[k]
        en_src = [r for r in rutas if r.startswith(wiki_dir + "/sources/")]
        en_raw = [r for r in rutas if r.startswith("raw/")]
        if en_src and en_raw:
            n_gen += 1
            A("- `%s` ↔ `%s`" % (en_src[0], en_raw[0]))
    A("")
    A("**%d pares** de este tipo." % n_gen)
    A("")

    A("## 7 · Barrido de identidad por nombre en el tooling")
    A("")
    A("**Control positivo:** el barrido debe encontrar `%s:%d` [%s], que sabemos que existe."
      % CONTROL)
    A("Resultado: **%s**. %s" % ("ENCUENTRA" if ctrl_ok else "NO ENCUENTRA",
                                 "" if ctrl_ok else "Los ceros de esta sección NO valen."))
    A("")
    A("| Fichero | Línea | Patrón | Código |")
    A("|---|---|---|---|")
    for f, i, etq, ln in sorted(hits):
        A("| `%s` | %d | %s | `%s` |" % (f, i, etq, ln.replace("|", "\\|")))
    A("")
    A("Triaje en el análisis: los de `bench` (×2) y `_hibrido` rompen la línea base;")
    A("`ipm_wiki_to_graph.py` está latente (invocación documentada sobre carpeta plana);")
    A("`ipm_wiki_lint_referencias.py` **ya devuelve `AMBIGUOUS`** — es el modelo a copiar.")
    A("`ipm_wiki_ingest.py` y `ipm_wiki_puentes.py` usan ruta completa: la identidad en la base")
    A("está sana, y eso descarta una migración de datos.")
    A("")

    pathlib.Path(ruta).write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Verifica el alcance del corpus indexado (solo lectura)")
    ap.add_argument("--wiki-dir", default="wiki")
    ap.add_argument("--raw-dir", default="raw")
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--solo-disco", action="store_true", help="0-bis + barrido, sin tocar la base")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    grupos, colisiones, dentro = censo_colisiones(args.wiki_dir, args.raw_dir)
    hits, ctrl_ok = barrido_identidad()
    print("0-bis: %d basenames unicos, %d grupos colisionan, %d dentro del indice"
          % (len(grupos), len(colisiones), len(dentro)))
    print("barrido: %d coincidencias | control positivo: %s"
          % (len(hits), "OK" if ctrl_ok else "FALLA"))
    if not ctrl_ok:
        sys.exit("ERROR: el control positivo del barrido no aparece. Un cero sin calibrar no "
                 "prueba nada; arreglar los patrones antes de publicar el informe.")

    db = None
    procedencia = None
    if not args.solo_disco:
        if args.dsn:
            dsn, procedencia = args.dsn, "--dsn"
        else:
            pw, procedencia = leer_password()
            if pw is None:
                sys.exit("Sin credencial: ni $IPM_CANONICAL_DB_PASSWORD ni %s" % RUTA_ENV_PROD)
            dsn = ("host=127.0.0.1 port=5433 dbname=meridian user=postgres password=" + pw)
        try:
            conn = psycopg2.connect(dsn, connect_timeout=10)
        except Exception as e:
            # El DSN lleva el secreto: no se propaga el mensaje crudo.
            sys.exit("ERROR de conexion: %s (detalle omitido, el DSN contiene la credencial)"
                     % type(e).__name__)
        conn.set_session(readonly=True, autocommit=True)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SET statement_timeout='25s'")
        try:
            db = medir_db(cur, args.wiki_dir)
        finally:
            conn.close()

        print("\nDB: %d documentos / %d chunks vigentes | raices: %s"
              % (db["docs_vigentes"], db["chunks_vigentes"], db["raices"]))
        print("Path ILIKE '%%prediction%%': %d filas" % len(db["predictions"]))
        print("deriva -> solo-DB %d | solo-disco %d | hash distinto %d"
              % (len(db["solo_db"]), len(db["solo_disco"]), len(db["hash_distinto"])))
        print("D3 -> resumen indexado: %s | fuente indexada: %s"
              % (db["d3_resumen_indexado"], db["d3_fuente_indexada"]))

    out = args.out or "ops/VERIFICACION_ALCANCE_CORPUS.md"
    escribir_informe(out, db, procedencia, grupos, colisiones, dentro, hits, ctrl_ok, args.wiki_dir)
    print("\ninforme -> %s" % out)


if __name__ == "__main__":
    main()
