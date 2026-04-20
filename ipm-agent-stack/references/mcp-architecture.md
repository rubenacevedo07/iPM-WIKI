# MCP Architecture — 7 Servers with Narrow Permissions

## Core principle

**Agents don't get SQL. Agents get narrow, auditable tools.**

MCP (Model Context Protocol) servers expose specific functions to agents. Every tool is schema-validated, parameterized, and permissions-scoped. No freeform access.

Why: Claude + Llama + DeepSeek are capable of constructing harmful SQL ("DROP TABLE PredictionLog"). The MCP layer makes this structurally impossible.

## The 7 servers

### 1. `mcp-ipm-postgres-ro` — Read-only structured state

**Role:** Reading from PostgreSQL for any agent

**Identity:** Dedicated DB user with `SELECT` grants only, no `INSERT/UPDATE/DELETE/DDL`

**Tools exposed:**

| Tool | Purpose |
|------|---------|
| `getSymbolContext(symbol)` | MarketSymbol + IdeologyProfile + recent metrics |
| `getLatestMarketSnapshot(symbol)` | Most recent MarketDataCache row |
| `getOpenPredictions(filters?)` | Unresolved PredictionLog entries |
| `getRecentExperimentLog(n, filters?)` | Latest ExperimentLog entries |
| `getCurrentIdeologyProfile(entityId)` | Latest IdeologyProfile snapshot |
| `getLatestCompositeIndexSnapshots` | Current regime indices |
| `getBrainScorecard(brainId?, regime?)` | Performance metrics |
| `getNodeCommunity(nodeId)` | Louvain community membership (Phase hybrid-graph+) |
| `getBridgeScore(nodeId)` | Betweenness centrality (Phase hybrid-graph+) |
| `getSemanticNeighbors(nodeId, k, filter?)` | KNN semantic matches (Phase hybrid-graph+) |
| `getNarrativeDrift(nodeId, windowDays)` | Cluster migration history (Phase hybrid-graph+) |

**Forbidden:**
- Freeform SQL execution
- Any write operation
- Schema changes

**Used by:** All 8 agents

### 2. `mcp-ipm-postgres-rw-lite` — Restricted writes to moat tables

**Role:** Insert operations into specific moat tables with schema validation

**Identity:** Separate DB user from ro server. `INSERT` grant on approved tables, no `UPDATE/DELETE/DDL`

**Tools exposed:**

| Tool | Writes to | Agent |
|------|-----------|-------|
| `insertPredictionLogPayload` | PredictionLog | Nomos |
| `insertPredictionResolutionPayload` | PredictionResolutionLog | Janus |
| `insertCentralBankTonePayload` | CentralBankToneLog | Argus |
| `insertMediaInterpretationPayload` | MediaInterpretationLog | Argus |
| `insertInterpretationGapPayload` | InterpretationGapLog | Argus (computed) |
| `insertGeoMacroFusionPayload` | GeoMacroFusionLog | Helios |
| `insertBrainLessonCandidatePayload` | BrainLessonCandidate | Memo, Atlas, Cassandra |
| `insertBrainLessonPromotionPayload` | BrainLessonPromotion | Janus (only) |
| `insertOracleWeightSnapshotPayload` | OracleWeightSnapshot | Janus (only) |

**Validation rules (hard):**
1. Every tool takes a structured payload object (not SQL)
2. Payload validated against JSON schema BEFORE database call
3. Payload mapped to parameterized SQL (no string concatenation)
4. Writes executed via stored procedures only
5. Write attempts outside approved tables → rejected
6. Write attempts with invalid payload → rejected

**Forbidden:**
- Freeform SQL execution (absolute)
- UPDATE on any table (moat tables are append-only)
- DELETE on any table
- Writes to MarketSymbol, MarketDataCache (schema-protected)
- Writes to RiskApprovalStatus without Aegis identity
- Risk rule modifications
- Capital movement (never — these aren't exposed anywhere)

**Identity-based tool access:**

Some tools restricted to specific agent identities:

- `insertBrainLessonPromotionPayload` — Janus identity ONLY
- `insertOracleWeightSnapshotPayload` — Janus identity ONLY
- `insertPredictionLogPayload` — Nomos identity (Atlas can submit via Nomos routing, not directly)

Enforcement via agent identity token passed through MCP call.

**Used by:** Agent-specific (see table above)

### 3. `mcp-ipm-memory` — Wiki + markdown bridge

**Role:** Read and update wiki + staging notes

**Tools:**

| Tool | Purpose |
|------|---------|
| `searchMemo(query, type?)` | Search wiki content |
| `readPage(slug)` | Full page contents |
| `writeMemoStaging(content, metadata)` | Add staging note (not yet promoted doctrine) |
| `promoteDoctrine(stagingId, rationale)` | Move staging to doctrine (Janus + Memo only) |
| `listRecentLessons(n)` | Recently added doctrine pages |
| `getWikiPageByDbId(type, dbId)` | Look up wiki page by entity DB ID |
| `updatePageFrontmatter(slug, fields)` | Controlled frontmatter updates (Memo only) |

**Security:** File system permissions. Staging area is readable/writable by Memo + Atlas. Doctrine area only writable by Janus + Memo via promotion flow.

**Used by:** Memo (primary), Atlas, Cassandra, Nomos (reads)

### 4. `mcp-ipm-marketdata` — Market data access

**Role:** Query current and recent market prices; trigger refresh of data

**Tools:**

| Tool | Purpose |
|------|---------|
| `getMarketLatest(symbol)` | Most recent price from MarketDataCache |
| `refreshSymbol(symbol)` | Trigger fresh API fetch for single symbol |
| `refreshAll` | Bulk refresh (rate-limited) |
| `getPriceHistory(symbol, days)` | Historical price series |

**Security:**
- Read access open to all agents
- `refreshSymbol` rate-limited (not abuse-able)
- `refreshAll` requires elevated identity

**Used by:** Helios, Nomos, Janus, Argus

### 5. `mcp-ipm-calendar` — Economic calendar

**Role:** Read economic events (Fed meetings, ECB, NFP, CPI, GDP, etc.)

**Tools:**

| Tool | Purpose |
|------|---------|
| `getNext24hEvents` | Events in next 24 hours |
| `getNext7dEvents` | Events in next 7 days |
| `getTodayHighImpactEvents` | Today's Tier 1 events |
| `getEventsByCountry(country, days)` | Filtered by country |

**Source:** Investing.com scraping or trading-economics API. Integrated via n8n.

**Used by:** Argus (scheduling), Atlas (briefing context), Helios (geo impact timing)

### 6. `mcp-ipm-docs` — Document retrieval

**Role:** Access speeches, transcripts, PDFs, research notes

**Tools:**

| Tool | Purpose |
|------|---------|
| `getSpeechText(centralBank, date)` | Fed/ECB/BoJ/BoE speech full text |
| `getTranscript(eventId)` | Press conference transcripts |
| `searchResearchNotes(query, sources?)` | Full-text search of research archive |
| `getPdfSummary(pdfId)` | Extract text from PDF |

**Used by:** Argus (tone scoring), Cassandra (precedent text), Helios (policy text)

### 7. `mcp-ipm-scorecards` — Moat metrics

**Role:** Query calibration metrics and Brain performance

**Tools:**

| Tool | Purpose |
|------|---------|
| `getBrainScorecard(brainId?, horizon?, regime?)` | Performance metrics |
| `getBrierBySymbol(symbol, windowDays)` | Brier for all brains on a symbol |
| `getBrierByRegime(regime, windowDays)` | Regime-segmented performance |
| `getInterpretationGapStats(bank, windowDays)` | InterpretationGap signal effectiveness |
| `getGeoMacroTriggerStats(windowDays)` | GeoMacroFusion trigger accuracy |

**Purpose:** Self-awareness. Agents can know their own performance and adjust.

**Used by:** Atlas (brief context), Janus (doctrine decisions), Nomos (confidence calibration)

## Separation of duties

### Read identity vs Write identity

`mcp-ipm-postgres-ro` and `mcp-ipm-postgres-rw-lite` use **separate database users**:
- `ipm_agent_read` — SELECT only, to all tables
- `ipm_agent_write` — INSERT only, to specified moat tables

Why: if `ipm_agent_read` credentials leak (e.g., OpenClaw local exposure), the attacker gets reads but cannot modify data.

### Agent identity propagation

When an agent calls an MCP tool, it passes its identity (e.g., `{"agent": "Nomos", "invocation_id": uuid}`).

MCP server verifies:
- Is this agent allowed to use this tool?
- Log the access in audit trail

Audit log stored in `MCPAccessLog` table (append-only). Queryable to detect anomalies.

## OpenClaw integration

OpenClaw hosts the agent processes. Each agent workspace has:
- Narrow MCP server access (only what that agent needs)
- Scoped staging directory
- Separate credentials per agent

Example: Argus workspace has access to:
- `mcp-ipm-postgres-ro` (read NewsEvent, MarketSymbol)
- `mcp-ipm-postgres-rw-lite` with `insertCentralBankTonePayload` scope only
- `mcp-ipm-docs` (read speeches)
- `mcp-ipm-calendar` (check schedule)
- NO access to `mcp-ipm-postgres-rw-lite insertPredictionLogPayload` (that's Nomos role)

## Failure modes + handling

### MCP server unavailable

- Agent operation degrades gracefully
- Atlas brief includes "tool unavailable" marker instead of fabricating
- Priority queue: IntelligenceOrder defers until tool restored

### Rate limit hit

- Tool calls queued
- Agent waits with exponential backoff
- Alerts if queue exceeds threshold

### Validation rejection

- Agent receives rejection payload with reason
- Agent must correct payload and retry
- Pattern recognition: if same agent rejected 3x for same reason → escalate to founder

### Identity spoofing attempt

- MCP server validates identity cryptographically
- Invalid identity → immediate rejection + alert
- Repeated attempts → revoke and require re-auth

## Implementation priority

When building MCP servers, build in this order:

1. `mcp-ipm-postgres-ro` — most used, enables any read work
2. `mcp-ipm-postgres-rw-lite` with `insertPredictionLogPayload` first — Nomos can start sealing
3. `mcp-ipm-postgres-rw-lite` with `insertPredictionResolutionPayload` — Janus can resolve
4. `mcp-ipm-memory` — Memo can curate
5. `mcp-ipm-docs` — Argus can ingest speeches
6. `mcp-ipm-calendar` — scheduling becomes automatic
7. `mcp-ipm-marketdata` — live market context
8. `mcp-ipm-scorecards` — self-awareness layer

MCP servers 1-3 enable 80% of moat value. Build those first.

## Security hardening checklist

- [ ] Separate DB users for read vs write
- [ ] All writes through stored procedures
- [ ] No agent has API keys exposed
- [ ] MCPAccessLog audit trail in place
- [ ] Rate limiting on all write endpoints
- [ ] Schema validation on every payload
- [ ] Identity tokens cryptographically signed
- [ ] Production credentials never in version control
- [ ] Emergency kill-switch: can disable all rw-lite writes in < 1 minute
- [ ] Regular audit: can founder review which agents wrote what in last 24h?
