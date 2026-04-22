# IMP LLM Wiki `CLAUDE.md`
# Intelligence Map Platform · Karpathy Pattern · v3.0

This file defines how Claude should operate the IMP LLM Wiki, adapted from Karpathy's
LLM Wiki pattern and specialized for geopolitical and markets intelligence.

The wiki lives in a vault with two main layers:
- `raw/` for immutable source evidence
- `wiki/` for synthesized, structured intelligence products

Claude acts as the maintainer of `wiki/`, continuously ingesting sources, updating
pages, and running health checks.

---

## 1. Mission

Maintain a persistent geopolitical and markets intelligence wiki for IMP that:
- turns raw sources into durable actor, country, institution, commodity, theme,
  narrative, scenario, indicator, and market-impact pages
- accumulates knowledge over time rather than re-deriving it on every query
- stays auditable, linkable, and inspectable inside Obsidian
- aligns with IMP's power-index architecture and knowledge-graph design

---

## 2. Folder Model

```text
IMP-wiki/
├── raw/
│   ├── central-banks/         ← Fed, ECB, BOJ, PBOC speeches, minutes, reports
│   ├── geopolitics/           ← conflict, diplomacy, election, treaty material
│   ├── institutions/          ← IMF, BIS, World Bank, NATO, EU docs
│   ├── commodities/           ← IEA, OPEC, commodity market reports
│   ├── markets/               ← macro notes, market commentary
│   ├── market-research/       ← sell-side notes, positioning
│   ├── transcripts/           ← speeches, interviews, press conferences, podcasts
│   ├── sanctions/             ← OFAC lists, EU sanctions packages
│   ├── legislation/           ← bills, directives, policy acts
│   ├── think-tanks/           ← CSIS, CFR, Bruegel, Chatham House, RAND
│   ├── internal-notes/        ← analyst notes, hypotheses, working memos
│   └── assets/                ← images, charts extracted from sources
└── wiki/
    ├── index.md               ← master catalog — always current
    ├── overview.md            ← macro regime map — updated on major shifts
    ├── log.md                 ← append-only activity log
    ├── actors/
    ├── countries/
    ├── institutions/
    ├── commodities/
    ├── themes/
    ├── narratives/
    ├── market-impact/
    ├── scenarios/
    ├── timelines/
    ├── sources/               ← one summary page per ingested raw file
    ├── dossiers/
    ├── comparisons/
    ├── indicators/
    ├── oracle/
    └── lint-reports/
```

Rules:
- treat `raw/` as read-only evidence — do not edit unless explicitly instructed
- treat `wiki/` as the editable intelligence layer
- always prefer updating existing canonical pages over creating duplicates

---

## 3. Frontmatter Governance

Use YAML frontmatter on all core pages. This is what enables Dataview dashboards
in Obsidian and makes the graph queryable.

### 3.1 Common schema — required on ALL five core page types

```yaml
title: <human-readable title>
slug: <stable-machine-id>
type: <actor|country|institution|theme|indicator>
region: <region-or-global>
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: <low|medium|high>
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
```

### 3.2 Type-specific additional fields

**Actor pages** — add:
```yaml
role: <leader|central-banker|minister|oligarch|general|ceo|official>
country: <primary-country-slug>
db_id: <integer>
db_type: PERSON
```

**Country pages** — add:
```yaml
db_id: <integer>
db_type: COUNTRY
```

**Institution pages** — add:
```yaml
institution_type: <central-bank|multilateral|military-alliance|regulator|ministry|sovereign-fund>
db_id: <integer>
db_type: COMPANY
```

**Indicator pages** — add:
```yaml
domain: <political|financial|coercive|hybrid|composite>
scope: <actor|country|institution|commodity|theme>
```

**Oracle pages** — add:
```yaml
machine_domain: <domain string>
brier_trend: <improving|stable|degrading|unknown>
```

### 3.3 Field rules

- `slug`: lowercase, hyphen-separated. Set once. Never change after creation unless
  user explicitly requests a rename or canonical merge.
- `created`: set once on first creation. Never change.
- `updated`: refresh every time the page is materially changed.
- `sources`: list raw file paths that materially inform this page. Do not add every
  globally related source — only what directly informs the content.
- `related_*`: use canonical slugs. Prefer slugs over freeform names. Use arrays
  even when there is only one value. Use `[]` when empty.
- `confidence`: `high` = multiple corroborating sources, recent, no contradictions.
  `medium` = single source or partially corroborated. `low` = thin sourcing.
  `conflicted` = sources actively contradict each other.
- `db_id` / `db_type`: IMP-specific. Always populate when the page maps to a
  PostgreSQL entity. See `wiki/indicators/DB-ID-Reference.md` for verified IDs.

### 3.4 Reciprocal relationship rule

Whenever you add X to a `related_*` field on page A, check whether page X should
also link back to A. Maintain bidirectional consistency where meaningful.

Avoid overlinking weak associations — noisy links reduce graph quality.

### 3.5 Deduplication rules

If near-duplicate pages exist:
1. Choose the canonical page (cleanest title, most complete content).
2. Preserve the strongest existing slug.
3. Merge sources and relationships carefully.
4. Update inbound references where possible.
5. Record the merge in `wiki/log.md`.

---

## 4. Page Types and Sections

### 4.1 Actor pages (`wiki/actors/`)

```markdown
---
title: LASTNAME, Firstname
slug: lastname-firstname
type: actor
role: central-banker
country: country-slug
region: region
tags: [domain, institution, archetype]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: medium
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
db_id: 0
db_type: PERSON
---

# LASTNAME, Firstname

## Summary
2–4 sentences. Who this actor is and why they matter.

## Role and Levers
Formal roles, informal networks, veto points, control over budgets,
institutions, and narratives. What can this actor actually do?

## Power Profile
- **Archetype:** FINANCIAL | COERCIVE | POLITICAL | INDUSTRIAL | TECHNOLOGICAL | HYBRID
- **DB ID:** 0
- **CompositeScore:** (if seeded)
- **Primary domain:**
- **Key institutions:**
- **Key relationships:**

## Current Assessment
Current posture, incentives, constraints, vulnerabilities. Sourced and dated.

## Narrative Shift
Recent changes in language, priorities, red lines, or omissions versus
prior appearances. What is new or different vs 6 months ago?

## Key Recent Actions
- YYYY-MM-DD: ...

## Market Impact
Likely or observed impact on rates, FX, equities, credit, commodities.

## Oracle Relevance
Which Oracle machines track this actor? What prediction domains?

## DB Sync Notes
Last known DB values vs wiki assessment. Flag gaps.

## Sources
## Open Questions
```

### 4.2 Country pages (`wiki/countries/`)

```markdown
---
title: COUNTRY NAME
slug: country-name
type: country
region: region
tags: [region, key-themes]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: medium
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
db_id: 0
db_type: COUNTRY
---

# COUNTRY NAME

## Strategic Summary
Core role in regional and global systems.

## Power Profile
- **DB ID:** 0
- **Military capacity:**
- **Economic weight:**
- **Information power:**
- **Diplomatic influence:**
- **Veto points:**
- **Chokepoint exposure:**

## Key Actors
## Domestic Pressures
## External Alignments
## Sanctions and Legal Constraints
## Narrative Trajectory
## Market Relevance
## Key Timelines
## DB Sync Notes
## Sources
## Open Questions
```

### 4.3 Institution pages (`wiki/institutions/`)

```markdown
---
title: Institution Name
slug: institution-slug
type: institution
institution_type: central-bank
region: region
tags: [institution-type, domain]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
db_id: 0
db_type: COMPANY
---

# Institution Name

## Mandate and Tools
## Internal Structure
## Current Regime
## Relationships
## Recent Moves
- YYYY-MM-DD: ...
## Narrative Shift
## Market Impact Channels
## Sources
## Open Questions
```

### 4.4 Commodity pages (`wiki/commodities/`)

```markdown
---
title: Commodity Name
slug: commodity-slug
type: commodity
tags: [commodity-type, sector]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
db_id: 0
db_type: COMMODITY
---

# Commodity Name

## Strategic Summary
## Supply Structure
## Demand Structure
## Chokepoints and Vulnerabilities
## Sanctions and Policy Risk
## Market Impact
## DB Sync Notes
## Sources
## Open Questions
```

### 4.5 Theme pages (`wiki/themes/`)

```markdown
---
title: Theme Name
slug: theme-slug
type: theme
region: global
tags: [domain, mechanisms]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: medium
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
---

# Theme Name

## Summary
## Drivers
## Constraints
## Key Actors
## Mechanisms
## Market Impact
## Sources
## Open Questions
```

### 4.6 Narrative pages (`wiki/narratives/`)

```markdown
---
title: Narrative Name
slug: narrative-slug
type: narrative
tags: [subject, region, domain]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: medium
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
---

# Narrative Name

## Current Narrative
## Historical Baseline
## Recent Shifts
## Carriers
## Conflicting Narratives
## Market Read-Through
## Sources
## Open Questions
```

### 4.7 Market-impact pages (`wiki/market-impact/`)

```markdown
---
title: Event/Theme → Markets
slug: event-markets
type: market-impact
tags: [trigger, asset-classes]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: medium
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
---

# Event/Theme → Markets

## Direct Channels
## Second-Order Channels
## Affected Countries
## Affected Commodities
## Asset-Class Impact
## Time Profile
## Key Uncertainties
## Sources
```

### 4.8 Scenario pages (`wiki/scenarios/`)

```markdown
---
title: Subject YYYY–YYYY Scenarios
slug: subject-scenarios
type: scenario
tags: [subject, region, time-horizon]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: low
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
---

# Subject YYYY–YYYY Scenarios

## Scenario Space
## Branch A: [Name]
## Branch B: [Name]
## Branch C: [Name]
## Cross-Branch Markers
## Oracle Relevance
## Sources
## Open Questions
```

### 4.9 Indicator pages (`wiki/indicators/`)

```markdown
---
title: Indicator Name
slug: indicator-slug
type: indicator
domain: political
scope: country
region: global
tags: [power-index, domain]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: medium
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
---

# Indicator Name

## Definition
## Rationale
## Inputs
## Calculation Logic
## Interpretation
## Limitations and Caveats
## Maintenance Rules
## Sources
```

### 4.10 Oracle pages (`wiki/oracle/`)

```markdown
---
title: MACHINE-NAME Oracle Context
slug: machine-name
type: oracle
machine_domain: domain string
brier_trend: unknown
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: medium
sources: []
related_actors: []
related_themes: []
---

# MACHINE-NAME

## Domain
## Accuracy Profile
## Recent Predictions
| Date | Prediction | Outcome | Score |
|------|-----------|---------|-------|
## Context Block (last used)
## Sources
```

### 4.11 Source summary pages (`wiki/sources/`)

```markdown
---
title: Summary - Source Name
slug: source-summary-slug
type: source-summary
source-path: raw/folder/filename.md
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
---

# Summary - Source Name

## Source
## Main Takeaways
## Key Claims
## Countries Most Affected
## Market Relevance
## DB Sync Notes
## Notes
```

---

## 5. Operations

### 5.1 Ingest

When asked to ingest a raw file:

1. Read this `CLAUDE.md`.
2. Read the source file in `raw/`.
3. Classify the source type using the priority tiers below.
4. Extract: actors, countries, institutions, commodities, dates, key claims,
   narrative shifts, market transmission channels.
5. Check `wiki/index.md` — identify all existing pages this source touches.
6. Create or update a source summary page in `wiki/sources/`.
7. Create or update relevant pages across wiki folders.
8. **Narrative shift detection:** for actor and institution pages, explicitly note if
   this source changes language, priorities, red lines, or omissions vs prior appearances.
9. **Market transmission:** update `wiki/market-impact/` pages where plausible.
10. **Reciprocal links:** when adding relationships, check both directions.
11. Flag contradictions with existing wiki content explicitly.
12. Update `wiki/index.md` if new pages were created.
13. Append a structured entry to `wiki/log.md`.
14. Return a file-by-file changelog.

**DB sync flag:** flag `DB SYNC NEEDED: {entity/edge/index} — {reason}` when
ingest reveals data that should update the PostgreSQL graph. Never write to DB directly.

**Source priority tiers:**

| Priority | Type | Best For |
|----------|------|----------|
| 1 | Official releases, transcripts, central bank statements | Direct institutional language |
| 2 | Laws, sanctions, directives, filings | Enforceable reality |
| 3 | Institutional reports (IMF, BIS, World Bank) | Broad structured evidence |
| 4 | Market notes, sell-side research | Transmission and positioning |
| 5 | Think tank analysis | Framing, scenarios, strategic logic |
| 6 | Media coverage | Speed and narrative detection — noisier |
| 7 | Internal notes | Hypotheses only — not source-of-truth |

**Specialized focus by source type:**

- **Speeches / press conferences:** rhetorical shifts vs prior appearances, new
  emphasis, omissions, forward guidance, affected countries/sectors/assets.
- **IMF / BIS / World Bank:** policy warnings, debt vulnerabilities, commodity
  implications, spillover channels, indicator definitions.
- **Sanctions:** sanctioned actors/sectors, enforcement, affected commodities/
  logistics/banking, evasion pathways, second-order market effects.
- **Internal notes:** treat as hypotheses. Separate evidence-backed claims from
  speculation. File durable insights into scenarios, comparisons, or dossiers.

### 5.2 Query

When answering a question:

1. Read `wiki/index.md` first.
2. Open only the relevant pages.
3. Synthesize from the wiki — not from raw files directly.
4. State uncertainty clearly. Distinguish facts, synthesis, and speculation.
5. Assess: does this answer create reusable knowledge? → file it.
6. Assess: does this reveal a DB sync need? → flag it.

### 5.3 Oracle Context

When preparing context for Oracle report generation or AI Analyst Avatars:

1. Pull relevant `wiki/actors/` pages for each avatar's domain.
2. Pull relevant `wiki/themes/`, `wiki/narratives/`, `wiki/market-impact/` pages.
3. Pull `wiki/oracle/` page for the specific machine if it exists.
4. Synthesize: current dominant narrative, actor posture changes, narrative shifts,
   open contradictions, prediction history.
5. File the context block in `wiki/oracle/{machine-slug}.md` after use.

### 5.4 Lint

When asked to run a health check:

1. Scan `wiki/` for:
   - contradictions between pages
   - stale pages (high-churn topic, updated >60 days ago)
   - orphan pages (no inbound links)
   - missing pages (entities mentioned frequently but no dedicated page)
   - unsourced claims
   - DB drift (wiki diverges from DB entity data)
   - missing cross-links
   - geopolitics disconnected from markets (no market-impact link)
   - narrative drift not captured (empty Narrative Shift sections)
   - indicator pages untethered from source evidence
   - timeline gaps
2. Output a structured lint report to `wiki/lint-reports/YYYY-MM-DD.md`.
3. Append a log entry to `wiki/log.md`.
4. Propose top 5 next sources to ingest.

---

## 6. Control Files

### `wiki/index.md`
Master catalog. Group by type. One-line descriptions. Update after every ingest
that creates new pages.

### `wiki/overview.md`
Macro regime map. Compact synthesis of major themes, key actors in motion,
structural constraints, scenario branches, market regime. Update on major shifts.

### `wiki/pending-db-sync.md`
**Single source of truth for wiki→DB gaps.** All open `DB SYNC NEEDED` flags live
here. Format: `CL-DB-NNN | entity/edge | description | raised | status`.

Rules:
- **Always check this file** before writing DB-related SQL or confirming DB state.
- When raising a new flag: add to Open Flags table + note in affected page's
  `## DB Sync Notes` + log in `wiki/log.md`.
- When a flag is confirmed live in DB: move to Closed Flags, update the wiki page,
  add a `db-sync` log entry.
- Never delete closed entries — they are a permanent audit trail.
- Sequential numbering: `CL-DB-001`, `CL-DB-002`, etc. Never reuse a number.

### `wiki/log.md`
Append-only. Never rewrite past entries. Format:

```markdown
## YYYY-MM-DD | {operation} | {subject}
- source: raw/folder/filename.md
- created: wiki/...
- updated: wiki/...
- contradictions: ...
- db-sync: yes/no
- notes: ...
```

---

## 7. IMP-Specific Conventions

**Entity naming:**
- Persons: `LASTNAME, Firstname` (matches IMP DB convention)
- File slugs: `lastname-firstname` (lowercase, hyphen)
- Countries: full English name in title, lowercase-hyphen in slug (e.g. `united-states`)
- Companies: full legal name in title

**DB entity references:**
- Always populate `db_id` and `db_type` when the page maps to a PostgreSQL entity
- See `wiki/indicators/DB-ID-Reference.md` for all verified IDs

**Chokepoints:** Hormuz · Malacca · Suez · Taiwan Strait · Black Sea · Bab el-Mandeb · Panama

**Power dimensions (DB column names):**
FinancialScore · MilitaryScore · SoftwareScore · CommodityScore · PoliticalScore · InformationScore

**Edge types:**
Governs · Owns · Influences · Finances · Sanctions · MilitaryConflict · Supplies ·
DependsOn · Partners · Sets · Regulates · Competes · Exports · Manufactures · Distributes

**PowerArchetype enum:**
FINANCIAL · POLITICAL · COERCIVE · INDUSTRIAL · TECHNOLOGICAL · HYBRID

---

## 8. What This Wiki Is Not

- Not a replacement for the PostgreSQL graph — the DB owns structure and quantitative data
- Not a real-time pipeline — the automation engine (n8n/Perplexity) owns that
- Not a user-facing product directly — it feeds Avatars, Oracle, and Due Diligence reports
- Not a RAG index — it is compiled, cross-referenced, maintained knowledge

---

*IMP LLM Wiki · CLAUDE.md v3.0 · April 2026 · Confidential — Solo Founder*
