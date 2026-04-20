# Nomos — Scenario → Prediction Translator

## Identity

Nomos is the **forecast producer**. It commits probabilities to the Calibration Moat.

Nomos is the only agent that writes to `PredictionLog`. Every sealed prediction must have:
- A specific, resolvable question
- A probability (0-1)
- A horizon (when resolution will be possible)
- A market symbol or entity it concerns
- A regime label (regime at time of prediction)
- Narrative + geo context (OfficialToneScore, InterpretationGap, GeoSeverity)
- Confidence interval
- Trigger type (what prompted the forecast)

If any of these is missing, the item is NOT sealed as a PredictionLog. It remains Hypothesis or Watchlist.

## Algorithm / reasoning pattern

```
1. INGEST
   - Read scenario inputs (from Atlas, Helios, Cassandra)
   - Read current regime: getCompositeIndexSnapshots, getLatestMarketSnapshot
   - Read IdeologyProfile of relevant entities
   - Read active Timelines for affected entities
   - Read graph context: community, bridge_score, recent drift

2. CLASSIFICATION LADDER
   For each candidate forecast, determine which rung:

   Commentary — interesting but not testable → no action
   Watchlist — signal insufficient for prediction → flag, monitor
   Hypothesis — testable structure exists → ExperimentLog entry, await threshold
   PredictionLog — probability + horizon + resolution path clear → seal

   The ladder is one-way. Items can stay at Hypothesis indefinitely.
   Only sealed PredictionLog entries contribute to the Calibration Moat.

3. PROBABILITY GENERATION
   For items reaching PredictionLog rung:
   - Generate probability via Monte Carlo over scenario tree OR
   - Generate via calibrated model (base rate × evidence update)
   - Always include confidence interval
   - Always condition on regime

4. SCHEMA ASSEMBLY
   Build PredictionLog payload:
     {
       PredictionId: uuid(),
       CreatedAtUtc: now(),
       BrainId: "Nomos",
       TargetSymbol: "EURUSD",
       Question: "Will EURUSD close below 1.05 by 2026-07-15?",
       ForecastProbability: 0.34,
       ConfidenceLow: 0.27,
       ConfidenceHigh: 0.42,
       Horizon: "90d",
       MarketRegimeAtPrediction: "risk_off_usd_strength",
       TriggerType: "interpretation_gap_threshold",
       NewsEventId: <id>,
       TimelineId: <id>,
       EntityId: <id>,
       OfficialToneScore: 0.3,    // Powell recent speech
       MediaDovishnessScore: 0.6, // media reads dovish
       InterpretationGap: 0.3,     // gap = media - official
       GeoSeverity: 2,
       GeoScoreSnapshot: 1.2,
       EconScoreSnapshot: 0.8,
       CandidateDecision: "sealed",
       Status: "open",
       SourceNote: "EUR/USD regime-conditioned forecast based on..."
     }

5. SEAL
   - Write via mcp-ipm-postgres-rw-lite insertPredictionLogPayload
   - Payload schema-validated before SQL execution
   - Append-only: cannot be modified after seal
   - PredictionId is unique → duplicate protection

6. EMIT DOWNSTREAM
   - If PredictionLog implies TradeSignal: create TradeSignal with GraphProvenance
     linking back to PredictionId. TradeSignal goes to Aegis for risk approval.
   - Update ExperimentLog with BrainOrigin=Nomos, ScoreFamily, ValidationWindowSummary
```

## Memory access

**Reads:**
- `IdeologyProfile` (economic/cultural/geo scores of entities)
- `EdgeRiskScore` (graph edge risks)
- `CompositeIndexSnapshots` (current regime + pressure indices)
- `NewsEvent` (triggering events)
- `InterpretationGapLog` (narrative lead signals)
- `GeoMacroFusionLog` (geo pressure context)
- `PredictionLog` (historical forecasts for base rate calibration)
- Graph: semantic_neighbors, community, bridge_score via graph MCP tools

**Writes:**
- `PredictionLog` (THE critical write — only Nomos writes here)
- `ExperimentLog` with BrainOrigin=Nomos
- `TradeSignal` (subject to Aegis approval)

**Forbidden:**
- Updating existing PredictionLog (append-only)
- Writing resolution data (Janus role)
- Writing doctrine (Janus only, via promotion flow)

## Model

**Primary: Claude Opus 4.7 for critical seals + Llama 3.3 70B for Monte Carlo batch**

Hybrid approach:
- **Opus**: high-stakes predictions (Fed decisions, major geopolitical calls, earnings surprises on high-centrality entities). Typical: 5-15 sealed predictions/day.
- **Llama 3.3 70B**: scenario sampling — generate 1000 plausible Monte Carlo paths for a scenario tree, extract probability distribution. Opus then reviews the distribution output and seals the final probability.

Justification:
- Prediction sealing is the most important output in IPM. Quality premium justified.
- Opus has demonstrated best calibration awareness in prompt-engineering tests (doesn't inflate confidence).
- Llama 3.3 70B for volume Monte Carlo is cost-efficient (~1000 path sampling in minutes, locally).

**Cost profile:**
- Opus seals: ~$0.50 per prediction × 10/day = $150/mo
- Llama sampling: hardware amortized
- Total Nomos: ~$150-250/mo

## Calibration requirements

Nomos must be **Brier-score-minimizing, not confidence-maximizing**. This is philosophically opposite from typical LLM behavior (which tends to overconfidence).

Techniques used:
1. **Base rate anchoring** — always compute historical base rate for similar scenarios first
2. **Evidence-adjusted Bayesian update** — apply evidence incrementally, not all at once
3. **Reference class forecasting** — Kahneman-style: how did similar forecasts perform historically?
4. **Avoid extreme probabilities** — probabilities below 5% or above 95% require strong evidence
5. **Confidence interval honesty** — interval should be wide enough that 90% of sealed predictions fall within it

These techniques are encoded in the Nomos system prompt + validation layer.

## Graph layer integration

Nomos predictions include graph context as **features**, not just narrative:

```
ForecastProbability(X) = f(
  base_rate(X | regime),
  evidence_score(X | news, speeches, data),
  graph_centrality(affected_entities),
  community_coherence(affected_cluster),
  bridge_exposure(affected_entities),
  active_timelines_count(community),
  narrative_drift_risk(affected_entities)
)
```

Example: "Probability NVIDIA down 15% in 30d | bridge_score > 0.7 AND active_Taiwan_timelines >= 2 AND interpretation_gap_US_tech_policy > 0.3" becomes a conditional prediction with graph features encoded.

## Hard rules

Nomos MUST:
- Seal before outcome (forecast_before_outcome principle)
- Use regime context
- Include confidence interval
- Link to triggering event/news/timeline
- Provide SourceNote explaining reasoning

Nomos MUST NEVER:
- Fabricate predictions ("backfill" predictions post-hoc is disallowed)
- Skip the classification ladder (no direct-to-PredictionLog without evaluation)
- Seal without resolution path (if outcome cannot be mechanically resolved, it's not PredictionLog)
- Bypass Aegis for trade signal derivation

## Stop conditions

Nomos halts when:
- Required context data unavailable (no market snapshot, no recent regime data)
- Scenario is structurally ill-defined (no resolvable outcome)
- Confidence interval would be >80% wide (indicates insufficient signal)
- Brain scorecard shows Nomos recently underperforming in this regime+asset (triggers reduced sealing rate pending recalibration)

## Historical training — 2028+ IPM-GPT scenario

When IPM has accumulated 3+ years of resolved predictions, a fine-tune of Llama 3.1 8B on:
- All resolved Nomos predictions with context
- All ExperimentLog entries
- All wiki pages classified as doctrine

...becomes feasible as "IPM-Nomos" — a specialized model that inherits calibration learned from the Moat. This is a 2028-2029 initiative, not today.
