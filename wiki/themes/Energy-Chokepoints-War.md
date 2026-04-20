---
title: Energy Chokepoints & War
slug: energy-chokepoints-and-war
type: theme
tags: [energy, chokepoints, war, iran, russia, houthis, oil, lng, shipping]
created: 2026-04-09
updated: 2026-04-09
confidence: high
sources:
  - raw/transcripts/powell-fomc-2026-04.md
  - raw/institutions/imf-weo-2026-04.md
  - raw/geopolitics/chokepoint-risk-2026-04.md
  - raw/sanctions/russia-oil-2026-04.md
related_actors: [vladimir-putin, mohammed-bin-salman, jerome-powell, christine-lagarde]
related_countries: [russia, saudi-arabia, iran, ukraine, united-states]
related_institutions: [opec, federal-reserve, ecb]
related_commodities: [oil, lng]
related_themes: [geoeconomic-fragmentation, monetary-policy-weaponized-world]
---

# Energy Chokepoints & War

## Strategic Summary

The world's critical energy infrastructure runs through five maritime chokepoints — Hormuz, Bab el-Mandeb, Suez, Malacca, and the Taiwan Strait — each controlled or threatened by a different geopolitical actor. When any one of these closes or becomes contested, the shock transmits through oil prices, shipping rates, inflation expectations, and central bank forward guidance simultaneously. In 2026, three of these five are under active threat simultaneously: Hormuz (IRGC), Bab el-Mandeb (Houthis), and Taiwan Strait (PLA). This is unprecedented in the post-Cold War era.

Russia's invasion of Ukraine added a second axis: energy as a sanctions weapon. The G7 price cap mechanism, shadow fleet operations, and India/China purchase volumes have turned Russian oil into a parallel market that runs alongside the Western system — not inside it. The net effect is structural fragmentation of global energy pricing.

## Core Chokepoints (current threat scores — April 2026)

| Chokepoint | Score | Controller | Active Threat |
|------------|-------|-----------|---------------|
| **Bab el-Mandeb** | 8/10 | Houthis (Yemen) | YES — active attacks, shipping rerouting |
| **Hormuz** | 7/10 | Iran (IRGC) | ELEVATED — no blockade but incident risk high |
| **Taiwan Strait** | 6/10 | China (PLA) | ELEVATED — exercises, grey-zone pressure |
| **Suez Canal** | 5/10 | Indirect (Red Sea) | INDIRECT — canal open, approach routes risky |
| **Malacca** | 5/10 | Latent | NO active threat — latent US-China risk |

See also: [[Chokepoint-Intelligence]] for full DB-linked analysis.

## Conflict & Sanctions Timeline (Key Milestones)

- **2022-02:** Russia invades Ukraine — European energy dependency exposed overnight
- **2022-12:** G7/EU oil price cap at $60/barrel introduced
- **2023-Q4:** Houthi attacks on Red Sea shipping begin — first significant rerouting
- **2024:** Shadow fleet operational at scale — hundreds of tankers evading price cap
- **2025:** India reduces Russian oil purchases as discounts narrow
- **2026-03:** Western enforcement tightened — more cargo inspections, blacklisting of shadow fleet entities
- **2026-04:** Bab el-Mandeb now highest active risk chokepoint (8/10) — surpassing Taiwan Strait

## Transmission Channels

**Oil & LNG supply:** Closure or partial blockage of any chokepoint removes supply from the market immediately. Hormuz closure = ~20% of global oil supply at risk. Bab el-Mandeb = Red Sea LNG route from Qatar to Europe.

**Shipping routes & insurance:** Houthi attacks have forced Cape of Good Hope rerouting — adding 10-14 days to Asia-Europe voyages, increasing fuel costs, and driving insurance premiums sharply higher. Lloyd's war risk zones now cover Red Sea permanently.

**Refining & product markets:** Rerouting disrupts just-in-time refinery scheduling. European refiners built for Brent crude face product shortages when Middle East supply is delayed. Crack spread volatility = refinery margin signal.

**Inflation and expectations:** Energy shocks enter CPI with a 2-4 week lag (fuel prices) and a 4-8 week lag (food, transport). More important: they change inflation expectations — which changes central bank behaviour before the actual inflation arrives.

## Link to Monetary Policy

Powell (March 2026): explicitly monitoring whether tariff and energy price shocks become "persistent." If they do, rate cuts are further delayed. The mechanism: energy shock → higher headline CPI → Fed cannot cut → USD stays strong → EM capital outflows → global growth drag.

Lagarde (ECB): similar concern but weaker. Europe is a net energy importer — energy shocks are stagflationary for the eurozone (higher prices + weaker growth simultaneously). This makes the ECB's job harder than the Fed's: it cannot simply hike to fight energy inflation without worsening recession risk.

The Fed-ECB divergence on how to handle persistent energy shocks is a direct input to the EUR/USD signal. See [[../comparisons/Powell-Lagarde-Divergence]].

## Market Impact Summary

- **Brent vs Urals discount:** Persists at $5-15/barrel — "Russia discount" reflecting sanctions risk and logistics cost
- **Freight rates:** Baltic Exchange indices elevated; Cape rerouting adds ~$1-2M per voyage vs Suez route
- **Rerouting costs:** Asia-Europe container shipping +15-20% cost vs pre-Houthi baseline
- **FX — net importers:** EUR, JPY, INR structurally pressured when oil spikes; USD benefits as energy exporter
- **Inflation premium:** Energy component of CPI in EU and Japan more volatile than US — adds to EUR/JPY weakness

## Key Actors

- **Iran (IRGC):** Controls Hormuz threat. Proxy of Houthi operations. Nuclear programme negotiation leverage.
- **Russia:** Oil supply via shadow fleet. Price cap evasion. Weaponising energy dependency.
- **Houthis (Yemen):** Iran-backed. Conducting Red Sea attacks. Bab el-Mandeb controller.
- **US, EU, GCC navies:** Operation Prosperity Guardian. Red Sea convoy protection. Patchy effectiveness.
- **Saudi Arabia (MBS):** OPEC+ swing producer. Can partially offset supply disruptions or amplify them.

## DB Sync Notes
- CommodityChokepoint table: Bab el-Mandeb threat score needs update (currently lower than wiki 8/10 assessment)
- RelationEdge: Iran→Threatens→Hormuz, Houthis→Threatens→Bab el-Mandeb rows should exist
- DB flag: CL-DB-003 OPEN

## Related Pages
- [[Chokepoint-Intelligence]]
- [[../countries/RUSSIA]]
- [[../countries/SAUDI-ARABIA]]
- [[../actors/MBS]]
- [[../actors/PUTIN-Vladimir]]
- [[../market-impact/Fed-Rate-Policy-Markets]]
- [[../timelines/Global-Energy-Shipping-2019-2026]]
- [[Geoeconomic-Fragmentation]]
