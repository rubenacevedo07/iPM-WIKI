---
entity_id: 5
ticker: AMZN
archetype: HYBRID
composite_score: 94.00
last_updated: 2026-04-19
source: ipm_db_auto_generated
aliases: [Amazon, AMZN]
tags: [ipm-entity, hybrid]
---

# Amazon

> **Hybrid power — crosses multiple power dimensions simultaneously.** Composite power score: **94/100** (rising trend). Country: United States.

## Power Index

**Archetype:** `HYBRID`  
**Composite:** █████████░ 94/100  
**Trend:** rising

| Dimension | Score | Bar |
|-----------|------:|-----|
| Financial | 97 | `█████████░` |
| Military | 45 | `████░░░░░░` |
| Political | 88 | `████████░░` |
| Technological | 94 | `█████████░` |
| Industrial | 93 | `█████████░` |
| Information | 95 | `█████████░` |

**Tiers:** Financial: Tier 1 (Dominant) · Political: Tier 1 (Dominant) · Military: Tier 2 (Significant)

## Leadership

- **Andy Jassy** — CEO of Amazon (🔴 Critical)
- **Jeff Bezos** — Founder & Executive Chairman (🟠 High)

### Jeff Bezos — Vision

**Archetype:** `Expansionist` · **Confidence:** 90/100  
**Horizon:** generational

Bezos conceptualized Amazon as a platform that can enter almost any industry where technology and logistics can be applied — relentlessly extending reach into new sectors while sacrificing short-term profits for long-term dominance. As Executive Chairman his expansionist vision operates at planetary scale: Blue Origin aims to industrialize space, the Bezos Earth Fund targets climate change, and his ownership of The Washington Post gives him indirect political influence. His Day 1 philosophy — perpetual invention and customer obsession — remains the foundational DNA of Amazon even as Jassy executes it operationally.

> *"It remains Day 1."*
> — Jeff Bezos 2016 Letter to Shareholders, 2017-04-12

> *"We are willing to be misunderstood for long periods of time."*
> — Jeff Bezos shareholder letter on long-term thinking, 2013-04-12

**⚠ Divergence flags:**
- [High] Stated: *Amazon's growth is aligned with customer obsession and societal benefit.*
  Observed: Regulators and critics argue Amazon's market power harms small sellers, workers, and competitors — major antitrust and labor actions ongoing in US and EU.
- [Medium] Stated: *Day 1 culture of relentless experimentation.*
  Observed: Under Jassy, Amazon pulled back from experimental bets (devices, healthcare) and prioritized cost-cutting — partial retreat from Bezos's expand-everywhere philosophy.

### Andy Jassy — Vision

**Archetype:** `Techno-Realist` · **Confidence:** 86/100  
**Horizon:** generational

Jassy has transitioned Amazon from Bezos's expansion-at-all-costs model to rigorous cost discipline combined with AI-centric infrastructure investment. He views AWS Bedrock and custom silicon (Trainium/Inferentia) as the keys to defending cloud dominance against Microsoft/OpenAI. His vision focuses on turning every Amazon vertical — logistics, advertising, healthcare — into a high-margin data business powered by AI. Pragmatic about competitive pressure: willing to absorb short-term margin pressure for long-term infrastructure positioning.

> *"Generative AI may be the largest technology transformation since the cloud, and perhaps since the internet."*
> — Amazon 2023 Shareholder Letter, 2024-04-11

> *"We are still in the very early stages of generative AI and we believe that much of this business will be built on top of AWS."*
> — Amazon Q3 2024 Earnings Call, 2024-10-30

**⚠ Divergence flags:**
- [Medium] Stated: *AI and infrastructure investments are disciplined and will generate strong long-term returns.*
  Observed: ~$75B capex in 2024 and projected $200B in 2026 are historically unprecedented levels — raising execution and regulatory risk as AWS faces stronger competition from Microsoft and Google.
- [Medium] Stated: *AWS is a neutral, secure cloud partner for all governments and enterprises.*
  Observed: AWS's role in defense and intelligence combined with market dominance has triggered regulatory pushback in US and UK over cloud concentration.

## Relations

### Outbound (this entity → others)

| Strength | Target | Type | Description |
|----------|--------|------|-------------|
| 🔴 Critical | **[[Anthropic|Anthropic]]** | `Finances` |  |
| 🟠 High | **[[NVIDIA|NVIDIA]]** | `DependsOn` | Amazon AWS deploys large NVIDIA GPU clusters for EC2 P-instances. Developing Tra... |
| 🟠 High | **[[Alphabet|Alphabet]]** | `Competes` | AWS vs Google Cloud in cloud (31% vs 11% share). Amazon Ads vs Google Search Ads... |
| 🟠 High | **[[Pentagon|Pentagon]]** | `Supplies` | AWS is one of four vendors in JCCES (Joint Warfighter Cloud Capability) alongsid... |
| 🟠 High | **[[OpenAI|OpenAI]]** | `Competes` | OpenAI's GPT-4/o models via Azure/Microsoft compete directly with Amazon Bedrock... |
| 🟡 Medium | **[[TSMC|TSMC]]** | `DependsOn` | Amazon custom silicon (Graviton CPU, Trainium AI accelerator, Inferentia inferen... |

### Inbound (others → this entity)

| Strength | Source | Type | Description |
|----------|--------|------|-------------|
| 🔴 Critical | **[[Anthropic|Anthropic]]** | `DependsOn` |  |
| 🔴 Critical | **[[Andy Jassy|Andy Jassy]]** | `Governs` | Andy Jassy succeeded Jeff Bezos in July 2021. |
| 🟠 High | **[[European Commission|European Commission]]** | `Regulates` | EC designated Amazon as DMA gatekeeper Sep 6, 2023 covering marketplace, ads, an... |
| 🟠 High | **[[Federal Trade Commission|Federal Trade Commission]]** | `Regulates` | FTC filed landmark antitrust suit Sep 26, 2023 targeting Amazon's marketplace mo... |
| 🟠 High | **[[NVIDIA|NVIDIA]]** | `Supplies` | NVIDIA supplies AWS for Anthropic hosting, SageMaker AI, and EC2 GPU instances. ... |
| 🟠 High | **[[Vanguard Group|Vanguard Group]]** | `Owns` | Vanguard Group is Amazon's largest institutional shareholder at approximately 7.... |
| 🟠 High | **[[Oracle|Oracle]]** | `Partners` | Oracle databases available as managed service on AWS. |
| 🟠 High | **[[../actors/BEZOS-Jeff|Jeff Bezos]]** | `Influences` | Bezos founded Amazon in 1994, served as CEO until July 2021, now Executive Chair... |
| 🟠 High | **[[BlackRock|BlackRock]]** | `Owns` |  |
| 🟠 High | **[[../companies/201_spacex|SpaceX]]** | `Competes` | SpaceX Starlink (6,000+ satellites, 4M+ subscribers, $8B ARR) vs Amazon Project ... |
| 🟠 High | **[[../actors/BEZOS-Jeff|Jeff Bezos]]** | `Owns` | Jeff Bezos founded Amazon in 1994. Executive chairman and largest shareholder. |
| 🟠 High | **[[Anthropic|Anthropic]]** | `Partners` | Amazon invested up to $4B. AWS is primary cloud. |
| 🟠 High | **[[Microsoft|Microsoft]]** | `Competes` | Two largest cloud providers by revenue. |
| 🟡 Medium | **«entidad no resuelta»** | `DependsOn` | Amazon AWS Data Center Cluster is a DataCenter facility operated by Amazon in As... |
| 🟡 Medium | **[[State Street Corporation|State Street Corporation]]** | `Owns` | State Street Corporation holds approximately 3.4% of Amazon via index ETFs per S... |
| 🟡 Medium | **«entidad no resuelta»** | `Distributes` | JFK8 Fulfillment Center is a Logistics facility operated by Amazon in Staten Isl... |
| 🟡 Medium | **«entidad no resuelta»** | `Distributes` | Amazon BFI4 Fulfillment Center is a Logistics facility operated by Amazon in Ken... |

## Recent Events

### 2026-04-09 — Amazon plans $200B capex in 2026 for AI data centers — Jassy calls it generational bet
`Critical` 📈 Positive · Source: Investing.com / Andy Jassy Shareholder Letter ✓
[Source](https://uk.investing.com/news/stock-market-news/amazon-ceo-jassy-outlines-ai-investment-strategy-expects-200b-capex-in-2026-93CH-3792900)

Andy Jassy told shareholders April 9, 2026 that Amazon plans ~$200B in capital expenditures in 2026, primarily on AI data centers, custom silicon, and networking. AWS AI revenue run rate surpassed $15B with Trainium/Graviton growing triple digits. Largest single-year corporate AI infrastructure commitment globally — signals Amazon's intent to match or exceed Microsoft in AI cloud infrastructure.

### 2025-09-24 — FTC secures historic $2.5B settlement against Amazon over deceptive Prime practices
`High` 📉 Negative · Source: Federal Trade Commission ✓
[Source](https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-secures-historic-25-billion-settlement-against-amazon)

FTC announced $2.5B settlement with Amazon on September 24, 2025 — $1B in civil penalties and $1.5B in consumer refunds — over allegations that Amazon enrolled millions of consumers in Prime without consent and made cancellation deliberately difficult. Requires Amazon to overhaul Prime enrollment and cancellation flows. Largest FTC consumer protection settlement ever.

### 2025-02-01 — Amazon FY2024: $638B revenue, $108B AWS — net income nearly doubles to $59B
`Critical` 📈 Positive · Source: Yahoo Finance / Amazon Earnings ✓
[Source](https://finance.yahoo.com/news/amazon-com-full-2024-earnings-113517187.html)

Amazon reported FY2024 revenue of $638B (+11% YoY) with AWS at $108B (+19%). Net income nearly doubled to $59.2B with operating margin ~10-11%. AWS and advertising are the primary profit engines. Results confirm the post-2022 efficiency pivot succeeded — Amazon became a margin-expansion story alongside a growth story.

### 2024-10-06 — Amazon begins Project Kuiper satellite constellation deployment
`High` 📈 Positive · Source: Bloomberg ✓

Amazon began deploying its Project Kuiper low-Earth orbit satellite constellation in October 2024 to compete with SpaceX Starlink and provide global broadband connectivity. Kuiper serves dual purpose: extend AWS reach into connectivity infrastructure and provide global internet access. $10B+ investment; directly competes with Starlink for enterprise, government, and underserved markets.

### 2024-03-27 — Amazon expands Anthropic partnership with $4B investment, makes AWS primary cloud
`Critical` 📈 Positive · Source: About Amazon ✓
[Source](https://www.aboutamazon.com/news/company-news/amazon-anthropic-expand-strategic-collaboration)

Amazon committed up to $4B to Anthropic and designated AWS as Anthropic's primary cloud provider on March 27, 2024 (a follow-on to the initial $1.25B in Sep 2023). Anthropic's Claude models integrated into Amazon Bedrock. Combined ~$8B total commitment makes Amazon the largest single investor in a frontier AI lab — Amazon's strategic counterweight to Microsoft/OpenAI.

### 2023-09-26 — FTC sues Amazon for illegally maintaining monopoly in online marketplace
`Critical` 📉 Negative · Source: Federal Trade Commission ✓
[Source](https://www.ftc.gov/news-events/news/press-releases/2023/09/ftc-sues-amazon-illegally-maintain-monopoly-power)

FTC and 17 state AGs filed antitrust lawsuit September 26, 2023 alleging Amazon uses anti-discounting and coercive tactics to maintain marketplace monopoly. Targets Prime bundling, self-preferencing in search results, and seller fee structures. Could force structural remedies threatening Amazon's flywheel. Largest antitrust action against Amazon to date.

### 2022-12-07 — DoD awards JCCES cloud contract to Microsoft, Amazon, Google, Oracle
`High` 📈 Positive · Source: US Department of Defense ✓
[Source](https://www.defense.gov/News/Releases/Release/Article/3239378/)

Pentagon awarded Joint Warfighter Cloud Capability (JCCES) contract to four vendors: Microsoft, AWS, Google, Oracle — replacing failed single-vendor JEDI. $9B total ceiling value. Microsoft Azure Government provides classified and unclassified DoD cloud workloads.

---
*Auto-generated from IPMDB on 2026-04-19. Edge count: 23.*
*Composite score: 94/100 | Archetype: HYBRID*