---
title: IMP Power Index System — Six Dimensions, Ten Indexes
type: theme
sources: [raw/IMP_Strategy_v2_2.docx]
related:
  - wiki/themes/IMP-Platform-Architecture.md
  - wiki/themes/IMP-Competitive-Moats.md
created: 2026-04-09
updated: 2026-04-09
confidence: high
---

# IMP Power Index System — Six Dimensions, Ten Indexes

## Summary
The analytical product no competitor offers at any price point. Converts the knowledge graph into quantified intelligence about who controls what and what happens when it changes.

## Six Power Dimensions

| Code | Index | Formula Components | Key Tables |
|---|---|---|---|
| **FPI** | Financial power | AUM × stake% × employees reached × sector × country coverage | RelationEdge.Value, AssetManagers, SWFs |
| **MPI** | Military power | Warheads × personnel × defense budget × cyber × space × nuclear | MilitaryCapacity, CountryEconomy |
| **SPI** | Software power | Enterprise lock-in × critical infra dependencies × switching cost | SoftwareDependencyScore, CompanyProviders |
| **CPI** | Commodity power | Production control × chokepoint dominance × supply risk | CommodityFacility, CommodityChokepoint |
| **PPI** | Political power | Population × GDP × alliance depth × ideology divergence | Countries, IdeologyProfile, CountryRelations |
| **IPI** | Information power | Press freedom × state media × disinfo × internet control × AI | InformationPowerScore |

**Note:** DB column names are full words, NOT abbreviations. Use `FinancialScore`, `MilitaryScore`, `SoftwareScore`, `CommodityScore`, `PoliticalScore`, `InformationScore` — never FPI/MPI/SPI etc. in SQL.

## PersonPowerIndex
Composite score per person = weighted sum of all 6 dimensions. Weights vary by ArchetypeCode.

**Archetypes:** FINANCIAL · POLITICAL · COERCIVE · INDUSTRIAL · TECHNOLOGICAL · HYBRID

**Seeded as of March 2026:**
- Fink (72) · Musk (74) · Huang (68) · Putin (81) · Xi (79) · Powell (62) · Lagarde (58) · Altman (55)
- Trump, MBS, Bessent — seeding pending

## Three Composite Risk Indexes

**GCRI — Global Crisis Risk Index**
`SUM(Severity × Probability × Centrality) / normalization`
EdgeRiskScore aggregate across oil, military, and supply chain edges weighted by node centrality.
Replaces keyword-counting GPR (Caldara-Iacoviello) with causal propagation through typed entity graph.

**DSI — Dollar System Index**
USD share of FX reserves + Treasury ownership trend + petrodollar substitution + BRICS settlement activity + central bank gold accumulation + Powell/Lagarde ideology divergence.
First public composite dollar-erosion signal.

**WPI — War/Peace Index**
Coercive power scores × ideology divergence × active conflict edge count × military spending acceleration.

**GPI — Global Power Index**
Composite of all six sub-indexes. "The public version of what Bridgewater built privately."

## EdgeRiskScore Formula
`EdgeRiskScore = SeverityLevel × BranchProbability`
- Range: 0–5
- Updated every 5 minutes from Polymarket CLOB
- No competitor has this signal at any price point

## DB State (as of April 2026)
- `PersonPowerIndex`: 8 rows seeded (Fink, Musk, Huang, Putin, Xi, Powell, Lagarde, Altman)
- `CompositeIndexSnapshots`: 0 rows — snapshot job not running (B-04 blocker)
- `EdgeRiskScore`: 31 rows — thin, should cover all 1,230+ edges eventually
- `MilitaryCapacity`: 18 rows
- `InformationPowerScore`: 8 rows


## Related Pages
- [[../actors/TRUMP-Donald]]
- [[../actors/PUTIN-Vladimir]]
- [[../actors/XI-Jinping]]
- [[../actors/FINK-Larry]]
- [[../indicators/DB-ID-Reference]]

## Open Questions
- When does the CompositeIndexSnapshots job get fixed? (B-04)
- What is the weighting formula per archetype for PersonPowerIndex composite?
- How does IdeologyProfile divergence translate into PPI contribution?
