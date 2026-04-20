---
title: IMP Product Ideas — Session 2026-03-27
slug: product-ideas-2026-03-27
type: dossier
created: 2026-04-09
updated: 2026-04-09
confidence: medium
sources:
  - raw/internal-notes/IPM_Session_Record_2026_03_27.md
related_actors: [larry-fink, jamie-dimon]
related_countries: []
related_institutions: [blackrock]
related_commodities: []
related_themes: [imp-business-model, imp-competitive-moats]
---

# IMP Product Ideas — Session 2026-03-27

*7 ideas generated in the 2026-03-27 build session. Recorded for compounding reference.*

---

## Idea 1 — Aladdin as a Chokepoint Node
**Status:** PENDING seed in DB

Aladdin (BlackRock's risk OS) manages risk calculations for $21.6T in assets across 200+ institutions. Company node with `IsChokepoint=TRUE`, `SoftwareDependencyScore=98`, `SubstitutionLatencyMonths=120`.

Intelligence story: one algorithm is simultaneously live inside competing funds. If Aladdin's model is wrong, it is wrong for everyone simultaneously. Highest `SoftwareDependencyScore` in the system — software power concentration at civilizational scale.

**Action needed:** Seed Aladdin as Company node in DB.

---

## Idea 2 — Power Dossier
**Status:** Defined, not built. Phase 2 feature.

Auto-generated single-page intelligence brief per entity. 8 sections:
1. Header (name / archetype / score / rank)
2. Reach metrics (AUM / population / employees)
3. Power profile (radar chart 6 axes)
4. Ideology (7-axis slider)
5. Graph position (edge breakdown by type)
6. Intelligence signals (last 3 NewsEvents + Timelines)
7. Risk flags
8. AI narrative (3 paragraphs from Claude API from DB fields)

Tier: Pro $49/month. Moat: Bloomberg shows Fink's AUM. IMP tells you what his power means, how it flows through the graph, and what the timelines say about where it goes next.

---

## Idea 3 — Power Velocity
**Status:** Defined, not built.

PersonPowerIndex is append-only (multiple rows per person at different `ComputedAt` timestamps). Query the delta between latest and previous row:
- `ScoreDelta`
- `RankDelta`
- `PowerTrajectory`: RISING / FALLING / STABLE

Shows who is gaining power and through which specific dimension. Identifies emerging nodes before the world notices. More commercially valuable than static ranking.

---

## Idea 4 — igreedmap.com as Invisible Hand Tracker
**Status:** Domain owned. Not built.

Free, single-purpose viral tool. User enters any event (war, bailout, rate hike, disaster). Platform traces through the ownership/finance graph and shows who actually benefits. Powered by `OilImpactRanking` + `RelationEdge` traversal. Drives traffic to IPM for the full intelligence picture.

---

## Idea 5 — Celonis Partnership (Oliver Mieth)
**Status:** Identified, not pursued.

Three angles:
1. Celonis enterprise clients as IPM Observatory/enterprise tier targets
2. Celonis process mining data as IPM supply chain signal source (supplier switching patterns = early geopolitical signal)
3. Joint pitch: "Celonis for internal process intelligence, IPM for external power intelligence"

Ask Oliver: "Which of your enterprise clients has the most exposure to geopolitical supply chain risk right now?"

---

## Idea 6 — DSI as a Standalone Product
**Status:** DSI table exists. Not yet marketed as standalone.

Dollar System Index = COFER + TIC + BIS + WGC + Fed/ECB ideology divergence → single 0-100 scalar.

No public equivalent exists. Commercial target: macro hedge funds, EM debt managers, FX desks. Methodologically novel vs GPR (graph-propagated vs keyword-counting). First public composite dollar-erosion signal.

---

## Idea 7 — Corporate Domain Strategy
**Status:** Deferred until Series A or first enterprise contract.

Candidate: `atlasint.com` or `atlasintelligence.com` — institutional feel, connects to Atlas brand universe. Not needed today. `ipowermap.com` covers everything for now.
