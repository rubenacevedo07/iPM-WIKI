# Memory Architecture — Karpathy Wiki + PostgreSQL + pgvector

## Three-layer memory substrate

IPM's memory is not monolithic. Three layers coordinate:

1. **Wiki (Karpathy-style)** — durable narrative memory
2. **PostgreSQL structured state** — queryable structured truth
3. **pgvector embeddings** — semantic memory for similarity search

Each has a different role, access pattern, and update cadence.

## Layer 1: Karpathy-style Wiki

### Origin

Named after Andrej Karpathy's minimalist, principled approach to knowledge systems. The wiki philosophy: markdown files with **strict frontmatter** + **bidirectional wikilinks** + **machine-readable templates** form a graph that's both human-navigable (via Obsidian or similar) and machine-processable (via frontmatter parsing).

### Structure

```
IPM-Wiki/
├── actors/
│   ├── powell-jerome.md
│   ├── lagarde-christine.md
│   └── ...
├── countries/
│   ├── united-states.md
│   ├── china.md
│   └── ...
├── institutions/
│   ├── federal-reserve.md
│   ├── blackrock.md
│   └── ...
├── commodities/
│   ├── crude-oil.md
│   ├── semiconductors.md
│   └── ...
├── themes/
│   ├── ai-compute-scarcity.md
│   ├── dollar-system-stress.md
│   └── ...
├── timelines/
│   ├── 2026-fed-rate-path.md
│   ├── 2026-taiwan-election.md
│   └── ...
├── scenarios/
│   ├── taiwan-strait-conflict.md
│   ├── hormuz-closure.md
│   └── ...
├── precedents/
│   ├── 1973-oil-crisis.md
│   ├── 2008-financial-crisis.md
│   └── ...
├── doctrine/
│   ├── prediction-methodology.md
│   ├── regime-classification.md
│   └── ...
└── dossiers/
    ├── musk-elon-2026.md
    └── ...
```

### Frontmatter schema (by type)

Every page has YAML frontmatter. Required fields vary by type.

**Actor page:**
```yaml
---
type: actor
slug: powell-jerome
db_id: 7
archetype: institutional
role: Federal Reserve Chair
related_countries: [united-states]
related_institutions: [federal-reserve]
related_commodities: [us-treasuries, usd]
related_themes: [monetary-policy, dollar-system-stress]
region_tags: [north-america]
power_score: 96
ideology_profile_id: 7
flags: [systemic, voting-member, anchor]
last_reviewed: 2026-04-15
---
```

**Scenario page:**
```yaml
---
type: scenario
slug: taiwan-strait-conflict
db_id_scenario_cascade: 42
archetype: geopolitical-systemic
probability_current: 0.12
probability_history: [{date: 2026-01-01, p: 0.08}, {date: 2026-04-01, p: 0.12}]
related_actors: [xi-jinping, biden-joe, lai-ching-te]
related_countries: [china, taiwan, united-states, japan]
related_commodities: [semiconductors, shipping]
related_themes: [ai-compute-scarcity, supply-chain-concentration]
horizon_years: 5
last_reviewed: 2026-04-10
flags: [systemic, tail-risk, watchlist]
---
```

**Precedent page:**
```yaml
---
type: precedent
slug: 1973-oil-crisis
archetype: geopolitical-economic-cascade
event_date: 1973-10-17
duration_months: 6
related_commodities: [crude-oil]
related_countries: [saudi-arabia, united-states, netherlands, opec-member-countries]
related_themes: [supply-shock, dollar-system-stress, inflation]
outcome_direction: oil_up_equity_down
outcome_magnitude: 400%
price_actions: [{asset: WTI, move: +400%}, {asset: SPX, move: -40%}]
analog_similarity_potential: [hormuz-closure, iran-supply-disruption]
---
```

### Bidirectional wikilinks

Every `[[wikilink]]` must create a backlink on the target page. Memo enforces this.

Example: if `powell-jerome.md` contains `[[federal-reserve]]`, then `federal-reserve.md` must have in its "Referenced by" section: `- [[powell-jerome]]`.

This forms a true graph (not just forward references) usable for:
- Obsidian graph view
- Memo coherence audits
- Cassandra analog retrieval (wikilinks = weak explicit edges)

### What goes in wiki vs DB

**Wiki**: narrative, reasoning, analysis, doctrine, precedent details, descriptions

**DB**: structured data, scores, relations, predictions, events, prices

**Principle**: if it's a paragraph, it's wiki. If it's a number or a row, it's DB.

### Wiki as training data for the future

The wiki accumulates human + AI reasoning over years. In 2028-2029, this becomes the corpus for fine-tuning IPM-GPT. 134 pages today → thousands in 3 years.

**Therefore**: never let wiki quality degrade. Memo is not optional. Wikilint reports audit regularly.

## Layer 2: PostgreSQL Structured State

### The source of truth

Whenever narrative and data conflict, data wins. If the wiki says "NVIDIA market cap $2T" but DB says $3T, Atlas uses $3T and Memo updates the wiki.

### Key table groups

**Entities:**
- Persons (~50 rows, 1000+ target)
- Companies (~248 rows, 2000+ target)
- Countries (~195 rows, stable)
- Institutions (~50 rows, 500+ target)
- Commodities (~80 rows, stable)

**Relations:**
- RelationEdge (1,294 active, 10K+ target over 3 years)
- SemanticEdge (NEW, via hybrid graph layer)

**Scores + profiles:**
- IdeologyProfile
- PersonPowerIndex
- EdgeRiskScore
- CompositeIndexSnapshots

**Moat (append-only):**
- PredictionLog
- PredictionResolutionLog
- BrainScorecard
- CentralBankToneLog
- MediaInterpretationLog
- InterpretationGapLog
- GeoMacroFusionLog
- BrainLessonCandidate
- BrainLessonPromotion
- OracleWeightSnapshot

**Market data:**
- MarketSymbol
- MarketDataCache
- TradeSignal
- ExperimentLog

**Operational:**
- IntelligenceOrder
- AnalystPrediction (legacy, being replaced by PredictionLog)

### Append-only principle for moat tables

Moat tables use INSERT only. No UPDATE, no DELETE.

Reasoning: The Calibration Moat's value is **non-fabricability**. If predictions can be modified post-hoc, the whole premise collapses.

Enforced by:
- Database permissions (agents use rw-lite identity, which has INSERT grant but no UPDATE/DELETE)
- MCP server layer (only `insert*` tools, no `update*` or `delete*`)
- Stored procedures validating append-only semantics

### Versioning within append-only

For entities that change (PersonPowerIndex, IdeologyProfile), versioning via `SnapshotDateUtc`:

- Never update existing row
- Always insert new row with today's date
- Query latest via `ORDER BY SnapshotDateUtc DESC LIMIT 1`

Result: full history always preserved, can query "what did IPM think Powell's score was on 2025-06-01?"

## Layer 3: pgvector Embeddings

### Purpose

Semantic memory. Find similar entities/events/scenarios based on meaning, not keywords.

### Implementation

Each entity table has `embedding vector(1024)` column.

Embedding source text: combination of:
- Wiki page body (if exists)
- Frontmatter fields (relationships, archetype, role)
- Recent news mentions (last 30 days)
- Description from DB

Stored as vector, indexed with pgvector HNSW index for fast KNN queries:

```sql
CREATE INDEX ON Persons
USING hnsw (embedding vector_cosine_ops);
```

### Query patterns

**KNN search:**
```sql
SELECT p2.Id, 1 - (p1.embedding <=> p2.embedding) AS similarity
FROM Persons p1, Persons p2
WHERE p1.Id = 7 AND p1.Id != p2.Id
ORDER BY p1.embedding <=> p2.embedding
LIMIT 15;
```

**Cross-type search** (person → similar companies):
```sql
SELECT c.Id, c.Name, 1 - (p.embedding <=> c.embedding) AS similarity
FROM Persons p, Companies c
WHERE p.Id = 7
ORDER BY p.embedding <=> c.embedding
LIMIT 10;
```

**Filtered search** (similar persons in same archetype):
```sql
SELECT p2.Id, p2.Name, 1 - (p1.embedding <=> p2.embedding) AS sim
FROM Persons p1, Persons p2
WHERE p1.Id = 7
  AND p2.Archetype = p1.Archetype
  AND p1.Id != p2.Id
ORDER BY p1.embedding <=> p2.embedding
LIMIT 10;
```

### Refresh cadence

- **On-demand**: when entity's wiki page or frontmatter changes → re-embed that entity
- **Weekly batch**: re-embed entities with recent news mentions (their context changed)
- **Monthly full rebuild**: re-embed everything with latest model version

Tracked via `last_embedded_at` column.

### Embedding model versioning

As embedding models improve (e.g., e5-mistral-7b becomes standard), wholesale rebuilds possible. Store `embedding_model_version` per row to know what generated each vector.

## Memory access coordination across agents

### Write coordination

**Only one agent writes to each memory store:**

| Store | Writer |
|-------|--------|
| Wiki markdown | Memo only |
| PredictionLog | Nomos only |
| PredictionResolutionLog | Janus only |
| BrainScorecard | Janus only |
| BrainLessonPromotion | Janus only |
| NewsEvent | Argus only |
| GeoMacroFusionLog | Helios only |
| RiskApprovalStatus | Aegis only |
| IntelligenceOrder | Atlas + user |
| ExperimentLog | Cassandra, Nomos (both) |
| SemanticEdge | Batch compute (not agent) |
| NodeMetrics | Batch compute (not agent) |
| Embeddings | Batch compute (not agent) |

Clear ownership prevents write conflicts.

### Read access

**All agents read freely from all memory stores via MCP ro tools.** No read contention concerns.

### Staleness awareness

Atlas must know data freshness:
- Every query response includes `last_updated_at`
- If critical data is stale (e.g., market snapshot > 5 min old), Atlas flags in brief
- Scheduled refresh jobs ensure key data is fresh (market data every minute, embeddings weekly, etc.)

## Backup + durability

### Wiki

- Git versioned (committed regularly)
- Mirrored to GitHub (private repo)
- Founder has local copy

### PostgreSQL

- Railway auto-backups (daily)
- Point-in-time recovery enabled
- Export dumps monthly to local storage

### Embeddings

- Regenerable from DB + wiki (do not need separate backup)
- If embedding model changes, rebuild from sources

## Memory growth projection

| Year | Wiki pages | DB rows | Embeddings |
|------|-----------|---------|------------|
| 2026 | ~150 | ~500K | ~600 |
| 2027 | ~500 | ~2M | ~2K |
| 2028 | ~1,500 | ~10M | ~10K |
| 2029 | ~3,500 | ~50M | ~30K |
| 2030 | ~7,000 | ~200M | ~80K |

Storage cost: negligible at this scale. Railway handles well until 2029. Then may migrate to self-hosted PostgreSQL cluster.
