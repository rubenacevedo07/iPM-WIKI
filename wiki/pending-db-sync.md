---
title: Pending DB Sync — Open Flags
slug: pending-db-sync
type: reference
region: global
tags: [imp-internal, db-sync, pending, postgresql]
created: 2026-04-09
updated: 2026-04-21
confidence: high
sources: []
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: []
---

# Pending DB Sync — Open Flags

*This file is the single source of truth for wiki→DB gaps.*
*Add flags here as they are raised. Mark CLOSED when confirmed live in DB.*
*Format: `CL-DB-NNN | entity/edge | description | raised | status`*
*Never delete closed entries — they are an audit trail.*

---

## Open Flags

| Flag | Entity / Edge | Description | Raised | Status |
|------|--------------|-------------|--------|--------|
| CL-DB-012 | PALANTIR (Company 96) | `db_id: TBD` fixed in wiki → verify Company row id=96 exists in DB. `SELECT id, name FROM "Companies" WHERE id = 96` | 2026-04-21 | OPEN |
| CL-DB-013 | Lockheed↔Northrop RelationEdges | Edge strength mismatch from companies/_sync_report.json dry-run: `Competes` wiki=High/db=Medium · `Partners` wiki=Medium/db=High — DB values are authoritative | 2026-04-19 | OPEN |
| CL-DB-014 | CIPS node + PBOC→CNY edge | CHINA.md Market Relevance now references CIPS (Cross-Border Interbank Payment System) and PBOC→Influences→CNY. Neither exists in DB. Seed: CIPS as Company node (institution_type: financial-infrastructure) + RelationEdge PBOC→Influences→CNY (Strength: Critical) | 2026-04-21 | OPEN |
| CL-DB-015 | BESSENT EstimatedWealthUsd | Key Square Group AUM and personal net worth not verified in Persons table for db_id=545. Wiki assessment: ~$700M–$1B net worth. Verify or seed EstimatedWealthUsd | 2026-04-21 | OPEN |
| CL-DB-016 | ASML RelationEdges | Seed: ASML→Supplies→Samsung (Strength: High) + ASML→DependsOn→Carl Zeiss (Strength: Critical). Carl Zeiss Meditec is in DB as subsidiary — verify parent company node exists | 2026-04-21 | OPEN |
| CL-DB-017 | Rheinmetall Company node | Seed Rheinmetall AG as Company node. Ticker='RHM.DE', NodeType='Company', SystemicImportanceLevel='High'. RelationEdges: Rheinmetall→Supplies→Germany, Rheinmetall→Partners→Ukraine | 2026-04-21 | OPEN |
| CL-DB-018 | Airbus Company node | Seed Airbus SE as Company node. Ticker='AIR.PA', NodeType='Company', SystemicImportanceLevel='High'. RelationEdges: Airbus→Supplies→France, Airbus→Supplies→Germany, Airbus→Competes→Lockheed Martin | 2026-04-21 | OPEN |
| CL-DB-019 | TotalEnergies Company node | Seed TotalEnergies SE as Company node. Ticker='TTE.PA', NodeType='Company', SystemicImportanceLevel='High'. RelationEdges: TotalEnergies→Exports→France, TotalEnergies→Partners→QatarEnergy, TotalEnergies→DependsOn→Hormuz | 2026-04-21 | OPEN |
| CL-DB-020 | Deutsche Bank Company node | Seed Deutsche Bank AG as Company node. Ticker='DBK.DE', NodeType='Company', SystemicImportanceLevel='Critical'. RelationEdges: Deutsche Bank→Finances→Germany, Deutsche Bank→Partners→ECB, Deutsche Bank→Competes→JPMorgan | 2026-04-21 | OPEN |
| CL-DB-021 | Volkswagen Group Company node | Seed Volkswagen AG as Company node. Ticker='VOW3.DE', NodeType='Company', SystemicImportanceLevel='High'. RelationEdges: VW→Manufactures→Germany, VW→Partners→SAIC, VW→DependsOn→China | 2026-04-21 | OPEN |
| CL-DB-022 | LVMH Company node + Arnault Person node | Seed LVMH Moët Hennessy Louis Vuitton SE as Company node. Ticker='MC.PA', NodeType='Company', SystemicImportanceLevel='High'. Also seed Bernard Arnault as Person node (PersonPowerIndex candidate, FINANCIAL archetype, est. rank 15-18). RelationEdges: Arnault→Owns→LVMH, LVMH→Exports→France, LVMH→DependsOn→China | 2026-04-21 | OPEN |
| CL-DB-023 | Peter Thiel — Person node | Seed Peter Thiel as Person node. PowerArchetype='FINANCIAL', EstimatedWealthUsd≈24000000000, Role='Founder/Investor'. SQL: `INSERT INTO "Persons" (name, "PowerArchetype", "EstimatedWealthUsd") VALUES ('Peter Thiel', 'FINANCIAL', 24000000000)` | 2026-04-22 | OPEN |
| CL-DB-024 | JD Vance — Person node | Seed JD Vance as Person node. PowerArchetype='POLITICAL', Role='Vice President of the United States'. SQL: `INSERT INTO "Persons" (name, "PowerArchetype", "Role") VALUES ('JD Vance', 'POLITICAL', 'Vice President')` | 2026-04-22 | OPEN |
| CL-DB-025 | AfD — Institution node | Seed Alternative für Deutschland as Company/institution node. NodeType='Company', SystemicImportanceLevel='Medium'. SQL: `INSERT INTO "Companies" (name, "NodeType", "SystemicImportanceLevel") VALUES ('Alternative für Deutschland', 'Company', 'Medium')` | 2026-04-22 | OPEN |
| CL-DB-026 | Thiel→Founded→Palantir RelationEdge | Edge: Thiel Person node → Palantir (id=96). Edge type: `Owns` (no 'Founded' enum yet — flag for enum extension). Strength: Critical. SQL pending Thiel Person node creation (CL-DB-023). | 2026-04-22 | OPEN |
| CL-DB-027 | Thiel→Finances→Vance RelationEdge | Edge: Thiel Person node → Vance Person node. Edge type: `Finances`, Strength: Critical ($15M Senate donation + Mar-a-Lago introduction). SQL pending both Person nodes (CL-DB-023, CL-DB-024). | 2026-04-22 | OPEN |
| CL-DB-028 | Palantir→Supplies→ICE RelationEdge | Edge: Palantir (id=96) → ICE. Edge type: `Supplies`, Strength: Critical. ImmigrationOS + $1B DHS contract. ICE Company node may need to be seeded first. SQL: `INSERT INTO "RelationEdge" ("SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified") VALUES ('Company',96,'Company',<ICE_id>,'Supplies','Critical','Palantir ImmigrationOS + $1B DHS contract',false)` | 2026-04-22 | OPEN |
| CL-DB-029 | Musk→Influences→AfD RelationEdge | Edge: Musk (id=7) → AfD Company node. Edge type: `Influences`, Strength: High. X Space endorsement + rally appearance + repeated X posts. SQL pending AfD node creation (CL-DB-025). | 2026-04-22 | OPEN |

---

## Closed Flags (audit trail)

| Flag | Entity / Edge | Description | Raised | Closed |
|------|--------------|-------------|--------|--------|
| CL-DB-001 | Trump↔Powell IdeologyProfile divergence | DSI signal data needed | 2026-04-09 | 2026-04-09 |
| CL-DB-002 | Powell↔Lagarde IdeologyProfile divergence | EUR/USD signal data | 2026-04-09 | 2026-04-09 |
| CL-DB-003 | Bab el-Mandeb CommodityChokepoint score | Update to 8 (Houthi elevation) | 2026-04-09 | 2026-04-10 |
| CL-DB-004 | BlackRock Owns edges | 10 RelationEdge INSERTs (RE 1285-1294) | 2026-04-09 | 2026-04-10 |
| CL-DB-005 | Semiconductor PowerMapRelation | 5 edges (ASML→TSMC, NVIDIA→Taiwan, Jensen→NVIDIA, Chang→TSMC, TSMC→Apple) | 2026-04-09 | 2026-04-09 |
| CL-DB-006 | IdeologyProfile 12 actors | SQL seeded for Xi, MBS, Fink, Bessent, Huang, Gates, Altman, Lagarde, Putin, Trump, Musk, Powell | 2026-04-09 | 2026-04-10 |
| CL-DB-007 | 6 country DB IDs | France=30, Germany=29, India=140, Iran=72, Israel=74, Japan=149 confirmed | 2026-04-09 | 2026-04-10 |
| CL-DB-008 | AI supply chain companies | Palantir=96, AMD=69, Arm=248, xAI=199 seeded | 2026-04-09 | 2026-04-10 |
| CL-DB-009 | AI supply chain edges | RE 1257-1271 (18 edges) confirmed live | 2026-04-09 | 2026-04-10 |
| CL-DB-010 | Commodity links | 315 CompanyCommodities + 22 CommodityFacility rows | 2026-04-09 | 2026-04-10 |
| CL-DB-011 | Institution RelationEdges | RE 1272-1284 (13 edges) confirmed live | 2026-04-09 | 2026-04-10 |

---

## How to Use This File

**When raising a new flag (wiki → DB):**
1. Add row to Open Flags table with next sequential CL-DB-NNN
2. Include the exact SQL check or INSERT needed where possible
3. Add `DB SYNC NEEDED: CL-DB-NNN` comment in the affected wiki page's `## DB Sync Notes` section
4. Log the flag in `wiki/log.md` under the relevant operation entry

**When closing a flag (DB confirmed):**
1. Move row from Open Flags to Closed Flags
2. Update the affected wiki page's `## DB Sync Notes` to show ✅
3. Add a `db-sync` log entry in `wiki/log.md`

**SQL patterns:**
```sql
-- Verify Company row
SELECT id, name, "NodeType" FROM "Companies" WHERE id = <id>;

-- Seed new Company
INSERT INTO "Companies" (name, "NodeType", "Ticker", "SystemicImportanceLevel")
VALUES ('CIPS', 'Company', NULL, 'Critical');

-- Seed RelationEdge
INSERT INTO "RelationEdge" ("FromEntityId", "ToEntityId", "FromEntityType", "ToEntityType", "RelationType", "Strength")
VALUES (<from_id>, <to_id>, 'Company', 'Country', 'Influences', 'Critical');
```
