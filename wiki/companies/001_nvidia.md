---
entity_id: 1
slug: nvidia
ticker: NVDA
archetype: TECHNOLOGICAL
composite_score: 72.00
last_updated: 2026-04-19
source: ipm_db_auto_generated
aliases: [NVIDIA, NVDA]
tags: [ipm-entity, technological]
---

# NVIDIA

> **Technological platform — AI, software, semiconductor, or cloud dominance.** Composite power score: **72/100** (rising trend). Country: United States.

## Power Index

**Archetype:** `TECHNOLOGICAL`  
**Composite:** ███████░░░ 72/100  
**Trend:** rising

| Dimension | Score | Bar |
|-----------|------:|-----|
| Financial | 93 | `█████████░` |
| Military | 38 | `███░░░░░░░` |
| Political | 65 | `██████░░░░` |
| Technological | 96 | `█████████░` |
| Industrial | 45 | `████░░░░░░` |
| Information | 60 | `██████░░░░` |

**Tiers:** Financial: Tier 1 (Dominant) · Political: Tier 2 (Significant) · Military: Tier 2 (Significant)

## Leadership

- **Jensen Huang** — CEO of NVIDIA (🔴 Critical)
- **Chris Malachowsky** — Co-founder (🟠 High)

### Jensen Huang — Vision

**Archetype:** `Techno-Utopian` · **Confidence:** 85/100  
**Horizon:** generational

Positions NVIDIA as core infrastructure provider for accelerated computing as the new industrial revolution. Argues GPU compute unlocks new scientific and industrial capabilities. Strong pro-Taiwan geopolitical stance given personal heritage.

> *"accelerated computing is the new industrial revolution"*
> — GTC 2024 Keynote, 2024-03-18

> *"AI is at an inflection point"*
> — GTC 2023 Keynote, 2023-03-21

**⚠ Divergence flags:**
- [Low] Stated: *Democratizing AI compute*
  Observed: Pricing and allocation favor hyperscalers over academic and open research

## Relations

### Outbound (this entity → others)

| Strength | Target | Type | Description |
|----------|--------|------|-------------|
| 🔴 Critical | **[[Ecuador|Ecuador]]** | `DependsOn` | All GPUs fabricated by TSMC in Taiwan. |
| 🔴 Critical | **[[SK Hynix|SK Hynix]]** | `DependsOn` |  |
| 🔴 Critical | **[[TSMC|TSMC]]** | `DependsOn` | NVIDIA fabricates ~100% of advanced chips (4nm, 3nm) at TSMC. Single point of fa... |
| 🟠 High | **[[Canada|Canada]]** | `Sanctions` | US export controls limit AI GPU sales. |
| 🟠 High | **[[ASML|ASML]]** | `DependsOn` | NVIDIA depends on ASML EUV tools indirectly through TSMC manufacturing. Critical... |
| 🟠 High | **[[Micron Technology|Micron Technology]]** | `DependsOn` |  |
| 🟠 High | **[[Alphabet|Alphabet]]** | `Supplies` | NVIDIA supplies Google Cloud for AI infrastructure. Dual relationship — Alphabet... |
| 🟠 High | **[[Advanced Micro Devices|Advanced Micro Devices]]** | `Competes` | MI300X/MI350 vs H100/H200/B200 in AI accelerators. |
| 🟠 High | **[[Amazon|Amazon]]** | `Supplies` | NVIDIA supplies AWS for Anthropic hosting, SageMaker AI, and EC2 GPU instances. ... |
| 🟠 High | **[[../institutions/META|Meta Platforms]]** | `Supplies` | NVIDIA supplies Meta for Llama training clusters. Estimated ~13% of NVIDIA reven... |
| 🟠 High | **[[Microsoft|Microsoft]]** | `Supplies` | NVIDIA supplies top client Microsoft for Azure AI. Estimated 15-19% of NVIDIA re... |
| 🟠 High | **[[xAI|xAI]]** | `Supplies` | xAI Colossus cluster uses 100,000 H100 GPUs. Top-10 NVIDIA customer 2024-2025. M... |
| 🟠 High | **[[OpenAI|OpenAI]]** | `Supplies` | NVIDIA supplies OpenAI primarily via Microsoft Azure. Direct relationship develo... |
| 🟡 Medium | **[[Pentagon|Pentagon]]** | `Supplies` | NVIDIA supplies GPUs to DoD for AI research and defense applications. Not a prim... |
| 🟡 Medium | **[[Anthropic|Anthropic]]** | `Supplies` | NVIDIA supplies Anthropic but with lower exposure than Microsoft/Meta. Anthropic... |
| 🟡 Medium | **[[../institutions/SAMSUNG|Samsung Electronics]]** | `Partners` | Samsung Foundry as alternative fab option. Not currently primary but strategic h... |
| 🟡 Medium | **[[Oracle|Oracle]]** | `Supplies` | Oracle strategic client for sovereign AI deployments. Growing relationship via O... |

### Inbound (others → this entity)

| Strength | Source | Type | Description |
|----------|--------|------|-------------|
| 🔴 Critical | **[[xAI|xAI]]** | `DependsOn` |  |
| 🔴 Critical | **[[../institutions/META|Meta Platforms]]** | `DependsOn` |  |
| 🔴 Critical | **[[../actors/HUANG-Jensen|Jensen Huang]]** | `Governs` | Jensen Huang co-founded NVIDIA in 1993. Largest individual shareholder. |
| 🔴 Critical | **[[SK Hynix|SK Hynix]]** | `Partners` | SK Hynix co-develops HBM3E/HBM4 specifications with NVIDIA. |
| 🟠 High | **[[Amazon|Amazon]]** | `DependsOn` | Amazon AWS deploys large NVIDIA GPU clusters for EC2 P-instances. Developing Tra... |
| 🟠 High | **[[Microsoft|Microsoft]]** | `DependsOn` | Microsoft Azure AI compute fleet depends heavily on NVIDIA H100 and H200 GPUs. T... |
| 🟠 High | **[[../institutions/PALANTIR|Palantir]]** | `DependsOn` |  |
| 🟠 High | **[[Alphabet|Alphabet]]** | `DependsOn` | Alphabet/Google DeepMind and GCP depend on NVIDIA H100/A100 for AI training. Own... |
| 🟠 High | **[[US Department of Commerce|US Department of Commerce]]** | `Regulates` | BIS export controls restrict A100, H100, and derivatives to China. NVIDIA respon... |
| 🟠 High | **[[Vanguard Group|Vanguard Group]]** | `Owns` | Vanguard Group is largest institutional holder of NVIDIA at approximately 8.6% a... |
| 🟠 High | **«entidad no resuelta»** | `Governs` | Santa Clara HQ Operations is a HQ facility operated by NVIDIA in Santa Clara |
| 🟠 High | **[[Intel|Intel]]** | `Competes` | Intel Gaudi vs NVIDIA GPUs for AI inference and training. |
| 🟠 High | **[[BlackRock|BlackRock]]** | `Owns` |  |
| 🟠 High | **[[Advanced Micro Devices|Advanced Micro Devices]]** | `Competes` |  |
| 🟠 High | **[[Arm Holdings|Arm Holdings]]** | `Supplies` |  |
| 🟠 High | **[[TSMC|TSMC]]** | `Supplies` | NVIDIA H100 on N4P, H200 and Blackwell on N3. TSMC is the only foundry capable o... |
| 🟠 High | **[[Chris Malachowsky|Chris Malachowsky]]** | `Owns` | Chris Malachowsky co-founded NVIDIA with Jensen Huang in 1993. |
| 🟡 Medium | **[[../companies/201_spacex|SpaceX]]** | `DependsOn` | Starlink ground stations and network management require GPU compute for beam-for... |
| 🟡 Medium | **«entidad no resuelta»** | `Influences` | NVIDIA Israel R&D Center is a R&D facility operated by NVIDIA in Yokneam |
| 🟡 Medium | **«entidad no resuelta»** | `Influences` | NVIDIA Bangalore Engineering Center is a R&D facility operated by NVIDIA in Bang... |
| 🟡 Medium | **[[State Street Corporation|State Street Corporation]]** | `Owns` | State Street Corporation holds approximately 4.2% of NVIDIA through institutiona... |
| 🟡 Medium | **[[../institutions/LOCKHEED-MARTIN|Lockheed Martin]]** | `Partners` | Lockheed integrates NVIDIA GPU-based AI for autonomous systems, targeting soluti... |
| ⚪ Low | **[[Apple|Apple]]** | `Competes` | Apple M4 Ultra targets professional creative workflows previously dominated by N... |

## Recent Events

### 2026-03-18 — NVIDIA H100 Demand Surges as Hyperscalers Double AI Capex
`Critical` 📈 Positive · Source: Bloomberg ✓
[Source](https://www.bloomberg.com/nvidia-h100-hyperscaler-2026)

Microsoft, Google, and Amazon committed a combined $200B in AI infrastructure spending in Q1 2026, with NVIDIA H100 and Blackwell chips as primary accelerators. Jensen Huang signals supply constraints easing by Q3.

### 2024-11-08 — NVIDIA joins Dow Jones Industrial Average, replaces Intel
`Medium` 📈 Positive · Source: Wall Street Journal ✓
[Source](https://www.wsj.com/finance/stocks/nvidia-dow-jones-intel)

NVIDIA replaced Intel in Dow Jones Industrial Average, reflecting shift in tech sector weight and AI era transition.

### 2024-08-02 — DOJ opens antitrust investigation into NVIDIA
`High` 📉 Negative · Source: Bloomberg ✓
[Source](https://www.bloomberg.com/news/articles/2024-08-01/nvidia-doj-antitrust)

DOJ investigating whether NVIDIA AI chip dominance raises competition concerns. Focus on bundling, allocation practices, and acquisitions. Ongoing investigation.

### 2024-03-18 — NVIDIA unveils Blackwell B200 architecture at GTC 2024
`Critical` 📈 Positive · Source: NVIDIA GTC 2024 Keynote ✓
[Source](https://nvidianews.nvidia.com/news/nvidia-blackwell-platform)

Blackwell architecture announced at GTC 2024 — generational leap for AI training. Cemented NVIDIA leadership in frontier-scale AI clusters. 2.5x performance vs Hopper.

### 2023-11-13 — NVIDIA launches H200 Tensor Core GPU
`High` 📈 Positive · Source: NVIDIA Press Release ✓
[Source](https://nvidianews.nvidia.com/news/nvidia-supercharges-hopper)

H200 launch — evolution of Hopper architecture with expanded HBM3e memory. Announced November 2023, deliveries Q1 2024. Significant uplift for AI training workloads.

---
*Auto-generated from IPMDB on 2026-04-19. Edge count: 40.*
*Composite score: 72/100 | Archetype: TECHNOLOGICAL*