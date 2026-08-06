# IMP Wiki — Activity Log
*Append-only. Never edit past entries. Format defined in CLAUDE.md.*

---

## 2026-08-06 | verificación + cierre de sesión | Alcance del corpus e identidad de documento en el tooling

> **ESTADO DEL FRENTE — pausa de 10 días desde hoy.** Esta entrada está escrita para alguien que no
> estuvo en la sesión. Si hace falta más contexto del que hay aquí, es un defecto de esta entrada.

- **Operation:** verificación (todo read-only sobre la base) + commit de material que estaba en disco y fuera de git
- **Disparador:** la arista `vault-wiki` del mapa (`iPM_GV/IPM_Infra/arquitectura_w4_componentes.json`) estaba `verified-absent` desde el 2026-07-28. Por la regla del mapa, un `current` de hace 9 días es hipótesis hasta reejecutar su `verifiedBy` — cuyo SQL nunca se persistió, sólo su descripción en prosa.

### Qué quedó hecho, y en qué commits

| Commit | Contenido |
|---|---|
| `88fb26f` | `ops/verificar_alcance_corpus.py` + `ops/VERIFICACION_ALCANCE_CORPUS.md` — el script y su informe, juntos |
| `687c211` | El pase Palantir del 2026-04-22 (19 ficheros): `wiki/incoming/` entero, 4 páginas nuevas en `wiki/`, 5 notas en `raw/internal-notes/` |
| `cb3e458` | `.claude/settings.json`, `.claude/skills/n8n-workflow/`, `n8n/`, `commands-for-agents.md`, `ipm-agent-stack/SKILL.md` |

**Todo pusheado a `origin/main`.** `b2a8204` (el linter de referencias, del 2026-08-05) también estaba sin pushear y salió en el mismo empujón — es el mismo riesgo, ya materializado.

**`687c211` merece leerse:** esos 19 ficheros **ya estaban en `wiki."Document"`**. `ipm_wiki_ingest.py` recorre `wiki/**/*.md`, así que `wiki/incoming/` entra al índice entero. **El corpus de 164 documentos contra el que se midió ADR-W4-04 incluía material que no estaba en ningún commit.**

### Reejecución del `verifiedBy` — CONFIRMA lo que la tarjeta afirmaba

```bash
python ops/verificar_alcance_corpus.py          # solo lectura; informe en ops/VERIFICACION_ALCANCE_CORPUS.md
```

**Prerrequisito — la credencial.** El script la busca por orden: `--dsn` → `$IPM_CANONICAL_DB_PASSWORD` → **`iPM_GV/IPM_Infra/env/.env.prod`, clave `IPM_CANONICAL_DB_PASSWORD`**, que es la vía normal y no requiere exportar nada. Sesión `readonly=True`, `statement_timeout='25s'`, TCP a `127.0.0.1:5433` (**jamás `docker exec psql`**), como `postgres` porque `ipm_analytics` da 42501 sobre `wiki.*`.

- **La raíz de los 164 `Path` es `wiki`** — confirmado. Y lo es *por construcción*: `ipm_wiki_ingest.py:103,115` tiene un solo `--wiki-dir` y hace `rglob` sobre él.
- **Cero documentos del vault** (`Path ILIKE '%prediction%'` → 0 filas) — confirmado.
- **Índice y disco coinciden hash a hash**, con una sola deriva: `wiki/log.md`, que es append-only y está dentro del corpus indexado, así que cada entrada que se le añade —incluida ésta— lo desincroniza hasta la siguiente ingesta. Esperado; se anota, no se corrige.

### Lo que la verificación destapó y no estaba en el `verifiedBy`

Análisis completo, con las tablas: **`ops/ANALISIS_ALCANCE_E_IDENTIDAD_2026-08-06.md`**.

1. **El alcance declarado del gold set es falso en dos sumandos.** Dice «wiki 164 + raw 15 + Predictions 30 ≈ 209 md». `Predictions` tiene **21** ficheros, no 30, y **cero indexados**. De los 15 `raw/`, sólo **4** llegaron al índice vía `wiki/incoming/`. Ausente del alcance declarado: **32 documentos**, no 30.
2. **19 grupos de basename colisionan** en el corpus declarado, **9 dentro del índice**. El bench identifica documentos por basename en minúsculas, así que un documento puede contar como acierto de otro.
3. **Seis de esas colisiones las genera `CLAUDE.md §4.11` por diseño**, al nombrar cada página de `wiki/sources/` igual que su fuente cruda. **Crecen solas: cada `raw/` que se resuma añade una.** El instrumento se degrada a medida que la wiki hace bien su trabajo.
4. **Cuatro etiquetas firmadas del gold set están comprometidas** (E9, S4, D2, D3). El primario de **D3** no está indexado — lo que el bench encuentra es `wiki/sources/Lagarde-ECB-2026-04.md`, **otro documento**. El de **S4** tampoco está. Medido por `Path` exacto, no inferido del código.
5. **El 1,00 en inglés de la pata densa queda SIN DETERMINAR.** `ADR-W4-04.md:144-146` lo apoya en E9; de sus tres `related`, uno está limpio, uno casa con otro documento y uno está ausente. Cuál produjo el acierto no se sabe sin reejecutar. **No está refutado: está sin determinar, que es distinto de estar mal y peor que estar bien.**
6. **La línea base de 0,85 sólo es reproducible en Windows.** Los dos benches usan mecanismos distintos de extracción de basename que sólo coinciden en este sistema operativo. Dependencia de entorno no declarada en ningún sitio.

### TRES DECISIONES SIN FIRMAR — bloquean todo lo demás

1. **¿Cuál de los dos `ipm_wiki_bench.py` es el bench?** Hay dos ficheros con el mismo nombre y **comportamiento distinto**: el de este repo (168 líneas, sólo léxico) y `IPM_Backend_AI/tools/` (310 líneas, con pata densa). **Los números de ADR-W4-04 salieron del de `tools/` — certeza, no inferencia: el de 168 no puede producir esa tabla.** Opciones A/B/C en `ops/ANALISIS_…:§6.1`; **recomendada C** (renombrar el de este repo a `ipm_wiki_bench_lexico.py`), la única que no toca nada firmado.
2. **¿Qué se hace con `wiki/incoming/`?** Sus 14 ficheros están indexados; 8 colisionan por basename con su página canónica y **los 8 difieren en contenido**. Bloquea también los 5 ambiguos del resolver y el `WikiSlug=NULL` de palantir. Quien la cierre debe aplicar la misma Opción C del corte del 2026-08-05 (entrada de abajo).
3. **¿`core_slug:` va al frontmatter de los 65?** Pendiente desde el efecto colateral de la reingesta del 2026-08-05.

### TRAMPA CARGADA — `ipm_wiki_to_graph.py:190`

Identifica documentos por `os.path.basename`. **Hoy no colapsa nada** porque su invocación documentada apunta a `wiki/companies/`, una carpeta plana con cero colisiones internas, y porque nadie lo usa como fuente de identidad (ver línea 59 de este log).

> **Se arma el día que alguien apunte `--wiki-dir` a `wiki/incoming/`** — exactamente donde están las 8 colisiones con contenido divergente. Dos documentos colapsarían en un nodo del grafo exportado.

- **Contradictions flagged:** none — la verificación confirma el análisis en todos sus puntos
- **DB sync needed:** no — nada de esta sesión escribe en la base
- **Notes:**
  - **Trabajo especificado y deliberadamente NO ejecutado** (`ops/ANALISIS_…:§7`): corregir el alcance en el gold set, ajustar `ADR-W4-04.md` §5/§6, abrir tres flags en `pending-db-sync.md`, corregir las aristas `vault-wiki` y `mcp_ro` del mapa, recalcular la línea base, y el fix de identidad (cinco sitios en dos repos). **Los cuatro primeros tocan documentos firmados y no hay quien los cierre durante la pausa. Un cambio a medias en un documento firmado es peor que no empezarlo.**
  - **`mcp-ipm-postgres-ro` no está configurado en ningún cliente** (`.claude.json` con `mcpServers` vacío; los `.mcp.json` del vecino sólo registran `ipm-devops`). El mapa dice que su consumidor «está fuera del sistema dibujado»; medido, `AccessLog=0` no significa «lo llama alguien de fuera del diagrama» sino **«nadie puede llamarlo»**.
  - **Cinco ficheros quedan sin commitear a propósito, ninguno borrado**, todos revisados: `aas` (7 KB, volcado de `git log` con nombres de commit y ficheros — regenerable, nombre que parece una redirección mal escrita); `link_occurrences.json` (187 KB, salida de `ipm_wiki_lint_referencias.py` — regenerable); `test.txt` y `raw/internal-notes/test.txt` (0 bytes); `raw/internal-notes/test.md` (contiene la palabra «test»). **No se tocó `.gitignore`**: clasificarlos es decisión con dueño, y se deja visible en vez de resuelta. `donald-trump.md` en la raíz está trackeado y vacío (0 bytes) — mismo caso.
  - `.claude/settings.local.json` queda fuera del commit **a propósito**: es configuración por máquina por convención de Claude Code. Ninguno de los `.claude/*.json` contiene secretos; se revisaron antes de añadir.
  - **Lección de método, y no es de wiki.** La credencial se pidió cuatro veces y se prometió cuatro veces, pero el mecanismo no podía funcionar: cada invocación del agente arranca un shell nuevo, así que un `export` en otra terminal nunca llega. Se resolvió leyéndola de donde ya vive (`.env.prod`), sin crear otra copia del secreto. **Toda dependencia que cruza sesiones necesita un mecanismo verificable, no un anuncio** — la misma regla que ya se aplicó al gate con `ipm_science`, resuelto con artefacto en disco + sha256.

---

## 2026-08-05 | fix | Bridge wikiDepth de 7 entidades — companies/ vs institutions/ duplicados

- **Operation:** fix (remediación del defecto medido en MEDICION_WIKI_CORE_2026-08-05.md, §2 y §4)
- **Contexto:** la limpieza de duplicados del 2026-07-31 retiró 8 páginas institutions/{NVIDIA,APPLE,MICROSOFT,AMAZON,TSMC,LOCKHEED-MARTIN,BLACKROCK,PALANTIR}.md sin puentear su contraparte más rica en companies/, dejando 7 entidades con wikiDepth=0 pese a tener 5.000-12.000 caracteres de contenido real esperando en companies/.
- **Decisión (Opción C, negociada con ipm_science tras descartar mover-fuera-de-wiki/ y excluir Palantir):**
  - `slug:` removido del frontmatter de 7 institutions/*.md (NVIDIA, APPLE, MICROSOFT, AMAZON, TSMC, LOCKHEED-MARTIN, BLACKROCK) — quedan en disco, sin bridge, para no perder el respaldo de las citas de `core.RelationEvidence.WikiChunkRef` que apuntan a sus chunks.
  - `slug:` agregado al frontmatter de 10 companies/*.md: 001_nvidia→nvidia, 002_apple→apple, 004_microsoft→microsoft, 005_amazon→amazon, 041_tsmc→tsmc, 068_lockheed_martin→lockheed-martin, 090_blackrock→blackrock, 097_northrop_grumman→northrop-grumman, 080_raytheon_technologies→raytheon-technologies, 201_spacex→spacex.
  - `institutions/PALANTIR.md` y `companies/096_palantir.md` explícitamente NO tocados: `core.Entity` de palantir tiene `WikiSlug=NULL` (bloqueado por los 5 ambiguos de wiki/incoming/), así que ninguno de los dos alimenta wikiDepth hoy — es un problema distinto, con otro dueño.
- **Commits:** `8be60d9` (7 institutions/), `dfe3d09` (10 companies/), `1b89c1f` (docs/ops: corte registrado)
- **Reingesta:** `ipm_wiki_ingest.py` corrido una sola vez, después de ambos commits. `MAX("IngestedAt")` en wiki.Document y wiki.Chunk: 2026-08-05 20:09:12 UTC (antes: 2026-07-25 21:38:14 en Document — Chunk ya tenía escrituras del 31/07 sin explicar, ver Notes).
- **Verificado tras la reingesta:**
  - Σ known (wikiDepth) sobre las 33 companies puenteadas: 161 → **157** (predicho antes de conocer el resultado, coincide exacto). El delta no es pérdida de cobertura: NVIDIA y Microsoft tenían 7 chunks vigentes por un escritor no identificado del 31/07 (2 de más cada uno, `Document.ChunkCount` seguía en 5) — la reingesta corrige a los 5 reales. Las otras 31 entidades, sin cambios. BlackRock no capeó (known=5, no 14) — ese era el objetivo de elegir C.
  - `citas_sobre_documento_retirado`: **13 → 0**. Los 8 institutions/ volvieron a vigente (el upsert pone `RetiredAt=NULL` a cualquier archivo presente en disco) y sus chunks con ellos — el `Id` es content-addressed (`content_uuid(ruta, encabezado, texto)`) y ninguno de esos textos cambió. Las 13 citas pasaron de resolver sobre documento retirado a resolver sobre documento vigente. Las 85 con referencia siguen resolviendo las 85.
    **Nota para el lector futuro:** los 7 archivos quedan VIGENTES en la base y SIN `slug:`. Eso no es contradictorio — es exactamente el estado que buscaba la Opción C: documento vivo, chunks vivos, citas resolviendo, sin bridge y por tanto sin colisión de Slug ni capeo de wikiDepth.
  - `ipm_wiki_audit.py`: 9 conflictos, sin cambios — los 5 `duplicado_en_wiki` siguen siendo los de la red Palantir/Thiel/Vance, ninguno nuevo introducido.
- **Contradictions flagged:** none
- **DB sync needed:** no — cambios wiki-only + reingesta, no tocan core.*
- **Notes / riesgos abiertos, fuera de este alcance:**
  - **Efecto colateral declarado, no un fallo:** la reingesta puso `CoreSlug` en NULL para los 62 documentos que lo tenían (`ipm_wiki_ingest.py` lo reescribe desde `fm.get("core_slug")`, y ningún .md del vault tiene ese campo en frontmatter — los 62 los había escrito `ipm_wiki_puentes.py` por UPDATE directo a la base, no el ingest). `wiki."v_PuenteIncoherente"` pasó de 10 a 65 en consecuencia. No afecta wikiDepth (une por `Slug`, no por `CoreSlug`) ni a `WikiChunkRef` (resuelve por `DocumentId`). Restaurar `CoreSlug` con `ipm_wiki_puentes.py aplicar()` queda pendiente, deliberadamente fuera de este corte — es escritura y necesita su propia medición antes/después.
  - `institutions/PALANTIR.md` resucitó como efecto colateral de la reingesta (queda en disco, cualquier archivo vivo se revive con `RetiredAt=NULL`). Inofensivo hoy porque `WikiSlug` de palantir es NULL — pero el día que esa ambigüedad se resuelva, este documento va a volver a sumar sus 13 chunks junto a companies/096_palantir.md, reproduciendo el mismo doble conteo que este fix acaba de resolver para los otros 7. Quien cierre wiki/incoming/ debe aplicar la misma Opción C ahí.
  - `ipm_wiki_generator.py` no escribe `slug:` en su plantilla y sus `--company-ids` por defecto (1,2,4,41,68,90,96) cubren 6 de estos 10 archivos. Si se vuelve a correr para "refrescar" las páginas auto-generadas, sobrescribe el `slug:` recién agregado sin aviso, y el defecto vuelve a aparecer recién en la siguiente reingesta. Diagnóstico y propuesta de fix: encargo aparte, no en este commit.
  - **Desviación de método registrada:** la predicción de `documentos_con_Slug` (140) se derivó del «137 páginas con slug: propio» del informe fuente en vez de medirlo con el parser del propio ingest. Medido: 142 antes del corte (y 22 sin slug, no 27), 145 después. No afecta a ningún contador de puerta — Σknown dio 157 exacto y Slug no era contador de verificación. Es la tercera cifra de MEDICION_WIKI_CORE_2026-08-05.md que no se reproduce, junto con «55 entidades puenteadas» (medía CoreSlug cuando el join de wikiDepth usa Slug) y «el ingest corrió una sola vez» (midió IngestedAt sobre Document y no sobre Chunk, que tenía 7 filas del 31/07 12:58 y 7 del 14:20). Ese informe se cita como catálogo con cuidado: cada cifra trae su consulta al lado, pero tres eligieron la columna adyacente a la que gobierna el comportamiento.

---

## 2026-08-02 | lint-fix | Wikilink dialect remediation (Acciones 1 y 2)

- **Operation:** lint-fix — normalización de wikilinks rotos/dialectales, sin creación de páginas nuevas
- **Commits:** `114c951` (Acción 1), `2463f7a` (Acción 2)
- **Acción 1 — rewrite dialectal:** 106 ocurrencias de wikilinks rotos (kebab-case gen-2 y nombre-natural-con-alias gen-3) reescritas a formato relativo canónico `[[../carpeta/PAGINA]]`, validado contra el filesystem. 27 archivos tocados (12 actors/, 11 companies/, comparisons/, oracle/, 2 themes/). Criterio: `institutions/` preferido sobre `companies/` en las 8 entidades duplicadas; `wiki/incoming/` excluido (cola de parches sin mergear — ver entrada 2026-04-22 fix).
- **Acción 2 — placeholder Unknown:** 27 `[[Unknown|Unknown]]` → texto plano «entidad no resuelta» en los 10 wiki/companies/*.md generados 2026-04-19. Origen: edges hacia *facilities* (HQ/DataCenter/Fab/Logistics), tipo excluido de core_vocabulario.json (451 filas fuera del vocabulario canónico) — el generador no encontró nombre canónico y dejó "Unknown".
- **Estado post-operación:** 950→923 ocurrencias `[[...]]` totales (-27 por Acción 2); rotos/ambiguos 232→99 (-133).
  - De los 99 restantes: 88 sin página destino (backlog — candidatos a Acción 3, creación de páginas), 6 dentro de wiki/incoming/ (fuera de alcance), 5 falsos positivos de prosa (ejemplos de sintaxis entre backticks en log.md:210 y lint-reports/2026-04-09.md:69,71,73 — no son links reales; excluyéndolos del check, el número objetivo baja a 94).
- **Contradictions flagged:** none
- **DB sync needed:** no — cambios wiki-only, no tocan schema ni entidades
- **Notes:** Los 27 «entidad no resuelta» quedan pendientes de cruce manual contra la tabla `Facilities` de la DB. `resolve-unresolved-facilities.sh` es un nombre **propuesto** para ese script futuro — no existe todavía, no confundir con un artefacto ya creado. No se tocó `core_vocabulario.md`, `raw/`, `ipm-agent-stack/`, ni `wiki/incoming/`.

---

## [2026-04-22] fix | Schema corrections — Palantir Political Network pages

- **Operation:** schema-fix (triggered by ipm_wiki_generator.py / ipm_wiki_to_graph.py audit)
- **Root cause:** Prior session created 4 pages using `last_updated` instead of `updated`, missing `created`, invalid enum values in `role` and `type` fields, and one pending-db-sync SQL with wrong column names.
- **Files updated:**
  - wiki/actors/THIEL-Peter.md — `last_updated` → `updated`; added `created: 2026-04-22`; `role: founder` → `role: oligarch` (enum fix); added missing `related_countries`, `related_commodities` fields
  - wiki/actors/VANCE-JD.md — `last_updated` → `updated`; added `created: 2026-04-22`; added missing `related_countries`, `related_commodities` fields
  - wiki/themes/Tech-Power-Nexus.md — `last_updated` → `updated`; added `created: 2026-04-22`; added missing `related_countries`, `related_commodities` fields
  - wiki/dossiers/Palantir-Political-Network.md — `last_updated` → `updated`; added `created: 2026-04-22`; `type: dossier` → `type: reference` (enum fix); added missing `sources`, `related_countries`, `related_commodities`
  - wiki/pending-db-sync.md — CL-DB-028 SQL corrected: `"FromEntityId"`/`"ToEntityId"` → `"SourceId"`/`"TargetId"` (actual DB schema confirmed via ipm_wiki_to_graph.py)
- **Known gap not fixed:** `institution_type: regulator` on PALANTIR.md is semantically wrong but no correct enum value exists — needs schema extension (`corporation` or `defense-tech`)
- **Known gap not fixed:** `wiki/incoming/` directory (14 stale draft files) — orphaned staging area from prior session; pending manual cleanup
- **Contradictions flagged:** none
- **DB sync needed:** no — fixes are wiki schema only
- **Notes:** The two pipeline scripts (`ipm_wiki_generator.py`, `ipm_wiki_to_graph.py`) are blind to hand-crafted pages (actors/institutions/themes use `db_id`; sync script requires `entity_id`). Hand-crafted pages reach DB exclusively via manual SQL in pending-db-sync.md.

---

## [2026-04-22] ingest | Palantir Political Network — research pass

- **Operation:** ingest (4 internal research notes → wiki pages)
- **Sources ingested:**
  - raw/internal-notes/palantir-manifesto-2025.md (Priority 7 — Karp doctrine, 22-point thread, reception)
  - raw/internal-notes/palantir-wars-ice-programs.md (Priority 7 — ImmigrationOS, Maven, Ukraine, Gaza)
  - raw/internal-notes/vance-thiel-palantir-network.md (Priority 7 — career pipeline, Thiel network in Trump 2.0)
  - raw/internal-notes/musk-afd-research-2025.md (Priority 7 — AfD endorsement timeline, DFRLab analysis)
- **Files created:**
  - wiki/actors/THIEL-Peter.md — co-founder Palantir, Founders Fund GP, Vance kingmaker, $24B est. net worth
  - wiki/actors/VANCE-JD.md — 49th/50th VP, Thiel protégé, Mithril→Narya→Senate→VP pipeline
  - wiki/themes/Tech-Power-Nexus.md — Silicon Valley → state coercive power convergence under Trump 2.0
  - wiki/dossiers/Palantir-Political-Network.md — synthesis: network map, manifesto, ICE stack, Maven, Musk/AfD, political risk
  - raw/internal-notes/palantir-manifesto-2025.md (source note)
  - raw/internal-notes/palantir-wars-ice-programs.md (source note)
  - raw/internal-notes/vance-thiel-palantir-network.md (source note)
  - raw/internal-notes/musk-afd-research-2025.md (source note)
- **Files updated:**
  - wiki/institutions/PALANTIR.md — full rewrite: product stack (Gotham/Foundry/AIP/Maven/Skykit/MetaConstellations), internal structure (Karp/Cohen/Sankar/Thiel), Trump 2.0 contract surge ($1.3B+), ImmigrationOS, Ukraine, narrative shift, market channels. db_id fixed to 96.
  - wiki/actors/MUSK-Elon.md — AfD endorsement entries added to Key Recent Actions (Dec 2024, Jan 9, Jan 25 2025); European political actor dimension added to Narrative Shift; afd added to related_institutions.
  - wiki/actors/TRUMP-Donald.md — Thiel/Vance/Palantir entries added to Key Recent Actions; thiel-peter + vance-jd added to related_actors; palantir added to related_institutions.
  - wiki/pending-db-sync.md — CL-DB-023 through CL-DB-029 registered (7 new flags: Thiel Person, Vance Person, AfD Company, Thiel→Palantir edge, Thiel→Vance edge, Palantir→ICE edge, Musk→AfD edge)
  - wiki/index.md — v28, 146 pages; THIEL + VANCE added to actors table; Tech-Power-Nexus added to themes; Palantir-Political-Network added to dossiers; PALANTIR db_id corrected to 96
- **Contradictions flagged:** None — internal notes are Priority 7 hypotheses; no contradiction with existing Priority 1-4 sourced wiki content
- **DB sync needed:** yes — CL-DB-023 (Thiel Person), CL-DB-024 (Vance Person), CL-DB-025 (AfD Company), CL-DB-026 (Thiel→Palantir edge), CL-DB-027 (Thiel→Vance edge), CL-DB-028 (Palantir→ICE edge), CL-DB-029 (Musk→AfD edge)
- **Notes:** All new pages confidence=MEDIUM per CLAUDE.md — Priority 7 sources only; requires upgrade when Priority 1-4 corroborating sources (official contract filings, Palantir SEC filings, Congressional testimony) ingested. IDF/Gaza claim confidence=LOW — allegation only, no direct contract confirmation. Total open DB flags now: 18 (CL-DB-012 through CL-DB-029).

---

## [2026-04-22] wiki-expansion | European Companies — 6 new institution pages
- **Operation:** wiki-expansion
- **Files created:**
  - wiki/institutions/RHEINMETALL.md — German defense; €50B+ order backlog, Ukraine JV, RHM.DE conviction proxy
  - wiki/institutions/AIRBUS.md — EU aerospace; 8,500+ aircraft backlog, Boeing crisis windfall, Eurofighter surge
  - wiki/institutions/TOTALENERGIES.md — French oil major; Qatar LNG JV, Hormuz exposure, Russia Arctic write-down
  - wiki/institutions/DEUTSCHE-BANK.md — German bank; €40T derivatives book, CDS spread as EU stress barometer
  - wiki/institutions/VOLKSWAGEN.md — German auto; China share 20%→12%, CARIAD delays, plant closure crisis
  - wiki/institutions/LVMH.md — French luxury; Bernard Arnault controlling shareholder, cognac tariff risk
- **Files updated:**
  - wiki/countries/GERMANY.md — related_institutions expanded; Related Pages section added (Rheinmetall, VW, Deutsche Bank, Airbus)
  - wiki/countries/FRANCE.md — related_institutions expanded; Related Pages section added (TotalEnergies, Airbus, LVMH)
  - wiki/pending-db-sync.md — CL-DB-016 through CL-DB-022 registered in Open Flags table
  - wiki/index.md — v27, 142 pages, European Companies section added to Institutions (31→37)
- **Contradictions flagged:** none
- **DB sync needed:** yes — CL-DB-016 (ASML edges), CL-DB-017 (Rheinmetall), CL-DB-018 (Airbus), CL-DB-019 (TotalEnergies), CL-DB-020 (Deutsche Bank), CL-DB-021 (Volkswagen), CL-DB-022 (LVMH + Arnault)
- **Notes:** All 6 pages follow CLAUDE.md v3.0 schema. institution_type set to 'regulator' as placeholder for industrial companies — enum should be extended to include 'manufacturer' or 'corporation'. DB IDs all TBD pending sync. Total open DB flags now: 11 (CL-DB-012 through CL-DB-022).

---

## [2026-04-09] init | IMP Wiki v1.0 created
- **Operation:** init
- **Files created:** CLAUDE.md, wiki/index.md, wiki/log.md, wiki/overview.md — full folder structure
- **Files updated:** —
- **Contradictions flagged:** none
- **DB sync needed:** no
- **Notes:** Repo initialized. Karpathy LLM Wiki pattern adapted for IMP. Option A confirmed — separate repo from main iPM_GV codebase. Ready for first ingest.

## [2026-04-09] ingest | IMP_Strategy_v2_2.docx
- **Operation:** ingest
- **Files created:**
  - wiki/sources/IMP-Strategy-v2-2.md
  - wiki/themes/IMP-Platform-Architecture.md
  - wiki/themes/IMP-Automation-Engine.md
  - wiki/themes/IMP-Oracle-System.md
  - wiki/themes/IMP-Competitive-Moats.md
  - wiki/themes/IMP-Business-Model.md
  - wiki/themes/IMP-Power-Index-System.md
  - wiki/timelines/IMP-Phase-Roadmap.md
  - wiki/oracle/Oracle-Machine-Roster.md
  - wiki/actors/DALIO-Ray.md
- **Files updated:** wiki/index.md
- **Contradictions flagged:** none
- **DB sync needed:** no — strategy doc is documentation, not entity data
- **Notes:** First real ingest. 10 pages created from one source. IMP platform skeleton now in wiki. All 20 Oracle machine names documented. Phase roadmap captured with current blocker status. DB state gaps flagged as open questions throughout.

## [2026-04-09] ingest | IPM_SQL_Seed_Reference.docx
- **Operation:** ingest
- **Files created:**
  - wiki/sources/IPM-SQL-Seed-Reference.md
  - wiki/indicators/DB-ID-Reference.md
  - wiki/indicators/Enum-Types-Reference.md
  - wiki/actors/TRUMP-Donald.md (db_id: 173)
  - wiki/actors/XI-Jinping.md (db_id: 171)
  - wiki/actors/PUTIN-Vladimir.md (db_id: 172)
  - wiki/actors/POWELL-Jerome.md (db_id: 192)
  - wiki/actors/LAGARDE-Christine.md (db_id: 191)
  - wiki/actors/FINK-Larry.md (db_id: 75)
  - wiki/actors/MUSK-Elon.md (db_id: 7)
  - wiki/actors/HUANG-Jensen.md (db_id: 1)
  - wiki/actors/DIMON-Jamie.md (db_id: 12)
  - wiki/actors/ALTMAN-Sam.md (db_id: 61)
  - wiki/actors/MACRON-Emmanuel.md (db_id: 174)
  - wiki/actors/BUFFETT-Warren.md (db_id: 9)
  - wiki/actors/BEZOS-Jeff.md (db_id: 66)
  - wiki/actors/GATES-Bill.md (db_id: 67)
  - wiki/actors/ZUCKERBERG-Mark.md (db_id: 6)
  - wiki/actors/CHANG-Morris.md (db_id: 113)
- **Files updated:** wiki/index.md
- **Contradictions flagged:** none
- **DB sync needed:** no — document defines DB state, does not require updates to it
- **Notes:** 16 actor stubs created with verified db_ids. 2 indicator pages created (DB-ID-Reference, Enum-Types-Reference). All PersonPowerIndex seeding status documented per actor. Musk + Trump flagged as standard migration test pair.

## [2026-04-09] manual-edit | CLAUDE.md upgraded to v2.0
- **Operation:** manual-edit
- **Files created:** CLAUDE.md v2.0
- **Files updated:** —
- **Contradictions flagged:** none
- **DB sync needed:** no
- **Notes:** Upgraded all 10 page templates based on Perplexity v2 guide review. Added: region+tags frontmatter, Role and Levers section, Narrative Shift section, Key Recent Actions with dates to actor template. Added Sanctions and Legal Constraints + Key Timelines to country template. Added full institution, commodity, narrative, market-impact, scenario templates (previously missing). Added domain frontmatter + Rationale + Inputs + Calculation Logic + Maintenance Rules to indicator template. Added source priority tiers table. Added specialized ingest focus rules by source type. Added narrative drift detection and geopolitics-to-markets connection rules.

## 2026-04-09 | schema-upgrade | CLAUDE.md v3.0 + frontmatter migration
- source: uploaded files (imp-mini-claude-frontmatter-rules.md, templates)
- created: CLAUDE.md v3.0
- updated: all 17 actor pages — new frontmatter schema applied
- contradictions: none
- db-sync: no
- notes: Added slug, related_actors, related_countries, related_institutions, related_commodities, related_themes arrays to all actor pages. Added role, country fields. Upgraded CLAUDE.md to v3.0 with full frontmatter governance section, reciprocal relationship rules, deduplication rules, 11 page type templates with new schema. Source priority tiers and specialized ingest modes preserved from v2.0.

## 2026-04-09 | ingest | IPM_Session_Record_2026_03_27.md
- source: raw/internal-notes/IPM_Session_Record_2026_03_27.md
- created: wiki/sources/Session-Record-2026-03-27.md
- created: wiki/timelines/IMP-DB-State-Timeline.md
- created: wiki/themes/Chokepoint-Intelligence.md
- created: wiki/dossiers/Product-Ideas-2026-03-27.md
- created: wiki/comparisons/IMP-Agent-Roles.md
- created: wiki/countries/UNITED-STATES.md (db_id: 1)
- created: wiki/countries/CHINA.md (db_id: 148)
- created: wiki/countries/RUSSIA.md (db_id: 64)
- created: wiki/countries/TAIWAN.md (db_id: 151)
- created: wiki/countries/UKRAINE.md (db_id: 65)
- created: wiki/countries/SAUDI-ARABIA.md (db_id: 71)
- updated: wiki/index.md
- contradictions: none
- db-sync: no — source IS the DB state record
- notes: First country pages created with full new frontmatter schema. DB state timeline established as append-only reference. 7 product ideas archived in dossiers/. Agent roles comparison documented. Chokepoint intelligence theme page created with all 7 IMP chokepoints. Key pending seeds flagged: Trump/MBS/Bessent PersonPowerIndex, Aladdin node, IdeologyProfiles for Fink/Xi/MBS.

## 2026-04-09 | ingest | IPM_Project_State_2026_04_01.md
- source: raw/internal-notes/IPM_Project_State_2026_04_01.md
- created: wiki/sources/Project-State-2026-04-01.md
- created: wiki/actors/MBS.md (db_id: 176)
- created: wiki/actors/BESSENT-Scott.md (db_id: 545)
- created: wiki/actors/MODI-Narendra.md (db_id: TBD)
- created: wiki/actors/YELLEN-Janet.md (db_id: TBD)
- updated: wiki/timelines/IMP-DB-State-Timeline.md — April 1 snapshot appended
- updated: wiki/actors/TRUMP-Donald.md — score confirmed 76 rank 1
- updated: wiki/actors/GATES-Bill.md — score confirmed 71 rank 8
- updated: wiki/indicators/DB-ID-Reference.md — full 14-person ranking added, MBS=176, Bessent=545
- updated: wiki/index.md — actors table now shows full ranking
- contradictions: none — Trump score was "target 76", now confirmed 76 ✅
- db-sync: no — source IS the DB state record
- notes: Full PersonPowerIndex ranking now documented (14 persons). 4 new actor pages. C# vs DB column name map archived in DB timeline. Auth blocker (B-02) confirmed COMPLETE. B-04 (CompositeIndexSnapshots) still failing.

## 2026-04-09 | ingest | IPM_Session_Handoff_2026_04_02.md + IPM_Launch_Plan_April21.html
- source: raw/internal-notes/IPM_Session_Handoff_2026_04_02.md
- source: raw/internal-notes/IPM_Launch_Plan_April21.html
- created: wiki/sources/Session-Handoff-2026-04-02.md
- created: wiki/sources/Launch-Plan-April-21.md
- created: wiki/dossiers/Launch-Plan-April-21.md
- updated: wiki/timelines/IMP-DB-State-Timeline.md — April 2 checkpoint appended
- updated: wiki/index.md
- contradictions: none
- db-sync: yes — Launch Plan flags two DB sync needs: (1) Trump↔Powell VsOverlay divergence data needed, (2) Semiconductor PowerMap PowerMapRelation edges still empty
- notes: All 6 internal IMP project sources now ingested. Launch plan archived as dossier with 6 persona profiles and critical path deadlines. April 21 is 12 days from today — active deadline. DB timeline now covers March 27 → April 1 → April 2.

## 2026-04-09 | query | Trump-Powell IdeologyProfile divergence
- source: live DB query (IdeologyProfile table, EntityIds 173 + 192)
- created: wiki/comparisons/Trump-Powell-Divergence.md
- updated: wiki/actors/TRUMP-Donald.md — ideology scores added
- updated: wiki/actors/POWELL-Jerome.md — ideology scores added
- contradictions: none
- db-sync: no — DB is source of truth, wiki now reflects it
- notes: DSI signal = 4.25 (high tension). Highest divergence: EnvScore 9.5. Most policy-relevant: AuthScore 7.5 gap. EconScore gap only 1.0 — both economically conservative. Trump-Powell divergence is a political pressure signal, not monetary policy divergence signal. DB sync flag CL-DB-001 RESOLVED.

## 2026-04-09 | query | Powell-Lagarde IdeologyProfile divergence — EUR/USD signal
- source: live DB query (IdeologyProfile table, EntityIds 191 + 192 + 173)
- created: wiki/comparisons/Powell-Lagarde-Divergence.md
- updated: wiki/actors/LAGARDE-Christine.md — ideology scores added
- contradictions: none
- db-sync: no — DB is source of truth, wiki now reflects it
- notes: EUR/USD signal = 4.5 (strong divergence zone). EconScore gap 6.0 = primary driver (Powell conservative 4.0 vs Lagarde left-of-center -2.0). Three-way comparison documented: Trump-Lagarde divergence 9.75 = near maximum in dataset. DB sync flag CL-DB-002 RESOLVED.

## 2026-04-09 | manual-edit | Graph view wikilinks — all pages updated
- Operation: manual-edit
- Files updated: 21 actor pages + 6 country pages + 5 theme/comparison pages + 10 institution stubs created
- Contradictions flagged: none
- DB sync needed: no
- Notes: Added [[wikilink]] syntax to Related Pages sections across all pages so Obsidian Graph View shows connections. Created institution stubs for BlackRock, Federal Reserve, ECB, JPMorgan, NVIDIA, TSMC, OpenAI, US Treasury, Kremlin, OPEC+. Graph now shows: actor-actor links, actor-institution links, actor-country links, country-country links, theme cross-links, comparison-actor links.

## 2026-04-09 | manual-edit | BlackRock ownership web — graph connections built
- Operation: manual-edit
- Files created: wiki/comparisons/BlackRock-Ownership-Web.md + 12 company institution stubs (Apple, Microsoft, Amazon, Alphabet, Meta, Tesla, ExxonMobil, Lockheed Martin, Samsung, ASML, Saudi Aramco, Goldman Sachs)
- Files updated: wiki/institutions/BLACKROCK.md — full ownership wikilinks added
- Contradictions: none
- DB sync needed: yes — BlackRock→Owns→NVIDIA/TSMC/ASML/ExxonMobil/Lockheed RelationEdge rows pending
- Notes: BlackRock now connects to 15 companies in graph view. Aladdin layer documented. Invisible Hand Tracker example trace built (Hormuz closure cascade). All holdings link bidirectionally back to BLACKROCK.md. Source a 13F filing for precise stake percentages.

## 2026-04-09 | lint | First health audit
- Operation: lint
- Files created: wiki/lint-reports/2026-04-09.md
- Files updated: wiki/index.md (full rebuild), wiki/themes/IMP-Automation-Engine.md, wiki/timelines/IMP-Phase-Roadmap.md, wiki/institutions/ECB.md, wiki/institutions/META.md, wiki/institutions/AMAZON.md, wiki/institutions/MICROSOFT.md
- Contradictions flagged: none
- DB sync needed: no
- Notes: 73 pages audited. 14 orphans found (8 fixed immediately). 21 thin pages (all institution stubs — acceptable). 11 actors with empty Current Assessment + Narrative Shift (root cause: no external sources ingested yet). 8 broken wikilinks fixed (naming convention mismatch). Index rebuilt with all 22 institution pages + new comparison pages. Missing: France, Germany, India, Iran country pages. Top priority next action: ingest first external source (Fed speech or ECB transcript) to populate empty actor sections.

## 2026-04-09 | manual-edit | IMP Raw Collection Prompts added
- Operation: manual-edit
- Files created: wiki/dossiers/IMP-Raw-Collection-Prompts.md
- Notes: 10-task prompt pack for collecting external sources into raw/. Tasks cover Fed/Powell, ECB/Lagarde, IMF WEO, BIS Quarterly, BlackRock 13F, TSMC earnings, chokepoint risk, China economy, Russia oil sanctions, Trump trade policy. Source URLs included. Compatible with Claude Code (direct file write) and Claude.ai (paste output for ingest).

## 2026-04-09 | ingest | 7 external sources (Perplexity batch)
- Operation: ingest
- Sources ingested:
  - raw/transcripts/powell-fomc-2026-04.md
  - raw/central-banks/lagarde-ecb-2026-04.md
  - raw/institutions/imf-weo-2026-04.md
  - raw/markets/blackrock-13f-2025-12-31.md
  - raw/geopolitics/chokepoint-risk-2026-04.md
  - raw/geopolitics/trump-trade-policy-2026-04.md
  - raw/sanctions/russia-oil-2026-04.md
- Created: wiki/sources/ (7 summaries), wiki/market-impact/Fed-Rate-Policy-Markets.md, wiki/market-impact/Trump-Trade-War-Markets.md, wiki/narratives/Global-Macro-Regime-2026-04.md
- Updated: POWELL-Jerome.md (Current Assessment + Narrative Shift), LAGARDE-Christine.md (same), TRUMP-Donald.md (same), RUSSIA.md (Narrative Trajectory), CHINA.md (Narrative Trajectory), Chokepoint-Intelligence.md (threat scores updated)
- Contradictions: Chokepoint DB scores diverge from wiki — DB has Hormuz=10/Taiwan=8, wiki April 2026 assessment has Bab el-Mandeb=8 as highest active risk
- DB sync needed: YES — CommodityChokepoint Bab el-Mandeb threat score needs update (Houthi campaign elevated it)
- Notes: FIRST EXTERNAL SOURCE INGESTS. Actor pages now have real Current Assessment and Narrative Shift content for Powell, Lagarde, Trump. BlackRock 13F partial — full verified data requires EDGAR XML download. All 7 raw files saved in correct raw/ subfolders.

## 2026-04-09 | manual-edit | Perplexity State Report v13 created
- Operation: manual-edit
- Files created: wiki/dossiers/Perplexity-State-Report-v13.md
- Notes: Full briefing for Perplexity on wiki v13 state. Includes: inventory of 96 pages, IdeologyProfile status per actor, active DB sync flags (CL-DB-003 to CL-DB-006), 5 priority collection tasks with ready-to-paste prompts, workflow summary, health metrics.

## 2026-04-09 | ingest | 6 Perplexity templates — 4 themes + 2 timelines
- Operation: ingest
- Source: Perplexity generated page templates
- Files created:
  - wiki/themes/Energy-Chokepoints-War.md
  - wiki/themes/AI-Supply-Chain-Export-Controls.md
  - wiki/themes/Geoeconomic-Fragmentation.md
  - wiki/themes/Monetary-Policy-Weaponized-World.md
  - wiki/timelines/Global-Energy-Shipping-2019-2026.md
  - wiki/timelines/AI-Tech-Decoupling-2019-2026.md
- Contradictions: none
- DB sync needed: CL-DB-003 (Bab el-Mandeb), CL-DB-005 (PowerMapRelation semiconductor edges) referenced in new pages
- Notes: Major structural upgrade — 4 new intelligence themes created that cross-link actors, countries, institutions, and signals. Two append-only timelines covering energy/shipping and AI/tech decoupling from 2019-2026. All pages fully wikilinked into graph. Wiki now has 11 theme pages (was 7).

## 2026-04-09 | manual-edit | Prompt Pack Operativo v2.0 creado
- Operation: manual-edit
- Files created: wiki/dossiers/IMP-Prompt-Pack-Operativo-v2.md
- Notes: Pack operativo completo alineado con CLAUDE.md v3.0. 5 prioridades con prompts listos para copiar/pegar en Perplexity. P1=IdeologyProfile 9 actores con DB column names correctos. P2=6 country pages con Power Profile fields (FinancialScore/MilitaryScore etc). P3=TSMC earnings + Jensen Huang narrative. P4=BIS Quarterly. P5=Weekly refresh (Powell/Lagarde/Chokepoints). Quick reference tables incluyen DB column names y verified IDs.

## 2026-04-09 | ingest | Mission Pack v1.0 — Tasks 1-5 executed
- Operation: ingest + manual-edit
- Files created:
  - raw/ideology/ideology-profiles-2026-04.md (9 actor scores)
  - raw/ideology/ideology-seed-sql-2026-04-09.sql (ready to run in pgAdmin)
  - wiki/countries/FRANCE.md (db_id: 30)
  - wiki/countries/GERMANY.md (db_id: 29)
  - wiki/countries/INDIA.md (db_id: 140)
  - wiki/countries/IRAN.md (db_id: 72)
  - wiki/countries/ISRAEL.md (db_id: 74)
  - wiki/countries/JAPAN.md (db_id: 149)
  - raw/internal-notes/IMP-mission-weekly-ops-2026-04-09.md
- Files updated: 9 actor pages (IdeologyProfile sections), wiki/index.md
- Contradictions: none
- DB sync needed: YES
  - CL-DB-006: Run ideology-seed-sql-2026-04-09.sql for 7 actors (Modi+Yellen pending PersonId confirmation)
  - CL-DB-007: Confirm 6 new country DB IDs in Countries table
- Notes: Task 1 (IdeologyProfiles) complete with knowledge-based scoring confidence 70-85%. Task 2 (6 country pages) complete with full CLAUDE.md v3.0 schema. Tasks 3-4 (TSMC/BIS) stubs created in Mission Pack — pending Perplexity source. Task 5 (Weekly Refresh) protocol documented with ready-to-paste prompts. Mission Pack v1.0 is the operating document for weekly intelligence operations.

## 2026-04-09 | db-sync | CL-DB-005 CLOSED — Semiconductor PowerMapRelation seeded
- Operation: db-sync
- DB changes confirmed:
  - PowerMapRelation row 1: ASML → Partners → TSMC (RE 55, Critical) ✅
  - PowerMapRelation row 2: NVIDIA → DependsOn → Taiwan (RE 91, Critical) ✅
  - PowerMapRelation row 3: Jensen → Governs → NVIDIA (RE 1, Critical) ✅
  - PowerMapRelation row 4: Morris Chang → Owns → TSMC (RE 38, High) ✅
  - PowerMapRelation row 5: TSMC → Partners → Apple (RE 53, Critical) ✅
- Files updated: wiki/themes/Chokepoint-Intelligence.md, wiki/themes/AI-Supply-Chain-Export-Controls.md
- DB sync flag: CL-DB-005 CLOSED
- Notes: Semiconductor PowerMap (ID=4) now has 5 live edges. PowerMapIntelligence view will render these in frontend. Samsung and Intel nodes not in PowerMap 4 — could be added as PowerMapNode inserts if needed for demo.

## 2026-04-09 | db-sync | CL-DB-006 PENDING — IdeologyProfile SQL ready to run
- Notes: SQL ready in raw/ideology/ideology-seed-sql-2026-04-09.sql. 7 actors with confirmed DB IDs: Xi(171), MBS(176), Fink(75), Bessent(545), Huang(1), Gates(67), Altman(61). Modi and Yellen not in Persons table — need person seed first.

## 2026-04-10 | db-sync | CL-DB-006 CLOSED — IdeologyProfile 12 actors confirmed live
- Operation: db-sync
- DB rows confirmed:
  Putin(172):   Econ=-2.0 Auth=10.0 Geo=9.0  Env=7.5  Label=Authoritarian nationalist imperialist  Conf=5
  Xi(171):      Econ=2.0  Auth=9.0  Geo=3.0  Env=-3.0 Label=CCP nationalist authoritarian          Conf=5
  MBS(176):     Econ=4.0  Auth=8.5  Geo=2.0  Env=6.0  Label=Modernising authoritarian              Conf=4
  Trump(173):   Econ=5.0  Auth=7.5  Geo=-4.0 Env=8.5  Label=Nationalist-populist authoritarian     Conf=5
  Musk(7):      Econ=7.5  Auth=4.0  Geo=6.0  Env=-2.0 Label=Techno-libertarian nationalist         Conf=5
  Bessent(545): Econ=6.0  Auth=1.0  Geo=-1.0 Env=4.0  Label=Fiscal hawk nationalist                Conf=4
  Powell(192):  Econ=4.0  Auth=0.0  Geo=1.0  Env=-1.0 Label=Technocratic institutionalist          Conf=4
  Fink(75):     Econ=3.0  Auth=-2.0 Geo=5.0  Env=-4.0 Label=Liberal financial multilateralist      Conf=4
  Altman(61):   Econ=4.0  Auth=-3.0 Geo=3.0  Env=-1.0 Label=AI accelerationist techno-optimist     Conf=4
  Lagarde(191): Econ=-2.0 Auth=-3.0 Geo=4.0  Env=-5.0 Label=Liberal multilateralist               Conf=4
  Huang(1):     Econ=5.0  Auth=-3.0 Geo=4.0  Env=-1.0 Label=Techno-optimist multilateralist        Conf=4
  Gates(67):    Econ=1.0  Auth=-4.0 Geo=7.0  Env=-6.0 Label=Techno-philanthropic multilateralist   Conf=5
- Constraint discovered: IdeologyProfile.Confidence CHECK 1-5 (not 0-100) — ipm-database SKILL updated
- DB sync flag: CL-DB-006 CLOSED
- Notes: AuthScore column shown in verify is GeoScore in schema (columns: Econ, Auth, Cultural, Gender, Geo, Env, Religion). Verify output matches expected values. Musk EconScore=7.5 = highest in dataset. Gates EnvScore=-6.0 = most interventionist. Putin AuthScore=10.0 = maximum.

## 2026-04-10 | db-sync | CL-DB-003 CLOSED — Bab el-Mandeb updated to 8
- Operation: db-sync
- Confirmed chokepoint scores:
  Hormuz=10, Bab el-Mandeb=8, Taiwan Strait=8, Black Sea=8, Suez=6, Malacca=5, Panama=3
- DB sync flag: CL-DB-003 CLOSED
- Notes: Bab el-Mandeb now matches wiki assessment (Houthi campaign elevated to 8). Taiwan Strait and Black Sea also at 8 — three chokepoints at critical tier simultaneously. Panama at 3 (drought-related capacity issues, not conflict).

## 2026-04-10 | ingest | Bitcoin integration — wiki + Thread Master config
- Operation: ingest + manual-edit
- Files created:
  - wiki/commodities/BITCOIN.md — supply structure, demand, chokepoints, market impact
  - wiki/themes/Bitcoin-Macro-Regime.md — 3 regimes (A=liquidity-on, B=liquidity-off, C=macro-hedge)
  - wiki/market-impact/Bitcoin-vs-Equities-Rates.md — direct/second-order channels, affected asset classes
  - raw/internal-notes/thread-master-bitcoin-integration.js — CONFIG additions, IMP_CONTEXT bridge, compatibilityRules
- Contradictions: none
- DB sync needed: yes — Bitcoin not yet in Commodities table (db_id pending)
- Notes: Current IMP regime = Regime B (liquidity-off, Fed hawkish). Bitcoin strategy BLOCKED in Thread Master until Powell pivot or DSI deterioration triggers Regime A or C. IMP_CONTEXT object provides weekly-updatable bridge between wiki and Thread Master config. BitcoinImpBadge component shows current bias in strategy selector UI.

## 2026-04-10 | ingest | Dollar System layer — Fed + Wall Street + Pentagon + 3 indicators
- Operation: ingest
- Files created:
  - wiki/institutions/WALL-STREET.md — financial ecosystem node, Fed relationship, Pentagon link
  - wiki/institutions/PENTAGON.md — US military projection, chokepoint control, defense industrial base
  - wiki/indicators/Fed-Liquidity-Pulse.md — balance sheet Δ + RRP + TGA + BTFP → Pulse Score -10 to +10
  - wiki/indicators/USD-Hegemony-Index.md — COFER + SWIFT + DXY + trade invoicing → 0-100 score
  - wiki/indicators/US-Military-Projection.md — budget + carriers + bases + nuclear → 0-100 score
  - wiki/themes/Dollar-System-Fed-Liquidity.md — connects all 3 indicators + 3 scenarios
- Contradictions: none
- DB sync needed: Wall Street + Pentagon need Company rows seeded
- Notes: Dollar power stack documented (Pentagon→Treasury→Fed→Wall Street→Global System). Current: Fed Liquidity Pulse ~-3 to -4 (mild contraction), USD Hegemony ~72/100 (gradual erosion), US Military ~78/100 (stressed but dominant). Bitcoin regime connections wired through Fed Liquidity Pulse. Three dollar scenarios: A=gradual erosion (baseline), B=crisis (tail), C=reinvigoration.

## 2026-04-10 | db-sync | Institutions seeded as Companies — 8 new rows confirmed
- Operation: db-sync
- DB rows confirmed:
  Federal Reserve=240, ECB=241, US Treasury=242, Pentagon=243
  Wall Street=244, IMF=245, BIS=246, NATO=247
- Files updated: FEDERAL-RESERVE.md, ECB.md, US-TREASURY.md, WALL-STREET.md, PENTAGON.md (db_ids added)
- Files created: IMF.md (db_id:245), BIS.md (db_id:246)
- SQL ready: raw/ideology/institutions-relationedge-seed.sql — 13 RelationEdge INSERTs
- Notes: NodeType='Company' used for all institutions (no schema change needed). Ticker=NULL, SystemicImportanceLevel=Critical/High. ipm-database SKILL updated with institution ID map. Skill now has: Federal Reserve=240, ECB=241, Treasury=242, Pentagon=243, Wall Street=244, IMF=245, BIS=246, NATO=247.

## 2026-04-10 | ingest | AI supply chain complete — AI companies, cloud, Palantir, commodities
- Operation: ingest
- Files created:
  - wiki/institutions/PALANTIR.md
  - wiki/institutions/AWS.md
  - wiki/institutions/AZURE.md
  - wiki/institutions/GOOGLE-CLOUD.md
  - wiki/institutions/ANTHROPIC.md (db_id: 197 confirmed)
  - raw/ideology/ai-supply-chain-complete-seed.sql (companies + commodities)
  - raw/ideology/ai-supply-chain-edges.sql (25 RelationEdge INSERTs — needs IDs from Step 0)
- Files updated: wiki/themes/AI-Supply-Chain-Export-Controls.md (complete 6-layer graph added)
- DB sync needed: YES
  1. Run ai-supply-chain-complete-seed.sql Step 1 to seed companies
  2. Run Step 0 verify to get actual IDs
  3. Replace [PLTR_ID],[AWS_ID],[AZURE_ID],[GCP_ID],[AMD_ID],[ARM_ID],[HYNIX_ID],[MICRON_ID],[XAI_ID] in ai-supply-chain-edges.sql
  4. Run edges SQL
  5. Seed commodities (Step 2)
- Notes: Complete AI supply chain now documented — 6 layers from rare earths to Palantir defense AI. Meta confirmed as largest single NVIDIA buyer (350K+ H100s). OpenAI exclusively on Azure. Anthropic exclusively on AWS. xAI Colossus = 100K+ H100s. Palantir connects AI supply chain to Pentagon/CIA/Ukraine.

## 2026-04-10 | db-sync | Commodity links seed — CompanyCommodities + CommodityFacility
- Operation: db-sync
- SQL ready: raw/ideology/commodity-links-seed.sql
- CompanyCommodities new rows (18 inserts):
  TSMC(41): Silicon Wafers(50) Critical, Photoresist EUV(54) Critical, Gallium(69) High, Germanium(68) High
  Samsung(43): Silicon Wafers(50) Critical, HBM(55) Critical, NAND(48) Critical, DRAM(49) Critical
  Intel(85): Silicon Wafers(50) Critical, Photoresist EUV(54) Critical, SiC Wafers(56) High
  OpenAI(198): GPU Compute(53) Critical 95%, HBM(55) High 75%
  Anthropic(197): GPU Compute(53) Critical 90%, HBM(55) High 70%
  BlackRock(90): Brent(1) High, Gold(12) High, GPU Compute(53) High
- CommodityFacility new rows (8 inserts):
  TSMC Fab18(41)→Advanced Logic(51) Produces Critical Risk=9
  TSMC Hsinchu(407)→Silicon Wafers(50) Input Critical Risk=8
  TSMC Arizona(454)→Advanced Logic(51) Produces High Risk=4
  ASML Veldhoven(21)→Photoresist EUV(54) Input Critical Risk=7
  Samsung Pyeongtaek(43)→HBM(55) Produces Critical Risk=6
  Samsung Pyeongtaek(43)→NAND(48) Produces High Risk=5
  Intel Fab42 AZ(175)→Mature Chips(52) Produces High Risk=3
  Intel Fab34 Ireland(447)→Advanced Logic(51) Produces Medium Risk=3
- ipm-database SKILL updated with full commodity ID map (117 commodities categorized)

## 2026-04-10 | ingest | 5 scenarios created — one per domain
- Operation: ingest
- Files created:
  - wiki/scenarios/Taiwan-Strait-2026-2028.md (Semiconductor domain)
  - wiki/scenarios/Hormuz-Iran-Crisis-2026.md (Energy/Chokepoint domain)
  - wiki/scenarios/Fed-Pivot-2026.md (Monetary/Macro domain)
  - wiki/scenarios/Dollar-System-Stress-2026-2028.md (Dollar/DSI domain)
  - wiki/scenarios/AI-Race-Breakpoint-2026-2028.md (AI/Tech domain)
- Each scenario: 3 branches (A/B/C), probability estimates, market cascades, IMP DB updates triggered, cross-branch markers, Oracle relevance
- DB sync: Taiwan Branch A triggers ScenarioCascade Oil $150 template. AGI Branch A needs new ScenarioCascade template.
- Notes: Taiwan scenario directly relevant for Oliver demo (Apr 21) — SupplyRiskScore=9 on TSMC Fab 18 now has narrative context. Fed Pivot scenario wired to Thread Master Bitcoin IMP_CONTEXT. Dollar scenario documents Trump paradox (short-term USD strength vs long-term erosion).

## 2026-04-10 | db-sync | 4 SQLs completados — AI supply chain + commodities LIVE
- Operation: db-sync
- Final counts confirmed:
  RelationEdge: 1,271 (+25 new AI supply chain edges)
  CompanyCommodities: 315 (+18 new links)
  CommodityFacility: 22 (+8 fab→commodity links)
  Commodities: 121 (+4: Rare Earths/Uranium/Phosphates/Bitcoin)
- New companies seeded: Palantir(96), AMD(69), Arm Holdings(248), Mistral AI, Cohere, xAI(199)
- Key edges live: NVIDIA→SK Hynix, NVIDIA→Micron, AMD→TSMC, Arm→NVIDIA, 
  Meta→NVIDIA, OpenAI→Microsoft, Microsoft→OpenAI, Anthropic→Amazon, 
  Amazon→Anthropic, Musk→xAI, xAI→NVIDIA, Altman→OpenAI,
  Palantir→Pentagon, Palantir→Ukraine, Palantir→USA, Palantir→NVIDIA
- DB sync flags: CL-DB-008 ✅, CL-DB-009 ✅, CL-DB-010 ✅
- Skill updated: Rule 13 (setval before nextval in batch), Rule 14 (CommodityFacility UsageType enum), Rule 15 (pg_get_serial_sequence pattern)
- Still pending: CL-DB-011 (institution RelationEdges — institutions-relationedge-seed.sql)

## 2026-04-10 | db-sync | CL-DB-011 CLOSED — Institution RelationEdges confirmed live
- Operation: db-sync
- 13 edges confirmed (RE 1272-1284):
  Powell(192)→Sets→Federal Reserve(240) Critical
  Lagarde(191)→Sets→ECB(241) Critical
  Bessent(545)→Governs→US Treasury(242) Critical
  Trump(173)→Governs→Pentagon(243) Critical
  Federal Reserve(240)→Sets→USA(1) Critical
  Federal Reserve(240)→Influences→Wall Street(244) Critical
  US Treasury(242)→Sanctions→Russia(64) Critical
  US Treasury(242)→Sanctions→Iran(72) Critical
  Pentagon(243)→Governs→USA(1) Critical
  Pentagon(243)→Finances→Lockheed Martin(68) Critical
  Fink(75)→Influences→Wall Street(244) High
  ECB(241)→Sets→Germany(29) Critical
  IMF(245)→Partners→Federal Reserve(240) High
- DB sync flag: CL-DB-011 CLOSED
- Final RelationEdge count: 1,284

## 2026-04-10 | db-sync | CL-DB-004 + CL-DB-007 CLOSED
- CL-DB-007: Country IDs confirmed — France=30, Germany=29, India=140, Iran=72, Israel=74, Japan=149
- CL-DB-004: BlackRock Owns edges seeded (RE 1285-1294):
  NVIDIA(1), TSMC(41), ASML(21), ExxonMobil(14), Lockheed(68)
  Microsoft(4), Apple(2), Alphabet(3), Amazon(5), Saudi Aramco(42)
  All Strength=High except Aramco=Medium
- Final RelationEdge count: 1,294
- ALL DB SYNC FLAGS CLOSED ✅

## 2026-04-17 | dossier-ingest | 6 actor pages enriched from external dossiers
- sources:
  - raw/dossiers-external/musk-elon-dossier-2026-04.html
  - raw/dossiers-external/trump-donald-power-profile-2026-04.html
  - raw/dossiers-external/fink-larry-dossier-2026-04.html
  - raw/dossiers-external/huang-jensen-dossier-2026-04.html
  - raw/dossiers-external/gates-bill-dossier-2026-04.html
  - raw/dossiers-external/zuckerberg-mark-dossier-2026-04.html
- created (raw/): 6 HTML dossiers copied to raw/dossiers-external/ for source traceability
- updated (wiki/actors/):
  - MUSK-Elon.md — added Wealth Composition, Companies & Valuations, Global Facilities, Commodities, Strategic Alliances, Ideology & Worldview, Risk Profile, enriched Current Assessment, Narrative Shift, Key Recent Actions, Market Impact
  - TRUMP-Donald.md — added Wealth Composition, Key Properties, Crypto Empire, Wall Street Influence, Winners/Losers, Media Allies/Enemies, AI Vision, Strategic Alliances, US SWF, Dollar as Weapon, Risk Profile, enriched Current Assessment with April 2026 synthesis
  - FINK-Larry.md — added BlackRock Empire Scope, Aladdin systemic infrastructure detail, Fourth Branch argument, Historical Milestones, Strategic Alliances, Revolving Door, Ideology, Risk Profile, Current Assessment April 2026 synthesis, Key Recent Actions, enriched Market Impact channels
  - HUANG-Jensen.md — added Financial Trajectory table, CUDA Moat detail, Product Stack, China Problem geopolitical exposure, Clients/Partners, Competitors, Physical AI, Ideology, Risk Profile, Current Assessment April 2026 synthesis
  - GATES-Bill.md — added Wealth Composition, Microsoft History, BMGF Global Health, Food/Farmland, COVID Role, Epstein Files, Philanthropy, AI Vision, Political Power, Myths vs Facts, Risk Profile, Current Assessment April 2026 synthesis
  - ZUCKERBERG-Mark.md — added Meta Empire scale, AI Open Source Bet, Political Pivot Jan 2025, Antitrust battles, CZI Philanthropy, Personal Transformation, Properties, Ideology, Risk Profile, Current Assessment April 2026 synthesis
- contradictions: none material — dossier content supplements stub sections marked "populate from ingests"
- db-sync: YES — multiple DB SYNC NEEDED flags raised across all 6 pages
  - Wealth figures (EstimatedWealthUsd) for all 6 actors need verification against Persons table
  - New Company node candidates: xAI (under SpaceX), Trump Media (DJT), World Liberty Financial, iShares, Starlink, CZI, Cascade Investment subsidiaries
  - New RelationEdge candidates: US-China NVIDIA/AMD 15% revenue deal, Fink→Advises→Ukraine reconstruction, Fink→Manages→US-Infrastructure-Fund, Zuckerberg→Influences→Trump
  - Chokepoint status review: Starlink (Musk), Aladdin (Fink — flag already open), CUDA (Huang, new candidate)
  - Sovereign AI partnerships (Huang dossier): UAE, Saudi, Japan, India, France, Singapore as new NVIDIA→Supplies edges
- notes:
  - Existing IdeologyProfile tables preserved on TRUMP, FINK, HUANG, GATES — not overwritten
  - Existing DB sync notes preserved; new flags appended rather than replacing
  - Related Pages links de-duplicated across sources
  - All 6 dossiers are external HTML retained in raw/dossiers-external/ for audit trail
  - 6 source-summary pages NOT created under wiki/sources/ — dossiers are cited in each actor's Sources section directly; consider adding formal summary pages in follow-up if dossiers become canonical references

## 2026-04-20 | dossier | GPT Context Report generated
- Operation: dossier creation
- Files created: wiki/dossiers/GPT-Context-Report-2026-04-20.md
- Purpose: self-contained briefing doc for ChatGPT/GPT sessions — parallel to Perplexity-State-Report-v13
- Contents: mission, structure, IMP glossary (archetypes, edges, chokepoints), full inventory with DB IDs, open DB sync flags, recent activity, prioritized work list, frontmatter rules, what-not-to-do
- Contradictions flagged: none
- DB sync needed: no
- Notes: Stand-alone doc. Paste into ChatGPT or upload as file. Does not duplicate raw wiki pages — summarizes and indexes.

## 2026-04-21 | lint | Monthly health audit — 130 pages
- Operation: lint
- Files created: wiki/lint-reports/2026-04-21.md
- Files updated: wiki/index.md (v24 — companies/ section added, header updated to 130 pages, new lint entry)
- Findings (10 total):
  - LINT-01 [HIGH]: 12 pages on old v1 schema (missing slug, using `related:` instead of `related_*` arrays) — 6 IMP themes, IMP-Phase-Roadmap, Oracle-Machine-Roster, 2 sources, 2 indicators
  - LINT-02 [HIGH]: companies/ folder (11 pages, added 2026-04-19) absent from wiki/index.md — now fixed
  - LINT-03 [MEDIUM]: wiki/index.md header stale — now fixed (v24, 130 pages)
  - LINT-04 [MEDIUM]: 7 high-churn intel pages last updated 2026-04-09 (Powell, Lagarde, Bessent, China, Ukraine, Iran, Global-Macro-Regime narrative)
  - LINT-05 [MEDIUM]: 3 dossiers without any frontmatter (IMP-Raw-Collection-Prompts, Perplexity-State-Report-v13, IMP-Prompt-Pack-Operativo-v2)
  - LINT-06 [MEDIUM]: PALANTIR.md has db_id: TBD — confirmed 96 in DB
  - LINT-07 [LOW]: Lockheed↔Northrop edge strength drift (Competes/Partners swap) — open from 2026-04-20 dry-run
  - LINT-08 [LOW]: 42 pages with sources: [] — chronic stub gap, no new external ingests since 2026-04-09
  - LINT-09 [NULL]: depends_on field does not exist in this schema — no broken slugs of that type
  - LINT-10 [LOW]: No individual oracle context pages — only Oracle-Machine-Roster exists
- Contradictions flagged: none
- DB sync needed: YES
  - CL-DB-012: PALANTIR db_id: TBD → 96 confirmed in DB
  - CL-DB-013: Lockheed↔Northrop edge strength mismatch (Competes=High→Medium, Partners=Medium→High)
- Top 5 next ingests: (1) Powell/Fed April 2026, (2) Lagarde/ECB April 2026, (3) TSMC Q1 2026 earnings, (4) BIS Quarterly Q1 2026, (5) China MOFCOM tariff retaliation
- Notes: 57 new pages since last lint (2026-04-09). Primary schema debt is the 12 old-v1-schema pages — these predate CLAUDE.md v3.0 upgrade and need frontmatter migration. companies/ section is now indexed. GPT-Context-Report dossier is untracked in git.

## 2026-04-21 | wiki-expansion | TAIWAN, narratives, 5 actors, pending-db-sync, CLAUDE.md
- Operation: content-enrichment + new-control-file + schema-update
- Files created:
  - wiki/pending-db-sync.md — single source of truth for all open DB flags (CL-DB-012 to CL-DB-015). Closed flags preserved as audit trail. SQL patterns included.
- Files updated (CLAUDE.md):
  - Added `wiki/pending-db-sync.md` as a named control file in Section 6 with full usage rules (raise/close protocol, sequential numbering, never-delete-closed-entries)
- Files updated (actors):
  - wiki/actors/POWELL-Jerome.md — removed duplicate Narrative Shift section, expanded with tariff-era posture, Key Recent Actions populated (knowledge-based)
  - wiki/actors/LAGARDE-Christine.md — removed duplicate Narrative Shift, added tariff shock fork analysis, April 2026 pivot signal, Key Recent Actions
  - wiki/actors/XI-Jinping.md — Current Assessment + Narrative Shift + Key Recent Actions populated (rare earth controls, PBOC RRR, Taiwan exercises)
  - wiki/actors/MACRON-Emmanuel.md — full Current Assessment + Role and Levers + Narrative Shift + Key Recent Actions + Market Impact + Oracle Relevance + DB Sync Notes
  - wiki/actors/DIMON-Jamie.md — Current Assessment (US debt thesis, tariff-driven hard landing risk) + Narrative Shift + Key Recent Actions
- Files updated (countries):
  - wiki/countries/TAIWAN.md — full expansion: Strategic Summary, Power Profile (silicon shield, Jade Mountain, Lai Ching-te), Domestic Pressures, External Alignments, Sanctions, Narrative Trajectory, Market Relevance (TAIEX/TWD/semiconductor shock/defense premium), IMP-Specific Significance
- Files updated (narratives):
  - wiki/narratives/Global-Macro-Regime-2026-04.md — Added tariff shock transmission section, updated Recent Shifts for April 2026 escalation (Liberation Day tariffs, rare earths, stagflation risk formalized)
- Contradictions flagged: none
- DB sync needed: YES
  - CL-DB-015: BESSENT EstimatedWealthUsd — Key Square AUM not verified in Persons table (db_id=545)
  - CL-DB-012/013/014: carried forward (see wiki/pending-db-sync.md)
- Notes: wiki/pending-db-sync.md is now the canonical DB sync tracking file. CLAUDE.md updated to mandate its use. All future DB flags should be logged there first. Page count: 136.

## 2026-04-21 | recommendations-pass | lint + Smart Connections audit implemented
- Operation: schema-fix + content-enrichment + new-pages
- Files updated (schema — old v1 → v3.0):
  - wiki/themes/IMP-Platform-Architecture.md — slug, region, tags, related_* arrays
  - wiki/themes/IMP-Automation-Engine.md — same
  - wiki/themes/IMP-Competitive-Moats.md — same
  - wiki/themes/IMP-Oracle-System.md — same
  - wiki/themes/IMP-Power-Index-System.md — same
  - wiki/themes/IMP-Business-Model.md — same
  - wiki/timelines/IMP-Phase-Roadmap.md — same
  - wiki/oracle/Oracle-Machine-Roster.md — slug + oracle-specific fields (machine_domain, brier_trend) + related_*
  - wiki/sources/IMP-Strategy-v2-2.md — slug, source-path, related_*
  - wiki/sources/IPM-SQL-Seed-Reference.md — slug, source-path, related_*
  - wiki/indicators/DB-ID-Reference.md — slug, domain, scope, related_*
  - wiki/indicators/Enum-Types-Reference.md — slug, domain, scope, related_*
- Files updated (content):
  - wiki/institutions/PALANTIR.md — db_id: TBD → 96 (confirmed from log 2026-04-10)
  - wiki/actors/BESSENT-Scott.md — Current Assessment, Narrative Shift, Key Recent Actions populated (knowledge-based, confidence: medium)
  - wiki/countries/CHINA.md — Market Relevance expanded (FX/CNY/PBOC/equities/commodities/rates/Taiwan premium)
  - wiki/countries/RUSSIA.md — Market Relevance expanded (oil/shadow fleet/grain/ruble/frozen assets/infrastructure)
  - wiki/countries/SAUDI-ARABIA.md — Market Relevance expanded (Aramco/petrodollar/SAR peg/Vision 2030 bonds/Abqaiq risk)
  - wiki/countries/UKRAINE.md — Market Relevance expanded (grain/defense multiplier/eurobonds/frozen assets/Palantir)
  - wiki/countries/ISRAEL.md — Market Relevance expanded (ILS/TASE/defense tech/Suez/Iran premium/reconstruction)
- Files updated (frontmatter added):
  - wiki/dossiers/IMP-Raw-Collection-Prompts.md — full YAML frontmatter added
  - wiki/dossiers/Perplexity-State-Report-v13.md — full YAML frontmatter added
  - wiki/dossiers/IMP-Prompt-Pack-Operativo-v2.md — full YAML frontmatter added
- Files created (new oracle context pages):
  - wiki/oracle/MEI-LIN-ZHANG.md — China/trade war/tech decoupling/CNY domain, full context block
  - wiki/oracle/CHEN-WEI.md — Asia Pacific/semiconductors/Taiwan/PLA domain, full context block
- Files updated (index/control):
  - wiki/index.md — v25, 135 pages, oracle section updated (3 pages), lint entry updated
- Contradictions flagged: none
- DB sync needed: YES
  - CL-DB-012: PALANTIR.md db_id fixed wiki-side (96) — verify Palantir Company row exists in DB
  - CL-DB-013: Lockheed↔Northrop edge strength mismatch — still open from 2026-04-19 dry-run
  - CL-DB-014: CHINA Market Relevance now references PBOC→Influences→CNY edge and CIPS node — neither seeded in DB
- Notes: All 10 lint findings from 2026-04-21 report addressed except LINT-07 (Lockheed↔Northrop = DB-side fix, not wiki) and LINT-04 (requires external source ingests). Schema debt from 12 old-v1 pages fully cleared. 3 oracle machines now have individual context pages (Roster + Mei Lin Zhang + Chen Wei). BESSENT assessment is knowledge-based pending source ingest — flag for Perplexity collection.

## 2026-04-20 | state-snapshot | no edits today
- Operation: state-snapshot
- Files created: —
- Files updated: —
- Page count: 118 core wiki pages + 11 companies pages (129 total)
- Last material edit: 2026-04-19 (companies/ pipeline + generator scripts, not yet logged as its own entry)
- Last logged operation: 2026-04-17 (6-actor dossier enrichment)
- Sync status (wiki/companies/_sync_report.json, 2026-04-19 dry-run):
  - 9 company pages scanned, 0 missing edges, 0 missing news
  - 1 DRIFT: Lockheed Martin (068) — edge_strength vs Northrop Grumman: Competes wiki=High/db=Medium, Partners wiki=Medium/db=High
- Contradictions flagged: none
- DB sync needed: no new flags today; Lockheed↔Northrop strength drift still open from 2026-04-19 report
- Notes: Snapshot entry only — no ingest, edit, or lint performed. wiki/index.md still shows "Last updated: 2026-04-17" and does not yet reference the companies/ section added 2026-04-19.
