---
title: Summary - IPM Session Record 2026-03-27
slug: session-record-2026-03-27
type: source-summary
source-path: raw/internal-notes/IPM_Session_Record_2026_03_27.md
created: 2026-04-09
updated: 2026-04-09
confidence: high
sources:
  - raw/internal-notes/IPM_Session_Record_2026_03_27.md
related_actors: [larry-fink, elon-musk, jensen-huang, vladimir-putin, xi-jinping, jerome-powell, christine-lagarde, sam-altman, donald-trump, jamie-dimon]
related_countries: [united-states, china, russia, ukraine, taiwan, saudi-arabia, iran, pakistan]
related_institutions: [federal-reserve, ecb, blackrock]
related_commodities: [oil]
related_themes: [imp-platform-architecture, imp-power-index-system, imp-automation-engine, chokepoint-intelligence, semiconductor-supply-chain]
---

# Summary — IPM Session Record 2026-03-27

## Source
`raw/internal-notes/IPM_Session_Record_2026_03_27.md` — Build session record prepared by Claudio. Documents what was built on 2026-03-27, intelligence order queue state, new product ideas, and pending tasks.

## Main Takeaways
- 10 new DB tables seeded or created in this session including MilitaryCapacity (18 rows), InformationPowerScore (8 rows), CommodityChokepoint (7 rows), PersonPowerIndex (8 rows)
- Hormuz threat score = 10 (IRGC closure confirmed). Taiwan Strait = 8, GDP impact 4.5%
- 5 new DB views live: PowerMapIntelligence v2, OilImpactRanking, GlobalPowerRanking, ChokepointRiskSummary, IndexLatest
- IntelligenceOrder queue established — 4 complete, 6 pending as of session date
- 6 Claudio-authored timelines seeded across 2 PowerMaps (Semiconductor + Financial)
- 7 major product ideas generated: Aladdin chokepoint node, Power Dossier, Power Velocity, igreedmap.com, Celonis partnership, DSI as product, domain strategy

## Key Claims
- Aladdin manages risk for $21.6T across 200+ institutions — SoftwareDependencyScore=98, SubstitutionLatencyMonths=120, IsChokepoint=TRUE
- AIRLINES sector OilSensitivityScore = -88, OIL_GAS = +92 (most extreme in 18-sector model)
- Pakistan: 170 nuclear warheads. Ukraine defense budget: $64.7B = 34% of GDP
- PersonPowerIndex seeded: Fink(72), Musk(74), Huang(68), Putin(81), Xi(79), Powell(62), Lagarde(58), Altman(55)
- PowerMapRelation table: EMPTY — wiring canonical edges to PowerMapNode is next seeding step
- Trump, MBS, Bessent PersonPowerIndex: NOT YET SEEDED as of session date

## Countries Most Affected
USA, China, Russia, Ukraine, Taiwan, Saudi Arabia, Iran, Pakistan

## DB Sync Notes
- Source IS the DB state record — no sync needed
- Pending seeds documented in timelines/IMP-DB-State-Timeline.md

## Notes
- Source type: internal session record (priority tier 7 — treat as ground truth for DB state, not external intelligence)
- Prepared by Claudio (AI system user 00000000-0000-0000-0000-000000000002)
