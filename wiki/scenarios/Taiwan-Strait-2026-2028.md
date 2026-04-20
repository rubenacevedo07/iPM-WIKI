---
title: Taiwan Strait 2026–2028 Scenarios
slug: taiwan-strait-scenarios
type: scenario
tags: [taiwan, china, tsmc, semiconductors, pla, military, ai-supply-chain]
created: 2026-04-10
updated: 2026-04-10
confidence: medium
sources:
  - raw/geopolitics/chokepoint-risk-2026-04.md
related_actors: [xi-jinping, jensen-huang, morris-chang, donald-trump]
related_countries: [taiwan, china, united-states, japan]
related_institutions: [tsmc, nvidia, asml, pentagon]
related_commodities: [semiconductors]
related_themes: [ai-supply-chain-export-controls, energy-chokepoints-war, geoeconomic-fragmentation]
---

# Taiwan Strait 2026–2028 Scenarios

*Current threat level: 6/10. Taiwan Strait is the single highest-consequence chokepoint in the IMP graph — not highest probability, but highest impact. TSMC produces 90%+ of the world's sub-5nm chips. A closure or blockade is an extinction-level event for the AI industry.*

---

## Scenario Space

**Trigger node:** Taiwan Strait `ClosureRiskScore` crosses 8/10
**Primary actor:** Xi Jinping (AuthScore=9.0, GeoScore=3.0)
**Constraint:** PLA readiness, US deterrence (Pentagon=78/100), economic cost to China

---

## Branch A — PLA Blockade / Military Action
*Probability: 15-20% by 2028 per IMP assessment*

**Trigger sequence:**
1. Taiwan independence declaration OR US arms sale threshold crossed
2. PLA activates "Joint Sword" operation — naval blockade + air exclusion zone
3. TSMC fabs operational but isolated — no materials in, no chips out
4. US 7th Fleet deploys — carrier strike group + submarine screen
5. Japan invokes mutual defence considerations

**First 30 days:**
- TSMC Fab 18 + Hsinchu park: operations continue but supply chain severed
- Advanced Logic Chips (Commodity 51) supply drops to ~0 within 60-90 days
- GPU Compute (Commodity 53) production: NVIDIA B100/B200 pipeline halted
- HBM (Commodity 55): Samsung Korea continues — partial mitigation

**Market cascade:**
- NVIDIA: −60 to −80% (existential supply shock)
- ASML: −40% (no new EUV shipments to Taiwan)
- S&P 500: −25 to −35% (AI infrastructure repricing)
- Brent: +$40-60/barrel (war premium + Malacca risk)
- USD: initial spike then structural sell (dollar weaponisation accelerates de-dollarization)
- Bitcoin: initial risk-off dump then Regime C macro-hedge bid

**IMP DB updates triggered:**
- Taiwan Strait `ClosureRiskScore` → 10
- RelationEdge TSMC→NVIDIA `Strength` → downgrade
- ScenarioCascade: Oil $150 template activates
- GCRI: estimated +25 points

**Resolution branches:**
- A1: US military intervention → deterrence restored → 6-18 month standoff
- A2: Negotiated ceasefire → Taiwan autonomy preserved but TSMC distributed
- A3: Escalation → direct US-China conflict → systemic reset

---

## Branch B — Grey Zone Escalation (Baseline)
*Probability: 60-70% over 2026-2028*

**Pattern:** PLA exercises, ADIZ incursions, cyber attacks on TSMC, economic coercion — but no kinetic action.

**Ongoing effects:**
- TSMC insurance premiums: +200-400% (Lloyd's Taiwan war risk zone)
- TSMC Arizona Phase 2 (2nm) accelerated — US government pressure
- Samsung/Intel foundry investment: +$50B announced globally
- Advanced Logic supply: tight but functional
- Taiwan brain drain: engineers accepting TSMC Arizona/Japan offers

**Market impact (slow-burn):**
- NVIDIA: resilient — demand exceeds supply regardless
- TSMC: discount to fair value (geopolitical risk premium)
- Intel: re-rating upward (foundry alternative narrative)
- Taiwan defense stocks: bid

**IMP DB updates triggered:**
- Taiwan Strait `ClosureRiskScore` holds 6-7
- New RelationEdge: TSMC→Partners→Intel (foundry backup discussions)
- PowerMapRelation: TSMC Arizona node gains weight

---

## Branch C — Diplomatic Resolution
*Probability: 15-20%*

**Trigger:** MBS-style Xi-Biden/Trump deal — "1992 Consensus" reaffirmed, TSMC sharing arrangement, export controls partially lifted.

**Effects:**
- Taiwan Strait `ClosureRiskScore` → 3
- TSMC China revenue partially restored
- Advanced Logic Chips supply eases
- AI hardware capex normalises
- NVIDIA China revenue recovers $10B+

---

## Cross-Branch Markers (watch for these)

| Signal | Branch A indicator | Branch B indicator | Branch C indicator |
|--------|-------------------|-------------------|-------------------|
| PLA exercises | >21 days continuous | <7 days per quarter | Cancelled |
| TSMC Arizona output | Emergency scale-up | Gradual ramp | Slow ramp |
| NVIDIA China revenue | Zero | Restricted | Partial recovery |
| Taiwan defense budget | >4% GDP | 2.5-3% GDP | <2% GDP |
| US carrier presence | 2+ CSG in theatre | 1 CSG rotating | Standard presence |

---

## Oracle Relevance
- Chen Wei (Taiwan/semiconductor domain) — primary tracking machine
- Alexandra Voss (USD/global macro) — dollar impact modelling
- David O'Connor (Fed/rates) — inflation shock from supply disruption

## DB Sync Notes
- CommodityFacility TSMC Fab18 `SupplyRiskScore`=9 already seeded ✅
- ScenarioCascade template for Branch A: similar to Oil $150 / Hormuz closure
- Timeline seeded: "Taiwan Strait" in Semiconductor PowerMap (PowerMap 4)

## Related Pages
- [[../institutions/TSMC]]
- [[../institutions/NVIDIA]]
- [[../actors/XI-Jinping]]
- [[../countries/TAIWAN]]
- [[../themes/AI-Supply-Chain-Export-Controls]]
- [[../timelines/AI-Tech-Decoupling-2019-2026]]
