---
title: AI Supply Chain & Export Controls
slug: ai-supply-chain-export-controls
type: theme
tags: [semiconductors, ai, export-controls, tsmc, nvidia, asml, china, decoupling]
created: 2026-04-09
updated: 2026-04-09
confidence: high
sources:
  - raw/geopolitics/china-economy-2026-04.md
  - raw/geopolitics/trump-trade-policy-2026-04.md
related_actors: [jensen-huang, morris-chang, xi-jinping, donald-trump]
related_countries: [united-states, taiwan, china]
related_institutions: [nvidia, tsmc, asml, apple, microsoft]
related_commodities: [semiconductors]
related_themes: [geoeconomic-fragmentation, energy-chokepoints-war]
---

# AI Supply Chain & Export Controls

## Strategic Summary

The global AI supply chain runs through a handful of irreplaceable chokepoints — TSMC's fabs in Taiwan, ASML's EUV machines in the Netherlands, NVIDIA's GPU designs in California — and every one of them sits at the intersection of US-China geopolitical competition. Export controls introduced since 2019 have created two diverging technology ecosystems: a US-aligned one with access to cutting-edge AI chips, and a China-constrained one building workarounds. The gap between them is widening, not closing.

This is not just a technology story. It is a power story. Whoever controls the chokepoints in this supply chain controls who can build frontier AI — which increasingly means who can build the next generation of economic and military capability.

## Core Nodes

**Foundries — who builds the chips:**
- [[../institutions/TSMC]] (ID: 41) — world's only maker of sub-3nm chips; Taiwan Strait risk=6/10
- Samsung — DRAM + NAND + foundry; South Korea exposure
- Intel — fabs in US and EU; behind TSMC on leading edge

**Tooling — who enables the fabs:**
- [[../institutions/ASML]] (ID: 21) — only maker of EUV and High-NA EUV lithography; `SubstitutionLatencyMonths=120`; `IsChokepoint=TRUE`
- Tokyo Electron — etch and deposition tools; Japan export control exposure
- Applied Materials, Lam Research — US-based; subject to BIS export rules

**Designers — who architects the chips:**
- [[../institutions/NVIDIA]] (ID: 1) — GPU monopoly for AI training; H100/H200/B100 series; export-controlled to China
- AMD — GPU designer; Instinct series; second to NVIDIA on AI
- Huawei/HiSilicon — China's attempt at self-sufficiency; Ascend NPUs; constrained by TSMC access

**Memory & Packaging:**
- HBM (High Bandwidth Memory): SK Hynix, Samsung, Micron — bottleneck for NVIDIA GPU assembly
- CoWoS advanced packaging: TSMC controls; capacity has been the binding constraint on H100 supply
- 2.5D/3D integration: next battleground for performance per watt

## Export Control Timeline (2019–2026)

- **2019:** Huawei added to Entity List — first major tech decoupling signal
- **2020:** TSMC cuts Huawei supply following US pressure
- **2022-10:** Biden administration BIS rules — restrict GPU exports (A100, H100) to China; extend to tools and components
- **2023:** Netherlands agrees to restrict ASML EUV shipments to China; Japan joins
- **2023:** NVIDIA launches A800/H800 "China versions" to circumvent controls — US closes loophole
- **2024:** Further tightening — broader entity list additions; Huawei Mate 60 Pro shocks US with SMIC-manufactured chip
- **2025:** New BIS rules close remaining workarounds; China GPU exports near zero for frontier models
- **2026-03:** Trump administration investigating additional trade restrictions on tech vs China and EU

## Capacity & Bottlenecks (current)

- **EUV/High-NA EUV:** ASML has a multi-year backlog. High-NA (next generation, sub-2nm capability) shipments just beginning. China cannot access EUV at all.
- **Advanced packaging (CoWoS):** TSMC CoWoS capacity was the binding constraint on H100 supply in 2023-24. Expanded but still tight.
- **Power & water:** Arizona TSMC fab delayed by skilled labour shortage and utility infrastructure. Power-hungry AI datacenters competing with fab power needs.
- **HBM:** SK Hynix dominant. Capacity expanding but 12-18 month lead times for new production.

## Geopolitical Split

**US-aligned ecosystem:**
NVIDIA (design) → TSMC (fab) → ASML (tools) → HBM vendors → CoWoS packaging → hyperscaler deployment
All nodes under US jurisdiction or US-allied control. Export controls protect this ecosystem.

**China-constrained ecosystem:**
Huawei/HiSilicon (design) → SMIC (fab, limited to ~7nm) → domestic tools (years behind) → domestic HBM attempts
Cannot access EUV. Cannot access CoWoS at scale. Running 2-3 generations behind on leading edge.

**Swing states:**
South Korea (Samsung) — allied with US but significant China revenue exposure
Japan (Tokyo Electron, Shin-Etsu) — joined export controls but economic ties to China remain
Taiwan — the ultimate swing state; TSMC is the chokepoint

## Market Impact Summary

- **Hyperscaler capex:** Microsoft, Google, Amazon, Meta all spending $50B+ annually on AI infrastructure — almost all flowing through NVIDIA → TSMC → HBM pipeline. This is the structural demand floor for the ecosystem.
- **NVIDIA valuation:** Priced as the toll booth on the AI supply chain. Any export control that reduces China addressable market is a direct revenue headwind. China was ~20-25% of data center revenue pre-controls.
- **Supply vs demand risk:** Current cycle is demand-constrained (more customers than supply). If TSMC CoWoS and HBM capacity catches up, the bottleneck moves to model quality and use case adoption.
- **China tech premium:** Chinese AI companies (Baidu, ByteDance, Alibaba) paying a "China discount" on compute — forced to use older chips or domestic alternatives, limiting model quality ceiling.

## DB Sync Notes
- PowerMap ID 4 (Semiconductor) has empty PowerMapRelation edges — CL-DB-005 ✅ CLOSED — 5 PowerMapRelation edges seeded 2026-04-09
- RelationEdge: NVIDIA→DependsOn→TSMC, ASML→Supplies→TSMC rows should be seeded
- SubstitutionLatencyMonths for ASML: 120 months (confirmed in DB)

## Related Pages
- [[../actors/HUANG-Jensen]]
- [[../actors/CHANG-Morris]]
- [[../actors/XI-Jinping]]
- [[../institutions/NVIDIA]]
- [[../institutions/TSMC]]
- [[../institutions/ASML]]
- [[../countries/TAIWAN]]
- [[../countries/CHINA]]
- [[../timelines/AI-Tech-Decoupling-2019-2026]]
- [[Geoeconomic-Fragmentation]]
- [[../comparisons/BlackRock-Ownership-Web]]

## Complete AI Supply Chain Graph (April 2026)

```
LAYER 0 — RAW MATERIALS
Rare Earth Elements (China=60% supply) → Silicon Wafers → Chip fab materials

LAYER 1 — TOOLING (chokepoints)
ASML (EUV/High-NA) → TSMC, Samsung
Tokyo Electron, Applied Materials → all fabs

LAYER 2 — FABRICATION
TSMC (node1) → NVIDIA, Apple, AMD, Qualcomm
Samsung (node) → DRAM/NAND/HBM
SK Hynix → HBM (critical for NVIDIA H100/B100)
Micron → HBM alternative
Intel → legacy nodes + trying 18A

LAYER 3 — CHIP DESIGN (fabless)
NVIDIA (node4) → H100/B100 AI GPUs → all AI companies
AMD → MI300X → competing AI GPUs
Arm Holdings → CPU/NPU architecture licenses
Intel → data center + PC

LAYER 4 — CLOUD INFRASTRUCTURE (middleware)
AWS (Amazon) → Anthropic (exclusive), NVIDIA H100 instances
Microsoft Azure → OpenAI (exclusive), NVIDIA H100
Google Cloud → DeepMind, NVIDIA H100 + TPU
All three → dependent on NVIDIA GPUs

LAYER 5 — AI FRONTIER LABS (consumers)
OpenAI (198) → Microsoft Azure (exclusive)
Anthropic (197) → AWS (exclusive)
xAI (Musk) → 100K+ NVIDIA H100 cluster
Meta (6) → largest single NVIDIA buyer (350K+ H100s)
Google DeepMind → Google Cloud + TPU
Mistral AI → European frontier model

LAYER 6 — AI APPLICATIONS / DEPLOYMENT
Palantir (PLTR) → Pentagon + CIA + Ukraine (defense AI)
                → AWS + NVIDIA (infrastructure)
Microsoft Copilot → Azure + OpenAI
AWS Bedrock → Anthropic + NVIDIA
```

## Gap: China Parallel Stack (constrained)
```
Huawei HiSilicon (Ascend NPUs) → SMIC (7nm, no EUV)
BIREN, Cambricon → domestic GPU alternatives
All running 2-3 generations behind US stack
Cannot access EUV → ceiling is ~7nm equivalent
```

## Palantir as Defense AI Node
Palantir connects the AI supply chain to the coercive power layer:
- Governs: [[../institutions/PENTAGON]] (Maven Smart System, DoD primary AI)
- Partners: US Intelligence Community (CIA Gotham, NSA analytics)
- Partners: Ukraine (battlefield targeting AI)
- DependsOn: AWS + NVIDIA (cloud + GPU infrastructure)
- The "picks and shovels" of AI warfare — whoever controls the targeting AI controls the battlefield
