# Verificación del alcance del corpus indexado

Reejecución del `verifiedBy` de la arista `vault-wiki`
(`iPM_GV/IPM_Infra/arquitectura_w4_componentes.json`), cuyo SQL original no se persistió.

**Generado por** `ops/verificar_alcance_corpus.py`. Ese script es la mitad del entregable:
lo que faltó el 2026-07-28 no fue la medición, fue que nadie pudiera re-correrla.

## Barreras declaradas

| Barrera | Valor |
|---|---|
| sesión | `set_session(readonly=True, autocommit=True)` — rechaza toda escritura |
| timeout | `SET statement_timeout='25s'` |
| transporte | TCP `127.0.0.1:5433` — **jamás `docker exec psql`** |
| usuario | `postgres`, porque `ipm_analytics` no tiene privilegio sobre `wiki.*` (42501) |
| credencial | leída de `iPM_GV/IPM_Infra/env/.env.prod` — **valor nunca impreso** |

## Veredicto

| Afirmación verificada | Resultado |
|---|---|
| La raíz de **todos** los `Path` es `wiki` | CONFIRMADA |
| **Cero** documentos del vault (`Predictions`) en el índice | CONFIRMADA |
| El primario de **D3** no está indexado; lo que casa es el resumen | CONFIRMADA |
| El primario de **S4** no está indexado | CONFIRMADA |
| Índice y disco son el mismo conjunto | **1 documento(s) con deriva** — ver §3 |

> **Sobre la única deriva.** Es `wiki/log.md`, el registro de actividad append-only.
> Está dentro del corpus indexado, así que **cada entrada que se le añade cambia su**
> **hash y lo desincroniza del índice hasta la siguiente ingesta**. Es esperado y
> benigno para este análisis —ningún target del gold set apunta a él— pero significa
> que el corpus nunca está exactamente sincronizado si alguien loggea. Se anota; no
> se corrige aquí.

## Estado del índice

| | |
|---|---|
| `wiki."Document"` vigentes | **164** |
| `wiki."Chunk"` vigentes | **1313** |
| última ingesta | 2026-08-05 20:09:12.992570+00:00 |

## 1 · Raíz de `Path` — `SELECT DISTINCT split_part("Path",'/',1)`

Raíces distintas: **`wiki`**

→ CONFIRMA la afirmación «la raíz de TODOS es `wiki`».

## 2 · Documentos del vault — `Path ILIKE '%prediction%'`

**0 filas.** → CONFIRMA «cero documentos del vault».

## 3 · Deriva `Path` + `ContentHash` — índice vs disco

Indexados: **164** · en disco bajo `wiki/`: **164**

| clase | n |
|---|---|
| sólo en DB (indexado, ya no en disco) | **0** |
| sólo en disco (no indexado) | **0** |
| mismo `Path`, **hash distinto** | **1** |

**hash distinto:**
- `wiki/log.md`

## 4 · Targets `raw/` del gold set, por basename

El bench identifica documentos por basename en minúsculas, así que un target `raw/`
«acierta» si existe CUALQUIER documento indexado con ese nombre de fichero.

| Etiqueta | Target declarado | Qué hay en el índice con ese basename |
|---|---|---|
| E9 primario | `raw/internal-notes/palantir-manifesto-2025.md` | `wiki/incoming/palantir-manifesto-2025.md` ← **otro `Path`** |
| E9 related | `raw/internal-notes/palantir-wars-ice-programs.md` | `wiki/incoming/palantir-wars-ice-programs.md` ← **otro `Path`** |
| E9 related | `raw/internal-notes/karp-alex-research-2026-04-22.md` | **AUSENTE — nada que casar** |
| S4 primario | `raw/sanctions/russia-oil-2026-04.md` | **AUSENTE — nada que casar** |
| D2 primario | `raw/internal-notes/musk-afd-research-2025.md` | `wiki/incoming/musk-afd-research-2025.md` ← **otro `Path`** |
| D3 primario | `raw/central-banks/lagarde-ecb-2026-04.md` | `wiki/sources/Lagarde-ECB-2026-04.md` ← **otro `Path`** |

## 5 · Colisión D3, por `Path` EXACTO

| `Path` | ¿indexado? |
|---|---|
| `wiki/sources/Lagarde-ECB-2026-04.md` (el resumen) | **SÍ** |
| `raw/central-banks/lagarde-ecb-2026-04.md` (la fuente) | **NO** |

→ **CONFIRMADO como medición, no como inferencia de código:** el primario declarado
de D3 no está en el índice. Lo que el bench encuentra es el resumen — **otro
documento** que colapsa al mismo basename en minúsculas.

## 6 · Censo de colisiones por basename (0-bis) — sólo disco

Corpus declarado (`wiki/` + `raw/`): **160** basenames únicos, **19 grupos colisionan**,
**9 dentro del índice** (`wiki/` es lo único que `ipm_wiki_ingest.py` recorre).

### Dentro del índice — un documento puede contar como acierto de otro

- `launch-plan-april-21.md`
  - `wiki/dossiers/Launch-Plan-April-21.md`
  - `wiki/sources/Launch-Plan-April-21.md`
- `musk-elon.md`
  - `wiki/actors/MUSK-Elon.md`
  - `wiki/incoming/MUSK-Elon.md`
- `palantir-political-network.md`
  - `wiki/dossiers/Palantir-Political-Network.md`
  - `wiki/incoming/Palantir-Political-Network.md`
- `palantir.md`
  - `wiki/incoming/PALANTIR.md`
  - `wiki/institutions/PALANTIR.md`
- `pending-db-sync.md`
  - `wiki/incoming/pending-db-sync.md`
  - `wiki/pending-db-sync.md`
- `tech-power-nexus.md`
  - `wiki/incoming/Tech-Power-Nexus.md`
  - `wiki/themes/Tech-Power-Nexus.md`
- `thiel-peter.md`
  - `wiki/actors/THIEL-Peter.md`
  - `wiki/incoming/THIEL-Peter.md`
- `trump-donald.md`
  - `wiki/actors/TRUMP-Donald.md`
  - `wiki/incoming/TRUMP-Donald.md`
- `vance-jd.md`
  - `wiki/actors/VANCE-JD.md`
  - `wiki/incoming/VANCE-JD.md`

### Generador estructural — `wiki/sources/` nombra igual que su fuente cruda

`CLAUDE.md §4.11` define la página de resumen con `source-path: raw/folder/filename.md`,
y la práctica la nombra igual. **Cada `raw/` que se resuma añade una colisión más.**

- `wiki/sources/BlackRock-13F-2025-12-31.md` ↔ `raw/markets/blackrock-13f-2025-12-31.md`
- `wiki/sources/Chokepoint-Risk-2026-04.md` ↔ `raw/geopolitics/chokepoint-risk-2026-04.md`
- `wiki/sources/IMF-WEO-2026-04.md` ↔ `raw/institutions/imf-weo-2026-04.md`
- `wiki/sources/Lagarde-ECB-2026-04.md` ↔ `raw/central-banks/lagarde-ecb-2026-04.md`
- `wiki/sources/Powell-FOMC-2026-04.md` ↔ `raw/transcripts/powell-fomc-2026-04.md`
- `wiki/sources/Trump-Trade-Policy-2026-04.md` ↔ `raw/geopolitics/trump-trade-policy-2026-04.md`

**6 pares** de este tipo.

## 7 · Barrido de identidad por nombre en el tooling

**Control positivo:** el barrido debe encontrar `ipm_wiki_bench.py:79` [split-ultimo], que sabemos que existe.
Resultado: **ENCUENTRA**. 

| Fichero | Línea | Patrón | Código |
|---|---|---|---|
| `../iPM_GV/IPM_Backend_AI/tools/ipm_wiki_bench.py` | 136 | basename | `return os.path.basename(ruta).lower()` |
| `../iPM_GV/IPM_Backend_AI/tools/registrar_migraciones_canonical.py` | 195 | basename | `sin_commitear.append(os.path.basename(ruta))` |
| `../iPM_GV/IPM_Infra/ops/verificar-vocabulario-slots.py` | 371 | basename | `version = f"PRUEBA:{os.path.basename(args.plantilla_json)}"` |
| `ipm_wiki_bench.py` | 79 | split-ultimo | `return ruta.replace("\\", "/").split("/")[-1].lower()` |
| `ipm_wiki_bench_hibrido.py` | 85 | split-ultimo | `return ruta.replace("\\", "/").split("/")[-1].lower()` |
| `ipm_wiki_generator.py` | 413 | basename | `fname = os.path.basename(fp)` |
| `ipm_wiki_lint_referencias.py` | 103 | basename | `base = os.path.splitext(os.path.basename(p["file"]))[0]` |
| `ipm_wiki_to_graph.py` | 190 | basename | `'file': os.path.basename(wiki_file),` |
| `ops/verificar_alcance_corpus.py` | 113 | .stem | `(".stem",        re.compile(r"\.stem\b")),` |
| `ops/verificar_alcance_corpus.py` | 205 | split-ultimo | `por_basename[ruta.split("/")[-1].lower()].append(ruta)` |
| `ops/verificar_alcance_corpus.py` | 208 | split-ultimo | `bn = t.split("/")[-1].lower()` |

Triaje en el análisis: los de `bench` (×2) y `_hibrido` rompen la línea base;
`ipm_wiki_to_graph.py` está latente (invocación documentada sobre carpeta plana);
`ipm_wiki_lint_referencias.py` **ya devuelve `AMBIGUOUS`** — es el modelo a copiar.
`ipm_wiki_ingest.py` y `ipm_wiki_puentes.py` usan ruta completa: la identidad en la base
está sana, y eso descarta una migración de datos.

