---
entity_id: 4
ticker: MSFT
archetype: HYBRID
composite_score: 79.00
last_updated: 2026-04-19
source: ipm_db_auto_generated
aliases: [Microsoft, MSFT]
tags: [ipm-entity, hybrid]
---

# Microsoft

> **Hybrid power — crosses multiple power dimensions simultaneously.** Composite power score: **79/100** (rising trend). Country: United States.

## Power Index

**Archetype:** `HYBRID`  
**Composite:** ███████░░░ 79/100  
**Trend:** rising

| Dimension | Score | Bar |
|-----------|------:|-----|
| Financial | 88 | `████████░░` |
| Military | 42 | `████░░░░░░` |
| Political | 82 | `████████░░` |
| Technological | 92 | `█████████░` |
| Industrial | 62 | `██████░░░░` |
| Information | 78 | `███████░░░` |

**Tiers:** Financial: Tier 1 (Dominant) · Political: Tier 1 (Dominant) · Military: Tier 3 (Minor)

## Leadership

- **Satya Nadella** — CEO of Microsoft (🔴 Critical)
- **Bill Gates** — Co-founder (🟠 High)

### Bill Gates — Vision

**Archetype:** `Preservationist` · **Confidence:** 89/100  
**Horizon:** 2045

Gates frames 2026 as a critical 5-year window — if current aid cuts continue, damage to global health may be irreversible by 2030. Foundation closes 2045 after committing $200B total. Top AI risk: bioterrorism via open-source models.

> *"An even greater risk than a naturally caused pandemic is that a non-government group will use open-source AI tools to design a bioterrorism weapon"*
> — Gates Notes Annual Letter 2026, 2026-01-09

> *"2026 is a critical five-year window — if aid cuts continue, damage to global health may be irreversible by 2030"*
> — Gates Notes Annual Letter 2026, 2026-01-09

**⚠ Divergence flags:**
- [High] Stated: *Gates Foundation is catalytic innovator — proves what works then scales*
  Observed: Western aid cuts force Foundation into compensatory funding role — mission drift from catalytic to gap-filling

### Satya Nadella — Vision

**Archetype:** `Techno-Realist` · **Confidence:** 87/100  
**Horizon:** generational

Nadella positions Microsoft as the AI platform layer for every enterprise — not an AI lab, but the entity that brings AI to scale via cloud, tools, and agents. OpenAI partnership is the crown jewel. Empowerment mission ("empower every person and organization") provides regulatory cover while pursuing platform dominance.

> *"every company is going to be an AI company"*
> — Davos 2024, 2024-01-16

> *"AI will reshape every software category we know"*
> — Microsoft Build 2023, 2023-05-23

**⚠ Divergence flags:**
- [Low] Stated: *Empowering every person and organization on the planet*
  Observed: Enterprise pricing for Copilot ($30/seat) limits access for SMBs and individuals
- [Medium] Stated: *Open AI ecosystem and responsible AI*
  Observed: OpenAI exclusivity on Azure creates concentration risk; Phi models suggest hedge

## Relations

### Outbound (this entity → others)

| Strength | Target | Type | Description |
|----------|--------|------|-------------|
| 🔴 Critical | **[[OpenAI|OpenAI]]** | `Finances` |  |
| 🟠 High | **[[NVIDIA|NVIDIA]]** | `DependsOn` | Microsoft Azure AI compute fleet depends heavily on NVIDIA H100 and H200 GPUs. T... |
| 🟠 High | **[[Pentagon|Pentagon]]** | `Supplies` | Microsoft is one of four JCCES (Joint Warfighter Cloud Capability) awardees alon... |
| 🟠 High | **[[Amazon|Amazon]]** | `Competes` | Two largest cloud providers by revenue. |
| 🟠 High | **[[Alphabet|Alphabet]]** | `Competes` | Azure vs GCP. Copilot vs Gemini. |
| 🟡 Medium | **[[TSMC|TSMC]]** | `DependsOn` | Microsoft custom AI chips (Maia 100 AI accelerator, Cobalt 100 ARM CPU) manufact... |
| 🟡 Medium | **[[Advanced Micro Devices|Advanced Micro Devices]]** | `Partners` | Azure deploys AMD EPYC processors across multiple VM series. AMD is strategic CP... |
| 🟡 Medium | **[[Apple|Apple]]** | `Partners` | Microsoft 365 and Teams are among top apps on iOS/macOS App Store. Structural co... |
| 🟡 Medium | **[[Anthropic|Anthropic]]** | `Competes` | Microsoft Copilot and Anthropic Claude compete for enterprise AI assistant marke... |

### Inbound (others → this entity)

| Strength | Source | Type | Description |
|----------|--------|------|-------------|
| 🔴 Critical | **[[OpenAI|OpenAI]]** | `DependsOn` |  |
| 🔴 Critical | **[[OpenAI|OpenAI]]** | `Partners` | Microsoft invested $13B in OpenAI. Azure is exclusive cloud. |
| 🔴 Critical | **[[Satya Nadella|Satya Nadella]]** | `Governs` | Satya Nadella pivoted Microsoft to Azure and AI since 2014. |
| 🟠 High | **[[European Commission|European Commission]]** | `Regulates` | EC opened formal Teams antitrust investigation Jun 25, 2024. Microsoft pre-empti... |
| 🟠 High | **[[Federal Trade Commission|Federal Trade Commission]]** | `Regulates` | FTC filed suit Dec 2022 to block $69B Activision acquisition. Lost in US federal... |
| 🟠 High | **[[NVIDIA|NVIDIA]]** | `Supplies` | NVIDIA supplies top client Microsoft for Azure AI. Estimated 15-19% of NVIDIA re... |
| 🟠 High | **[[Vanguard Group|Vanguard Group]]** | `Owns` | Vanguard Group is largest institutional holder of Microsoft at approximately 8.5... |
| 🟠 High | **[[../actors/GATES-Bill|Bill Gates]]** | `Owns` | Bill Gates co-founded Microsoft in 1975. |
| 🟠 High | **[[Oracle|Oracle]]** | `Competes` | Compete in cloud databases and enterprise software. |
| 🟠 High | **[[Unknown|Unknown]]** | `Governs` | Redmond Campus is a HQ facility operated by Microsoft in Redmond |
| 🟠 High | **[[BlackRock|BlackRock]]** | `Owns` |  |
| 🟡 Medium | **[[Unknown|Unknown]]** | `DependsOn` | Quincy Data Center Complex is a DataCenter facility operated by Microsoft in Qui... |
| 🟡 Medium | **[[Unknown|Unknown]]** | `DependsOn` | Dublin Data Center is a DataCenter facility operated by Microsoft in Dublin |
| 🟡 Medium | **[[US Department of Commerce|US Department of Commerce]]** | `Regulates` | BIS AI model export control ANPRM 2024 affects Microsoft/OpenAI model distributi... |
| 🟡 Medium | **[[Apple|Apple]]** | `Partners` | Microsoft 365 (Word, Excel, Teams, Outlook) among top apps on iOS/macOS App Stor... |
| 🟡 Medium | **[[TSMC|TSMC]]** | `Supplies` | Microsoft custom silicon (Maia 100 AI accelerator, Cobalt 100 ARM CPU) manufactu... |
| 🟡 Medium | **[[../institutions/LOCKHEED-MARTIN|Lockheed Martin]]** | `Partners` | Microsoft Azure Government (IL4/IL5 and TS/SCI environments) provides classified... |
| 🟡 Medium | **[[State Street Corporation|State Street Corporation]]** | `Owns` | State Street Corporation holds approximately 3.8% of Microsoft per SEC 13F Q4 20... |
| 🟡 Medium | **[[../actors/GATES-Bill|Bill Gates]]** | `Influences` | Bill Gates co-founded Microsoft 1975. Resigned from board March 2020. Retains ~1... |
| 🟡 Medium | **[[Apple|Apple]]** | `Competes` | Apple increasingly targets enterprise with iPhone+Mac+iPad combo vs Microsoft 36... |

## Recent Events

### 2024-06-25 — European Commission opens formal antitrust investigation into Microsoft Teams
`High` 📉 Negative · Source: European Commission Press Release ✓
[Source](https://ec.europa.eu/commission/presscorner/detail/en/IP_24_3446)

EC opened formal investigation into Microsoft Teams bundling with Microsoft 365 and Office on June 25, 2024. Concerns: tying Teams gives Microsoft unfair advantage over competitors like Slack and Zoom. Microsoft pre-emptively unbundled Teams globally in Oct 2023.

### 2023-11-15 — Microsoft launches Copilot for Microsoft 365 and reveals Maia AI chip
`Critical` 📈 Positive · Source: Microsoft Ignite 2023 ✓
[Source](https://azure.microsoft.com/en-us/blog/microsoft-ignite-2023-ai-infrastructure/)

At Ignite 2023, Microsoft launched Copilot for Microsoft 365 GA ($30/user/month) and unveiled Maia 100 AI accelerator and Cobalt 100 ARM CPU — first custom Azure silicon. Signals long-term NVIDIA GPU dependency reduction strategy.

### 2023-10-13 — Microsoft completes $69B acquisition of Activision Blizzard
`High` 📈 Positive · Source: Microsoft News ✓
[Source](https://news.microsoft.com/2023/10/13/microsoft-completes-acquisition-of-activision-blizzard/)

Microsoft closed $68.7B Activision Blizzard acquisition after UK CMA gave final clearance Oct 13, 2023. FTC injunction request denied in US court July 2023. Largest gaming M&A in history. Added Call of Duty, Candy Crush, Diablo to Game Pass.

### 2023-01-23 — Microsoft commits $10B to OpenAI in landmark AI partnership
`Critical` 📈 Positive · Source: Microsoft News ✓
[Source](https://news.microsoft.com/2023/01/23/microsofts-multibillion-dollar-investment-in-openai-ushers-in-new-era-of-ai/)

Microsoft announced $10B strategic investment in OpenAI extending the 2019 and 2021 partnerships. OpenAI models to power Azure AI services; Azure becomes exclusive cloud provider for OpenAI. Gave Microsoft the core AI asset for Copilot product line.

### 2022-12-07 — DoD awards JCCES cloud contract to Microsoft, Amazon, Google, Oracle
`High` 📈 Positive · Source: US Department of Defense ✓
[Source](https://www.defense.gov/News/Releases/Release/Article/3239378/)

Pentagon awarded Joint Warfighter Cloud Capability (JCCES) contract to four vendors: Microsoft, AWS, Google, Oracle — replacing failed single-vendor JEDI. $9B total ceiling value. Microsoft Azure Government provides classified and unclassified DoD cloud workloads.

---
*Auto-generated from IPMDB on 2026-04-19. Edge count: 29.*
*Composite score: 79/100 | Archetype: HYBRID*