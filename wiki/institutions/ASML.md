---
title: ASML
slug: asml
type: institution
institution_type: regulator
region: europe
tags: [semiconductors, lithography, euv, chokepoint, netherlands, export-controls]
created: 2026-04-09
updated: 2026-04-21
confidence: high
sources: []
related_actors: [jensen-huang, morris-chang]
related_countries: [netherlands, united-states, china, taiwan, south-korea, japan]
related_institutions: [tsmc, samsung, nvidia, blackrock]
related_commodities: [semiconductors]
related_themes: [ai-supply-chain-export-controls, chokepoint-intelligence, geoeconomic-fragmentation]
db_id: 21
db_type: COMPANY
---

# ASML

## Mandate and Tools
ASML is the sole global manufacturer of Extreme Ultraviolet (EUV) lithography machines — the equipment required to print chips below 7nm. Without ASML EUV tools, no foundry can produce advanced semiconductors. This is the hardest physical chokepoint in the AI supply chain: no substitute exists, no competitor is within a decade of parity.

**Key products:**
- **EUV (NXE series):** ~€180M/unit. Required for 7nm and below. TSMC, Samsung, Intel are the primary customers.
- **High-NA EUV (EXE series):** Next generation, ~€350M/unit. Sub-2nm capability. First units delivered 2024.
- **DUV (immersion):** Older technology, still critical for mature nodes (28nm–180nm). China's primary workaround target.

## Internal Structure
- HQ: Veldhoven, Netherlands
- ~42,000 employees globally
- R&D: ~15% of revenue (~€4.5B/year)
- Key suppliers: Carl Zeiss (Germany, optics — sole supplier), Cymer (US, light source)
- Manufacturing: primarily Netherlands, some assembly in US/Korea

## Current Regime
*(Knowledge-based · April 2026)*

ASML is caught between its two largest markets: China (~15% of revenue pre-controls) and the US/Taiwan/Korea alliance that controls its export licenses. Dutch government — under US pressure — has progressively restricted EUV and then DUV exports to China since 2023. China is ASML's last remaining growth market that is being actively closed off.

Revenue 2025: ~€28B. Order backlog: ~€40B+. Demand exceeds supply capacity — ASML controls the pace of the entire semiconductor industry's expansion.

## Relationships
- **TSMC:** Primary EUV customer. ASML→Partners→TSMC (Critical, RE 55 seeded)
- **Samsung:** Second largest EUV customer
- **Intel:** Third major customer, Fab 34 Ireland uses EUV
- **Carl Zeiss:** Sole optics supplier — ASML owns 25% stake. Single point of failure
- **US BIS:** Export license authority — US has de facto veto on all ASML China sales
- **Dutch MOCIT:** Dutch export license authority — signed MOU with US on coordinated controls

## Recent Moves
- 2023: Netherlands banned EUV exports to China (already US-restricted since 2020)
- 2024: Netherlands expanded ban to cover DUV immersion systems for China
- 2026-Q1: China's SMIC attempting to use smuggled/grey-market DUV equipment — enforcement ongoing
- 2026-Q1: High-NA EUV first production units shipping to TSMC Arizona and Samsung

## Narrative Shift
Export controls have bifurcated ASML's strategic narrative. Pre-2022: global champion of open technology. Post-2022: instrument of Western tech containment. Veldhoven is now geopolitically significant in a way no Dutch company has been since Shell's Cold War era. The Dutch government is uncomfortable with this role but has little leverage vs US pressure.

## Market Impact Channels
- **ASML stock (ASML:AS / ASML:NASDAQ):** Leading indicator for semiconductor capex cycle. Also sensitive to China revenue guidance — any China news = ±5-10% move.
- **Semiconductor capex cycle:** ASML order intake = 6-18 month leading indicator for fab expansion → chip supply → chip prices.
- **Export control escalation:** Any tightening beyond current DUV ban → ASML revenue hit → semiconductor supply constraint → AI capex delay.
- **Carl Zeiss dependency:** Single optics supplier (Veldhoven-Oberkochen axis) = concentrated geopolitical risk if Germany disrupted.

## DB Sync Notes
- DB ID: 21 ✅ confirmed
- institution_type corrected from 'ministry' → should be 'regulator' or create new enum value 'manufacturer'
- CommodityFacility: ASML Veldhoven → Photoresist EUV (Input, Critical, Risk=7) ✅ seeded
- RelationEdge ASML→Partners→TSMC (RE 55, Critical) ✅ seeded
- Missing edges: ASML→Supplies→Samsung, ASML→Supplies→Intel, ASML→DependsOn→Carl Zeiss

**DB SYNC NEEDED (CL-DB-016):** ASML→Supplies→Samsung RelationEdge not seeded. ASML→DependsOn→Carl Zeiss not seeded (Carl Zeiss not in Companies table).

## Related Pages
- [[../actors/HUANG-Jensen]]
- [[../actors/CHANG-Morris]]
- [[../countries/NETHERLANDS]] *(page pending)*
- [[../countries/CHINA]]
- [[../countries/TAIWAN]]
- [[../institutions/TSMC]]
- [[../institutions/SAMSUNG]]
- [[../themes/AI-Supply-Chain-Export-Controls]]
- [[../themes/Chokepoint-Intelligence]]

## Open Questions
- Carl Zeiss: seed as Company node in DB?
- ASML High-NA EUV delivery schedule to TSMC Arizona — on track?
- Chinese domestic EUV program (SMEE) — realistic timeline assessment?
