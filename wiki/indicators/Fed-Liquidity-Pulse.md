---
title: Fed Liquidity Pulse
slug: fed-liquidity-pulse
type: indicator
domain: financial
scope: institution
region: global
tags: [fed, liquidity, balance-sheet, qt, qe, money-supply, dollar]
created: 2026-04-10
updated: 2026-04-10
confidence: medium
sources:
  - raw/transcripts/powell-fomc-2026-04.md
related_actors: [jerome-powell, scott-bessent]
related_countries: [united-states]
related_institutions: [federal-reserve, wall-street]
related_commodities: [bitcoin]
related_themes: [monetary-policy-weaponized-world, dollar-dominance, bitcoin-macro-regime]
---

# Fed Liquidity Pulse

## Definition
A composite indicator measuring the net liquidity that the Federal Reserve is injecting into or draining from the financial system. Positive = liquidity expansion (QE, low rates, facility usage). Negative = liquidity contraction (QT, rate hikes, facility wind-down).

## Rationale
The Fed balance sheet is the root of global dollar liquidity. When the Fed expands it (QE), dollars flow into every risk asset globally — equities, credit, EM, crypto. When it contracts (QT), global dollar funding tightens. This indicator is the primary driver of IMP Bitcoin Macro Regime (A/B/C) and feeds directly into the DSI (Dollar System Index).

## Inputs

| Input | Source | Frequency | Weight |
|-------|--------|-----------|--------|
| Fed total assets (weekly change) | Fed H.4.1 release | Weekly | 40% |
| Overnight Reverse Repo (RRP) balance | NY Fed | Daily | 20% |
| Treasury General Account (TGA) | US Treasury | Daily | 15% |
| BTFP / facility usage | Fed | Weekly | 10% |
| Real Fed Funds Rate (FFR minus PCE) | FRED | Monthly | 15% |

## Calculation Logic
```
Net Liquidity = Fed Assets Δ - TGA Δ - RRP Δ + Facility Usage

Pulse Score (−10 to +10):
  > +5  = Strong QE / crisis injection
  +2 to +5 = Mild expansion
  −2 to +2 = Neutral / maintenance
  −5 to −2 = Mild QT / tightening
  < −5  = Aggressive QT / contraction
```

## Interpretation

**Score > +3 (Expansion):**
- Fed is net adding dollars to system
- Risk assets bid: equities, credit, EM, Bitcoin
- Dollar tends to weaken
- IMP Bitcoin Bias: overweight
- IMP Macro Regime: Regime A (liquidity-on)

**Score −3 to +3 (Neutral):**
- Fed holding steady — monitor for direction change
- Markets range-bound
- IMP Bitcoin Bias: neutral/monitor

**Score < −3 (Contraction):**
- Fed is net draining dollars from system
- Risk assets under pressure
- Dollar tends to strengthen
- IMP Bitcoin Bias: underweight
- IMP Macro Regime: Regime B (liquidity-off)

## Current State (April 2026)
- Fed total assets: ~$7.0T (down from $9T peak 2022) — ongoing QT
- RRP: declining (from $2.5T peak to ~$400B) — liquidity gradually returning
- TGA: ~$700B — neutral
- Real FFR: ~2.5% (4.5% FFR - 2.0% inflation) — restrictive
- **Estimated Pulse Score: −3 to −4 (mild-moderate contraction)**
- **IMP Regime: B (liquidity-off)**

**What changes it:**
- Fed signals rate cut → real FFR falls → Pulse moves toward neutral/positive
- QT ends / balance sheet stabilises → Pulse improves
- New crisis facility launched → Pulse spikes positive temporarily

## Maintenance Rules
- Update monthly from FRED data (H.4.1 release every Thursday)
- OP-5 weekly refresh monitors narrative shift signals from Powell
- Flag when Pulse crosses ±3 threshold — regime change signal
- DB target: `CompositeRiskIndex` table with IndexCode = custom or new "FLP" code

## Sources
- [[../actors/POWELL-Jerome]]
- [[../institutions/FEDERAL-RESERVE]]
- [[../themes/Monetary-Policy-Weaponized-World]]
- [[../themes/Bitcoin-Macro-Regime]]
