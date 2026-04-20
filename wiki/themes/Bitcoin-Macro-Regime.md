---
title: Bitcoin Macro Regime
slug: bitcoin-macro-regime
type: theme
tags: [bitcoin, macro, liquidity, rates, risk-on, regime]
created: 2026-04-10
updated: 2026-04-10
confidence: medium
sources:
  - raw/transcripts/powell-fomc-2026-04.md
  - raw/institutions/imf-weo-2026-04.md
related_actors: [jerome-powell, christine-lagarde, larry-fink]
related_countries: [united-states]
related_institutions: [federal-reserve, blackrock]
related_commodities: [bitcoin]
related_themes: [monetary-policy-weaponized-world, dollar-dominance, energy-chokepoints-war]
---

# Bitcoin Macro Regime

*How Bitcoin behaves across IMP regime states. Used by Thread Master to gate BTC strategies.*

---

## The Three IMP Regimes for Bitcoin

### REGIME A — Liquidity ON (Bitcoin OVERWEIGHT)
**IMP signals:** Fed dovish or pivoting, real yields falling, M2 expanding, USD weakening, risk assets rallying.

**Bitcoin behaviour:** High beta risk-on outperformance. Institutional ETF inflows accelerate. Correlation with Nasdaq ~1.5-2.0x. Halving cycle tailwind compounds.

**IMP indicators:**
- Powell narrative: "data-dependent cuts" or "insurance cut" language
- EUR/USD signal: contracting (less USD dominance)
- GCRI: <60 (low geopolitical stress)
- Real 10Y yield: falling or negative

**Thread Master action:** `bitcoinBias: "overweight"` — michael-sailor-btc strategy ACTIVE

---

### REGIME B — Liquidity OFF (Bitcoin UNDERWEIGHT)
**IMP signals:** Fed hawkish, higher-for-longer, real yields rising, USD strengthening, risk-off, credit spreads widening.

**Bitcoin behaviour:** Underperforms vs cash and short-duration. Correlated with Nasdaq drawdown. ETF outflows. Leverage washouts = amplified downside.

**IMP indicators:**
- Powell narrative: "no hurry to cut", "inflation above target" (current — April 2026)
- EUR/USD signal: widening (USD bid)
- GCRI: N/A (liquidity = primary driver in this regime)
- Real 10Y yield: rising

**Thread Master action:** `bitcoinBias: "underweight"` — michael-sailor-btc strategy BLOCKED

**Current state (April 2026):** Fed held at 4.5-4.75%, higher-for-longer, inflation 2.7%. **REGIME B — Bitcoin underweight.**

---

### REGIME C — Monetary System Stress (Bitcoin MACRO HEDGE)
**IMP signals:** Dollar confidence erosion, sanctions weaponisation, capital controls, de-dollarization acceleration, sovereign debt crisis.

**Bitcoin behaviour:** Decouples from risk-on/off framework. Acts as censorship-resistant store of value. Demand from sanctioned actors, capital flight markets, sovereign diversifiers.

**IMP indicators:**
- DSI (Dollar System Index): deteriorating
- Trump GeoScore -4.0 (isolationism) + sanctions expansion = dollar weaponisation
- Emerging market capital controls or currency crises
- Central bank gold accumulation accelerating (China, Russia)
- Hormuz/Bab el-Mandeb at 8+ = energy system stress → dollar system stress

**Thread Master action:** `bitcoinBias: "macro-hedge"` — different strategy parameters (longer hold, lower leverage)

---

## Signal Matrix

| IMP Signal | Regime A (Long) | Regime B (Short/Flat) | Regime C (Hedge) |
|-----------|-----------------|----------------------|-----------------|
| Fed stance | Dovish/pivot | Hawkish/hold | Credibility crisis |
| Real yields | Falling | Rising | Negative real / USD dump |
| EUR/USD signal | Contracting | Widening | Breakdown |
| GCRI | <60 | Any | >80 + monetary stress |
| Chokepoints | Low | Any | 3+ at critical tier |
| DSI | Stable | Stable | Deteriorating |
| ETF flows | Inflows | Outflows | Inflows (flight) |

---

## How This Feeds Thread Master

```javascript
// Derived from wiki/themes/bitcoin-macro-regime.md
// Updated weekly via OP-5 refresh

const IMP_CONTEXT = {
  macroRegime: "liquidity-off",     // Regime B — April 2026
  bitcoinBias: "underweight",       // Fed hawkish, higher-for-longer
  chokepointRisk: 8,                // Bab el-Mandeb + Taiwan Strait
  dsiBias: "stable",                // No active dollar system stress
  source: "wiki/narratives/Global-Macro-Regime-2026-04.md"
};

// Compatibility rule — gates BTC strategy
{
  id: "btc-regime-gate",
  evaluate: (s, cfg) => {
    if (s.strategyId !== "michael-sailor-btc") return true;
    return IMP_CONTEXT.bitcoinBias === "overweight"
        || IMP_CONTEXT.bitcoinBias === "macro-hedge";
  },
  message: "Bitcoin strategy requires liquidity-on or macro-hedge IMP regime. Current: liquidity-off (Fed hawkish Apr 2026)."
}
```

---

## Historical Regime Examples

**2020-2021 (Regime A):** COVID QE → M2 expansion → Bitcoin 10x. Textbook liquidity-on.

**2022 (Regime B):** Fed 525bps hikes → real yields surge → Bitcoin -75% peak to trough. Textbook liquidity-off.

**2022 Russia sanctions (Regime C flash):** Ruble collapse → Russian capital flight to BTC. Brief macro-hedge bid within broader downtrend.

**2023-2024 (Regime A building):** ETF anticipation → institutional demand → halving April 2024 → Bitcoin ATH $73K. Fed pivot narrative drove regime.

**2025-2026 (Regime B):** Higher-for-longer confirmed → BTC range-bound. ETF inflows slowed. Regime B until Fed pivots.

---

## Key Actors in Bitcoin Regime

- **[[../actors/POWELL-Jerome]]** — primary regime driver. His AuthScore=0 means pure data-dependence. When he pivots, Regime A begins.
- **[[../actors/FINK-Larry]]** — BlackRock IBIT = $50B+. His GeoScore=5.0 (multilateralist) aligns with BTC as global asset. Institutional legitimiser.
- **[[../actors/BESSENT-Scott]]** — Treasury. His EconScore=6.0 (fiscal conservative). Pro-Bitcoin positioning in 2025 campaign context.
- **[[../actors/TRUMP-Donald]]** — Executive orders on crypto regulation. GeoScore=-4.0 (isolationist) = potentially accelerates Regime C via dollar weaponisation.

## Related Pages
- [[../commodities/BITCOIN]]
- [[../market-impact/Bitcoin-vs-Equities-Rates]]
- [[../themes/Monetary-Policy-Weaponized-World]]
- [[../comparisons/Powell-Lagarde-Divergence]]
- [[../narratives/Global-Macro-Regime-2026-04]]
