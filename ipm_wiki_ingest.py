#!/usr/bin/env python3
"""
IPM Wiki → wiki.* — Ingesta del corpus como fuente de evidencia
===============================================================

Carga los documentos .md en wiki."Document" y wiki."Chunk", dando destino a
core."RelationEvidence"."WikiChunkRef", que hasta ahora apuntaba a un uuid que no
existía en ninguna tabla.

ESTE SÍ ESCRIBE. Es deliberadamente un archivo distinto de ipm_wiki_audit.py,
que es de solo lectura por declaración y abre la sesión como READ ONLY. Mezclar
ambos habría convertido esa garantía en una promesa.

QUÉ ESCRIBE Y QUÉ NO
--------------------
Escribe en wiki.*, schema nuevo y propio del corpus.
NO toca core.*, que está congelado. En particular no escribe ni una fila en
core."RelationEvidence": decidir qué documento sostiene qué arista es juicio, no
mecánica, y esa decisión no la toma un cargador.

IDENTIDAD DE UN CHUNK
---------------------
Id = primeros 16 bytes de sha256(ruta|encabezado|texto), formateados como uuid.
Reingerir un documento sin cambios produce los mismos Ids, así que la operación
es idempotente y un puntero de evidencia sobrevive a la reingesta. Si el texto de
una sección cambia, cambia su Id: es un chunk distinto, no el mismo editado.

Las secciones que desaparecen se marcan con RetiredAt en vez de borrarse — una
evidencia que apuntase a ellas debe seguir resolviendo (AX1).

Uso:
    python ipm_wiki_ingest.py --wiki-dir wiki [--dry-run]
"""

import argparse
import hashlib
import os
import pathlib
import re
import sys
import uuid

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    sys.exit("pip install psycopg2-binary")


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def content_uuid(*partes):
    """uuid derivado del contenido: mismos datos, mismo Id."""
    h = hashlib.sha256("|".join(p or "" for p in partes).encode("utf-8")).digest()
    return str(uuid.UUID(bytes=h[:16]))


def sha256_hex(s):
    return hashlib.sha256((s or "").encode("utf-8")).hexdigest()


# Un chunk por debajo de esto no sostiene ninguna afirmación: son encabezados
# con un resto vacío o marcadores de sección. Descarta 79 de 1391 (5,7%) sin
# tocar contenido real — el percentil 10 son 37 caracteres. El número de
# descartados se imprime siempre: filtrar en silencio sería peor que no filtrar.
MIN_CHARS_CHUNK = 20


def split_sections(cuerpo):
    """Parte por encabezados de segundo nivel (##), que es como ya están
    estructurados los documentos (Summary, Role and Levers, Relations...).

    El preámbulo anterior al primer ## —normalmente el título H1— se conserva
    como sección 0: descartarlo perdería texto citable.
    """
    lineas = cuerpo.splitlines()
    secciones, actual, encabezado = [], [], None
    for ln in lineas:
        if re.match(r"^##\s+\S", ln) and not ln.startswith("###"):
            if actual and "".join(actual).strip():
                secciones.append((encabezado, "\n".join(actual).strip()))
            encabezado = ln.lstrip("#").strip()
            actual = []
        else:
            actual.append(ln)
    if actual and "".join(actual).strip():
        secciones.append((encabezado, "\n".join(actual).strip()))
    return secciones


def main():
    ap = argparse.ArgumentParser(description="Ingesta del corpus wiki en wiki.*")
    ap.add_argument("--wiki-dir", default="wiki")
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    dsn = args.dsn or (
        "host=localhost port=5433 dbname=meridian user=postgres password="
        + os.environ.get("IPM_CANONICAL_DB_PASSWORD", "")
    )

    docs, chunks = [], []
    descartados = 0
    for path in sorted(pathlib.Path(args.wiki_dir).rglob("*.md")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        fm, cuerpo = parse_frontmatter(raw)
        rel = str(path).replace("\\", "/")
        doc_id = content_uuid("doc", rel)
        todas = split_sections(cuerpo)
        secciones = [(h, t) for h, t in todas if len(t) >= MIN_CHARS_CHUNK]
        descartados += len(todas) - len(secciones)
        docs.append({
            "Id": doc_id, "Path": rel, "Slug": fm.get("slug"),
            "Title": fm.get("title"), "DocType": fm.get("type"),
            "CoreSlug": fm.get("core_slug"), "ContentHash": sha256_hex(raw),
            "ChunkCount": len(secciones),
        })
        for i, (encabezado, texto) in enumerate(secciones):
            chunks.append({
                "Id": content_uuid("chunk", rel, encabezado, texto),
                "DocumentId": doc_id, "Ordinal": i, "Heading": encabezado,
                "Content": texto, "ContentHash": sha256_hex(texto),
                "CharCount": len(texto),
            })

    print(f"documentos: {len(docs)}   chunks: {len(chunks)}")
    largos = sorted((c["CharCount"] for c in chunks), reverse=True)
    if largos:
        print(f"tamaño de chunk — máx {largos[0]}  ·  mediana {largos[len(largos)//2]}  ·  mín {largos[-1]}")
    sin_encabezado = sum(1 for c in chunks if not c["Heading"])
    print(f"chunks de preámbulo (sin ##): {sin_encabezado}")
    print(f"descartados por debajo de {MIN_CHARS_CHUNK} caracteres: {descartados}")

    if args.dry_run:
        print("\n[dry-run] no se escribió nada")
        return

    conn = psycopg2.connect(dsn)
    conn.autocommit = False
    cur = conn.cursor()
    try:
        psycopg2.extras.execute_batch(cur, """
            INSERT INTO wiki."Document"
                ("Id","Path","Slug","Title","DocType","CoreSlug","ContentHash","ChunkCount")
            VALUES (%(Id)s,%(Path)s,%(Slug)s,%(Title)s,%(DocType)s,%(CoreSlug)s,
                    %(ContentHash)s,%(ChunkCount)s)
            ON CONFLICT ("Id") DO UPDATE SET
                "Slug"=EXCLUDED."Slug", "Title"=EXCLUDED."Title",
                "DocType"=EXCLUDED."DocType", "CoreSlug"=EXCLUDED."CoreSlug",
                "ContentHash"=EXCLUDED."ContentHash", "ChunkCount"=EXCLUDED."ChunkCount",
                "IngestedAt"=now(), "RetiredAt"=NULL
            """, docs)

        psycopg2.extras.execute_batch(cur, """
            INSERT INTO wiki."Chunk"
                ("Id","DocumentId","Ordinal","Heading","Content","ContentHash","CharCount")
            VALUES (%(Id)s,%(DocumentId)s,%(Ordinal)s,%(Heading)s,%(Content)s,
                    %(ContentHash)s,%(CharCount)s)
            ON CONFLICT ("Id") DO UPDATE SET
                "Ordinal"=EXCLUDED."Ordinal", "IngestedAt"=now(), "RetiredAt"=NULL
            """, chunks)

        # Lo que ya no está en el corpus se retira, no se borra: una evidencia
        # que apunte a un chunk desaparecido debe seguir resolviendo.
        vivos = tuple(c["Id"] for c in chunks) or ("00000000-0000-0000-0000-000000000000",)
        cur.execute("""
            UPDATE wiki."Chunk" SET "RetiredAt" = now()
             WHERE "RetiredAt" IS NULL AND "Id" NOT IN %s
            """, (vivos,))
        retirados = cur.rowcount
        conn.commit()
        print(f"\nescrito. chunks retirados en esta pasada: {retirados}")
    except Exception as e:
        conn.rollback()
        sys.exit(f"ERROR, rollback: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
