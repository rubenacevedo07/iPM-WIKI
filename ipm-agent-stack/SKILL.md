---
name: ipm-agent-stack
description: Canonical reference for the IPM 8-agent system (Atlas + Memo + Argus + Helios + Nomos + Cassandra + Aegis + Janus), model selection doctrine, hybrid graph layer (explicit RelationEdge + KNN semantic + Louvain communities), Karpathy-wiki memory substrate, Calibration Moat tables, and MCP permission architecture. Load this skill whenever discussing: IPM agent roles, which LLM to use for which task, Llama vs Claude vs DeepSeek tradeoffs, embedding model selection, hybrid graph implementation, KNN + Louvain pipeline, wiki structure, Karpathy-style memory, Atlas orchestration, subagent reasoning patterns, PredictionLog architecture, BrainScorecard design, OpenClaw workspace design, n8n night loops, MCP server permissions, local-vs-API model decisions, or 5-year intelligence platform roadmap. Also trigger on: "qué modelo uso para X", "cómo funciona el agente Y", "cómo se integra KNN con los brains", "arquitectura agentes IPM", "razonamiento de Nomos/Helios/Cassandra", "memoria wiki-karpathy", "pgvector IPM", "embeddings IPM", "night loops IPM", "cost hardware local IPM", "revenue streams IPM". This is the authoritative agent architecture document for IPM — load it before making any design decision about how agents reason, remember, or interact.
---

# IPM Agent Stack Architecture — Canonical Reference

This skill defines **how the 8 canonical IPM agents are constructed**, what models power each one, how memory and reasoning flow through the system, and where the hybrid graph layer (KNN + Louvain + explicit edges) enhances agent capabilities.

## Scope boundaries

This skill covers:
- The 8-agent canonical system (Atlas, Memo, Argus, Helios, Nomos, Cassandra, Aegis, Janus)
- Model selection per task tier
- Hybrid graph layer integration (explicit + semantic KNN + Louvain communities)
- Memory architecture (Karpathy wiki + PostgreSQL structured state + pgvector)
- MCP permission architecture and OpenClaw workspace design
- 5-year capability roadmap

This skill does NOT cover:
- Frontend implementation (see `ipm-frontend`, `ipm-frontend-design-system`)
- Specific trading signal logic (see `ipm-ideology-trading`, `ipm-eurusd-autoresearch`)
- Database schema details (see `ipm-database`)
- Strategic prioritization (see `ipm-project-state`)

## The 8 Canonical Agents

Each agent is a **specialist role** in the IPM reasoning system. Together they form the Calibration Moat runtime. Each has a defined model, memory access, write permissions, and reasoning pattern.

For deep per-agent specifications, see **references/agents/**.

### Quick map

| Agent | Role | Primary Model | Memory Access | Write Scope |
|-------|------|---------------|---------------|-------------|
| **Atlas** | Meta-orchestrator | Claude Opus 4.7 | Full read (via MCP ro) | IntelligenceOrder, ExecutiveBrief |
| **Memo** | Wiki curator + doctrine compiler | Claude Opus 4.7 | Full wiki + DB | BrainLessonCandidate, IPMWiki, staging notes |
| **Argus** | Event watcher + ingestion | Llama 3.3 70B (local) | NewsEvent, Timeline, feeds | NewsEvent, CentralBankToneLog, GeoMacroFusionLog |
| **Helios** | Geo-macro synthesis | Claude Opus 4.7 | NewsEvent, MarketData, SIPRI | GeoMacroFusionLog, CompositeIndexSnapshots |
| **Nomos** | Scenario → prediction translator | Claude Opus 4.7 | IdeologyProfile, EdgeRiskScore, graph | PredictionLog, ExperimentLog, TradeSignal |
| **Cassandra** | Precedent search + stress-testing | DeepSeek R1 (local) + Opus for final | PredictionLog, GeoMacro, wiki, Timeline | ExperimentLog, ScenarioCascade |
| **Aegis** | Risk gate + kill-switch | Llama 3.3 70B (local) | TradeSignal, BacktestResult, risk_state | TradeSignal (veto only), IntelligenceOrder |
| **Janus** | Evaluation + doctrine promotion | Claude Opus 4.7 (hard calls) + Llama 3.3 (batch) | All resolution + history | BrainScorecard, BrainLessonPromotion, OracleWeightSnapshot |

### Atlas — Meta-orchestrator

Atlas is NOT a chatbot. Atlas is a **routing + synthesis + state-awareness layer**.

**When Atlas is invoked:**
- User submits `IntelligenceOrder` via UI
- Scheduled morning brief trigger fires
- Subagent completion triggers synthesis

**What Atlas does:**
1. Reads the `IntelligenceOrder` payload
2. Decomposes into subtasks (ingest? synthesize? predict? validate?)
3. Routes each subtask to appropriate subagents via MCP calls
4. Waits for subagent outputs
5. Synthesizes into structured brief using Atlas v1 output schema (identity card, entity snapshot, live market context, EventExchange, graph intelligence, narrative signals, causal analysis, strategic positioning, bottom line, what to watch next)
6. Returns brief + triggers doctrine promotion check (→ Janus) if new lessons emerge

**Atlas does NOT:**
- Execute trades (defers to Aegis for risk approval, then user-controlled execution)
- Promote doctrine (defers to Janus)
- Write raw SQL (uses `mcp-ipm-postgres-rw-lite` only)
- Fabricate data (marks unavailable tools explicitly)

**Model: Claude Opus 4.7 (API)**
- Reasoning requirement: highest. Atlas must handle edge cases, maintain Atlas voice, respect hard rules.
- Context window usage: large (subagent outputs + grafo subgraph + historical context). 500K+ tokens justified.
- Cost: ~$0.20-0.50 per orchestration call. 50 calls/day = $10-25/day = $300-750/mo.
- Trade-off accepted: API dependency for the quality ceiling.

**Atlas reasoning pattern** (canonical):
```
1. ingest_context (read structured state via MCP ro)
2. extract_narrative_and_geo_signals (identify what's salient)
3. convert_to_structured_scores (map to IPM ontology)
4. test_if_prediction_worthy (classification ladder)
5. seal_prediction_if_threshold_met (PredictionLog via mcp-rw-lite)
6. store_artifacts_in_moat_tables_or_memory_staging
7. wait_for_resolution (no premature learning)
8. learn_only_from_scored_history
```

### Memo — Wiki curator + doctrine compiler

Memo is the **keeper of durable memory**. It ensures that everything the system learns becomes reusable across sessions.

**Responsibilities:**
- Write new wiki pages for entities, events, scenarios, narratives when Atlas/Nomos/Cassandra produce insights
- Maintain frontmatter (slug, db_id, archetype, related_entities, scores, flags)
- Update wikilinks bidirectionally (if Page A links to Page B, Page B must back-link)
- Compile `BrainLessonCandidate` rows from recurring patterns across predictions
- Keep staging notes for "almost-promoted" ideas
- Enforce template consistency (actors, countries, institutions, commodities, themes, timelines, scenarios, etc.)

**What triggers Memo:**
- Subagent produces content that merits durable storage
- Scheduled wiki-coherence audit (weekly)
- Janus promotes a lesson → Memo must write it to doctrine pages

**Memory model**: Karpathy-style wiki
- Markdown files with strict frontmatter schema
- Bidirectional wikilinks form the graph substrate
- Machine-readable structure (frontmatter) + human-readable body
- Version controlled (git)
- Accumulates across runs; never ephemeral

**Model: Claude Opus 4.7**
- Requirement: excellent at following strict templates + preserving subtle context + generating clean markdown
- Usage: ~10-20 calls/day (not continuous). $1-3/day.

### Argus — Event watcher + ingestion

Argus is the **sensory layer**. Runs continuously, ingests data, extracts entities, flags novel events.

**Responsibilities:**
- Monitor news feeds (financial + geopolitical), speech transcripts, calendar items
- Extract entities (persons, companies, countries, commodities)
- Classify events (central bank communication, regulatory decision, geopolitical crisis, earnings)
- Insert `NewsEvent` rows with structured fields
- Compute preliminary `OfficialToneScore` on speech texts
- Flag anomalies (event affecting high-centrality nodes in the graph)

**What triggers Argus:**
- Continuous polling (every 10-30 min)
- Webhook on new speech published (Fed, ECB, BoJ, BoE)
- Market event signal (flash move + news correlation)

**Model: Llama 3.3 70B local (night) + small classifier models**
- Volume is high (hundreds of events/day). API cost would be prohibitive.
- Entity extraction + classification = commodity task, local models suffice (>90% accuracy)
- For ambiguous cases, escalate to Claude Opus via MCP
- Cost: hardware amortized + $50-100/mo occasional Opus fallback

### Helios — Geo-macro synthesis

Helios translates **geopolitical events into structured macro pressure**. Core of the GeoMacroFusionLog.

**Responsibilities:**
- Read new `NewsEvent` flagged as geopolitical
- Compute `GeoSeverity` (0-10 scale, bucketed)
- Evaluate four channels: EnergyExposureScore, FiscalImpulseRisk, WarBurdenInflationRisk, SupplyShockPersistence
- Determine if economic-review trigger should fire (threshold-based)
- Write `GeoMacroFusionLog` row + update `CompositeIndexSnapshots` pressure fields
- Link affected `MarketSymbol` IDs in JSON array

**What triggers Helios:**
- New `NewsEvent` with geopolitical classification from Argus
- Scheduled SIPRI refresh (quarterly)
- Manual `IntelligenceOrder` requesting geo analysis

**Model: Claude Opus 4.7**
- Requirement: sophisticated causal reasoning (how does conflict X → commodity Y → inflation Z?)
- Requirement: historical context + precedent awareness (1973 oil crisis, 2022 Ukraine gas shock)
- Volume moderate: 5-20 analyses/day. Cost: $2-10/day.

**Hybrid graph integration:**
- Helios reads `community` membership of affected nodes
- If event hits a bridge node (high betweenness), propagation analysis extends across communities
- Example: Ukraine war hits "European Energy" cluster AND "Agriculture Commodities" cluster (via Russia-wheat bridge)

### Nomos — Scenario → prediction translator

Nomos is the **forecast producer**. Where other agents analyze, Nomos commits.

**Responsibilities:**
- Read scenario context (from Atlas, Helios, Cassandra)
- Generate probability distribution for N possible outcomes
- Convert selected scenarios to `PredictionLog` rows with: probability, horizon, market symbol, regime label, trigger, confidence interval, narrative context (OfficialToneScore, InterpretationGap, GeoSeverity), entity links
- Classification ladder: ensure item has passed Commentary → Watchlist → Hypothesis gates before PredictionLog seal
- Link predictions to trade signals where applicable (via `TradeSignal` with GraphProvenance)

**What triggers Nomos:**
- Scheduled `prediction_log_sealing` at 04:00 (n8n workflow)
- InterpretationGapLog threshold exceeded (>= 0.35 + market confirmation)
- Manual IntelligenceOrder requesting forecast

**Model: Claude Opus 4.7 (critical calls) + Llama 3.3 70B (batch sampling)**
- Critical requirement: **calibration awareness**. Nomos must be Brier-minimizing, not confidence-maximizing.
- Requirement: structured output (JSON matching PredictionLog schema exactly)
- Requirement: regime conditioning (prediction probability depends on regime)
- Hybrid approach: Opus for sensitive predictions (Fed decisions, geopolitical), Llama for batch Monte Carlo scenario sampling

**Hybrid graph integration:**
- Nomos queries the graph for `semantic_neighbors` of affected entities
- Predictions include graph context: "P(NVIDIA down 15% | bridge score > 0.7 AND active Taiwan timelines >= 2 AND interpretation gap in US tech policy > 0.3)"
- Community migration detection: if NVIDIA migrates from "AI Compute" cluster to "Geopolitical Risk" cluster, update prediction priors

### Cassandra — Precedent search + stress-testing

Cassandra is the **skeptic**. For every scenario, finds the strongest historical analog, validates or invalidates.

**Responsibilities:**
- Take Nomos scenario drafts or Helios hypotheses
- Query wiki + `Timeline` + `PredictionResolutionLog` for historical analogs
- Compute similarity: semantic (via embeddings) + structural (via graph topology)
- Stress-test: "If this scenario is correct, we should see X. Do we see X? If not, why not?"
- Write `ExperimentLog` entries with `BrainOrigin='Cassandra'`, validation window summary
- Write `ScenarioCascade` rows if scenario is validated

**What triggers Cassandra:**
- Scheduled `precedent_retrieval_and_hypothesis_generation` at 02:00
- New scenario from Nomos needs validation before PredictionLog seal
- Anomaly detected: unexpected cluster co-occurrence (hybrid graph layer trigger)

**Model: DeepSeek R1 (local, batch) + Claude Opus 4.7 (final synthesis)**
- Reasoning requirement: causal chain generation + counterfactual thinking. DeepSeek R1 excels here.
- Volume high for batch analog searches (hundreds of precedents scanned)
- Opus for final "is this precedent actually analogous?" call

**Hybrid graph integration — Cassandra is the PRIMARY consumer of the KNN+Louvain layer:**
- Semantic KNN neighbors as candidate analogs (not just text similarity)
- Louvain community matching: precedent is strongest when same community AND similar regime
- Anomaly detection: Cassandra flags when current cluster composition differs from all historical precedents → "unprecedented regime" warning

### Aegis — Risk gate + kill-switch

Aegis is the **guardrail**. Can veto any TradeSignal. Cannot initiate trades (no agent can — trades are founder-controlled).

**Responsibilities:**
- Read TradeSignal proposals from Nomos
- Evaluate against risk limits (exposure, drawdown, concentration)
- Check BacktestResult for signal robustness
- Veto signals that exceed hard risk rules
- Set `RiskApprovalStatus` on TradeSignal
- Emergency kill-switch on regime detection (if risk-off triggers, halt new signals)

**What triggers Aegis:**
- New TradeSignal from Nomos awaiting approval
- Risk state change (volatility regime shift)
- Manual override request from founder

**Model: Llama 3.3 70B local**
- Requirement: deterministic rule application (not creative reasoning)
- Requirement: fast (trade signals are time-sensitive)
- Local preferred for privacy (trade strategy is sensitive IP)
- Escalation path: if rule ambiguous, request human (founder) decision via IntelligenceOrder

**Aegis must NEVER:**
- Modify hard risk rules (those require founder approval + schema change)
- Approve signals that fail backtest validation
- Move capital (trades execute via external broker with founder authentication)

### Janus — Evaluation + doctrine promotion

Janus is the **learning engine**. Resolves predictions, scores brains, promotes lessons.

**Responsibilities:**
- Resolve open predictions (horizon expired, observable outcome exists)
- Write `PredictionResolutionLog` with Brier score, hit, return-if-followed, drawdown
- Aggregate into `BrainScorecard` (per brain, horizon, regime, asset class)
- Evaluate `BrainLessonCandidate` entries
- Promote lessons to doctrine via `BrainLessonPromotion` when criteria met
- Refresh `OracleWeightSnapshot` when brain performance shifts

**What triggers Janus:**
- Scheduled `resolution_and_scorecards` at europe_close + us_close (2x/day)
- Manual resolution trigger for high-priority predictions
- Scheduled doctrine review (weekly)

**Promotion criteria** (from doctrine):
- Minimum sample size (usually 20+ predictions)
- Brier score improvement over baseline (>= 10% better)
- Stability across regimes (not just one regime fluke)
- Cross-brain replication (lesson must hold for multiple brain contexts)

**Model: Claude Opus 4.7 (promotion decisions) + Llama 3.3 70B (batch resolution)**
- Resolution is mechanical (Brier = (forecast - outcome)^2) — any model
- Promotion is nuanced — requires Opus judgment

**Janus is the ONLY agent that can promote doctrine.** Atlas, Memo, and others can propose via `BrainLessonCandidate`. Janus decides.

## Model Selection Doctrine

For the full decision tree, see **references/model-selection-doctrine.md**.

### Quick decision table

| Task Type | Preferred Model | Fallback | Cost tier |
|-----------|----------------|----------|-----------|
| Atlas orchestration | Claude Opus 4.7 | — | High |
| Prediction sealing (Nomos) | Claude Opus 4.7 | Llama 3.3 70B | High |
| Precedent reasoning (Cassandra) | DeepSeek R1 | Opus for final | Medium |
| Geo-macro synthesis (Helios) | Claude Opus 4.7 | — | High |
| Event ingestion (Argus) | Llama 3.3 70B local | Small classifiers | Low |
| Risk evaluation (Aegis) | Llama 3.3 70B local | Rule engine | Low |
| Doctrine promotion (Janus) | Claude Opus 4.7 | — | Medium |
| Batch resolution (Janus) | Llama 3.3 70B | — | Low |
| Wiki curation (Memo) | Claude Opus 4.7 | — | Medium |
| Embeddings (all agents) | multilingual-e5-large | bge-large-en | Zero marginal |

### Cost-conscious principle

**The moat is in the Calibration Moat data, not in the model.** Models are replaceable. Use Opus where quality matters (edge cases, final calls, user-facing briefs). Use local models for volume (night loops, batch processing, parsing). Budget allocation: 70% volume local, 30% critical calls API.

## The Hybrid Graph Layer (KNN + Louvain)

The hybrid graph is the **structural substrate** that enhances every agent's reasoning. See **references/hybrid-graph-layer.md** for full implementation timeline.

### Three edge types coexist

1. **Explicit edges** (`RelationEdge`): human-curated or ingest-derived. Ground truth, 1,294 active edges currently.

2. **Semantic edges** (`SemanticEdge`): computed from embeddings via KNN. Discovers non-obvious neighbors based on textual/contextual similarity.

3. **Hybrid edges**: weighted combination, tagged with source (`explicit_only`, `semantic_only`, `confirmed_both`).

### Louvain communities enable new reasoning

- **Community membership**: every node belongs to a primary cluster (and sometimes secondary). Communities are named by human validation (e.g., "AI Compute Hegemon", "Fed Hawks", "Oil Chokepoint").

- **Bridge nodes**: high betweenness centrality. Disruption in a bridge node propagates across multiple communities. Critical for risk analysis.

- **Community drift**: temporal snapshots detect when nodes migrate between communities. Early warning of narrative shifts.

### Agent integration with graph layer

| Agent | How the graph layer enhances reasoning |
|-------|---------------------------------------|
| Atlas | Briefs include `community_summary`, `bridge_scores`, `narrative_drift` |
| Memo | Community names inform wiki taxonomy (new cluster = new theme page) |
| Argus | Events hitting high-bridge nodes get priority flagging |
| Helios | Geo-macro propagation analysis uses community topology |
| Nomos | Predictions conditioned on graph context (bridge score, active timelines per community) |
| Cassandra | Precedent search uses semantic neighbors, not just explicit edges |
| Aegis | Concentration risk = multiple high-bridge positions in same community |
| Janus | Scorecards segment by community (Brier score for Nomos in "Fed Hawks" cluster) |

## Memory Architecture

### Three complementary stores

1. **Wiki (Karpathy-style)** — durable markdown memory
   - Human + machine readable
   - Git versioned
   - Bidirectional wikilinks form a graph
   - Strict frontmatter schema (slug, db_id, archetype, related_entities, flags)
   - Accumulates across runs; never ephemeral

2. **PostgreSQL structured state** — the source of truth for queryable data
   - 121+ tables, 23+ moat tables
   - Append-only for prediction/resolution logs
   - Versioned snapshots for time-series analysis

3. **pgvector embeddings** — semantic memory
   - Column `embedding vector(1024)` on every entity table
   - Generated by `multilingual-e5-large`
   - KNN queries via cosine similarity
   - Refresh cycle: weekly full, delta on content changes

### Agent memory access patterns

- **Atlas**: reads all three. Writes via MCP rw-lite.
- **Memo**: writes to wiki primarily. Reads from DB.
- **Argus**: streams to NewsEvent. Minimal wiki interaction.
- **Helios**: reads wiki (historical precedents) + DB (current state). Writes to DB.
- **Nomos**: heavy DB access (regime data, IdeologyProfile, graph). Writes PredictionLog.
- **Cassandra**: heavy wiki + embeddings access. Writes ExperimentLog.
- **Aegis**: DB only (TradeSignal, risk state).
- **Janus**: DB only (resolution + scorecards).

For memory architecture details, see **references/memory-architecture.md**.

## MCP Permission Architecture

Full reference: **references/mcp-architecture.md**

### 7 MCP servers with narrow permissions

1. `mcp-ipm-postgres-ro` — read-only structured state
2. `mcp-ipm-postgres-rw-lite` — restricted writes to moat tables only
3. `mcp-ipm-memory` — wiki + markdown bridge
4. `mcp-ipm-marketdata` — market data read + refresh
5. `mcp-ipm-calendar` — economic calendar
6. `mcp-ipm-docs` — speeches, transcripts, PDFs
7. `mcp-ipm-scorecards` — calibration metrics

### Security rules (hard)

- NO freeform SQL writes (ever)
- Separate read/write identities
- Parameterized SQL + stored procedures only
- OpenClaw never writes to MarketSymbol or MarketDataCache
- Real capital movement requires founder auth outside the agent layer

## 5-Year Capability Roadmap

Abbreviated here; full detail in **references/5-year-roadmap.md**.

| Year | Milestone |
|------|-----------|
| 2026 | Frontend complete (CompanyView, PersonOverlay, ScenarioImpact), OpenClaw + n8n operational, pgvector installed, Atlas v1 in production |
| 2027 | Hybrid graph layer live (KNN + Louvain), Atlas v2 with community awareness, first paying customers (enterprise tier) |
| 2028 | 3 years of calibration track record, hypothesis generation loop (GraphMind) in production, enterprise clients scaling |
| 2029 | Possible IPM-GPT fine-tune experimental, diversified revenue streams, $1.5M-$4M ARR |
| 2030-2031 | Platform maturity, calibration certification product, $3M-$15M ARR, acquisition interest |

## When to reference each sub-document

- **references/agents/atlas.md** — full Atlas specification + example orchestration calls
- **references/agents/memo.md** — Memo wiki curation + doctrine promotion flow
- **references/agents/argus.md** — Argus ingestion pipeline + entity extraction
- **references/agents/helios.md** — Helios geo-macro synthesis + GeoMacroFusionLog
- **references/agents/nomos.md** — Nomos prediction generation + classification ladder
- **references/agents/cassandra.md** — Cassandra precedent retrieval + stress-testing
- **references/agents/aegis.md** — Aegis risk gate + veto logic
- **references/agents/janus.md** — Janus resolution + promotion + scorecards
- **references/model-selection-doctrine.md** — full decision tree + cost analysis
- **references/hybrid-graph-layer.md** — KNN + Louvain implementation (α through ζ phases)
- **references/memory-architecture.md** — wiki + DB + pgvector coordination
- **references/mcp-architecture.md** — 7 MCP servers with tool specifications
- **references/5-year-roadmap.md** — capability evolution with concrete milestones
- **references/revenue-streams.md** — 12 revenue streams across 3 commercial layers (World Model + Agent Context + Visual Platform), with sub-brand architecture (IMP Core/Markets/Experts/Foresight/Risk), pricing tiers, buyer profiles, and time-to-revenue matrix

## Non-negotiable principles

These come from IPM doctrine and must be respected by every agent design:

1. **Forecast before outcome** — all predictions sealed in PredictionLog before resolution possible
2. **Append-only memory** — no UPDATE or DELETE on moat tables
3. **Calibration over narrative** — Brier score is the metric, not confidence
4. **Graph-conditioned reasoning** — predictions include graph context as features
5. **Regime-conditioned evaluation** — performance segmented by regime, not aggregate
6. **Narrow MCP permissions** — agents access only approved tools
7. **Local-first private runtime** — OpenClaw sovereign, API only where quality requires
8. **Human-supervised risk** — no agent moves capital, all trades founder-approved
9. **Skills define doctrine** — agent behavior codified in skills, not hardcoded prompts
10. **Wiki as durable memory** — learnings persist as markdown, not ephemeral context
11. **Database as structured truth** — DB rows beat agent memory in all conflicts
