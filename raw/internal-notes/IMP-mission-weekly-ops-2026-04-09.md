# IMP Wiki — Mission Pack Weekly Ops v1.0
**Created:** 2026-04-09
**Path:** raw/internal-notes/IMP-mission-weekly-ops-2026-04-09.md
**Status:** ACTIVE — use every week

---

## OVERVIEW

This file defines the 5 recurring intelligence operations for the IMP LLM Wiki.
Each operation has: trigger, source, prompt (ready to paste), output target, ingest command.

Workflow:
```
1. Copy prompt → Perplexity Max
2. Paste Perplexity output here in Claude.ai
3. Claude runs: ingest [filename] → wiki updates + SQL if needed
4. git commit → ipm-wiki-v[N].zip
```

---

## OP-1 — IdeologyProfile Batch
**Trigger:** Once (bootstrap) then when new major actor added to DB
**Status:** ✅ COMPLETE for 7 actors (Xi, MBS, Fink, Bessent, Huang, Gates, Altman)
**Pending:** Modi (DB ID TBD), Yellen (DB ID TBD) — seed after confirming PersonIds
**SQL ready:** `raw/ideology/ideology-seed-sql-2026-04-09.sql` — run in pgAdmin

**Next action:**
```sql
-- Find Modi and Yellen PersonIds
SELECT "Id", "Name", "LastName"
FROM public."Persons"
WHERE "Name" ILIKE '%Modi%'
   OR "Name" ILIKE '%Yellen%';
```
Then add 2 more INSERT blocks to the SQL file and run.

**Perplexity prompt (for future actors):**
```
For [PERSON NAME], based only on their PUBLIC record (speeches, decisions, policies):
Score each axis from -10 to +10:
EconScore (left/state = -10, right/market = +10)
AuthScore (liberal/democratic = -10, authoritarian = +10)
CulturalScore (progressive = -10, conservative = +10)
GenderScore (progressive = -10, traditional = +10)
GeoScore (isolationist = -10, multilateralist = +10)
EnvScore (climate activist = -10, deregulatory = +10)
ReligionScore (secular = -10, religious governance = +10)

Output:
=== FILENAME: raw/ideology/[lastname]-[firstname]-ideology-[YYYY-MM-DD].md ===
EconScore: [value]
AuthScore: [value]
CulturalScore: [value]
GenderScore: [value]
GeoScore: [value]
EnvScore: [value]
ReligionScore: [value]
LabelPrimary: [2-4 word label in English]
Confidence: [0-100]
Key evidence per axis: [one sentence each]
=== END ===
```

---

## OP-2 — Country Pages (6 Missing)
**Trigger:** Once (bootstrap)
**Status:** ✅ COMPLETE — France, Germany, India, Iran, Israel, Japan created
**Wiki paths:**
- wiki/countries/FRANCE.md ✅
- wiki/countries/GERMANY.md ✅
- wiki/countries/INDIA.md ✅
- wiki/countries/IRAN.md ✅
- wiki/countries/ISRAEL.md ✅
- wiki/countries/JAPAN.md ✅

**Next:** Confirm DB IDs for each country:
```sql
SELECT "Id", "Name" FROM public."Countries"
WHERE "Name" IN ('France','Germany','India','Iran','Israel','Japan')
ORDER BY "Name";
```
Update `db_id` in each country page frontmatter once confirmed.

**Perplexity prompt (for future countries):**
```
For [COUNTRY], provide an intelligence brief for the IMP Wiki using this format:

=== FILENAME: raw/geopolitics/[country-slug]-country-brief-[YYYY-MM-DD].md ===
# [Country] — Intelligence Brief [Date]
Source URLs: [list]

## Strategic Summary
[2-3 sentences: global role, why it matters for geopolitics and markets]

## Power Scores (0-100 each)
FinancialScore: [value + 1 sentence justification]
MilitaryScore: [value + 1 sentence justification]
SoftwareScore: [value + 1 sentence justification]
CommodityScore: [value + 1 sentence justification]
PoliticalScore: [value + 1 sentence justification]
InformationScore: [value + 1 sentence justification]
PowerArchetype: [FINANCIAL|POLITICAL|COERCIVE|INDUSTRIAL|TECHNOLOGICAL|HYBRID]

## Key Actors (top 3)
## Domestic Pressures (top 3)
## External Alignments
## Sanctions and Legal Constraints
## Narrative Trajectory (current — what changed in last 6 months)
## Market Relevance (FX, key exports, commodity exposure, IMP signals)
=== END ===
```

---

## OP-3 — TSMC Earnings + Jensen Huang
**Trigger:** Quarterly (after each TSMC earnings call)
**Status:** ⏳ PENDING — source needed from Perplexity/TSMC IR
**Next TSMC earnings:** ~April 2026 (Q1 2026 results)
**Source:** ir.tsmc.com/english/quarterly-results

**Perplexity prompt:**
```
Summarize the most recent TSMC earnings call (Q1 2026 or latest available).
Focus on: revenue guidance, AI/HPC demand signal, CoWoS capacity, N2/N3 node
progress, Arizona/Japan fab status, China revenue and export control impact,
management narrative shift vs prior quarter.

=== FILENAME: raw/transcripts/tsmc-earnings-[YYYY-MM-DD].md ===
# TSMC Earnings — [Quarter] [Year]
Date: [date]
Source URLs: [list]

## Revenue + Guidance
## AI/HPC Demand Signal
## Technology Nodes (N3/N2 status)
## CoWoS Packaging Capacity
## Geographic Fab Progress (Arizona, Japan)
## China Revenue + Export Controls
## Management Narrative Shift vs Prior Quarter
=== END ===
```

**Ingest targets (run after Perplexity output):**
- Update `wiki/institutions/TSMC.md` → Current Assessment + Narrative Shift
- Update `wiki/actors/HUANG-Jensen.md` → Key Recent Actions
- Update `wiki/themes/AI-Supply-Chain-Export-Controls.md` → current capacity data
- Append to `wiki/timelines/AI-Tech-Decoupling-2019-2026.md` if new milestone

**Say to Claude:** `ingest raw/transcripts/tsmc-earnings-[date].md`

---

## OP-4 — BIS Quarterly Review
**Trigger:** Quarterly (March, June, September, December)
**Status:** ⏳ PENDING — source needed
**Source:** bis.org/publ/qtrpdf/index.htm (March 2026 edition)

**Perplexity prompt:**
```
Summarize the BIS Quarterly Review most recent edition (March 2026 or latest).
Focus on: global financial conditions, dollar system health, credit/leverage warnings,
cross-border capital flows, EM vulnerabilities, key quotes from Overview.

=== FILENAME: raw/institutions/bis-quarterly-[YYYY-MM-DD].md ===
# BIS Quarterly Review — [Date]
Source URLs: [list]

## Global Financial Conditions
## Dollar System Health
[USD reserves share, SWIFT, de-dollarization evidence or absence]
## Credit and Leverage Warnings
## Cross-Border Capital Flows
## EM Vulnerabilities
## Key Quotes from Overview (paraphrased)
=== END ===
```

**Ingest targets:**
- Update `wiki/themes/Monetary-Policy-Weaponized-World.md` → dollar system data
- Update `wiki/themes/Geoeconomic-Fragmentation.md` → fragmentation evidence
- Update `wiki/narratives/Global-Macro-Regime-2026-04.md` if major shift
- Flag DSI inputs: USD reserves share, gold data → DB sync for CentralBankReserves

**Say to Claude:** `ingest raw/institutions/bis-quarterly-[date].md`

---

## OP-5 — Weekly Refresh (every Monday)
**Trigger:** Weekly — Monday morning
**Status:** 🔄 RECURRING
**Covers:** Powell/Fed, Lagarde/ECB, Chokepoints

**Perplexity prompt (copy entire block):**
```
Run IMP Wiki Weekly Intelligence Refresh — [today's date]

SUBTASK A — Powell/Fed
Search: Fed statements, speeches, FOMC communications in last 7 days.
=== FILENAME: raw/transcripts/powell-weekly-[YYYY-MM-DD].md ===
# Powell/Fed — Weekly Update [Date]
Source URLs: [list]
## Event this week? [Yes/No + what]
## Change vs prior week [new language, emphasis, omissions]
## Key claims (paraphrased, only if new)
## Narrative shift signal [Yes/No + what would change in POWELL-Jerome.md]
=== END ===

SUBTASK B — Lagarde/ECB
Search: Lagarde speeches, ECB communications in last 7 days.
=== FILENAME: raw/central-banks/lagarde-weekly-[YYYY-MM-DD].md ===
[Same structure as Subtask A]
=== END ===

SUBTASK C — Chokepoints
Search: Hormuz, Bab el-Mandeb/Red Sea, Taiwan Strait, Suez incidents last 7 days.
=== FILENAME: raw/geopolitics/chokepoints-weekly-[YYYY-MM-DD].md ===
# Chokepoints — Weekly Update [Date]
Source URLs: [list]
## Incidents this week [by chokepoint — Yes/No + description if Yes]
## Threat level changes
| Chokepoint | Prior | Current | Reason |
|---|---|---|---|
| Hormuz | 7 | ? | |
| Bab el-Mandeb | 8 | ? | |
| Taiwan Strait | 6 | ? | |
| Suez | 5 | ? | |
| Malacca | 5 | ? | |
## DB Sync Needed? [Yes/No — which table]
=== END ===
```

**Ingest targets (run after Perplexity output):**
- `wiki/actors/POWELL-Jerome.md` → Current Assessment + Narrative Shift if changed
- `wiki/actors/LAGARDE-Christine.md` → same
- `wiki/themes/Chokepoint-Intelligence.md` → threat scores table
- `wiki/themes/Energy-Chokepoints-War.md` → Core Chokepoints table
- `wiki/timelines/Global-Energy-Shipping-2019-2026.md` → append if incident

**Say to Claude:** `ingest weekly batch [date]` — I process all 3 files in one pass.

---

## SCHEDULE

| Day | Operation | Frequency |
|-----|-----------|-----------|
| Monday | OP-5 Weekly Refresh (Powell + Lagarde + Chokepoints) | Weekly |
| After TSMC earnings | OP-3 TSMC + Huang | Quarterly |
| After BIS release | OP-4 BIS Quarterly | Quarterly |
| When new actor added to DB | OP-1 IdeologyProfile | On-demand |
| When new country needed | OP-2 Country Page | On-demand |

---

## CURRENT OPEN FLAGS

| Flag | Description | Action |
|------|-------------|--------|
| CL-DB-003 | Bab el-Mandeb threat score outdated in DB | Run `UPDATE public."CommodityChokepoint" SET "ClosureRiskScore"=8 WHERE "Name" ILIKE '%Bab%'` |
| CL-DB-004 | BlackRock Owns edges missing | Seed RelationEdge rows — SQL pending |
| CL-DB-005 | Semiconductor PowerMap edges empty | Run PowerMapRelation introspection first |
| CL-DB-006 | IdeologyProfile: Modi + Yellen DB IDs TBD | `SELECT Id FROM Persons WHERE Name ILIKE '%Modi%'` |
| CL-DB-007 | 6 new country pages — DB IDs need confirmation | `SELECT Id, Name FROM Countries WHERE Name IN (...)` |

---

*IMP Wiki · Mission Pack Weekly Ops v1.0 · 2026-04-09*
