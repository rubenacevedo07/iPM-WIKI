# IMP Wiki — Prompt Pack Operativo v2.0
*Alineado con CLAUDE.md v3.0 · April 2026*
*Para usar con Perplexity Max → pegar output en Claude.ai → Claude ingesta automáticamente*

---

## Instrucciones Generales (pegar siempre al inicio)

```
Eres un agente de recolección de inteligencia para el IMP LLM Wiki.
Tu output alimenta directamente páginas wiki con este schema de frontmatter YAML:

Actor pages requieren: title, slug, type, role, country, region, tags, db_id,
  db_type, related_actors, related_countries, related_institutions,
  related_themes, confidence, sources

Country pages requieren: title, slug, type, region, db_id, db_type,
  PowerArchetype (FINANCIAL|POLITICAL|COERCIVE|INDUSTRIAL|TECHNOLOGICAL|HYBRID),
  FinancialScore (0-100), MilitaryScore (0-100), SoftwareScore (0-100),
  CommodityScore (0-100), PoliticalScore (0-100), InformationScore (0-100)

Secciones obligatorias en actor pages:
  ## Power Profile, ## IdeologyProfile, ## Current Assessment,
  ## Narrative Shift, ## Key Recent Actions, ## Market Impact,
  ## DB Sync Notes

Secciones obligatorias en country pages:
  ## Strategic Summary, ## Power Profile, ## Key Actors,
  ## Domestic Pressures, ## External Alignments,
  ## Narrative Trajectory, ## Market Relevance

Formato de output: siempre con wrapper === FILENAME === ... === END ===
No reproduzcas texto completo con copyright — sintetiza y extrae claims clave.
Incluye Source URLs para cada afirmación.
```

---

## PRIORITY 1 — IdeologyProfile para 9 actores

*Alimenta: `IdeologyProfile` table en DB + sección `## IdeologyProfile` en actor pages*
*DB columns: EconScore, AuthScore, CulturalScore, GenderScore, GeoScore, EnvScore, ReligionScore (-10 to +10)*

```
Basándote SOLO en el registro PÚBLICO de cada persona (discursos, entrevistas,
posiciones publicadas, decisiones documentadas), proporciona puntuaciones en
7 ejes para cada uno.

Escala: -10 a +10
1. EconScore: ideología económica (-10=izquierda/control estatal, +10=derecha/mercado libre)
2. AuthScore: autoritarismo vs liberalismo (-10=liberal/democrático, +10=autoritario)
3. CulturalScore: conservadurismo cultural (-10=progresista, +10=conservador)
4. GenderScore: actitudes de género (-10=progresista, +10=tradicional)
5. GeoScore: orientación geopolítica (-10=aislacionista, +10=multilateralista)
6. EnvScore: postura medioambiental (-10=intervencionista/activista, +10=desregulador)
7. ReligionScore: religión en gobernanza (-10=laico, +10=religioso)

Personas a puntuar:
- Xi Jinping (China, Secretario General PCCh) — DB ID: 171
- Mohammed bin Salman (Arabia Saudí, Príncipe Heredero) — DB ID: 176
- Larry Fink (CEO BlackRock) — DB ID: 75
- Scott Bessent (Secretario del Tesoro EEUU) — DB ID: 545
- Jensen Huang (CEO NVIDIA) — DB ID: 1
- Bill Gates (filántropo, ex-CEO Microsoft) — DB ID: 67
- Sam Altman (CEO OpenAI) — DB ID: 61
- Narendra Modi (India, Primer Ministro) — DB ID: TBD
- Janet Yellen (ex-Secretaria del Tesoro EEUU) — DB ID: TBD

Para cada persona, output en este formato exacto:
=== FILENAME: raw/ideology/[lastname-firstname]-ideology-2026-04.md ===
# IdeologyProfile — [Nombre Completo]
**DB ID:** [id]
**Fecha:** 2026-04-09
**Source URLs:** [lista]

## Puntuaciones
EconScore: [valor]
AuthScore: [valor]
CulturalScore: [valor]
GenderScore: [valor]
GeoScore: [valor]
EnvScore: [valor]
ReligionScore: [valor]
LabelPrimary: [etiqueta 2-4 palabras en inglés]
Confidence: [0-100]

## Justificación por eje
- Econ: [evidencia concreta]
- Auth: [evidencia concreta]
- Cultural: [evidencia concreta]
- Gender: [evidencia concreta]
- Geo: [evidencia concreta]
- Env: [evidencia concreta]
- Religion: [evidencia concreta]

## Divergencia más relevante para IMP
[Con qué otro actor del sistema tiene la mayor divergencia y en qué eje]
=== END ===
```

---

## PRIORITY 2 — Country Pages: Francia, Alemania, India, Irán, Israel, Japón

*Alimenta: `wiki/countries/` + DB Countries table*
*Secciones CLAUDE.md v3.0: Strategic Summary, Power Profile, Key Actors, Domestic Pressures, External Alignments, Sanctions, Narrative Trajectory, Market Relevance*

```
Para cada país, crea un brief de inteligencia estructurado para el IMP Wiki.
Usa datos actuales (abril 2026).

=== FILENAME: raw/geopolitics/[country-slug]-country-brief-2026-04.md ===
# [País] — Intelligence Brief April 2026
**Source URLs:** [lista]

## Strategic Summary
[2-3 frases: rol central en sistema regional/global, por qué importa para IMP]

## Power Profile
- FinancialScore (0-100): [valor + breve justificación]
- MilitaryScore (0-100): [valor + breve justificación]
- SoftwareScore (0-100): [valor + breve justificación]
- CommodityScore (0-100): [valor + breve justificación]
- PoliticalScore (0-100): [valor + breve justificación]
- InformationScore (0-100): [valor + breve justificación]
- PowerArchetype: [FINANCIAL|POLITICAL|COERCIVE|INDUSTRIAL|TECHNOLOGICAL|HYBRID]
- Chokepoint exposure: [chokepoints relevantes]
- Veto points: [instituciones donde tiene veto real]

## Key Actors (top 3)
- [Nombre] — [rol] — DB ID si conocido
- [Nombre] — [rol]
- [Nombre] — [rol]

## Domestic Pressures (top 3 actuales)
- [presión 1 + fuente]
- [presión 2 + fuente]
- [presión 3 + fuente]

## External Alignments
- Alianzas clave: [lista]
- Rivalidades activas: [lista]
- Postura vs EEUU/China: [descripción]

## Sanctions and Legal Constraints
[Sanciones activas, restricciones de tratados, compromisos internacionales relevantes]

## Narrative Trajectory (April 2026)
[Qué ha cambiado en los últimos 6 meses: qué está ganando/perdiendo poder,
qué narrativa domina, qué narrativa está emergiendo]

## Market Relevance
- FX: [par de divisas relevante y drivers]
- Exportaciones clave: [top 3]
- Exposición a commodities: [petróleo, gas, semiconductores, alimentos]
- Deuda soberana / credit: [rating, spread, riesgo]
- Link a señales IMP: [qué señales IMP afectan a este país]
=== END ===

Países: France (slug: france), Germany (slug: germany), India (slug: india),
Iran (slug: iran), Israel (slug: israel), Japan (slug: japan)
```

---

## PRIORITY 3 — TSMC Earnings + Jensen Huang Narrative Update

*Alimenta: `wiki/institutions/TSMC.md`, `wiki/actors/HUANG-Jensen.md`, `wiki/themes/AI-Supply-Chain-Export-Controls.md`, `wiki/timelines/AI-Tech-Decoupling-2019-2026.md`*

```
Sintetiza los resultados del earnings call más reciente de TSMC (Q4 2025 o Q1 2026)
y cualquier declaración pública reciente de Jensen Huang (NVIDIA).

=== FILENAME: raw/transcripts/tsmc-earnings-2026-04.md ===
# TSMC Earnings — [Trimestre] [Año]
**Fecha:** [fecha]
**Source URLs:** [lista]

## Revenue + Guidance
- Ingresos: [cifra + variación YoY]
- Guidance próximo trimestre: [cifra]
- Márgenes brutos: [%]

## Technology Nodes — Demand Signal
- N3 (3nm): [% revenue, demanda, clientes]
- N2 (2nm): [estado producción, primera producción, clientes clave]
- Avanzado (<7nm): [% total revenue]

## AI/HPC Demand
- Qué porcentaje del revenue viene de AI/HPC
- Qué clientes mencionados (NVIDIA, Apple, AMD, otros)
- Qué dice sobre demanda forward

## CoWoS Packaging Capacity
- Estado actual de capacidad
- Cuándo se resuelve el bottleneck
- Impacto en deliveries NVIDIA

## Arizona / Japan Fab Progress
- Arizona: estado de producción, timeline N2
- Japan: estado Kumamoto fabs
- Cualquier retraso o actualización

## China Revenue + Export Controls
- % revenue de China
- Cambios por export controls
- Cómo está afectando el plan de capacidad

## Management Narrative Shift vs Prior Quarter
[Qué cambió en el tono, qué enfatizan ahora que antes no, qué omiten]
=== END ===

=== FILENAME: raw/transcripts/jensen-huang-narrative-2026-04.md ===
# Jensen Huang — Narrative Update April 2026
**Source URLs:** [lista]

## Current Posture
[Qué está diciendo Jensen en público sobre AI demand, infrastructure, competition]

## Narrative Shift vs 6 months ago
[Qué ha cambiado en su lenguaje, énfasis, o posición]

## Key Claims (paraphrased)
- Sobre demanda de GPUs: ...
- Sobre China/export controls: ...
- Sobre competencia (AMD, custom silicon, Huawei): ...
- Sobre próxima generación (Blackwell, Rubin): ...

## Market Impact Signals
[Cómo reaccionó el mercado a sus declaraciones recientes]
=== END ===
```

---

## PRIORITY 4 — BIS Quarterly Review

*Alimenta: `wiki/themes/Monetary-Policy-Weaponized-World.md`, DSI index inputs, `wiki/narratives/Global-Macro-Regime-2026-04.md`*

```
Sintetiza el BIS Quarterly Review más reciente (Q1 2026 o el más actual disponible).

=== FILENAME: raw/institutions/bis-quarterly-2026-04.md ===
# BIS Quarterly Review — [Fecha]
**Source URLs:** [lista]

## Global Financial Conditions
- Condiciones de liquidez globales: [tight/neutral/loose + drivers]
- Spreads de crédito: [investment grade, high yield — tendencia]
- Flujos de capital cross-border: [tendencia principal]

## Dollar System Health
- USD share en reservas FX (COFER data si disponible): [%]
- USD en facturación comercial: [% si disponible]
- SWIFT USD share: [% si disponible]
- Signos de de-dolarización: [qué evidencia hay, qué evidencia NO hay]

## Credit and Leverage (Key Warnings)
- Sectores con apalancamiento excesivo: [lista]
- Países con vulnerabilidad de deuda elevada: [lista]
- Riesgo sistémico bancario: [nivel de alerta]

## Cross-Border Capital Flows
- Tendencia principal: [entrada/salida EMs, dirección USD, EUR, CNY]
- Fragmentación geoeconómica en flujos: [evidencia]

## EM Vulnerabilities
- Países más vulnerables a higher-for-longer: [lista]
- Exposición a deuda en USD: [datos si disponibles]

## Key Quotes from Overview
[2-3 parafraseos clave del Overview del BIS — no texto literal]
=== END ===
```

---

## PRIORITY 5 — Weekly Refresh (cadencia semanal)

*Alimenta: actor pages Powell/Lagarde, Chokepoint-Intelligence.md, Energy-Chokepoints-War.md*
*Ejecutar cada lunes — 3 subtareas independientes*

```
=== SUBTAREA A: Powell / Fed — Weekly Update ===

Busca: cualquier declaración, discurso, o comunicado de la Fed o Jerome Powell
en los últimos 7 días.

=== FILENAME: raw/transcripts/powell-weekly-[YYYY-MM-DD].md ===
# Powell / Fed — Weekly Update [Fecha]
**Source URLs:** [lista]

## ¿Hubo evento esta semana?
[Sí/No — qué evento: discurso, minutos, comunicado, entrevista]

## Cambio vs semana anterior
[Qué es nuevo, qué cambió en el tono o mensaje]

## Key Claims (paraphrased)
[Solo si hay contenido nuevo — no repetir lo ya documentado]

## Narrative Shift Signal
[¿Hay algún cambio de narrativa que requiera actualizar POWELL-Jerome.md?
Sí/No + qué cambiaría]
=== END ===

=== SUBTAREA B: Lagarde / ECB — Weekly Update ===

Busca: cualquier declaración pública de Christine Lagarde o del BCE en los
últimos 7 días.

=== FILENAME: raw/central-banks/lagarde-weekly-[YYYY-MM-DD].md ===
# Lagarde / ECB — Weekly Update [Fecha]
[Mismo formato que subtarea A]
=== END ===

=== SUBTAREA C: Chokepoints — Weekly Threat Assessment ===

Busca: incidentes en Hormuz, Bab el-Mandeb/Mar Rojo, Estrecho de Taiwán,
Canal de Suez, Estrecho de Malaca en los últimos 7 días.

=== FILENAME: raw/geopolitics/chokepoints-weekly-[YYYY-MM-DD].md ===
# Chokepoints — Weekly Update [Fecha]
**Source URLs:** [lista]

## ¿Incidentes esta semana?
[Por chokepoint — Sí/No + descripción si Sí]

## Cambio en threat level vs semana anterior
| Chokepoint | Score anterior | Score nuevo | Motivo |
|---|---|---|---|
| Hormuz | 7 | [?] | [si cambió] |
| Bab el-Mandeb | 8 | [?] | [si cambió] |
| Taiwan Strait | 6 | [?] | [si cambió] |
| Suez | 5 | [?] | [si cambió] |
| Malacca | 5 | [?] | [si cambió] |

## DB Sync Needed?
[Sí/No — qué tabla actualizar si cambió algún score]
=== END ===
```

---

## Quick Reference — DB Column Names (para alinear con DB)

| Wiki field | DB table | DB column |
|-----------|----------|-----------|
| EconScore | IdeologyProfile | EconScore |
| AuthScore | IdeologyProfile | AuthScore |
| CulturalScore | IdeologyProfile | CulturalScore |
| GenderScore | IdeologyProfile | GenderScore |
| GeoScore | IdeologyProfile | GeoScore |
| EnvScore | IdeologyProfile | EnvScore |
| ReligionScore | IdeologyProfile | ReligionScore |
| LabelPrimary | IdeologyProfile | LabelPrimary |
| FinancialScore | PersonPowerIndex | FinancialScore |
| MilitaryScore | PersonPowerIndex / MilitaryCapacity | MilitaryScore |
| SoftwareScore | PersonPowerIndex | SoftwareScore |
| PowerArchetype | PersonPowerIndex | ArchetypeCode |
| Threat level | CommodityChokepoint | ClosureRiskScore |

## Quick Reference — Verified DB IDs

| Actor | DB ID | Archetype |
|-------|-------|-----------|
| Jensen Huang | 1 | TECHNOLOGICAL |
| Xi Jinping | 171 | HYBRID |
| Elon Musk | 7 | HYBRID |
| Jamie Dimon | 12 | FINANCIAL |
| Larry Fink | 75 | FINANCIAL |
| Sam Altman | 61 | TECHNOLOGICAL |
| Jeff Bezos | 66 | FINANCIAL |
| Bill Gates | 67 | FINANCIAL |
| Morris Chang | 113 | INDUSTRIAL |
| Donald Trump | 173 | POLITICAL |
| Emmanuel Macron | 174 | POLITICAL |
| MBS | 176 | COERCIVE |
| Christine Lagarde | 191 | POLITICAL |
| Jerome Powell | 192 | POLITICAL |
| Scott Bessent | 545 | FINANCIAL |

---

*IMP Wiki · Prompt Pack Operativo v2.0 · Alineado con CLAUDE.md v3.0 · April 2026*
*Workflow: Perplexity → Claude.ai (paste output) → Claude ingesta → git commit → zip*
