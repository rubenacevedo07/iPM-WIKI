---
title: IMP LLM Wiki — State Report for GPT
slug: gpt-context-report-2026-04-20
type: dossier
created: 2026-04-20
updated: 2026-04-20
confidence: high
sources: [wiki/index.md, wiki/log.md, CLAUDE.md, wiki/companies/_sync_report.json]
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
---

# IMP LLM Wiki — State Report for GPT
**Version:** v1 · **Date:** 2026-04-20 · **Prepared by:** Claude
**Repo:** https://github.com/rubenacevedo07/iPM-WIKI (private)

---

## 0. How to Use This Document

You (GPT) are being onboarded to the IMP LLM Wiki as a consulting analyst. This single document is a compressed, self-contained snapshot of the wiki's state as of 2026-04-20. When the user asks you about a specific actor, country, institution, theme, or market-impact question, use this document as ground truth. If the user gives you the full repo (file upload, GitHub connector, or pasted pages), prefer the raw pages over this summary for any specific page.

**Read these first, in order:** (1) Section 1 — Mission, (2) Section 2 — Structure, (3) Section 3 — Conventions (archetypes, edge types, chokepoints — IMP jargon), (4) Section 4 — Current Inventory, (5) Section 5 — Known Open Questions.

---

## 1. Mission

Maintain a persistent geopolitical and markets intelligence wiki for the **Intelligence Map Platform (IMP)** that:
- turns raw sources into durable actor/country/institution/commodity/theme/narrative/scenario/indicator/market-impact pages
- accumulates knowledge over time rather than re-deriving on every query
- feeds the IMP product: AI Analyst Avatars, Oracle prediction machines, Due Diligence reports
- stays auditable, linkable, and inspectable inside Obsidian

The wiki is the **narrative layer** above the IMP PostgreSQL graph (116 tables, 1,294+ RelationEdges, 545 persons, 239 companies, 171 countries as of April 2026).

**What this wiki is not:**
- Not a replacement for the DB — the DB owns quantitative structure.
- Not real-time — automation engine (n8n/Perplexity) handles ingestion cadence.
- Not user-facing — it feeds Avatars, Oracle, Due Diligence.
- Not a RAG index — it is compiled, cross-referenced, maintained knowledge.

---

## 2. Structure

```
iPM-WIKI/
├── CLAUDE.md                   ← operational doctrine (v3.0)
├── raw/                        ← immutable source evidence (read-only)
│   ├── central-banks/ geopolitics/ institutions/ commodities/
│   ├── markets/ market-research/ transcripts/ sanctions/
│   ├── legislation/ think-tanks/ internal-notes/ assets/
│   ├── dossiers-external/ ideology/
└── wiki/                       ← synthesized intelligence (editable)
    ├── index.md                ← master catalog
    ├── overview.md             ← macro regime map
    ├── log.md                  ← append-only activity log
    ├── actors/ (21)            countries/ (12)       institutions/ (31)
    ├── companies/ (13)         commodities/ (1)      themes/ (13)
    ├── narratives/ (1)         scenarios/ (5)        indicators/ (5)
    ├── timelines/ (4)          sources/ (13)         dossiers/ (5)
    ├── market-impact/ (3)      comparisons/ (4)      oracle/ (1)
    └── lint-reports/
```

Plus outside `wiki/`:
- `ipm-agent-stack/` — references for IMP agent fleet (Atlas, Cassandra, Helios, Nomos, etc.)
- `doctrine/` — IMP-wide doctrine documents
- `roadmap/5-year-roadmap.md` — product roadmap
- `ipm_wiki_generator.py`, `ipm_wiki_to_graph.py` — Python tooling for DB↔wiki sync

---

## 3. IMP-Specific Conventions (GLOSSARY — READ THIS)

### PowerArchetype enum (every actor has one)
`FINANCIAL · POLITICAL · COERCIVE · INDUSTRIAL · TECHNOLOGICAL · HYBRID`

### Power dimensions (DB column names on entities)
`FinancialScore · MilitaryScore · SoftwareScore · CommodityScore · PoliticalScore · InformationScore`

### RelationEdge types (DB)
`Governs · Owns · Influences · Finances · Sanctions · MilitaryConflict · Supplies · DependsOn · Partners · Sets · Regulates · Competes · Exports · Manufactures · Distributes`

### Strategic chokepoints tracked
Hormuz · Malacca · Suez · Taiwan Strait · Black Sea · Bab el-Mandeb · Panama

### Entity naming
- Persons: `LASTNAME, Firstname` in title; `lastname-firstname` in slug
- Countries: full English name in title; lowercase-hyphen in slug
- DB IDs live in `db_id` frontmatter field; see `wiki/indicators/DB-ID-Reference.md`

### Confidence levels
`high` = multiple corroborating recent sources, no contradictions
`medium` = single source or partial corroboration
`low` = thin sourcing
`conflicted` = sources actively contradict

---

## 4. Current Inventory (2026-04-20)

### 4.1 Actors (21) — PersonPowerIndex Global Ranking

| Rank | Name | DB ID | Archetype | Score | Ideology Seeded |
|------|------|-------|-----------|-------|-----------------|
| 1 | TRUMP, Donald | 173 | POLITICAL | 76 | ✅ Auth=7.5 |
| 2 | XI, Jinping | 171 | HYBRID | 79 | ✅ Auth=9.0 |
| 3 | PUTIN, Vladimir | 172 | COERCIVE | 81 | ✅ Auth=10.0 |
| 4 | MUSK, Elon | 7 | HYBRID | 74 | ✅ Econ=7.5 |
| 5 | FINK, Larry | 75 | FINANCIAL | 72 | ✅ Geo=5.0 |
| 6 | MBS (Mohammed bin Salman) | 176 | COERCIVE | 78 | ✅ Auth=8.5 |
| 7 | HUANG, Jensen | 1 | TECHNOLOGICAL | 68 | ✅ Auth=-3.0 |
| 8 | GATES, Bill | 67 | FINANCIAL | 71 | ✅ Env=-6.0 |
| 9 | MODI, Narendra | TBD | POLITICAL | 64 | ✅ Religion=8.0 |
| 10 | POWELL, Jerome | 192 | POLITICAL | 62 | ✅ Auth=0.0 |
| 11 | LAGARDE, Christine | 191 | POLITICAL | 58 | ✅ Env=-5.0 |
| 12 | BESSENT, Scott | 545 | FINANCIAL | 58 | ✅ Econ=6.0 |
| 13 | ALTMAN, Sam | 61 | TECHNOLOGICAL | 55 | ✅ Auth=-3.0 |
| 14 | YELLEN, Janet | TBD | FINANCIAL | 48 | ❌ |
| — | DIMON, Jamie | 12 | FINANCIAL | pending | ❌ |
| — | MACRON, Emmanuel | 174 | POLITICAL | pending | ❌ |
| — | BUFFETT, Warren | 9 | FINANCIAL | pending | ❌ |
| — | BEZOS, Jeff | 66 | FINANCIAL | pending | ❌ |
| — | ZUCKERBERG, Mark | 6 | TECHNOLOGICAL | pending | ❌ |
| — | CHANG, Morris | 113 | INDUSTRIAL | pending | ❌ |
| — | DALIO, Ray | — | FINANCIAL | — | ❌ |

6 actors (MUSK, TRUMP, FINK, HUANG, GATES, ZUCKERBERG) were enriched on 2026-04-17 with external dossiers — they have full Wealth Composition, Companies/Valuations, Strategic Alliances, Ideology, Risk Profile, and April 2026 Current Assessment sections.

### 4.2 Countries (12)

| Country | DB ID | Region | Key Signal |
|---------|-------|--------|------------|
| United States | 1 | NA | Fed, Dollar, Pentagon |
| China | 148 | EA | Rare Earths 60%, TSMC risk |
| Russia | 64 | EU | Urals oil, sanctions |
| Taiwan | 151 | EA | TSMC chokepoint, SupplyRisk=9 |
| Ukraine | 65 | EU | War, Palantir AI |
| Saudi Arabia | 71 | ME | OPEC, Arab Light, MBS |
| France | 30 | EU | ECB, Macron, CAC 40 |
| Germany | 29 | EU | Industrial base, BIS HQ |
| India | 140 | SA | Russia oil buyer, Modi |
| Iran | 72 | ME | Hormuz=10, IRGC |
| Israel | 74 | ME | IDF, tech, Iran proxy |
| Japan | 149 | EA | BOJ, TSMC Kumamoto, yen carry |

### 4.3 Institutions (31)

- **Central Banks & Multilateral:** Federal Reserve (240), ECB (241), BIS (246), IMF (245)
- **Government & Military:** US Treasury (242), Pentagon (243), Kremlin, OPEC
- **Finance:** BlackRock (90), Wall Street (244), JPMorgan (12), Goldman Sachs (63)
- **AI & Tech:** NVIDIA (1), OpenAI (198), Anthropic (197), Palantir, Microsoft (4), Azure, Alphabet (3), Google Cloud, Amazon (5), AWS, Meta (6), Apple (2), Tesla (7)
- **Semiconductors (chokepoints):** TSMC (41), ASML (21), Samsung (43)
- **Energy & Defense:** ExxonMobil (14), Saudi Aramco (42), Lockheed Martin (68)

### 4.4 Companies — Auto-Generated (13)

Added 2026-04-19 via `ipm_wiki_generator.py`. Parallel to `institutions/` but driven by DB entity sync. Current set: Nvidia (1), Apple (2), Microsoft (4), Amazon (5), TSMC (41), Lockheed Martin (68), Raytheon (80), BlackRock (90), Palantir (96), Northrop Grumman (97), SpaceX (201), + index + sync report.

**Known drift:** Lockheed Martin — edge strength vs Northrop Grumman: wiki says Competes=High/Partners=Medium, DB says Competes=Medium/Partners=High. Unresolved since 2026-04-19.

### 4.5 Themes (13) — all `high` confidence except Bitcoin-Macro-Regime (`medium`)

- **IMP Product:** Platform-Architecture, Automation-Engine, Oracle-System, Competitive-Moats, Business-Model, Power-Index-System
- **Geopolitical:** Chokepoint-Intelligence, Energy-Chokepoints-War, AI-Supply-Chain-Export-Controls, Geoeconomic-Fragmentation, Monetary-Policy-Weaponized-World, Dollar-System-Fed-Liquidity, Bitcoin-Macro-Regime

### 4.6 Scenarios (5)
- AI-Race-Breakpoint-2026-2028
- Dollar-System-Stress-2026-2028
- Fed-Pivot-2026
- Hormuz-Iran-Crisis-2026
- Taiwan-Strait-2026-2028

### 4.7 Indicators (5)
- DB-ID-Reference (all verified DB IDs — canonical)
- Enum-Types-Reference (DB enums — canonical)
- Fed-Liquidity-Pulse (financial, Fed/global)
- USD-Hegemony-Index (financial, global)
- US-Military-Projection (coercive, USA)

### 4.8 Comparisons (4)
- Powell-Lagarde-Divergence → EUR/USD signal = 4.5/10
- Trump-Powell-Divergence → political pressure = 6.43/10
- BlackRock-Ownership-Web → 15 companies (Invisible Hand Tracker)
- IMP-Agent-Roles

### 4.9 Market-Impact (3)
- Fed-Rate-Policy-Markets
- Trump-Trade-War-Markets
- Bitcoin-vs-Equities-Rates

### 4.10 Narratives (1)
- Global-Macro-Regime-2026-04 — current dominant narrative

### 4.11 Oracle (1)
- Oracle-Machine-Roster — 20 prediction machines, domains defined

### 4.12 Sources (13) — raw file summaries
IMP-Strategy-v2-2, IPM-SQL-Seed-Reference, Session-Record-2026-03-27, Project-State-2026-04-01, Session-Handoff-2026-04-02, Launch-Plan-April-21, Powell-FOMC-2026-04, Lagarde-ECB-2026-04, IMF-WEO-2026-04, BlackRock-13F-2025-12-31, Chokepoint-Risk-2026-04, Trump-Trade-Policy-2026-04, Russia-Oil-Sanctions-2026-04

### 4.13 Dossiers (5)
- Launch-Plan-April-21 (go-to-market, 6 personas)
- Product-Ideas-2026-03-27 (7 product ideas)
- IMP-Raw-Collection-Prompts (10-task Perplexity pack)
- IMP-Prompt-Pack-Operativo-v2 (5-priority ops prompts)
- Perplexity-State-Report-v13 (parallel briefing for Perplexity)

---

## 5. DB Sync Status

All 2026-04-10 flags CLOSED:
- CL-DB-003 Bab el-Mandeb score=8 ✅
- CL-DB-004 BlackRock Owns edges (RE 1285-1294, 10 edges) ✅
- CL-DB-005 Semiconductor PowerMapRelation ✅
- CL-DB-006 IdeologyProfile 12 actors ✅
- CL-DB-007 Country IDs (France=30, Germany=29, India=140, Iran=72, Israel=74, Japan=149) ✅
- CL-DB-008 AI supply chain companies (Palantir=96, AMD=69, Arm=248, xAI=199) ✅
- CL-DB-009 AI supply chain edges (RE 1257-1271, 18 edges) ✅
- CL-DB-010 Commodity links (315 CompanyCommodities, 22 CommodityFacility) ✅
- CL-DB-011 Institution RelationEdges (RE 1272-1284, 13 edges) ✅

**Final RelationEdge count: 1,294**

**Open flags (from 2026-04-17 dossier enrichment):**
- Wealth figures (EstimatedWealthUsd) for 6 dossier actors need verification against Persons table
- New Company candidates: xAI (under SpaceX), Trump Media (DJT), World Liberty Financial, iShares, Starlink, CZI
- New edges: US-China NVIDIA/AMD 15% revenue deal, Fink→Advises→Ukraine reconstruction, Fink→Manages→US-Infrastructure-Fund, Zuckerberg→Influences→Trump
- Chokepoint candidates: Starlink (Musk), Aladdin (Fink), CUDA (Huang)
- Sovereign AI NVIDIA→Supplies edges: UAE, Saudi, Japan, India, France, Singapore

**Drift (from 2026-04-19 companies/_sync_report.json):**
- Lockheed Martin (068) — edge strengths vs Northrop Grumman flipped between wiki and DB

---

## 6. Recent Activity

| Date | Op | Summary |
|------|------|---------|
| 2026-04-09 | init + ingest × N | Repo initialized; IMP strategy doc ingested; 16 actor stubs seeded with DB IDs; country pages first round; CLAUDE.md v3.0 frontmatter migration |
| 2026-04-10 | db-sync × multiple | All 9 DB sync flags closed; RelationEdge count reached 1,294 |
| 2026-04-17 | dossier-ingest | 6 actor pages enriched from external HTML dossiers (MUSK, TRUMP, FINK, HUANG, GATES, ZUCKERBERG) |
| 2026-04-19 | auto-gen (unlogged) | `wiki/companies/` directory generated with 11 entity pages + `_INDEX.md` + `_sync_report.json` |
| 2026-04-20 | state-snapshot | No edits today; this report generated |

Full append-only log: `wiki/log.md`.

---

## 7. What Would Be Most Useful For GPT to Do

Prioritized, in decreasing order of leverage:

1. **Populate `wiki/overview.md`** — it's still a stub. Synthesize a dominant-narratives + top-actors + key-themes-under-watch snapshot from the 13 theme pages + 1 narrative page + 13 source pages.
2. **Enrich the 8 un-ideologized actors** (DIMON, MACRON, BUFFETT, BEZOS, ZUCKERBERG already dossiered but no Ideology score, CHANG, DALIO, YELLEN). Each needs: Ideology profile (economic/authoritarian/religious/environmental axes, –10 to +10), Current Assessment, Market Impact, Key Recent Actions.
3. **Write the missing country pages** — wiki only has 12 of 171 DB countries. Priority candidates: Turkey, UAE, South Korea, Brazil, Mexico, UK, Indonesia, Vietnam, Poland, Nigeria.
4. **Write dedicated pages for Aladdin, CUDA, Starlink** — they are functioning chokepoints per the dossier ingests but have no wiki page yet.
5. **Resolve the Lockheed↔Northrop edge-strength drift** — decide authoritative value, update either wiki or DB.
6. **Fill `wiki/oracle/` with individual machine pages** — currently only the roster exists; each of 20 machines needs its own page with prediction history + accuracy profile (per CLAUDE.md §4.10 template).
7. **Lint pass** — check contradictions across pages, orphans, stale pages (>60 days on high-churn topics), unsourced claims. Output to `wiki/lint-reports/YYYY-MM-DD.md`.

---

## 8. How to Write New Pages (If Asked)

Every core page needs YAML frontmatter. Minimum required fields on all pages:

```yaml
title: <human-readable>
slug: <stable-lowercase-hyphen>
type: <actor|country|institution|theme|indicator|narrative|scenario|market-impact|source-summary|dossier|oracle>
region: <region-or-global>
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: <low|medium|high|conflicted>
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
```

Plus type-specific fields (see `CLAUDE.md` §3.2):
- Actor: `role`, `country`, `db_id`, `db_type: PERSON`
- Country: `db_id`, `db_type: COUNTRY`
- Institution: `institution_type`, `db_id`, `db_type: COMPANY`
- Indicator: `domain`, `scope`
- Oracle: `machine_domain`, `brier_trend`

Section templates for each page type live in `CLAUDE.md` §4. Always reciprocate relationships (if A links to B, check B links back to A). Always append an entry to `wiki/log.md`. Always update `wiki/index.md` if new pages are created.

---

## 9. What Not To Do

- Do not edit `raw/` — it is immutable source evidence.
- Do not create duplicate pages when one exists with a close slug. Check `wiki/index.md` first. Deduplication rules in `CLAUDE.md` §3.5.
- Do not invent `db_id` values. If unknown, write `TBD` and flag in notes. The authoritative DB ID list is `wiki/indicators/DB-ID-Reference.md`.
- Do not change `slug` or `created` fields after first write.
- Do not silently drop existing Ideology tables, DB sync notes, or related_* arrays when editing — merge, don't replace.
- Do not overlink weak associations in `related_*` fields — noisy links reduce graph quality.
- Do not use `#` headings inside frontmatter. Frontmatter is YAML.

---

*IMP LLM Wiki · GPT Context Report v1 · 2026-04-20 · Confidential — Solo Founder*
