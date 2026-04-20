---
title: IMP Platform Architecture — Five Layers
type: theme
sources: [raw/IMP_Strategy_v2_2.docx]
related:
  - wiki/themes/IMP-Automation-Engine.md
  - wiki/themes/IMP-Oracle-System.md
  - wiki/themes/IMP-Power-Index-System.md
  - wiki/themes/IMP-Competitive-Moats.md
created: 2026-04-09
updated: 2026-04-09
confidence: high
---

# IMP Platform Architecture — Five Layers

## Summary
IMP is built in five sequential layers. Each layer depends on the one below it. No layer can be skipped. The architecture converts raw geopolitical reality into actionable intelligence signals.

## Layer 1 — Reality Layer · The Knowledge Graph
The irreplaceable asset. 18-month build. A competitor starting today cannot fast-follow.

- 82 PostgreSQL tables (95+ as of April 2026)
- 1,230+ typed, weighted, verified edges
- 458 persons, 100+ companies, 50+ countries, 30+ commodities
- **GraphNode types:** Company, Person, Country, Commodity, AssetManager, Bank, ETF, Sector, SWF, Facility
- **GraphEdge types:** Governs, Owns, Influences, Finances, Sanctions, MilitaryConflict, Supplies, DependsOn, Partners
- **GraphEdgeWithTimelines:** every edge shows open prediction timelines + aggregate EdgeRiskScore
- **7 Chokepoints:** Hormuz · Malacca · Suez · Taiwan Strait · Black Sea · Bab el-Mandeb · Panama

## Layer 2 — Social Intelligence Layer
The community prediction and validation layer. Fundamental unit = relationship between entities, not content.

- Predictions anchored to specific graph edges (e.g. "NVIDIA → depends_on → TSMC will break within 6 months")
- Community probability aggregation ranked by verified Analyst Score
- Analyst Score backed by real Polymarket P&L and Brier score accuracy — not self-reported
- Sentiment and risk signals per relationship — not per article

## Layer 3 — Simulation & Timeline Layer
"What if X happens?" modeled as binary outcome Timelines backed by real USDC via Polymarket CLOB.

- Branch A vs B probability: live Polymarket CLOB midpoint
- Probability sparkline: 30-day history of belief
- Market confidence: CLOB spread (tight = high conviction)
- Open interest in USDC backing each branch
- IMP earns 0.5% builder fee on every CLOB order placed

**Sub-tools:**
- Cascade Simulator: pick any edge, walk 3 hops downstream
- Scenario Diff Viewer: Branch A vs B side by side, affected edges colored
- Butterfly Effect Engine: remove any decision node, watch cascade animate
- Invisible Hand Tracker: follow event to true beneficiaries through ownership edges

## Layer 4 — Personal Workspace
The user's thesis made structural.

- Personal PowerMap: custom graph with selected entities
- Personal Timelines: Free tier 2 max · Analyst tier unlimited
- Alerts via SignalR: fire when branch probability crosses threshold
- Strategy Lab: backtesting conditioned on graph state (Pro tier)
- Portfolio Exposure Map: holdings mapped to graph nodes showing structural risk

## Layer 5 — Enterprise Automation Engine
What makes IMP self-sustaining. See [[IMP-Automation-Engine.md]].

Protocol: IMP_ENVELOPE v1 — Perplexity (collects) + Claude (structures) + n8n (orchestrates)

## Key Architectural Principle
> "Without the automation engine, IMP is a read-only intelligence tool. With it, IMP is a living, self-updating intelligence system."

## Open Questions
- When does pgvector semantic search get added for natural language queries over accumulated intelligence?
- GNN upgrade evaluation (Apache AGE) planned for Phase 4 — what triggers the decision?
