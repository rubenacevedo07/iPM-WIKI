# Hybrid Graph Layer — KNN + Louvain Implementation

## Concept

IPM's graph is enhanced from **explicit-edges-only** to **hybrid multi-source**:

1. **Explicit edges** — `RelationEdge` table, 1,294 active edges, hand-curated + ingest-derived
2. **Semantic edges** — `SemanticEdge` table (NEW), computed via KNN over entity embeddings
3. **Merged weighted graph** — combines both with salience modulation
4. **Louvain communities** — detected over weighted graph, updated temporally

This layer is consumed primarily by Cassandra (precedent search), Nomos (prediction conditioning), Helios (propagation analysis), and Atlas (brief enrichment).

## Six-phase implementation timeline

### Phase α — Infrastructure (1 week)

**Tasks:**
1. Install pgvector extension in Railway PostgreSQL
2. Add `embedding vector(1024)` column to:
   - `Persons`
   - `Companies`
   - `Countries`
   - `Commodities`
   - `Institutions`
   - `Themes` (wiki pages with type=theme)
   - `Scenarios`
   - `Timelines`
   - `NewsEvents`
3. Setup Ollama locally with `multilingual-e5-large`
4. Create Python batch embedding script:
   - Reads DB rows
   - Constructs text per entity (wiki body + frontmatter + recent context)
   - Embeds
   - Writes vector back to DB
   - Tracks `last_embedded_at` timestamp

**Deliverable:** All entities have embeddings. Can run `SELECT` with cosine distance operator.

**Blockers:** None material.

### Phase β — First KNN pass (1 week)

**Tasks:**
1. Create `SemanticEdge` table:
   ```sql
   CREATE TABLE SemanticEdge (
     Id SERIAL PRIMARY KEY,
     SourceNodeType TEXT NOT NULL,
     SourceNodeId INT NOT NULL,
     TargetNodeType TEXT NOT NULL,
     TargetNodeId INT NOT NULL,
     Similarity REAL NOT NULL,
     ComputedAtUtc TIMESTAMP NOT NULL,
     UNIQUE(SourceNodeType, SourceNodeId, TargetNodeType, TargetNodeId)
   );
   ```
2. KNN compute script per node type:
   - Person → K=15 nearest neighbors
   - Company → K=20
   - Country → K=10
   - Commodity → K=10
   - Theme → K=15
   - Scenario → K=8
3. Batch execution: 500 nodes × 20 neighbors = 10K edges. Manageable.
4. Jupyter notebook for visual inspection:
   - For top 20 entities, print 5 nearest neighbors
   - Human review: do these make sense?
   - Iterate K, similarity threshold if needed

**Deliverable:** `SemanticEdge` populated. Quality validated manually.

**Success criteria:** ≥80% of semantic neighbors "make sense" to human review.

### Phase γ — Salience weighting (1 week)

**Tasks:**
1. Define salience functions:
   ```python
   def salience(a, b, context):
       w = a.similarity_to(b)

       # Archetype coherence
       if a.archetype == b.archetype:
           w *= 1.3

       # Graph confirmation (explicit edge exists too)
       if has_explicit_edge(a, b):
           w *= 2.0

       # Anchor proximity
       if is_anchor(a) or is_anchor(b):
           w *= 1.5

       # Temporal freshness
       if shared_recent_news(a, b, days=30) > 0:
           w *= 1.2

       # Divergence cross-score
       if both_affect_same_trading_signal(a, b):
           w *= 1.4

       return w
   ```

2. Define anchors formally:
   - Persons with PersonPowerIndex ≥ 85 (Powell, Lagarde, Trump, Xi, Fink, Huang, Putin, MBS, ~30 people)
   - Countries classified as "pivot" (USA, China, Taiwan, Russia, Saudi Arabia, ~15 countries)
   - Institutions classified as "systemic" (Fed, ECB, BoJ, PBoC, IMF, BlackRock, Aramco, ~20 institutions)

3. Store anchor list in `AnchorEntity` table with manual maintenance

4. Recompute `SemanticEdge` with weighting applied → stored as `SalienceWeight` column

**Deliverable:** Every semantic edge has both `Similarity` (raw) and `SalienceWeight` (modulated)

### Phase δ — Louvain + metrics (3-4 days)

**Tasks:**
1. Python script using `networkx` + `python-louvain`:
   ```python
   import networkx as nx
   from community import community_louvain

   # Build hybrid graph
   G = nx.Graph()
   for edge in RelationEdge.all():
       G.add_edge(edge.source_nodeid, edge.target_nodeid,
                  weight=edge.strength_numeric, source='explicit')

   for edge in SemanticEdge.all():
       existing = G.get_edge_data(edge.source, edge.target)
       if existing:
           # Merge: keep max, tag as confirmed_both
           G[edge.source][edge.target]['weight'] = max(existing['weight'], edge.salience_weight)
           G[edge.source][edge.target]['source'] = 'confirmed_both'
       else:
           G.add_edge(edge.source, edge.target,
                      weight=edge.salience_weight, source='semantic')

   # Run Louvain
   partition = community_louvain.best_partition(G, weight='weight')

   # Compute centrality metrics
   betweenness = nx.betweenness_centrality(G)
   degree = dict(G.degree(weight='weight'))

   # Persist
   for node_id, community_id in partition.items():
       NodeMetrics.upsert(
           node_id=node_id,
           snapshot_date=today,
           primary_community=community_id,
           betweenness=betweenness[node_id],
           degree=degree[node_id]
       )
   ```

2. Run over full graph (~500 nodes, ~5K-10K edges): completes in seconds

3. Validate clusters manually:
   - For each community, print top-10 members by degree
   - Assign human-readable name ("AI Compute Hegemon", "Fed Hawks", etc.)
   - Review: do the clusters match intuition?
   - Iterate if community structure seems wrong (increase resolution parameter)

**Deliverable:** `NodeMetrics` table populated with community + betweenness + degree per node.

**Success criteria:** Top-10 communities match human expectation (semiconductor cluster, energy cluster, central bank cluster, etc.)

### Phase ε — Atlas integration (1 week)

**Tasks:**
1. Add MCP tools to `mcp-ipm-postgres-ro`:
   - `getNodeCommunity(nodeId)` → primary community + members
   - `getBridgeScore(nodeId)` → betweenness centrality
   - `getSemanticNeighbors(nodeId, k, filter)` → non-obvious similarity matches
   - `getNarrativeDrift(nodeId, windowDays)` → cluster migration history (requires Phase ζ for data)

2. Update Atlas v1 system prompt → Atlas v2:
   - Add graph_intelligence section to brief schema
   - Train Atlas (via prompt examples) to use community awareness

3. Test on 5 pilot entities:
   - Powell, NVIDIA, Saudi Arabia, BlackRock, Taiwan
   - Generate briefs with + without graph layer
   - Compare: does brief include new insights?

**Deliverable:** Atlas briefs include graph_intelligence data. Pilot validated.

### Phase ζ — Temporal snapshots (1 week)

**Tasks:**
1. Weekly cron job:
   - Re-embed any entity whose text changed (via `last_embedded_at` vs `content_updated_at`)
   - Re-KNN for affected entities only (delta update, not full re-compute)
   - Re-run Louvain if enough graph changes (threshold: >5% of edges changed)
   - Compute diff vs previous `NodeMetrics` snapshot
   - Flag nodes with cluster migration

2. Migration detection:
   - If node X was in community A last week, community B this week → flag
   - Generate `NarrativeDrift` record
   - Notify Cassandra: "potential regime change signal"

3. Long-term storage:
   - `NodeMetrics` keeps weekly snapshots (52 rows/year/node)
   - Can query: "show evolution of NVIDIA's community membership over 6 months"

**Deliverable:** System detects narrative drift automatically. Snapshots accumulate for longitudinal analysis.

## Integration with the 8 agents

### Cassandra (primary consumer)

**How graph layer transforms Cassandra:**

*Without graph layer*: Cassandra searches explicit edges for analog entities. Limited to hand-curated connections.

*With graph layer*: Cassandra searches:
- Semantic neighbors (non-obvious analogs)
- Same-community entities (structurally similar)
- Anomaly detection: current cluster composition vs historical

New capability: **hypothesis generation**. Cassandra can flag unprecedented regimes, propose new mechanisms based on cluster topology.

### Nomos (heavy user)

**How graph layer transforms Nomos:**

Predictions gain graph-conditioned probabilities:

*Without graph layer*: "P(NVIDIA down 15% in 30d) = 0.28"

*With graph layer*: "P(NVIDIA down 15% in 30d | bridge_score=0.72, active_timelines_in_ai_compute_community=3, narrative_drift_detected=no, interpretation_gap_us_tech_policy=0.31) = 0.34 ± 0.07"

Much more precise. Much more useful for backtest + calibration.

### Helios (propagation analysis)

**How graph layer transforms Helios:**

Geo events now trace through community topology:

*Without graph layer*: "Oil spike affects oil companies"

*With graph layer*: "Oil spike propagates from 'Energy Chokepoint' community → 'Global Shipping' community via bridge node (Suez Canal Authority) → 'LNG Import Dependency' community with lag ~7 days"

### Atlas (brief enrichment)

**How graph layer transforms Atlas:**

Briefs include community_summary, bridge_scores, narrative_drift. Analyst gets structural intelligence, not just facts.

### Memo (taxonomy generation)

**How graph layer transforms Memo:**

When Louvain detects a new stable community (emerged over 3+ months, 10+ members), Memo creates a new **theme page** in the wiki representing that community. Taxonomy emerges bottom-up from data.

### Argus, Aegis, Janus (lighter use)

- Argus: prioritizes events hitting high-bridge nodes
- Aegis: concentration risk = multiple positions in same community or adjacent community
- Janus: scorecards segmented by community (Brier score for Nomos in "Fed Hawks" cluster specifically)

## Cost profile

**One-time setup:**
- Install pgvector: $0
- Ollama setup: $0 (uses existing hardware)
- Scripts development: 2-3 weeks of founder time

**Ongoing:**
- Embedding compute: CPU or mini-GPU, essentially free
- KNN computation: seconds per node, batch nightly
- Louvain: seconds for 10K edges, batch weekly
- Storage: negligible (10K-50K semantic edges, 500 KB total)

**Total marginal cost of the graph layer: near zero.** This is pure added value.

## Risks and mitigations

### Risk 1: Embedding quality insufficient

**Symptom:** Semantic neighbors don't match intuition

**Mitigation:**
- Try different embedding models (multilingual-e5-large → bge-large-en → OpenAI ada)
- Improve input text (include more wiki body, recent context, relationships mentioned)
- Fine-tune embedding model on IPM corpus (year 2028+)

### Risk 2: Louvain unstable clustering

**Symptom:** Clusters vary significantly run-to-run

**Mitigation:**
- Seed random number generator for reproducibility
- Use weighted graph (weights stabilize communities)
- Alternative: Leiden algorithm (more stable than Louvain)

### Risk 3: Graph layer produces spurious anomalies

**Symptom:** Cassandra flags "unprecedented regime" too frequently

**Mitigation:**
- Calibrate anomaly threshold on historical data
- Require human validation of unprecedented flags
- Track false positive rate in BrainScorecard for Cassandra

### Risk 4: Community labels drift over time

**Symptom:** "AI Compute Hegemon" cluster grows to include unrelated entities

**Mitigation:**
- Periodic manual review of community boundaries
- Memo writes "community coherence" report monthly
- Flag drift for human attention

## When to launch

**Don't launch graph layer until:**
- CompanyView + PersonOverlay + ScenarioImpact are in production
- OpenClaw + n8n are operational
- pgvector is stable in Railway

**Target launch: 2026 Q4** (October-December)

**Rationale:** Frontend first (users see value), then graph layer enhances agent reasoning (users see MORE value).
