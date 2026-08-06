# Análisis — alcance declarado del corpus e identidad de documento en el tooling

**Fecha:** 2026-08-06 · **Naturaleza:** análisis + medición · **Toca DB:** no (todo read-only)

> **Por qué este fichero está en el repo.** El análisis se produjo en una sesión de agente y vivía
> sólo en el directorio de planes, fuera de git. Es exactamente el fallo que este mismo documento
> cataloga —información correcta viviendo fuera del control de versiones— así que se trae dentro.
> Las mediciones que lo sostienen son reproducibles con `ops/verificar_alcance_corpus.py`; su
> salida es `ops/VERIFICACION_ALCANCE_CORPUS.md`.

## Qué se preguntó

La arista `vault-wiki` del mapa de arquitectura (`iPM_GV/IPM_Infra/arquitectura_w4_componentes.json`)
declara `ipm_vault → wiki · Predictions → corpus embebido · DECLARADA, NUNCA INGERIDA`, con
`target=stopped`, `state=verified-absent`, `verifiedAt=2026-07-28`. Por la regla del mapa, un
`current` verificado hace más de una semana es hipótesis hasta reejecutar su `verifiedBy`.

## Respuesta corta

**La tarjeta es cierta, y es el hallazgo menor.** Lo grande es que el tooling identifica documentos
por nombre de fichero, la wiki tiene una convención que fabrica nombres repetidos, y eso alcanza a
cuatro de las 27 etiquetas ya firmadas del gold set.

---

## 1 · Lo que la tarjeta afirmaba — CONFIRMADO

| Afirmación | Veredicto | Evidencia |
|---|---|---|
| El gold set declara 209 md | CIERTO | `WAVE4_WIKI_GOLDSET_RATIFICACION_2026-07-24.md:15` |
| Cero documentos del vault en el índice | CIERTO | medido: `Path ILIKE '%prediction%'` → 0 filas |
| La raíz de todos los `Path` es `wiki` | CIERTO | medido: `DISTINCT split_part("Path",'/',1)` → `['wiki']` |
| El bench corre sobre 164 mientras el alcance habla de 209 | CIERTO | `ADR-W4-04.md:14,54,55` |

El cero del vault es **cierto por construcción**, no por accidente: `ipm_wiki_ingest.py:103,115`
tiene un solo argumento `--wiki-dir` (default `wiki`) y hace `rglob` sobre él. `Predictions` no
tiene por dónde entrar aunque alguien quisiera.

Disco: `wiki/` = 164 `.md` · `raw/` = 15 · `iPM_GV/iPM_VAULT/Predictions` = 21.
Índice: 164 documentos / 1313 chunks, última ingesta 2026-08-05 20:09:12.

## 2 · Lo que la tarjeta no decía

**(a) El sumando «Predictions (30)» también es falso.** Son **21** ficheros, y dos ni son
predicciones (`_template.md`, `PREDICTION_LOG_SETUP.md`). El 209 nunca cuadró.

**(b) El hueco es mayor que Predictions.** `ADR-W4-04.md:150-151` dice *"los `raw/` sí están,
reubicados bajo `wiki/incoming/`"*. Son **4 de 15**, y sólo 2 son copias exactas. Los **11 restantes
no están en el índice** — entre ellos los primarios de S4 y D3 del gold set. Ausente del alcance
declarado: **21 + 11 = 32 documentos**, no 30.

## 3 · Censo de colisiones de basename

El bench identifica documentos por **basename en minúsculas**. Sobre el corpus declarado
(`wiki/` + `raw/` = 179 ficheros, 160 basenames únicos): **19 grupos colisionan, 9 dentro del
índice**. Son **dos poblaciones distintas: una se cierra, la otra crece.**

### 3.1 · Población A — 8 pares de `wiki/incoming/` · DEUDA

`musk-elon`, `palantir`, `palantir-political-network`, `pending-db-sync`, `tech-power-nexus`,
`thiel-peter`, `trump-donald`, `vance-jd` (más `launch-plan-april-21`, que es `dossiers/`↔`sources/`).
Existen porque una cola de staging del 2026-04-22 nunca se mergeó, y **los ocho difieren en
contenido** de su página canónica. Se cierran de golpe el día que se decida qué hacer con
`incoming/` — la misma decisión que bloquea los 5 ambiguos del resolver y el `WikiSlug=NULL` de
palantir.

### 3.2 · Población B — 6 pares de `wiki/sources/` · GENERADOR

Los produce **`CLAUDE.md §4.11` por diseño**: la página de resumen lleva
`source-path: raw/folder/filename.md` y se nombra igual que su fuente.

| resumen | fuente cruda |
|---|---|
| `wiki/sources/BlackRock-13F-2025-12-31.md` | `raw/markets/blackrock-13f-2025-12-31.md` |
| `wiki/sources/Chokepoint-Risk-2026-04.md` | `raw/geopolitics/chokepoint-risk-2026-04.md` |
| `wiki/sources/IMF-WEO-2026-04.md` | `raw/institutions/imf-weo-2026-04.md` |
| `wiki/sources/Lagarde-ECB-2026-04.md` | `raw/central-banks/lagarde-ecb-2026-04.md` |
| `wiki/sources/Powell-FOMC-2026-04.md` | `raw/transcripts/powell-fomc-2026-04.md` |
| `wiki/sources/Trump-Trade-Policy-2026-04.md` | `raw/geopolitics/trump-trade-policy-2026-04.md` |

6 de las 13 páginas de `wiki/sources/`. **No se cierran con una decisión editorial: crecen solos.
Cada `raw/` que se resuma añade uno.** El instrumento se degrada a medida que la wiki hace bien su
trabajo.

> **El ítem a registrar no es «19 colisiones». Es: la convención de nombrado de `wiki/sources/` y el
> comparador del bench son incompatibles, y sólo uno de los dos puede quedarse como está.**

## 4 · Consecuencia sobre el gold set — 4 etiquetas comprometidas

| Etiqueta | Target declarado | Qué casa realmente |
|---|---|---|
| **E9** primario | `raw/internal-notes/palantir-manifesto-2025.md` | `wiki/incoming/…` — mismo contenido (colisión benigna) |
| **E9** related | `raw/internal-notes/palantir-wars-ice-programs.md` | `wiki/incoming/…` — **CONTENIDO DISTINTO** (4.908 B vs 8.761 B) |
| **E9** related | `raw/internal-notes/karp-alex-research-2026-04-22.md` | **AUSENTE del índice** |
| **S4** primario | `raw/sanctions/russia-oil-2026-04.md` | **AUSENTE del índice** |
| **D2** primario | `raw/internal-notes/musk-afd-research-2025.md` | `wiki/incoming/…` — **CONTENIDO DISTINTO** |
| **D3** primario | `raw/central-banks/lagarde-ecb-2026-04.md` | `wiki/sources/Lagarde-ECB-2026-04.md` — **el resumen, otro documento** |

Verificado por `Path` exacto, no por inferencia de código: el resumen de D3 **está** indexado y su
fuente cruda **no**.

**Son dos clases de fallo, no una:**

- **Fallo del COMPARADOR** (D3, D2, related de E9): la etiqueta casa con el documento equivocado.
- **Fallo de la ESPECIFICACIÓN** (S4, related `karp-alex-…` de E9): el target no está en el índice.
  La validez de S4 depende de la **pregunta 2 del gold set (multi-doc), SIN FIRMAR**: con
  *single-doc* pasa a fallo y la línea base cambia. **Una etiqueta cuya validez depende de una
  decisión no tomada no está firmada, aunque tenga OK en su fila.**

### 4.1 · El 1,00 en inglés queda SIN DETERMINAR

`ADR-W4-04.md:144-146` justifica que el inglés no llega a 1,00 sin contar `related` *"porque E9
apunta a un doc que sólo es alcanzable por su related"*. De los tres related de E9: **uno limpio**
(`wiki/companies/096_palantir.md`), **uno que casa con otro documento**, **uno ausente**. Cuál
produjo el acierto no es determinable sin reejecutar.

> El 1,00 de inglés de la pata densa —el número que decidió autorizar la descarga del modelo—
> descansa en parte sobre una etiqueta cuyo mecanismo de acierto no se conoce. **No está refutado.
> Está SIN DETERMINAR, que es distinto de estar mal y peor que estar bien.**

## 5 · El patrón está en cinco sitios, no en uno

Barrido con **control positivo** (si no encuentra una línea que sabemos que existe, aborta — un cero
sin calibrar no prueba nada):

| Fichero | Línea | Peso |
|---|---|---|
| `iPM-WIKI/ipm_wiki_bench.py` | 79 | **P1** — rompe la línea base |
| `iPM-WIKI/ipm_wiki_bench_hibrido.py` | 85 | **P1** — el bench que cierra ADR-W4-04 |
| `IPM_Backend_AI/tools/ipm_wiki_bench.py` | 136 | **P1** — **el que corrió el ADR** |
| `iPM-WIKI/ipm_wiki_to_graph.py` | 190 | nota al pie — ver §5.2 |
| `iPM-WIKI/ipm_wiki_lint_referencias.py` | 101-126 | **el modelo a copiar** — ya avisa |

**`ipm_wiki_ingest.py` y `ipm_wiki_puentes.py` NO tienen el patrón**: usan ruta completa. La
identidad en la base está sana; la que se rompe es la del tooling que la consulta. **Eso descarta
una migración de datos.**

### 5.1 · El linter y el bench tratan la misma ambigüedad al revés

`ipm_wiki_lint_referencias.py:124-125` devuelve `AMBIGUOUS` cuando hay más de un candidato: **la
expone**. El bench toma el primero que aparece y lo cuenta como acierto: **la traga**. Y el que se la
traga es el que produce los números que decidieron autorizar la descarga del modelo.

**Eso da la forma del fix sin necesidad de diseñarlo:** el resolver del linter ya sabe hacer lo
correcto. No hay que inventar una regla de identidad — hay que hacer que el bench use la que ya
existe y **falle ruidosamente en vez de elegir el primero**.

> **Un empate silencioso resuelto por orden de iteración es indistinguible de un acierto.**

### 5.2 · `ipm_wiki_to_graph.py` — trampa cargada, no disparo

Lo que lo saca de P1 **no** es que apunte a `IPMDB:5432` ni que su `glob` no sea recursivo: eso son
propiedades de hoy que cambian con un argumento. Es que **nadie lo usa como fuente de identidad** —
`wiki/log.md:59` ya registra que los dos scripts de pipeline son ciegos a las páginas hechas a mano,
que llegan a la DB por SQL manual.

> **Condición de activación:** se arma **el día que alguien apunte `--wiki-dir` a `wiki/incoming/`**,
> exactamente donde están las 8 colisiones con contenido divergente. Dos documentos colapsarían en un
> nodo del grafo exportado.

Un riesgo sin su disparador nombrado es un riesgo que nadie va a reconocer cuando ocurra.

### 5.3 · Hay DOS `ipm_wiki_bench.py`, y son dos programas distintos

| Fichero | Líneas | Flags |
|---|---|---|
| `iPM-WIKI/ipm_wiki_bench.py` | 168 | `--dsn --goldset --k` |
| `IPM_Backend_AI/tools/ipm_wiki_bench.py` | 310 | `--pata --comparar --modelo --barrer-k --k-chunks --top-docs …` |

**El de 168 líneas NO PUEDE producir la tabla del ADR** — no tiene pata densa. **Certeza, no
inferencia: los números salieron del de `tools/`.** El de este repo es un ancestro léxico que nunca
se retiró.

Consecuencia: nadie puede saber hoy si el de 168 reproduce el 0,85, y `ADR-W4-04.md:192-193` exige
reproducir la línea base antes de citar nada. Ahora **hay dos cosas que pueden diferir a la vez: el
corpus (1312→1313 chunks) y el programa.**

### 5.4 · La línea base sólo es reproducible en Windows

Los dos benches no usan la misma función: `os.path.basename("a\\b.md")` **en POSIX devuelve la
cadena entera**; el `.replace("\\","/").split("/")[-1]` del otro normaliza. **En Windows coinciden.
La equivalencia es del entorno, no del código.**

> *"La reproducibilidad de la línea base depende del sistema operativo. Los dos benches usan
> mecanismos distintos de extracción de basename que sólo coinciden en Windows. Cualquier
> reejecución en Linux o en CI produciría un conjunto de identidades distinto sin que nada lo
> señale."*

Para un número que decidió autorizar la descarga de un modelo, es una dependencia oculta del entorno
que no está declarada ni en el ADR, ni en `LINEA_BASE_LEXICA_2026-07-26.md`, ni en los docstrings.

---

## 6 · Decisiones SIN FIRMAR que bloquean lo demás

### 6.1 · ¿Cuál de los dos `ipm_wiki_bench.py` es el bench?

| Opción | Qué hace | Coste |
|---|---|---|
| **A · retirar** el de `iPM-WIKI` | mata la ambigüedad de raíz | rompe `LINEA_BASE_LEXICA_2026-07-26.md:91`, que lo cita |
| **B · renombrar** el de `tools/` | deja el nombre corto al ancestro | toca el fichero del que salieron los números firmados |
| **C · renombrar el de ESTE repo** a `ipm_wiki_bench_lexico.py` | conserva el ancestro, mata la ambigüedad, **no toca nada firmado** | actualizar la referencia de `LINEA_BASE_LEXICA:91` |

**Recomendada: C.** **Firma:** ____

### 6.2 · ¿Qué se hace con `wiki/incoming/` y sus 8 colisiones?

Sus 14 ficheros **están dentro del corpus indexado**. Los 8 que colisionan difieren en contenido de
su página canónica. Bloquea también los 5 ambiguos del resolver y el `WikiSlug=NULL` de palantir.
Quien la cierre debe aplicar la misma Opción C del corte del 2026-08-05 (ver `wiki/log.md`).
**Firma:** ____

### 6.3 · ¿`core_slug:` va al frontmatter de los 65?

Pendiente desde el efecto colateral de la reingesta del 2026-08-05. **Firma:** ____

---

## 7 · Trabajo especificado y NO ejecutado

Todo lo siguiente toca documentos firmados y quedó deliberadamente sin empezar:

1. **Corregir el alcance en el gold set** — revisión fechada bajo "Alcance del corpus", dejando el
   209 visible (el registro se extiende, no se reescribe). Predictions = 21, `target=stopped`, no se
   ingiere. Los 11 `raw/` ausentes, nombrados. **Las 27 etiquetas no se tocan** — lo que cambia no
   son las etiquetas, es lo que el instrumento hace con cuatro de ellas.
2. **Ajustar `ADR-W4-04.md`** — §5:150-151 *"los raw sí están"* → 4 de 15; 8 pares → 9 dentro del
   índice / 19 en el corpus. Seis entradas nuevas en §6: la regla de identidad, las dos poblaciones,
   fallo del comparador, fallo de la especificación, el 1,00 SIN DETERMINAR, y la dependencia del
   sistema operativo.
3. **Tres flags en `wiki/pending-db-sync.md`** — los 11 `raw/` ausentes; las 8 colisiones de
   `incoming/`; el generador de `wiki/sources/`. Separados: tienen dueños y ciclos de vida distintos.
4. **Corregir la arista `vault-wiki`** del mapa (30→21, hueco = Predictions + 11 raw, "los raw sí
   están"→4 de 15, censo de colisiones) **y el nodo `mcp_ro`**: hoy dice que su consumidor *"está
   fuera del sistema dibujado"*, pero `mcp-ipm-postgres-ro` **no está configurado en ningún cliente**
   — `AccessLog=0` no es "lo llama alguien de fuera del diagrama", es "nadie puede llamarlo".
5. **Recalcular la línea base** marcando las 4 comprometidas y reportando dos cifras: con las 27 y
   con las 23 limpias. Reproducir el 0,85 tal cual no probaría que la línea base es buena — probaría
   que el mismo instrumento da el mismo número.
6. **El fix de identidad**: comparar por `Path` relativo en vez de basename toca **cinco sitios en
   dos repos**, no una línea.

---

## 8 · Nota de método

Antes de medir, este análisis estimó *"25 consultas limpias, 2 comprometidas"*. Medido: **23 limpias
y 4 comprometidas**. La estimación se ajustó hacia abajo al contacto con los datos, que es lo que se
le pide a una estimación — y la razón por la que el censo de colisiones se corrió antes que nada.

Igualmente: las primeras citas de este trabajo decían "`ipm_wiki_bench.py:79`" sin decir qué copia.
Se refieren a la de **`iPM-WIKI`** (168 líneas). Los números del ADR salieron de
**`IPM_Backend_AI/tools/ipm_wiki_bench.py:136`**. Corregir una cita sólo hacia delante es como el
próximo lector hereda el error.
