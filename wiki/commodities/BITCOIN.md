---
title: Bitcoin
slug: bitcoin
type: commodity
region: global
tags: [crypto, store-of-value, risk-on, macro-hedge, monetary-system]
created: 2026-04-10
updated: 2026-04-10
confidence: medium
sources: []
related_actors: [larry-fink, scott-bessent, donald-trump]
related_countries: [united-states]
related_institutions: [blackrock, federal-reserve]
related_commodities: []
related_themes: [bitcoin-macro-regime, dollar-dominance, de-dollarization, monetary-policy-weaponized-world]
db_id:
db_type: COMMODITY
---

# Bitcoin

## Strategic Summary
Bitcoin is the only commodity in the IMP graph with a fixed, algorithmically enforced supply schedule — 21 million coins, halving every ~4 years. This makes it structurally different from oil, gold, or semiconductors: it has no OPEC, no mining cartel, no single chokepoint controller. Its price is a real-time referendum on global liquidity conditions, dollar confidence, and risk appetite. In 2024 the launch of US spot ETFs (BlackRock iShares Bitcoin Trust = largest ETF launch in history) transformed BTC from a crypto-native asset to an institutional macro instrument.

## Supply Structure
- **Fixed supply:** 21 million BTC hard cap — algorithmic, not political
- **Current supply:** ~19.7M BTC mined as of 2026
- **Halving schedule:** Every ~210,000 blocks (~4 years). Most recent: April 2024 (block reward halved to 3.125 BTC)
- **Next halving:** ~2028
- **Mining concentration:** ~60-65% hashrate in USA + Kazakhstan + Russia. US dominant post-China ban
- **Energy dependency:** ~150 TWh/year globally. Stranded energy economics increasingly relevant
- **No chokepoint controller** — mining is geographically distributed. Protocol change requires ~51% hashrate consensus

## Demand Structure
- **Institutional (post-ETF):** BlackRock IBIT, Fidelity FBTC, others. Combined AUM $50B+
- **Corporate treasury:** MicroStrategy (~200K BTC), Tesla, others
- **Retail HODLers:** ~50M+ wallets with non-zero balance
- **Emerging market capital flight:** Turkey, Argentina, Nigeria — BTC as inflation hedge
- **Sovereign:** El Salvador legal tender. Rumoured sovereign reserves (Russia, Iran, others)
- **Stablecoin ecosystem:** USDT/USDC as on-ramp — Tether is #1 BTC trading vehicle

## Chokepoints and Vulnerabilities
- **Exchanges:** Binance, Coinbase, OKX control most liquidity. Regulatory action = immediate price shock
- **Stablecoins:** Tether (USDT) $100B+ — unregulated dollar proxy. Failure = systemic crypto contagion
- **On/off ramps:** Banking access for crypto firms. Fed/OCC guidance = structural constraint
- **Mining energy:** Grid access and energy costs. China ban (2021) = concentration shift to US
- **Protocol risk:** Quantum computing (long-dated). 51% attack (theoretical at current hashrate)
- **Regulatory:** US spot ETF = regulatory legitimacy. EU MiCA = European framework. China ban permanent

## Market Impact
- **Primary correlation:** Global liquidity (M2 growth), risk appetite (Nasdaq), real yields (inverse)
- **Fed hawkish:** Higher real rates → USD strength → BTC under pressure (risk-off)
- **Fed dovish:** Lower rates → liquidity expansion → BTC outperforms (risk-on, high beta)
- **War/energy shocks:** Mixed — initial risk-off (sell BTC) then potential safe-haven bid if dollar confidence erodes
- **Sanctions/capital controls:** Strong positive — BTC as censorship-resistant store of value
- **ETF flows:** BlackRock IBIT flows = institutionalised demand. Inflow days = price support
- **Beta to Nasdaq:** ~1.5-2.0x on average — amplified tech risk proxy

## DB Sync Notes
- No DB entity yet — pending Commodities table seed
- Suggest: INSERT into public."Commodities" with IsChokepoint=FALSE, tag crypto
- MarketSymbol BTC already seeded (confirmed in MarketSymbol table — 25 instruments)

## Related Pages
- [[../themes/Bitcoin-Macro-Regime]]
- [[../market-impact/Bitcoin-vs-Equities-Rates]]
- [[../themes/Monetary-Policy-Weaponized-World]]
- [[../themes/Geoeconomic-Fragmentation]]
- [[../actors/FINK-Larry]]
- [[../institutions/BLACKROCK]]
