---
title: IMP DB State Timeline
slug: imp-db-state-timeline
type: timeline
created: 2026-04-09
updated: 2026-04-09
confidence: high
sources:
  - raw/internal-notes/IPM_Session_Record_2026_03_27.md
  - raw/internal-notes/IPM_Project_State_2026_04_01.md
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: [imp-platform-architecture, imp-power-index-system]
---

# IMP DB State Timeline

*Append-only record of DB state at key session dates. Used to track what exists vs what is pending.*

---

## 2026-03-27 — Session: Power Index Migration v1

### Tables seeded / created this session

| Table | Rows | Key Data |
|-------|------|----------|
| MilitaryCapacity | 18 | USA through Brazil. Pakistan 170 warheads. Ukraine $64.7B (34% GDP). |
| InformationPowerScore | 8 | USA, China, Russia, UK, France, PRK, Iran, Saudi |
| CommodityChokepoint | 7 | Hormuz=10 (IRGC closure confirmed). Taiwan Strait=8, GDP impact 4.5% |
| PersonPowerIndex | 8 | Fink(72), Musk(74), Huang(68), Putin(81), Xi(79), Powell(62), Lagarde(58), Altman(55) |
| EdgeRiskScore | 0 | Table exists. Feeds from Polymarket Phase 3 |
| ScenarioCascade | 1 | Oil $150 / Hormuz closure seeded |
| CompositeRiskIndex | 0 | Table exists. Feeds from computation engine |
| PowerMapNode | ~60 | 5 maps seeded with real entity IDs |
| PowerMapRelation | 0 | Table created. EMPTY — wiring canonical edges pending |
| IntelligenceOrder | 10 | 4 COMPLETE, 6 PENDING |

### New fields added to existing tables
- `Sector.OilSensitivityScore` — 18 sectors (AIRLINES -88, OIL_GAS +92)
- `Companies.IsChokepoint`, `SoftwareDependencyScore`, `DefenseRevenuePercent`
- `Countries.NuclearWarheads`, `DefenseBudgetUsd`, `VetoPowerScore`, `CyberCapacityScore`
- `Persons.ArchetypeCode` — 19 persons assigned

### Views live after this session
- PowerMapIntelligence v2
- OilImpactRanking
- GlobalPowerRanking
- ChokepointRiskSummary
- IndexLatest

### Seed data added
- 6 Claudio timelines across 2 PowerMaps (Semiconductor + Financial)
- 6 PX newsevents (Hormuz closure, Russia offensive, Fed hold, ECB hold, Russia sanctions, China fertilizer)
- 27 CentralBankReserves rows (gold + COFER + TIC data)
- 4 AI system users seeded (imp_system, Claudio, PX, Base44)

### PowerMap IDs confirmed
- 1 = Technology Infrastructure
- 2 = Financial
- 3 = Technology Infrastructure (duplicate — flag)
- 4 = Semiconductor
- 5 = Energy
- 6 = Defense

---

## Pending Seeds as of 2026-03-27

- PersonPowerIndex: Trump (POLITICAL, 76), MBS (COERCIVE, CPI 78), Bessent (FINANCIAL)
- IdeologyProfiles: Fink, Xi Jinping, MBS
- ScenarioCascade templates: 1994 bond crash, 2008 Lehman, 2020 COVID
- PowerMapRelation edges — wire canonical RelationEdge IDs to PowerMapNode for 5 maps
- Financial map timelines: Trump, JPMorgan, Dimon (0 open timelines — CL-002 pending)
- Aladdin Company node: IsChokepoint=TRUE, SoftwareDependencyScore=98, SubstitutionLatencyMonths=120

---

## Intelligence Order Queue State as of 2026-03-27

| Code | Agent | Priority | Status | Task |
|------|-------|----------|--------|------|
| PX-001 | PX | 1 | ✅ COMPLETE | IMF COFER + US Treasury TIC data |
| PX-002 | PX | 2 | ✅ COMPLETE | Military budgets 8 countries (SIPRI 2025) |
| CL-001 | CLAUDIO | 3 | ✅ COMPLETE | Financial map timelines |
| B44-001 | BASE44 | 2 | ✅ COMPLETE | Gold reserves patch (China +45t, India +26.57t) |
| PX-003 | PX | 2 | ⏳ PENDING | Oracle feed — analyst predictions last 14 days |
| B44-002 | BASE44 | 3 | ⏳ PENDING | ChokepointRiskPanel React component |
| CL-002 | CLAUDIO | 3 | ⏳ PENDING | Financial map timelines Trump/JPMorgan/Dimon |
| PX-004 | PX | 3 | ⏳ PENDING | PersonPowerIndex inputs: Trump, MBS, Bessent |
| PX-005 | PX | 3 | ⏳ PENDING | Chokepoint risk refresh post-Hormuz |
| B44-003 | BASE44 | 4 | ⏳ PENDING | GlobalPowerRankingCard React component |
| PX-006 | PX | 4 | ⏳ PENDING | InformationPowerScore RSF 2025/2026 |

---

## 2026-04-01 — Full Project State Audit

### DB Row Counts (verified)

| Table | Rows | Status |
|-------|------|--------|
| Persons | 545 | Good |
| Companies | 239 | Good |
| Countries | 171 | Complete |
| RelationEdge | 1,246+ | Good |
| PersonPowerIndex | 14 | ✅ Clean — ranks fixed |
| PowerMap | 10 | Seeded |
| PowerMapNode | 79 | Seeded |
| EdgeRiskScore | 31 | Thin |
| TimelineEntity | 51 | Active |
| AnalystPrediction | 3 | Hollow — Oracle not live |
| CompositeIndexSnapshots | 0 | ⚠️ B-04 — job not working |
| PersonVision | 0 | PX-007 pending |
| TradingSystem | 4 | Seeded |

### Stack confirmed
- Backend: ASP.NET Core 8, 43+ controllers, ~155 endpoints
- DB: PostgreSQL (Railway), 116 tables, 18+ views
- Frontend IPM: React 19 + TypeScript + Vite + DeckGL
- Frontend Sherman: React 18 + TypeScript + Vite + Recharts
- Auth: JWT + BCrypt + refresh tokens + Google OAuth — ✅ LIVE
- Automation: n8n self-hosted Docker port 5678, Python FastAPI sidecar port 8001
- Payments: Stripe — NOT YET IMPLEMENTED

### PersonPowerIndex — Final Ranking (14 rows)

| Rank | Name | Archetype | Composite | DB ID |
|------|------|-----------|-----------|-------|
| 1 | Donald Trump | POLITICAL | 76.00 | 173 |
| 2 | Xi Jinping | POLITICAL | 79.00 | 171 |
| 3 | Vladimir Putin | COERCIVE | 81.00 | 172 |
| 4 | Elon Musk | HYBRID | 74.00 | 7 |
| 5 | Larry Fink | FINANCIAL | 72.00 | 75 |
| 6 | Mohammed bin Salman | COERCIVE | 78.00 | 176 |
| 7 | Jensen Huang | TECHNOLOGICAL | 68.00 | 1 |
| 8 | Bill Gates | FINANCIAL | 71.00 | 67 |
| 9 | Narendra Modi | POLITICAL | 64.00 | TBD |
| 10 | Jerome Powell | POLITICAL | 62.00 | 192 |
| 11 | Christine Lagarde | POLITICAL | 58.00 | 191 |
| 12 | Scott Bessent | FINANCIAL | 58.00 | 545 |
| 13 | Sam Altman | TECHNOLOGICAL | 55.00 | 61 |
| 14 | Janet Yellen | FINANCIAL | 48.00 | TBD |

### New Entity IDs confirmed this session
- MBS (Mohammed bin Salman): **176**
- Scott Bessent: **545**
- Modi: TBD
- Yellen: TBD

### GraphEdgeWithTimelines — Top Edges by Timeline Count
- Dimon→USA: **9** open timelines (highest in platform)
- Samsung→USA: **8**
- TSMC→USA: **8**
- Trump→USA: **7**
- Total edges: 2,669 | Edges with timelines: 324

### Open Blockers as of 2026-04-01

| ID | Description | Status |
|----|-------------|--------|
| B-01 | BillingController + Stripe | In progress |
| B-02 | Auth frontend + backend | ✅ COMPLETE |
| B-03 | PersonPowerIndex seeding | ✅ COMPLETE — 14 rows |
| B-04 | CompositeIndexSnapshots snapshot job | ⚠️ 500 error |
| B-05 | IBKR TWS integration for Sherman | Not started |
| B-06 | Alpha Vantage n8n automation | Not started |

### C# vs DB Column Name Map (critical — never confuse)
| C# Property | DB Column |
|-------------|-----------|
| FPI | FinancialScore |
| MPI | MilitaryScore |
| SPI | SoftwareScore |
| CPI | CommodityScore |
| PPI | PoliticalScore |
| IPI | InformationScore |
| ReachMetricA | EstimatedAumUsd |
| ReachMetricB | EstimatedPopulationGoverned |
| ReachMetricC | EstimatedGdpControlledUsd |
| ReachMetricD | EstimatedEmployeesReached |

### Intelligence Orders — PENDING as of 2026-04-01
- PX-004 — Trump/MBS/Bessent power inputs
- PX-005 — Chokepoint refresh
- PX-006 — RSF press freedom
- PX-007 — Vision Collection top 20 persons
- B44-002 — ChokepointRiskPanel component
- CL-002 — Financial map timelines Trump/JPMorgan/Dimon

### Pending Seeds as of 2026-04-01
- IdeologyProfiles: Xi, MBS, Fink
- ScenarioCascade templates: 1994 bond crash, 2008 Lehman, 2020 COVID
- PowerMapRelation edges for 5 maps
- Aladdin node (IsChokepoint=TRUE, SoftwareDependencyScore=98, SubstitutionLatencyMonths=120, InfluenceScore=99)
- PersonVision for top 20 (PX-007)

---

## 2026-04-02 — Session: Migration 0007 + Controller Consolidation

### Work completed
- Migration 0007 applied cleanly to Railway PostgreSQL — all tables/columns confirmed
- C# models updated — `Persons` model uses `Name` + `LastName` (no single Name field)
- Controllers wired to new models — no regressions on existing controllers
- React Router verified: 48 routes, 0 TS errors
- All 8 verification checks passed

### File state checkpoint
- `iPM_Welcome_V1 (2).html`: production-ready, login form insertion point identified
- PersonPowerIndex: 14 rows clean (unchanged from 2026-04-01)
- BillingController: open stub — Stripe keys not yet connected

### Open items carried forward
- 🔴 Login form integration into welcome screen
- 🔴 BillingController + Stripe
- 🟡 CL-002: Financial map timelines Trump/JPMorgan/Dimon
- 🟡 PX-004: Trump/MBS/Bessent power inputs
- 🟢 Aladdin node SQL
- 🟢 Power Dossier component
