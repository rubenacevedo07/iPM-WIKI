---
title: US Military Projection Power
slug: us-military-projection
type: indicator
domain: coercive
scope: country
region: global
tags: [military, pentagon, coercive, nato, chokepoints, budget, nuclear]
created: 2026-04-10
updated: 2026-04-10
confidence: medium
sources:
  - raw/geopolitics/chokepoint-risk-2026-04.md
related_actors: [donald-trump, scott-bessent]
related_countries: [united-states, ukraine, taiwan, russia, china]
related_institutions: [pentagon, lockheed-martin]
related_commodities: [oil]
related_themes: [energy-chokepoints-war, geoeconomic-fragmentation]
---

# US Military Projection Power

## Definition
Composite measure of US ability to project coercive military power globally — not just domestic defence capability but the capacity to intervene, deter, and enforce at any point on the IMP map. High score = global hegemony. Declining score = multipolar military competition.

## Rationale
The Pentagon's power projection capability is what gives the dollar its ultimate backstop — "dollar hegemony at gunpoint" is a real structural relationship. US control of maritime chokepoints (carrier strike groups), nuclear deterrence, and alliance network (NATO/QUAD) define the ceiling for how much geopolitical risk the world can actually price before the US military intervenes. When this score declines, chokepoint risk scores structurally rise.

## Inputs

| Input | Source | Frequency | Weight |
|-------|--------|-----------|--------|
| Defense budget (% global total) | SIPRI | Annual | 25% |
| Carrier strike groups operational | USN | Monthly | 15% |
| Overseas basing footprint (countries) | DoD | Annual | 15% |
| Nuclear warhead superiority index | SIPRI/Arms Control | Annual | 20% |
| Alliance commitments active (NATO+) | DoD/State | Annual | 10% |
| Active military deployments | DoD | Monthly | 15% |

## Calculation Logic
```
Projection Score (0-100):
  90-100 = Unchallenged unipolar dominance (1991-2001)
  75-89  = Strong dominant with rising challengers
  65-74  = Contested — China/Russia closing capability gap
  50-64  = Multipolar military competition
  < 50   = US relative decline — regional powers fill vacuum
```

## Current State (April 2026)

| Input | Value | Trend |
|-------|-------|-------|
| Defense budget | $858B (~40% global) | ↑ nominally, ↓ as % GDP |
| Carrier strike groups | 11 operational | Stable |
| Overseas bases | 750+ in 80 countries | ↓ (consolidation) |
| Nuclear warheads | ~5,500 (1,700 deployed) | Stable |
| Alliance commitments | NATO + QUAD + AUKUS | ↑ (expanding) |
| Active deployments | Ukraine (material), ME, Indo-Pacific | ↑ (high tempo) |

**Estimated Score: ~78/100** — Strong dominant but with visible stress indicators.

**Stress factors:**
- Two-front demand: Ukraine + Indo-Pacific + Middle East simultaneously
- Readiness costs: high operational tempo degrading equipment lifecycles
- Budget pressure: Bessent fiscal consolidation vs Pentagon budget expansion
- Recruitment shortfall: US military missed recruiting targets 2023-2024
- China capability catch-up: PLAN carrier programme, hypersonics, cyber

## Relationship to Chokepoint Scores

Pentagon projection power is the inverse of chokepoint risk:
- Pentagon strong → chokepoints held open → global trade flows → lower GCRI
- Pentagon weakening or distracted → chokepoint opportunism rises → Houthis, IRGC test limits

Current: Pentagon stretched but not retreating. Red Sea operation ongoing but limited effectiveness (Houthi attacks continue despite strikes). Taiwan deterrence credible but tested by PLA exercises. Score consistent with chokepoints at 6-8/10 rather than 3-4.

## Interpretation for IMP

| Score | IMP Effect |
|-------|-----------|
| >85 | Chokepoints held, dollar backstopped, low conflict premium |
| 70-85 | Current state — deterrence credible but not unchallenged |
| 55-70 | Chokepoint risk structurally elevated, GCRI high |
| <55 | Multipolar security vacuum — regional conflicts proliferate |

## Maintenance Rules
- Update annually from SIPRI data
- Monthly operational deployment tracking (major deployments)
- Flag when score moves >5 points — GCRI recalibration trigger
- Feeds into: GCRI, WPI (War/Peace Index), ChokepointRiskSummary view

## Sources
- [[../institutions/PENTAGON]]
- [[../institutions/LOCKHEED-MARTIN]]
- [[../actors/TRUMP-Donald]]
- [[../countries/UNITED-STATES]]
- [[../themes/Energy-Chokepoints-War]]
- [[../themes/Geoeconomic-Fragmentation]]
