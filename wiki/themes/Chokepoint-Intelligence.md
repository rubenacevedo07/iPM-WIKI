---
title: Chokepoint Intelligence
slug: chokepoint-intelligence
type: theme
region: global
tags: [chokepoints, supply-chain, geopolitics, commodities, military]
created: 2026-04-09
updated: 2026-04-09
confidence: high
sources:
  - raw/internal-notes/IPM_Session_Record_2026_03_27.md
related_actors: []
related_countries: [iran, china, russia, saudi-arabia, egypt, panama]
related_institutions: []
related_commodities: [oil, natural-gas, semiconductors]
related_themes: [semiconductor-supply-chain, energy-security, sanctions]
---

# Chokepoint Intelligence

## Summary
IMP models 7 geographic control points as `CommodityChokepoint` entities. Each has a threat score (0–10), GDP impact estimate, and a controlling military capacity. This is a core IMP data moat — sub-10-minute intelligence advantage on chokepoint risk events.

## The 7 IMP Chokepoints

| Chokepoint | Threat Score | Controller | Key Commodity | GDP Impact |
|---|---|---|---|---|
| **Hormuz** | 10 | Iran (IRGC) | Oil, LNG | ~3.5% global GDP |
| **Taiwan Strait** | 8 | China (PLA) | Semiconductors | 4.5% GDP impact |
| **Suez** | — | Egypt (military) | General trade | ~12% global trade |
| **Malacca** | — | Singapore/Malaysia/Indonesia | Oil, LNG, China trade | ~30% global trade |
| **Black Sea** | — | Russia/Ukraine conflict zone | Wheat, grain | EM food supply |
| **Bab el-Mandeb** | — | Yemen (Houthis) | Oil, container shipping | Red Sea routing |
| **Panama** | — | Panama (US influence) | Container shipping | US-Asia trade |

## Current Threat Scores (updated 2026-04-09)

| Chokepoint | Threat Score | Key Actor | Status |
|---|---|---|---|
| **Hormuz** | 7/10 | Iran (IRGC) | Elevated — no blockade but IRGC risk of incident |
| **Bab el-Mandeb** | 8/10 | Houthis (Yemen) | Highest active risk — shipping rerouting via Cape |
| **Taiwan Strait** | 6/10 | China (PLA) | Frequent exercises, grey-zone pressure elevated |
| **Suez** | 5/10 | Indirect (Red Sea) | Canal operational but approach routes risky |
| **Malacca** | 5/10 | No active crisis | Latent risk from US-China tension |

*Note: DB CommodityChokepoint table has Hormuz=10, Taiwan Strait=8 from March 2026 seed.
Wiki assessment April 2026 shows Bab el-Mandeb now at 8 — potential DB update needed.*

**DB SYNC NEEDED:** Update CommodityChokepoint Bab el-Mandeb threat score — Houthi campaign elevated this above Taiwan Strait in current risk assessment.

## Drivers
- Military capacity of controlling power
- Alternative routing feasibility (SubstitutionLatencyMonths)
- Commodity dependence of major economies
- Active conflict or coercive actor presence

## Market Impact
Hormuz closure → oil +$30–50/bbl → AIRLINES -88, OIL_GAS +92 (OilSensitivityScore).
Taiwan Strait blockade → semiconductor supply → NVIDIA, ASML, TSMC → global tech production.
Suez disruption → container shipping detour → shipping rates → global inflation.

## DB State
- CommodityChokepoint: 7 rows seeded
- ChokepointRiskSummary VIEW: live
- EdgeRiskScore: 0 rows (Polymarket integration Phase 3)
- PX-005 (chokepoint risk refresh): PENDING

## Related Pages
- [[../indicators/DB-ID-Reference.md]]
- [[../timelines/IMP-DB-State-Timeline.md]]

## Open Questions
- PX-005 execution: when does chokepoint risk refresh run?
- Bab el-Mandeb: Houthi campaign status and shipping rerouting impact?
- Taiwan Strait: current PLA naval exercise frequency vs baseline?
