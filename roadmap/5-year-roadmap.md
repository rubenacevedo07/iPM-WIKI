# 5-Year Capability Roadmap

## Framing

IPM's 5-year trajectory is **not about reaching "AI predicts the future"** (physically impossible for complex reflexive systems). It's about building **the most auditable, graph-conditioned, regime-aware intelligence system in existence**.

The moat is cumulative. Every year operating strengthens it.

## 2026 — Foundation

### Q1 (Jan-Mar) ✅ Mostly complete
- [x] Calibration Moat Day 1 (sealed 2026-04-17)
- [x] Phase 4.3c frontend (compact OverlayPanel)
- [x] Backend endpoints (Company risk profile, supply chain)
- [x] 248 companies, 50 power index entries, 1,294 relation edges

### Q2 (Apr-Jun) — Current phase
- [ ] Phase 5.0a-d: CompanyView full-screen Bloomberg terminal
- [ ] Phase 5.1: PersonOverlay migrated to v2 design
- [ ] Phase 5.2: ScenarioImpactPreview
- [ ] Continue Calibration Moat accumulation (Day 1 → Day 60+)

### Q3 (Jul-Sep)
- [ ] OpenClaw + n8n operational
- [ ] First night loops running (limited: Argus ingestion only initially)
- [ ] MCP servers 1-3 built (`postgres-ro`, `postgres-rw-lite`, `memory`)
- [ ] First Atlas briefs generated (manual trigger, not automatic yet)

### Q4 (Oct-Dec)
- [ ] pgvector installed, embeddings for all entities
- [ ] Phase α-β of hybrid graph layer (KNN compute)
- [ ] Atlas v1 in production
- [ ] Target: 500+ sealed predictions in Calibration Moat by Dec 31

**End of 2026 state:**
- Frontend complete, used daily by founder
- Agent runtime operational with 2-3 agents (Argus, Atlas, Nomos manual)
- Embeddings + KNN baseline available
- Revenue: $0 (still pre-revenue)

## 2027 — Agent Stack Maturation

### Q1 (Jan-Mar)
- [ ] Phase γ-δ hybrid graph (salience weighting + Louvain)
- [ ] Atlas v2 with community awareness
- [ ] Cassandra agent deployed (precedent retrieval)
- [ ] Helios agent deployed (geo-macro synthesis)

### Q2 (Apr-Jun)
- [ ] Janus agent deployed (resolution + scorecard)
- [ ] Aegis agent deployed (risk gate)
- [ ] Full 8-agent system operational
- [ ] Phase ε hybrid graph (Atlas integration of graph data)

### Q3 (Jul-Sep)
- [ ] Phase ζ temporal snapshots (drift detection)
- [ ] First BrainLessonPromotion approved (Janus working)
- [ ] First paying customer (pilot, probably Track 1 hedge fund)
- [ ] Morning brief automated (OpenClaw workflow)

### Q4 (Oct-Dec)
- [ ] 2-3 enterprise pilots active
- [ ] Calibration track record ≥ 1 year
- [ ] Target: 2,000+ sealed predictions, 500+ resolved
- [ ] BrainScorecard reliable signal

**End of 2027 state:**
- Full agent stack operational
- Hybrid graph layer live
- First revenue ($100K-$300K ARR from pilots)
- Calibration Moat credible for sales demonstrations

## 2028 — Scale + Hypothesis Generation

### Q1 (Jan-Mar)
- [ ] GraphMind hypothesis generation in production
- [ ] Cassandra generates 10+ hypotheses/day
- [ ] Morning briefs include hypotheses for founder review

### Q2 (Apr-Jun)
- [ ] 5-10 paying enterprise clients
- [ ] First think tank / government client
- [ ] Brain performance metrics start showing regime specialization

### Q3 (Jul-Sep)
- [ ] Calibration certification beta launch (limited forecasters)
- [ ] Public leaderboard live
- [ ] Marketing via published aggregate scorecards

### Q4 (Oct-Dec)
- [ ] First IPM-GPT fine-tune experiment (Llama 3.1 8B on predictions corpus)
- [ ] Evaluate: does domain-specific model outperform Llama 3.3 70B on IPM tasks?
- [ ] Target: 10,000+ sealed predictions, 3,000+ resolved

**End of 2028 state:**
- Agent system proven over 2+ years
- Calibration certification has early users (demonstrates uniqueness)
- Revenue: $600K-$1.5M ARR
- First acquisition interest from bigger players (early, not offers)

## 2029 — Diversification + Platform Maturity

### Q1-Q2
- [ ] Revenue diversification: Track 1 + Track 2 + Track 3 + Track 4 all active
- [ ] Consider first hire (data engineer or ingestion specialist)
- [ ] Platform UX polish (professional product, not bootstrapped feel)

### Q3-Q4
- [ ] IPM-GPT deployment (if experiments successful)
- [ ] Enterprise client count: 10-20
- [ ] Community-hosted instance offerings for gov/defense (air-gapped)

**End of 2029 state:**
- Revenue: $1.5M-$4M ARR
- Potentially raise Series A ($5M-$15M) if scaling choice made
- OR stay bootstrapped with smaller team (1-3 hires)
- Calibration track record: 3+ years, publicly auditable

## 2030-2031 — Platform Maturity + Possible Exit

### 2030
- [ ] Full agent stack v3 (AI-Native)
- [ ] 500-2,000 certified forecasters on platform
- [ ] API available to 3rd party developers (Track 5)
- [ ] Revenue: $3M-$8M ARR
- [ ] Acquisition offers start arriving (Bloomberg, S&P, Palantir, possibly sovereign wealth)

### 2031
- [ ] Revenue: $5M-$15M ARR
- [ ] Decision point: accept acquisition ($300M-$1B range) OR continue independent
- [ ] If independent: raise Series B or operate profitably
- [ ] Calibration Moat: 5 years of data, unfalsifiable credibility

## Capability milestones (across years)

### What the system can do by year

| Capability | 2026 | 2027 | 2028 | 2029 | 2030 |
|------------|------|------|------|------|------|
| Seal predictions with context | Manual | Auto | Auto | Auto | Auto |
| Resolve predictions mechanically | Manual | Semi | Auto | Auto | Auto |
| Compute Brier by regime | No | Yes | Yes | Yes | Yes |
| Generate hypotheses from graph | No | No | Yes | Yes | Yes |
| Detect narrative drift | No | Basic | Mature | Mature | Mature |
| Community-aware briefings | No | Yes | Yes | Yes | Yes |
| Propagation analysis | No | Basic | Advanced | Advanced | Advanced |
| Custom scenario planning | No | No | Yes | Yes | Yes |
| Promoted doctrine auto-applied | No | No | Yes | Yes | Yes |
| Regime-conditioned pricing | No | No | Yes | Yes | Yes |

## Technical capability evolution

### Prediction quality (Brier score target)

| Year | Target Brier score (macro, 30-90d horizon) | Notes |
|------|---|---|
| 2026 | 0.28 | Baseline, small sample |
| 2027 | 0.25 | More data, regime conditioning |
| 2028 | 0.22 | GraphMind hypotheses improving signal |
| 2029 | 0.20 | IPM-GPT fine-tune if deployed |
| 2030 | 0.18 | Mature system, compound learning |

For reference: random guess Brier = 0.25 for 50/50 predictions. Professional analysts typically 0.20-0.23 on comparable tasks. Target <0.20 beats industry standards.

### Graph richness

| Year | Nodes | Explicit edges | Semantic edges | Communities detected |
|------|-------|----------------|-----------------|--------------------|
| 2026 | 500 | 1,300 | 10,000 | 15-20 |
| 2027 | 1,500 | 5,000 | 35,000 | 35-50 |
| 2028 | 5,000 | 20,000 | 150,000 | 80-120 |
| 2029 | 15,000 | 60,000 | 500,000 | 150-250 |
| 2030 | 30,000+ | 150,000+ | 1,500,000+ | 300+ |

### Resolved predictions (Calibration Moat size)

| Year | Cumulative resolved |
|------|---|
| 2026 | 100 |
| 2027 | 2,000 |
| 2028 | 8,000 |
| 2029 | 25,000 |
| 2030 | 60,000+ |

## What IPM is NOT becoming (explicit non-goals)

- NOT a broker (no trade execution)
- NOT a chatbot (structured intelligence, not conversational)
- NOT a "general AI" platform (domain: geopolitics + macro + trading specifically)
- NOT open source of the production system (opens moat to arbitrage)
- NOT a consumer product for retail speculation
- NOT a newsletter (outputs are structured, auditable, API-accessible)

## Risks to roadmap

### Risk 1: BigTech duplication

Anthropic, OpenAI, Google could build graph-intelligence genérica. Mitigation: moat is not the algorithm but the **archive + curation + brand**. Their version would lack the 5-year Calibration track record.

### Risk 2: Key person dependency (founder burnout)

Solo founder is risk to 5-year execution. Mitigation: consider 1-2 hires at year 3+ when revenue supports. Keep critical agent architecture documented so successor could continue.

### Risk 3: Regulatory changes

EU AI Act, US state AI regulations could constrain operations. Mitigation: Germany-based, independent, non-advisory positioning. Calibration certification explicitly NOT investment advice.

### Risk 4: Calibration shows system doesn't outperform

If after 2 years, Brier scores don't meaningfully beat simple heuristics, pivot required. Mitigation: early signal at year 1 from pilot customers gives time to adjust. Worst case: platform pivots to "intelligence management" (not prediction).

## Critical path dependencies

```
Phase 5 frontend (2026 Q2)
  ↓
OpenClaw + n8n (2026 Q3)
  ↓
First agents deployed (2026 Q3-Q4)
  ↓
pgvector + KNN (2026 Q4)
  ↓
Hybrid graph layer live (2027 Q1-Q2)
  ↓
Full agent stack (2027 Q2)
  ↓
First paying customer (2027 Q3)
  ↓
Calibration year 1 complete (2027 Q4)
  ↓
Revenue diversification (2028+)
```

Any delay early cascades. Prioritize frontend + OpenClaw + first agents in 2026. These are foundational.
