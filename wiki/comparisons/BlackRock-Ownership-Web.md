---
title: BlackRock Ownership Web
slug: blackrock-ownership-web
type: comparison
created: 2026-04-09
updated: 2026-04-09
confidence: medium
sources: []
related_actors: [larry-fink]
related_countries: [united-states, taiwan, saudi-arabia]
related_institutions: [blackrock, nvidia, apple, microsoft, amazon, alphabet, meta, tesla, exxonmobil, lockheed-martin, jpmorgan, goldman-sachs, samsung, asml, tsmc, saudi-aramco]
related_commodities: [oil, semiconductors]
related_themes: [global-liquidity, financial-stability, imp-competitive-moats]
---

# BlackRock Ownership Web

*The Invisible Hand Tracker seed page. BlackRock (~$10T AUM) holds significant positions
in virtually every strategically important company in the IMP graph.*

**Key insight:** BlackRock doesn't just own financial assets — it owns structural chokepoints.
NVIDIA (AI chips), TSMC (semiconductors), ASML (lithography), ExxonMobil (energy),
Lockheed Martin (defense). When any geopolitical event moves through the IMP graph,
trace the blast radius through BlackRock's positions to find the true beneficiary.

---

## Technology & AI Cluster

| Company | DB ID | Strategic Significance | BlackRock Exposure |
|---------|-------|----------------------|--------------------|
| [[../institutions/APPLE]] | 2 | Largest consumer tech co. Supply chain China-dependent. | Top holding ~6-7% |
| [[../institutions/MICROSOFT]] | 4 | Cloud (Azure) + OpenAI partner. CUDA competitor via Azure AI. | Top holding ~5-6% |
| [[../institutions/NVIDIA]] | 1 | AI chip monopoly. GPU supply = AI infrastructure chokepoint. | Major position |
| [[../institutions/ALPHABET]] | 3 | Search + cloud + DeepMind. Ad revenue = digital economy signal. | Top holding |
| [[../institutions/META]] | 6 | Social graph + Llama AI. 3B+ users. | Top holding |
| [[../institutions/AMAZON]] | 5 | AWS cloud + logistics. Critical digital infrastructure. | Top holding |
| [[../institutions/TESLA]] | 7 | EV + battery + energy storage. Musk HYBRID archetype. | Significant position |
| [[../institutions/OPENAI]] | 198 | Frontier AI. Microsoft partnership. | Indirect via Microsoft |

## Semiconductor Chokepoint Cluster

| Company | DB ID | Strategic Significance | BlackRock Exposure |
|---------|-------|----------------------|--------------------|
| [[../institutions/TSMC]] | 41 | World's most critical fab. Taiwan Strait risk = 8. | Significant position |
| [[../institutions/ASML]] | 21 | Only maker of EUV lithography machines. Irreplaceable. | European exposure |
| [[../institutions/SAMSUNG]] | 43 | DRAM + NAND + foundry. Korean strategic asset. | Asian exposure |

## Financial Cluster

| Company | DB ID | Strategic Significance | BlackRock Exposure |
|---------|-------|----------------------|--------------------|
| [[../institutions/JPMORGAN]] | 12 | Largest US bank. Dimon→USA: 9 open timelines. | Significant position |
| [[../institutions/GOLDMAN-SACHS]] | 63 | Investment banking. Sanctions + M&A intelligence. | Significant position |

## Energy & Defense Cluster

| Company | DB ID | Strategic Significance | BlackRock Exposure |
|---------|-------|----------------------|--------------------|
| [[../institutions/EXXONMOBIL]] | 14 | Largest Western oil major. Hormuz exposure. | Major position |
| [[../institutions/SAUDI-ARAMCO]] | 42 | World's largest oil company. Saudi state = MBS power. | Indirect via Aramco float |
| [[../institutions/LOCKHEED-MARTIN]] | 68 | F-35, hypersonics, missile defense. Defense budget signal. | Significant position |

---

## The Aladdin Layer

Beyond equity ownership, BlackRock's **Aladdin** platform manages risk for $20T+
across 200+ competing institutions — including many that hold these same assets.

```
IMP DB: Companies.IsChokepoint = TRUE
        SoftwareDependencyScore = 98
        SubstitutionLatencyMonths = 120
```

When a geopolitical event hits — Hormuz closure, Taiwan Strait escalation, Fed rate
surprise — Aladdin's risk model fires simultaneously inside BlackRock **and** inside
its competitors. If Aladdin's model is wrong, it is wrong for everyone at the same time.
This is software power concentration at civilizational scale.

---

## Invisible Hand Tracker — Example Trace

**Event:** Iran closes Hormuz (threat score 10)

```
Hormuz closure
  → ExxonMobil supply disruption      → BlackRock ExxonMobil position ↓
  → Saudi Aramco production benefit   → BlackRock Aramco indirect ↑
  → AIRLINES sector −88               → BlackRock airline ETF exposure ↓
  → Defense spending acceleration     → BlackRock Lockheed Martin ↑
  → Oil price spike → inflation       → BlackRock Fed rate path repricing
  → Aladdin risk model triggers       → 200+ institutions rebalance simultaneously
  → Net: BlackRock hedged across the entire cascade
```

No single entity benefits more from geopolitical volatility than the one that
owns all sides of every trade and runs the risk model for the entire market.

---

## Related Pages
- [[../actors/FINK-Larry]]
- [[../institutions/BLACKROCK]]
- [[../themes/Chokepoint-Intelligence]]
- [[../themes/IMP-Competitive-Moats]]
- [[../dossiers/Product-Ideas-2026-03-27]]

## DB Sync Notes
- BlackRock equity stakes not yet modeled as RelationEdge rows in DB
- Suggested edge type: `Owns` with `Value` = estimated stake %
- This page uses known public positions — source a 13F filing for precise figures
- **DB SYNC NEEDED:** Add BlackRock→Owns→NVIDIA, TSMC, ASML, ExxonMobil, Lockheed as RelationEdge rows

## Open Questions
- What are BlackRock's current top 10 positions by % stake from latest 13F?
- Does Aladdin have a specific CompanyId in the DB yet? (Pending seed)
- How does BlackRock's ownership web change after a major geopolitical shock?
