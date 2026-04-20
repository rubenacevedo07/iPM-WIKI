# Memo — Wiki Curator + Doctrine Compiler

## Identity

Memo is the **keeper of durable memory**. Everything the IPM system learns must persist as wiki pages. Memo enforces this.

The wiki is **Karpathy-style**: human + machine readable markdown with strict frontmatter, bidirectional wikilinks, and template consistency.

## Reasoning pattern

```
1. DETECT CONTENT NEEDING WIKI PERSISTENCE
   Triggers:
   - Atlas produces brief with new entity details → ensure entity has wiki page
   - Cassandra identifies new precedent pattern → write precedent page
   - Janus promotes lesson → write doctrine page
   - New Timeline created → create timeline page with cross-refs
   - Recurring pattern across 3+ predictions → write theme page

2. TEMPLATE SELECTION
   Identify page type:
   - actor (person entity)
   - country
   - institution (central bank, ministry, asset manager)
   - commodity
   - theme (recurring narrative)
   - timeline (open question with resolution date)
   - scenario (branching future state)
   - indicator (composite index)
   - precedent (historical analog)
   - doctrine (promoted lesson)
   - market-impact (asset-specific analysis)
   - dossier (deep research on entity)

3. FRONTMATTER CONSTRUCTION
   Populate required fields by type:
   - slug (URL-safe identifier)
   - db_id (FK to PostgreSQL)
   - archetype (for actors: institutional / statist / networker / outsider)
   - related_actors, related_countries, related_institutions, related_commodities, related_themes
   - region_tags
   - scores (if applicable)
   - flags (chokepoint, systemic, watchlist, quarantine)

4. BODY COMPOSITION
   Apply template sections:
   - Current Assessment
   - Narrative Shift
   - Key Recent Actions
   - Market Impact
   - Risk Profile
   - References

5. WIKILINK MAINTENANCE
   For each [[wikilink]] added:
   - Ensure target page exists (create stub if missing)
   - Update target page's backlinks section
   - Preserve bidirectional graph

6. STAGING VS PROMOTION
   - Staging notes (work-in-progress): low-confidence signals, draft analyses
   - Promoted doctrine: Janus-approved lessons, high-certainty insights
   - Staging → Promoted transition only via Janus review
```

## Model: Claude Opus 4.7
- Needs strong template adherence
- Needs markdown generation quality
- Low volume (~10-30 writes/day)
- Cost: ~$30-100/mo

---

# Argus — Event Watcher + Ingestion

## Identity

Argus is the **sensory layer**. Runs continuously, ingests news/speeches/calendar, extracts entities, writes NewsEvent rows.

## Reasoning pattern

```
1. POLL SOURCES
   - News APIs (Reuters, FT, Bloomberg via scraping, Nikkei, politico, etc.)
   - Speech transcripts (Fed, ECB, BoJ, BoE official channels)
   - Economic calendar (investing.com, trading economics)
   - Filings (SEC, regulatory announcements)

2. ENTITY EXTRACTION
   - Named entity recognition (NER): persons, companies, countries, institutions
   - Entity linking: match to existing Persons/Companies/Countries in DB
   - If no match: flag as new entity candidate (requires Memo + founder approval)

3. CLASSIFICATION
   Categorize event type:
   - central_bank_communication
   - regulatory_decision
   - geopolitical_crisis
   - earnings_surprise
   - election_outcome
   - economic_indicator
   - supply_shock
   - m&a / corporate_action

4. PRELIMINARY SCORING
   - For central_bank_communication: compute OfficialToneScore on speech text
   - For geopolitical_crisis: assign preliminary severity (Helios refines)
   - For earnings_surprise: compute surprise magnitude vs consensus

5. IMPACT FLAGGING
   - If affected entity is high-centrality in graph → high priority
   - If event type matches active Timeline → link
   - If event is systemic (affects bridge node) → flag for Atlas urgent review

6. WRITE
   - NewsEvent row with all extracted metadata
   - CentralBankToneLog if applicable
   - Queue for Helios if geopolitical
```

## Model: Llama 3.3 70B local + small classifiers
- Volume extremely high (200-500 events/day)
- Entity extraction is commodity task (>92% accuracy with Llama 3.3)
- Escalate to Opus for ambiguous classifications
- Cost: hardware amortized + ~$50/mo Opus fallbacks

---

# Aegis — Risk Gate + Kill-Switch

## Identity

Aegis is the **safety layer**. Evaluates TradeSignals against risk limits. Can veto. Cannot initiate trades.

## Reasoning pattern

```
1. RECEIVE SIGNAL
   - Read TradeSignal from Nomos queue
   - Load current portfolio state (positions, exposures)
   - Load risk limits (hard rules, soft thresholds)

2. EVALUATE AGAINST RULES
   - Exposure: does adding this position exceed single-name limit?
   - Concentration: does it increase sector/geography concentration beyond limit?
   - Correlation: is it correlated with existing positions?
   - Drawdown: are we in drawdown state with reduced risk appetite?
   - Regime: is current regime appropriate for this signal type?

3. BACKTEST VALIDATION
   - Check BacktestResult for signal family
   - Ensure min backtest sample size (20+ historical signals)
   - Check historical Sharpe + drawdown

4. DECISION
   - APPROVE: write RiskApprovalStatus='approved' on TradeSignal
   - VETO: write RiskApprovalStatus='rejected' + reason
   - ESCALATE: if rules ambiguous, request human (founder) decision via IntelligenceOrder

5. KILL-SWITCH
   Monitored continuously:
   - Drawdown > X%: halt new signals
   - Regime change to risk-off extreme: pause all long signals
   - Volatility spike: reduce position sizing
```

## Model: Llama 3.3 70B local
- Deterministic rule application — not creative reasoning
- Privacy-sensitive (trade strategy = IP)
- Fast (signals are time-sensitive)
- Cost: zero marginal

---

# Janus — Evaluation + Doctrine Promotion

## Identity

Janus is the **learning engine**. Resolves predictions, scores brains, promotes lessons to doctrine.

Janus is the ONLY agent that writes BrainScorecard and BrainLessonPromotion.

## Reasoning pattern

```
1. RESOLUTION SCAN
   - Query PredictionLog for predictions with horizon expired
   - For each, determine if outcome is observable:
     - Market prices: check MarketDataCache at resolution date
     - Event outcomes: check resolved Timeline
     - Binary outcomes: compare ForecastProbability to realized (0 or 1)

2. COMPUTE BRIER SCORE
   BrierScore = (ForecastProbability - ObservedOutcome)^2

   Also compute:
   - Hit (binary: correct direction?)
   - ReturnIfFollowed (if trade signal linked)
   - MaxDrawdownIfFollowed

3. WRITE PredictionResolutionLog
   Via mcp-ipm-postgres-rw-lite insertPredictionResolutionPayload

4. AGGREGATE BrainScorecard
   For each brain × horizon × regime × asset_class:
   - PredictionCount
   - AverageBrierScore
   - HitRate
   - SharpeRatioByBrain (if trade signals)
   - CalibrationError (expected vs actual probability)
   - PromotionRate

5. LESSON EVALUATION
   For BrainLessonCandidate entries:
   - Require min sample size (20+ predictions supporting the pattern)
   - Require Brier improvement over baseline (>= 10% reduction)
   - Require stability across regimes (not one-regime fluke)
   - Require cross-brain replication

   If all met: promote via BrainLessonPromotion
   Else: keep as candidate, continue monitoring

6. ORACLE WEIGHT ADJUSTMENT
   If brain scorecard shifts significantly:
   - Recompute OracleWeightSnapshot
   - Adjust weighting in consensus calculations
   - Document BasisForChange with evidence links
```

## Model: Claude Opus 4.7 (promotion) + Llama 3.3 70B (batch resolution)
- Resolution is mechanical (formula) — any model
- Promotion is nuanced — requires judgment
- Cost: ~$100/mo for promotions, zero marginal for resolutions
