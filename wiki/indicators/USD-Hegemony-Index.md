---
title: USD Hegemony Index
slug: usd-hegemony-index
type: indicator
domain: financial
scope: global
region: global
tags: [dollar, usd, reserves, swift, de-dollarization, dsi, hegemony]
created: 2026-04-10
updated: 2026-04-10
confidence: medium
sources:
  - raw/institutions/imf-weo-2026-04.md
  - raw/geopolitics/trump-trade-policy-2026-04.md
  - raw/sanctions/russia-oil-2026-04.md
related_actors: [jerome-powell, scott-bessent, donald-trump, janet-yellen]
related_countries: [united-states, china, russia, saudi-arabia]
related_institutions: [federal-reserve, us-treasury, wall-street]
related_commodities: [oil, bitcoin]
related_themes: [dollar-dominance, de-dollarization, monetary-policy-weaponized-world, geoeconomic-fragmentation]
---

# USD Hegemony Index

## Definition
Composite measure of the US dollar's structural dominance in the global monetary system. Tracks four dimensions: reserve currency share, trade invoicing share, financial system centrality, and weaponisation risk. High score = dollar dominance intact. Low/falling score = de-dollarization pressure building.

## Rationale
The dollar's reserve status is the foundation of US financial power — it allows the US to run persistent deficits, impose financial sanctions, and set global monetary conditions via the Fed. IMP's DSI (Dollar System Index) feeds from this indicator. Structural decline here is a slow-moving but irreversible threat to US power projection.

## Inputs

| Input | Source | Frequency | Weight |
|-------|--------|-----------|--------|
| USD share of global FX reserves (COFER) | IMF quarterly | Quarterly | 35% |
| USD share of global trade invoicing | BIS/IMF | Annual | 20% |
| SWIFT USD payment share | SWIFT | Monthly | 15% |
| DXY (trade-weighted dollar) normalised | FRED | Daily | 15% |
| USD funding spread (cross-currency basis) | Bloomberg/BIS | Daily | 15% |

## Calculation Logic
```
USD Hegemony Score (0-100):
  90-100 = Unchallenged dominance (Cold War peak)
  75-89  = Strong dominance with emerging alternatives
  60-74  = Moderate dominance — structural erosion visible
  45-59  = Contested reserve status — multipolar transition
  < 45   = Post-hegemony / multipolar monetary system
```

## Current State (April 2026)

| Input | Value | Trend |
|-------|-------|-------|
| USD FX reserves share | ~58% | ↓ (was 72% in 2000) |
| USD trade invoicing | ~54% | ↓ slowly |
| SWIFT USD share | ~42% | Stable |
| DXY | Elevated | ↑ (Fed hawkish) |
| USD funding spreads | Moderate | Stable |

**Estimated Score: ~72/100** — Strong dominance with visible structural erosion.

**Trend: gradual decline** — 15 percentage points lost in FX reserves share since 2000. Not collapse, but clear directionality.

## Threats to Dollar Dominance (ranked by IMP assessment)

**1. Weaponisation risk (HIGH — active)**
Trump GeoScore −4.0 (isolationist) + sanctions expansion = using dollar as weapon.
When adversaries face dollar exclusion, they accelerate alternatives (BRICS payment systems, CNY, gold, Bitcoin).
Russia oil in rubles/yuan post-2022 is the first major case.

**2. Fiscal sustainability (MEDIUM — building)**
US debt/GDP >120%. Bessent "3-3-3 plan" attempts stabilisation.
If bond market loses confidence → dollar reserve status at risk.
IMF WEO April 2026 flags US fiscal path as top risk.

**3. BRICS+ alternatives (LOW → MEDIUM)**
BRICS+ payment system in development. mBridge (China/UAE/Saudi). Gold accumulation.
Not near-term threat but structural trajectory.

**4. Bitcoin/crypto (VERY LONG-DATED)**
Censorship-resistant alternative store of value.
Relevant only in Regime C (monetary system stress).

## Interpretation for IMP Signals

| Score | IMP Signal | Bitcoin Regime | EUR/USD Bias |
|-------|-----------|----------------|--------------|
| >80 | Dollar dominance intact | Regime B (USD bid) | USD structural bid |
| 70-80 | Erosion visible, intact | Neutral | Neutral |
| 60-70 | Contested — monitor | Regime C emerging | EUR/BTC bid |
| <60 | Multipolar transition | Regime C active | USD structural sell |

## Maintenance Rules
- Update quarterly from IMF COFER data (released ~3 months after quarter end)
- Monthly SWIFT data update
- Flag when quarterly score moves >3 points — DSI update trigger
- Feeds into: DSI index, IMP Bitcoin Regime assessment, EUR/USD signal context

## Sources
- [[../actors/POWELL-Jerome]]
- [[../actors/BESSENT-Scott]]
- [[../actors/TRUMP-Donald]]
- [[../institutions/FEDERAL-RESERVE]]
- [[../institutions/US-TREASURY]]
- [[../themes/Monetary-Policy-Weaponized-World]]
- [[../comparisons/Powell-Lagarde-Divergence]]
