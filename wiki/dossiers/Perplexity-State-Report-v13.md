# IMP LLM Wiki — State Report for Perplexity
**Version:** v13 · **Date:** 2026-04-09 · **Prepared by:** Claudio

---

## What You Are Reading

This is a structured briefing for Perplexity Max on the current state of the IMP LLM Wiki — a persistent geopolitical and markets intelligence knowledge base built on the Karpathy LLM Wiki pattern. The wiki is the narrative layer above the IMP Intelligence Map Platform PostgreSQL graph (116 tables, 1,246+ edges, 545 persons, 239 companies, 171 countries).

This report tells you: what the wiki contains, what it needs, and what Perplexity should collect next.

---

## 1. Wiki Inventory — What Exists

### Scale
- **96 pages** across 14 folders
- **7 raw sources** in `raw/` (all from today's first external batch)
- **Git commits:** 15 operations since initialization

### Folder breakdown

| Folder | Pages | Quality |
|--------|-------|---------|
| `wiki/actors/` | 21 | Medium — stubs now have ideology scores + current assessment for 3 key actors |
| `wiki/countries/` | 6 | Medium — USA, China, Russia, Taiwan, Ukraine, Saudi Arabia |
| `wiki/institutions/` | 22 | Low-Medium — stubs only, BlackRock richest |
| `wiki/themes/` | 7 | High — IMP platform architecture fully documented |
| `wiki/comparisons/` | 4 | High — Powell-Lagarde EUR/USD signal, Trump-Powell divergence, BlackRock ownership web |
| `wiki/market-impact/` | 2 | High — Fed rate policy, Trump trade war |
| `wiki/narratives/` | 1 | High — Global Macro Regime April 2026 |
| `wiki/sources/` | 13 | High — one per ingested source |
| `wiki/timelines/` | 2 | High — DB state timeline, IMP phase roadmap |
| `wiki/dossiers/` | 3 | High — launch plan, product ideas, raw collection prompts |
| `wiki/oracle/` | 1 | Medium — 20 machine roster documented |
| `wiki/indicators/` | 2 | High — verified DB IDs, enum types |
| `wiki/lint-reports/` | 1 | High — first health audit April 9 |
| `wiki/comparisons/` | 4 | High — ideology divergence documented |

### Actor pages — IdeologyProfile status

| Actor | DB ID | PowerIndex | IdeologyProfile | Current Assessment |
|-------|-------|------------|-----------------|-------------------|
| Putin | 172 | 81 | ✅ seeded | Empty |
| Xi | 171 | 79 | ❌ not seeded | Empty |
| MBS | 176 | 78 | ❌ not seeded | Empty |
| Trump | 173 | 76 | ✅ seeded — scores documented | ✅ Updated Apr 9 |
| Musk | 7 | 74 | ✅ seeded | Empty |
| Gates | 67 | 71 | ❌ not seeded | Empty |
| Fink | 75 | 72 | ❌ not seeded | Empty |
| Huang | 1 | 68 | ❌ not seeded | Empty |
| Modi | TBD | 64 | ❌ not seeded | Empty |
| Powell | 192 | 62 | ✅ seeded — scores documented | ✅ Updated Apr 9 |
| Lagarde | 191 | 58 | ✅ seeded — scores documented | ✅ Updated Apr 9 |
| Bessent | 545 | 58 | ❌ not seeded | Empty |
| Altman | 61 | 55 | ❌ not seeded | Empty |
| Yellen | TBD | 48 | ❌ not seeded | Empty |

### Key intelligence already compiled

**Signal models:**
- Powell vs Lagarde EUR/USD signal = **4.5/10** (strong divergence zone, EconScore gap 6.0 = primary driver)
- Trump vs Powell political pressure signal = **6.43/10** (AuthScore gap 7.5 = Fed independence risk)
- Trump vs Lagarde = **9.75/10** (near maximum — ideological opposites)

**Chokepoint threat scores (wiki assessment April 2026):**
- Bab el-Mandeb: **8/10** (Houthis — highest active risk, shipping rerouting)
- Hormuz: **7/10** (IRGC — elevated but no active blockade)
- Taiwan Strait: **6/10** (PLA exercises, grey-zone pressure)
- Suez: **5/10** (indirect risk via Red Sea)
- Malacca: **5/10** (latent)

**⚠ DB SYNC NEEDED:** Bab el-Mandeb threat score in PostgreSQL DB is set lower than current wiki assessment. Houthi campaign has elevated it to highest active chokepoint.

---

## 2. Active DB Sync Flags

These are discrepancies between the wiki and the IMP PostgreSQL database that need resolution:

| Flag | Description | Action Needed |
|------|-------------|---------------|
| CL-DB-003 | Bab el-Mandeb chokepoint threat score outdated in DB | Update CommodityChokepoint row |
| CL-DB-004 | BlackRock→Owns→NVIDIA/TSMC/ASML/ExxonMobil/Lockheed RelationEdge rows missing | Seed RelationEdge rows |
| CL-DB-005 | Semiconductor PowerMap (PowerMap ID 4) PowerMapRelation edges empty | Wire canonical edges to nodes |
| CL-DB-006 | IdeologyProfile missing for: Xi, MBS, Fink, Bessent, Huang, Gates, Altman, Modi, Yellen | Seed IdeologyProfile rows via PX |

---

## 3. What Perplexity Should Collect Next

### Priority 1 — IdeologyProfile inputs (PX-006 extension)
The wiki needs ideology scores for the 9 actors currently missing them. These feed:
- Xi vs Trump geopolitical tension signal
- Fink vs Powell financial establishment vs monetary signal
- MBS vs Powell petrodollar signal
- Huang/Altman tech ideology profiles for Avatar context

**Prompt for Perplexity:**
```
For each person below, based only on their PUBLIC record (speeches, interviews, published positions, documented decisions), provide scores on these 7 axes, each from -10 to +10:

1. EconScore: Economic ideology (-10 = far left / state control, +10 = far right / market fundamentalist)
2. AuthScore: Authoritarian vs liberal (-10 = strongly liberal/democratic, +10 = strongly authoritarian)
3. CulturalScore: Cultural conservatism (-10 = progressive, +10 = conservative)
4. GenderScore: Gender attitudes (-10 = strongly progressive, +10 = strongly traditional)
5. GeoScore: Geopolitical orientation (-10 = isolationist, +10 = strongly multilateralist/internationalist)
6. EnvScore: Environmental stance (-10 = strongly interventionist/climate activist, +10 = strongly deregulatory/anti-environment)
7. ReligionScore: Religious orientation in governance (-10 = strongly secular, +10 = strongly religious)

Also provide: LabelPrimary (2-4 word label), Confidence (0-100), SourceUrl (one key reference)

Persons to score:
- Xi Jinping (China, CCP General Secretary)
- Mohammed bin Salman (Saudi Arabia, Crown Prince)
- Larry Fink (BlackRock CEO)
- Scott Bessent (US Treasury Secretary)
- Jensen Huang (NVIDIA CEO)
- Bill Gates (philanthropist, former Microsoft CEO)
- Sam Altman (OpenAI CEO)
- Narendra Modi (India, Prime Minister)
- Janet Yellen (former US Treasury Secretary)

Output format per person:
Name: [name]
EconScore: [value]
AuthScore: [value]
CulturalScore: [value]
GenderScore: [value]
GeoScore: [value]
EnvScore: [value]
ReligionScore: [value]
LabelPrimary: [label]
Confidence: [0-100]
SourceUrl: [url]
```

### Priority 2 — Missing country pages
The wiki is missing pages for France, Germany, India, Iran, Israel, Japan. These are frequently referenced but have no dedicated intelligence pages.

**Prompt for Perplexity:**
```
For each country below, provide a structured intelligence brief in this exact format:

=== FILENAME: raw/geopolitics/[country-slug]-country-brief-2026-04.md ===
# [Country] — Intelligence Brief April 2026

## Strategic Summary
[2-3 sentences: core role in regional/global system, why it matters]

## Power Profile
- Military capacity: [brief]
- Economic weight: [GDP, key sectors]
- Information power: [media, tech, AI]
- Key chokepoint exposure: [relevant chokepoints]

## Key Actors
[Top 2-3 decision makers with roles]

## Domestic Pressures
[Top 3 current internal pressures]

## External Alignments
[Key alliances, rivalries, partnerships]

## Sanctions and Legal Constraints
[Any active sanctions or treaty constraints]

## Market Relevance
[FX, key exports, commodities exposure, financial markets link]

## Sources
[2-3 URLs]
=== END ===

Countries needed: France, Germany, India, Iran, Israel, Japan
```

### Priority 3 — TSMC earnings call summary
The wiki has a TSMC institution stub with almost no content. TSMC is the highest-stakes chokepoint company in the graph (8 open timelines linked to Taiwan Strait). A recent earnings call summary would populate TSMC.md and update the Taiwan scenario.

**Prompt for Perplexity:**
```
Summarize the most recent TSMC earnings call (Q4 2025 or Q1 2026):

=== FILENAME: raw/transcripts/tsmc-earnings-2026-[date].md ===
# TSMC Earnings — [Quarter] [Year]
**Date:** [date]
**Source URLs:** [list]

## Revenue + Guidance
## Key Technology Nodes (N3, N2 demand)
## AI/HPC Demand Signal
## CoWoS Packaging Capacity
## Arizona/Japan Fab Progress
## China Revenue Exposure + Export Controls
## Management Narrative Shift vs Prior Quarter
=== END ===
```

### Priority 4 — BIS Quarterly Review
Missing from first batch. The BIS Quarterly feeds the DSI (Dollar System Index) and provides the best structured view of global financial conditions, dollar system health, and cross-border capital flows.

**Prompt for Perplexity:**
```
Summarize the most recent BIS Quarterly Review (Q1 2026 or latest available):

=== FILENAME: raw/institutions/bis-quarterly-2026-[date].md ===
# BIS Quarterly Review — [Date]
**Source URLs:** [list]

## Global Financial Conditions
## Dollar System Health (USD share of reserves, SWIFT, FX)
## Credit and Leverage (key warnings)
## Cross-Border Capital Flows
## EM Vulnerabilities
## Key Quotes from Overview
=== END ===
```

### Priority 5 — Weekly refresh cadence
After the initial bootstrap, Perplexity should run a weekly update on the 3 highest-velocity sources:

```
Weekly IMP Wiki Refresh — [date]

1. Powell/Fed: Any statements, speeches, or Fed minutes since last update?
   → Update raw/transcripts/powell-[date].md

2. Lagarde/ECB: Any ECB statements or Lagarde speeches since last update?
   → Update raw/central-banks/lagarde-[date].md  

3. Chokepoints: Any significant incidents at Hormuz, Bab el-Mandeb, Taiwan Strait?
   → Update raw/geopolitics/chokepoint-risk-[date].md
```

---

## 4. How to Send Output Back

Paste Perplexity's output directly into Claude.ai in this project. Claude will:
1. Save each `=== FILENAME === ... === END ===` block to the correct `raw/` path
2. Create/update all relevant `wiki/` pages automatically
3. Flag any DB sync needs
4. Commit to git with a descriptive message
5. Package updated `ipm-wiki-v[N].zip` for download

Alternatively use Claude Code inside `ipm-wiki/` — it writes files directly without the zip step.

---

## 5. Wiki Health Status

From first lint audit (2026-04-09):

| Metric | Status |
|--------|--------|
| Total pages | 96 |
| Orphan pages | 6 remaining (source summaries — acceptable) |
| Thin pages | 19 institution stubs (acceptable — graph nodes) |
| Actor pages with empty Current Assessment | 18 of 21 (improving — 3 now populated) |
| Missing country pages | 4 (France, Germany, India, Iran) |
| DB sync flags open | 4 (CL-DB-003 through CL-DB-006) |
| External sources in raw/ | 7 (first batch — April 9) |

**Overall assessment:** Bootstrap complete. Internal structure solid. External intelligence layer just started. The wiki will compound significantly with each Perplexity batch.

---

## 6. Workflow Summary for Perplexity

```
Perplexity collects → pastes output to Claude.ai → Claude ingests → wiki updates → git commit
```

Frequency: weekly for Priority 3 (refresh); on-demand for Priorities 1-2 (bootstrap completion).

The `wiki/dossiers/IMP-Raw-Collection-Prompts.md` file contains the full 10-task prompt library.

---

*IMP LLM Wiki · Perplexity State Report · v13 · 2026-04-09 · Confidential — Solo Founder*
