# IPM Master Business Model — 12 Revenue Streams across 3 Commercial Layers

**Last updated:** 2026-04-18
**Status:** Consolidated from 9 source documents + agent stack architecture

---

## 1. Strategic reframe

IPM is not one product. IPM is **three commercial layers that can be sold independently or bundled**:

```
┌──────────────────────────────────────────────────────────────────┐
│  LAYER 1 — WORLD MODEL ENGINE                                    │
│  The durable moat: graph + calibration + structured truth         │
│  - 121 tables, 27 views, 148 functions, 1,294 edges               │
│  - Calibration Moat (PredictionLog + resolution + scorecards)     │
│  - Hybrid graph (explicit + KNN semantic + Louvain)               │
│  - Wiki-backed narrative memory                                   │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  LAYER 2 — AGENT CONTEXT INFRASTRUCTURE                          │
│  API access for agents (OpenClaw, Claude Code, n8n, 3rd party)   │
│  - MCP servers (7 narrow-permission servers)                      │
│  - Atlas v1/v2 orchestration                                      │
│  - Graph-RAG endpoints                                            │
│  - Scorecards + calibration metrics API                           │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  LAYER 3 — VISUAL WORKSTATION PLATFORM                           │
│  Premium UX: overlays, globe, dossiers, relation views           │
│  - Bloomberg-terminal quality, independent aesthetic              │
│  - Customizable per vertical (macro, commodity, geo, OSINT)      │
│  - White-label potential                                          │
│  - Visual operating system for agents                             │
└──────────────────────────────────────────────────────────────────┘
```

Each layer commands different pricing, serves different buyers, and scales differently.

### Sub-brand architecture

Under parent brand **IMP** (Intelligence, Markets, Power), we have 5 modules that can be sold/marketed separately:

| Sub-brand | Domain | Primary layer |
|-----------|--------|---------------|
| **IMP Core** | Research + workflow + scenarios | All 3 layers |
| **IMP Markets** | Forecasting (non-real-money prediction market) | Layer 3 primarily |
| **IMP Experts** | Expert marketplace + certification | Layer 3 primarily |
| **IMP Foresight** | Leader future visions + scenario intelligence | Layer 1 + Layer 3 |
| **IMP Risk** | Systemic risk + tokenization + chokepoint | Layer 1 + Layer 3 |

---

## 2. The 12 revenue streams — ranked by time-to-revenue

### TIER A — Can launch within 6-12 months (2026 H2 / 2027 H1)

#### Stream 1: IMP Pro (Freemium + Pro subscriptions)

**Layer:** 3 (Visual Platform)
**Buyer:** Individual analysts, sophisticated retail traders, journalists, grad students, researchers
**Pricing:**
- Free: limited overlays, 30-day history
- Pro $49/mo: full history, advanced scenarios, watchlists
- Premium $99/mo: Pro + API access + weekly briefings

**Revenue math:**
- Year 1: 100 Pro users = $5K/mo = $60K ARR
- Year 2: 500 Pro users = $25K/mo = $300K ARR
- Year 3: 2,000 Pro users = $100K/mo = $1.2M ARR
- Year 5: 5,000 users mixed = $2.5M ARR

**Role:** Top-of-funnel + data flywheel + brand building

---

#### Stream 2: Predictive Research Reports

**Sub-brand:** IMP Core + IMP Foresight
**Layer:** 1 + 3
**Buyer:** Family offices, RIAs, corporate strategy teams
**Pricing:** $2K-$10K per report, or $20K-$80K per quarterly subscription (4 reports)

**Reports examples:**
- "EUR/USD 90-day macro regime analysis"
- "Taiwan Strait supply chain vulnerability 2027"
- "Saudi Arabia post-oil transition: 10-year forecast"
- "Tokenized finance systemic risks" (IMP Risk product)

**Revenue math:**
- Year 1: 10 reports/month × $3K avg = $30K/mo = $360K ARR
- Year 3: 40 reports/mo + 10 quarterly subs = $150K/mo = $1.8M ARR

**Role:** Cashflow generation + client learning loop

---

#### Stream 3: IMP Foresight — Leader Future Vision Intelligence

**Sub-brand:** IMP Foresight
**Layer:** 1 + 3
**Buyer:** Policy researchers, strategic consultants, family offices, think tanks, corporate strategy, nation-state intelligence (friendly)

**Product:** Structured database + dashboard mapping the stated future visions of:
- Political leaders (Xi, Putin, Trump, Macron, Meloni, Modi)
- Central bankers (Powell, Lagarde, Bailey)
- CEOs with geopolitical weight (Musk, Fink, Altman, Dalio, Huang)
- Military strategists
- Sovereign wealth decision-makers (PIF, GIC, Norges Bank, CIC)
- Multilateral institutions (IMF, World Bank, BIS)

**Data model per leader:**
- Future vision by theme: economy, technology, war, energy, governance, AI, demography
- Time horizon: near/medium/long-term
- Sources: speeches, interviews, policy papers, annual letters
- **Contradictions over time** (flag when vision shifts — narrative drift signal)
- Influence score + scenario relevance

**Pricing:**
- Individual analyst: $199/mo
- Team (5 seats): $799/mo
- Enterprise: $2K-$10K/mo with custom research

**Revenue math:**
- Year 2: 50 individual + 5 teams = $14K/mo = $170K ARR
- Year 4: 300 individual + 30 teams + 5 enterprise = $100K/mo = $1.2M ARR

**Why this works:** Zero direct competition. Eurasia Group does similar but qualitative + expensive. IMP Foresight is structured, queryable, auditable. Unique value prop.

---

### TIER B — Launch 12-24 months (2027-2028)

#### Stream 4: Intelligence-as-a-Service for Hedge Funds

**Sub-brand:** IMP Core + Risk
**Layer:** 1 + 3 (full stack access)
**Buyer:** Hedge funds $50M-$500M AUM
**Pricing:** $60K-$150K/year per fund

**Product:**
- Platform access for analyst team
- Custom API integration
- Auditable Brier scorecards (unique selling point)
- 2x/week founder commentary
- Custom scenarios

**Revenue math:**
- Year 2: 2-3 pilots = $150K ARR
- Year 3: 5-8 clients = $500K-$1M ARR
- Year 5: 8-12 clients = $900K-$1.8M ARR

**Critical dependency:** 18+ months of public calibration track record before serious pitching.

---

#### Stream 5: IMP Experts (Expert Marketplace)

**Sub-brand:** IMP Experts
**Layer:** 3 (Visual Platform) primarily
**Buyer dual-sided:**
- **Supply side:** top analysts, macro commentators, trading educators (creators)
- **Demand side:** traders, investors, allocators wanting access to expertise

**Product:**
- Verified expert profiles
- Subscription access to strategy pages, private notes, journals, historical calls
- Payment split: 70% expert / 30% IMP
- Integrated with IMP certification (creates credibility moat)

**Revenue math (IMP's 30% take):**
- Year 2: 20 experts × $5K/mo avg × 30% = $3K/mo = $36K ARR
- Year 4: 100 experts × $8K/mo avg × 30% = $24K/mo = $288K ARR
- Year 5: 300 experts × $12K/mo avg × 30% = $108K/mo = $1.3M ARR

**Why this works:** Substack × Seeking Alpha × CFA. Creators already proven business model. IMP adds verified calibration as unique differentiation.

---

#### Stream 6: Calibration Certification Program

**Sub-brand:** IMP Experts
**Layer:** 1 (Calibration Moat as core)
**Buyer:** Newsletter operators, LinkedIn/X analysts, trading educators, research analysts, journalists, think tank researchers

**Pricing:**
- Basic $500/mo: 20 predictions/mo, public badge
- Pro $1,500/mo: unlimited, custom niche, premium badge
- Elite $5,000/mo: team accounts, API access, custom reports

**Revenue math (mature year 4-5):**
- 300 Basic + 150 Pro + 30 Elite = $525K/mo = **$6.3M ARR**

**Market:** ~20-25K addressable forecasters globally. Capturing 1-3% = 200-750 certified.

**Why this is the biggest moat:** Network effect. More forecasters → more credibility → more aspirants. Zero competitors. CFA Institute equivalent revenue: $400M+.

---

#### Stream 7: IMP Markets — European Play-Money Prediction Market

**Sub-brand:** IMP Markets
**Layer:** 3 (Visual Platform)
**Buyer:** Sophisticated retail, institutional teams wanting forecasting exercise, universities, corporate strategy teams, policy research

**Product:**
- European Polymarket-alternative but **without real money** (regulatory-safe in EU)
- Virtual credits + leaderboards
- Focus: Europe-specific markets (elections, ECB decisions, sanctions, regulation, energy)
- Resolution engine with transparent criteria
- Reputation-based scoring

**Why non-real-money:**
- EU regulation for prediction markets fragmented (gambling vs financial instrument depending on country)
- Non-real-money version legally clean
- Preserves forecasting + signal value
- Polymarket Europe-banned users are addressable market

**Pricing:**
- Free tier: basic participation
- Pro $29/mo: advanced analytics, historical performance, API
- Enterprise $2K-$20K/mo: team accounts, custom markets, private leagues for corporate/university use

**Revenue math:**
- Year 3: 5K free + 200 Pro + 3 enterprise = $9K/mo = $108K ARR
- Year 5: 50K free + 2K Pro + 30 enterprise = $118K/mo = $1.4M ARR

**Dual value:** Revenue stream + data moat (aggregated predictions feed IMP Core signals).

---

### TIER C — Launch 24-48 months (2028-2030)

#### Stream 8: Claude Trading Strategy OS ⭐ Big opportunity

**Sub-brand:** IMP Core (trading vertical)
**Layer:** 3 + 2
**Buyer:** Individual discretionary traders (10M+ TradingView paid users), prop traders, small trading teams, trading educators

**Product (from claude_trading_platform_marketing_document.md):**
- Structured playbook builder (capture trading setup in structured fields)
- Claude converts playbook → Pine Script / Python code
- Automated backtest orchestration (via TradingView or custom engine)
- Alert generation + pre-session checklists
- Trade journal + automatic autopsy (screenshots → pattern tags → coaching feedback)
- Version control on strategies, prompts, results

**Critical positioning:**
- NOT "AI predicts markets" (lawsuits + bad reputation)
- YES "AI operationalizes trader's edge"
- NOT signal service
- YES process automation tool

**Pricing:**
- Starter $49/mo: basic playbook → code
- Pro $199/mo: full workflow + backtest + journal
- Teams $499/mo: multi-user + governance + audit trail
- Institutional $2K-$10K/mo: compliance + integration with broker APIs

**Revenue math:**
- Year 3: 500 Starter + 100 Pro + 5 Teams = $44K/mo = $528K ARR
- Year 5: 5K Starter + 1K Pro + 50 Teams + 5 Institutional = $522K/mo = **$6.3M ARR**

**Why this works:**
- TradingView 90M+ users, ~10M paid → huge TAM
- Claude/OpenAI already proven as coding assistants for traders
- Nobody has packaged as end-to-end workflow OS
- Integration with IMP Core = differentiation (structural context as input)

**Integration with existing IMP:** This product uses IMP Core as intelligence substrate. Strategies built here reference IMP signals. Creates cross-sell.

---

#### Stream 9: IMP Risk — Tokenization Systemic Risk Intelligence

**Sub-brand:** IMP Risk
**Layer:** 1 + 3 (investigation + visualization)
**Buyer:** Central banks, regulators, systemic risk teams at large banks, policy researchers, specialized hedge funds (macro)

**Context (from imp_platform_master_brief.md):**
- IMF warned tokenized finance could accelerate crises
- Major exchanges pushing crypto into market plumbing
- Settlement risk, 24/7 markets, collateral spirals = new systemic questions

**Product:**
- Ongoing research stream + quarterly deep reports
- Real-time monitoring dashboard: tokenization infrastructure state, systemic risk metrics, contagion channels
- Scenario library: "Tokenized Treasury freeze", "Stablecoin bank run", "24/7 margin call cascade"
- Early-warning system with thresholds

**Pricing:**
- Research subscription $5K-$20K/year (reports + access to data)
- Enterprise monitoring $50K-$250K/year (real-time + API + custom)
- Consulting $500-$2K/hr for specific investigations

**Revenue math:**
- Year 3: 10 research + 2 enterprise = $120K/year = $120K ARR
- Year 5: 40 research + 10 enterprise + consulting = $2M-$4M ARR

**Why this works:**
- Nobody has a dedicated monitoring system for tokenization systemic risks
- Regulators NEED this, aren't staffed for it
- Very specific niche = low competition = high pricing power

---

#### Stream 10: API / Context Infrastructure for Agents (B2B2C)

**Sub-brand:** IMP Core API
**Layer:** 2 (Agent Context Infrastructure)
**Buyer:** AI startups building analyst copilots, fintech platforms, research platforms

**Product:**
- `/api/v1/graph/{entity}` — graph subsection
- `/api/v1/scorecard/{brain}/{regime}` — calibration metrics
- `/api/v1/prediction/{topic}` — current predictions + historical
- `/api/v1/risk/{entity}` — risk scoring
- `/api/v1/scenario/{id}` — scenario tree + probabilities

**Pricing:**
- Developer: $500/mo for 10K calls
- Growth: $2K/mo for 100K calls
- Enterprise: $10K-$100K/mo custom

**Revenue math:**
- Year 3: 10 Developer + 3 Growth = $11K/mo = $132K ARR
- Year 5: 50 Developer + 15 Growth + 3 Enterprise = $180K/mo = $2.2M ARR

**Role:** Distribution amplifier. Other products integrate IMP → IMP becomes default infrastructure.

---

### TIER D — Launch 48+ months (2030+)

#### Stream 11: White-label Visual Platform

**Sub-brand:** IMP Platform
**Layer:** 3 (Visual Platform)
**Buyer:** Large consulting firms, boutique research firms, sovereign wealth funds, central banks wanting private deployments

**Product:**
- IPM frontend deployed with client branding
- Client data + IMP intelligence integrated
- Custom entities, overlays, workflows
- Air-gapped deployment options (for gov/defense)

**Pricing:** $500K-$5M/year per white-label client
**Target:** 3-8 clients in years 4-6
**Revenue range:** $2M-$15M ARR

**Why this works:** Premium customers who don't want SaaS but want IMP's capabilities.

---

#### Stream 12: Private Intelligence for Hedge Funds (Exclusive Premium)

**Sub-brand:** IMP Core Premium
**Layer:** 1 + 2 + 3 (full stack)
**Buyer:** Top-tier hedge funds ($1B+ AUM) willing to pay for exclusivity
**Pricing:** $500K-$2M/year per client

**Differentiation from Stream 4:**
- Stream 4 = $60-150K, platform access, SaaS
- Stream 12 = $500K-2M, exclusive access, custom research, founder direct relationship

**Product:**
- Real-time predictions with reasoning chains
- Graph context access
- Custom scenarios on request
- Monthly founder calls
- Early access to new signals before they reach public track

**Revenue math:**
- Year 5: 3-5 clients × $1M avg = **$3-5M ARR**

**Max ceiling:** 5-7 clients (service constraints). After that, requires team.

**Why exclusivity matters:**
- Soros reflexivity applied to product: publishing signals → arbitrage → value destruction
- Privacy preserves premium pricing
- Bridgewater model (Daily Observations paid, trading propio)

---

## 3. 5-year revenue stack projection (aggregate)

### Conservative scenario

```
Year 2026: $0 (pre-launch + calibration accumulation)
Year 2027: $300K-$600K ARR
Year 2028: $1.2M-$2.5M ARR
Year 2029: $3M-$6M ARR
Year 2030: $6M-$12M ARR
Year 2031: $10M-$25M ARR
```

### Aggressive scenario (everything goes right)

$25M-$50M ARR by 2031. Acquisition offers from Bloomberg/S&P/Palantir in the $500M-$2B range.

---

## 4. Data source strategy

### Free / low-cost essentials (2026-2027)
- **FRED**: US macro data, $0
- **ECB Data Portal**: EU macro, $0
- **World Bank Open Data**: global macro, $0
- **GDELT**: global events database, $0
- **SEC EDGAR**: filings, $0
- **Frankfurter**: FX rates, $0
- **CoinGecko**: crypto free tier
- **Wikipedia dumps**: entity base

**Total**: $0/month. Covers 60-70% of Tier 1 revenue needs.

### Paid Tier 1 ($200-500/mo total)
- **Trading Economics**: calendar + macro, $49-$299/mo
- **Finnhub**: equities + news, $0-$79/mo
- **Alpha Vantage**: equities + FX + commodities, $0-$250/mo
- **Polymarket API**: prediction data, free
- **NewsAPI**: news aggregation, $0-$449/mo

### Paid Tier 2 ($1K-5K/mo at scale)
- **FactSet / Refinitiv lite**: institutional data
- **S&P CapitalIQ**: fundamentals + ownership data
- **CB Insights / Pitchbook**: private market intelligence
- **Bloomberg Terminal**: only if absolutely necessary ($25K/seat/year)

### Investing.com specifically

**Assessment**: No public official API. Scraping = fragile + legally gray.

**Better-positioned alternatives**:
- For calendar: Trading Economics API ($49/mo)
- For technical analysis: TradingView (via Pine Script ecosystem)
- For sentiment: NewsAPI + custom NLP

**Recommendation**: Do NOT depend on investing.com as backbone. OK as experimental secondary source, not infrastructure.

---

## 5. Time-to-revenue matrix

| Stream | Earliest launch | Conservative ARR Year 3 | Ceiling ARR Year 5 |
|--------|-----------------|-------------------------|--------------------|
| 1. Pro subs | 2026 Q4 | $300K | $2.5M |
| 2. Research reports | 2026 Q4 | $500K | $2M |
| 3. Foresight | 2027 Q2 | $170K | $1.5M |
| 4. HF Intelligence | 2027 Q3 | $500K | $1.8M |
| 5. Expert Marketplace | 2028 Q1 | $100K | $1.3M |
| 6. Certification | 2028 Q2 | $600K | $6.3M |
| 7. IMP Markets | 2028 Q3 | $108K | $1.4M |
| 8. Trading Strategy OS | 2029 Q1 | $500K | $6.3M |
| 9. IMP Risk | 2029 Q2 | $150K | $4M |
| 10. API infrastructure | 2029 Q3 | $130K | $2.2M |
| 11. White-label | 2030 Q1 | n/a | $15M |
| 12. Premium HF | 2029 Q4 | $1M | $5M |

**Sum Year 3 (conservative):** $3M-$5M ARR
**Sum Year 5 (conservative):** $12M-$25M ARR
**Sum Year 5 (aggressive):** $30M-$50M ARR

---

## 6. Strategic priorities for the founder

### Do NOT try to launch all 12 simultaneously

Single-founder constraint requires serialization. Order:

**Phase 1 (2026 H2 - 2027 H1):** Foundation
- Launch Stream 1 (Pro subs) — drives brand + data flywheel
- Launch Stream 2 (Research reports) — cashflow + learning
- Launch Stream 3 (Foresight) — differentiation

**Phase 2 (2027 H2 - 2028):** Enterprise
- Launch Stream 4 (HF pilots)
- Beta Stream 5 (Experts) + Stream 6 (Certification)
- Beta Stream 7 (IMP Markets)

**Phase 3 (2028-2029):** Scale
- Scale Streams 4-7
- Launch Stream 8 (Trading OS) — massive TAM
- Launch Stream 9 (IMP Risk) — niche premium
- Beta Stream 10 (API)

**Phase 4 (2030+):** Maturity
- Scale all streams
- Launch Stream 11 (White-label) with enterprise clients
- Launch Stream 12 (Premium HF) with top-tier clients
- Consider Series A or acquisition

### Key decision: exclusivity vs scale

Three orientations:

1. **Private-first** (3-5 premium HF clients, $5-10M ARR ceiling): Streams 12 + 4 + selected. Bridgewater model.

2. **Certification-first** (Track 4 as flagship, $3-8M ARR from certification alone): Stream 6 primary. CFA model.

3. **Platform-first** (balanced portfolio, $10-25M ARR): All streams modest scale. Bloomberg lite.

**Recommendation:** Private-first framework 2027-2028 (generates cash), then expand to Platform-first 2029-2030 when team + infra support it. Avoid Certification-first as primary — too dependent on 3+ years track record before launch.

---

## 7. Branding + positioning

From `Refining the branding strategy...md`:

**Core positioning sentence:**
> "An AI-driven intelligence platform that turns global signals, expert strategies, and foresight into an institutional operating layer for decisions."

**Three pillars:**
1. Structured intelligence (geopolitics + markets + leader visions)
2. Automated workflows (idea to validated strategy)
3. Trusted foresight (risk, tokenization, systemic early warnings)

**Tagline candidates:**
- "Intelligence infrastructure for the next crisis cycle"
- "Where signals, strategies, and foresight connect"
- "From global noise to institutional conviction"

**Visual direction:**
- Deep navy/ink + muted beige + restrained accent (old-gold or teal)
- Serif headlines + clean sans-serif body
- Maps, flows, graphs, information diagrams
- Zero AI-stock-photo aesthetic

**Brand rule:** "Sounds like an institutional memo, looks like a modern product."

---

## 8. What NOT to do (explicit non-goals)

- Do NOT position as "AI predicts the market" (lawsuits, bad reputation)
- Do NOT enter crowded consumer trading app space
- Do NOT open-source production system (arbitrages moat)
- Do NOT depend on investing.com scraping for production
- Do NOT try to launch >3 streams simultaneously as solo founder
- Do NOT sell investment advice directly (regulatory nightmare)
- Do NOT promise calibration that isn't yet demonstrated (need 18+ months track record before Tier B pitches)
- Do NOT expand to new geographies before consolidating EU/US

---

## 9. What makes IPM unique (defensibility)

1. **The Calibration Moat** — non-fabricable, compounds daily, can't be bought
2. **Graph-conditioned reasoning** — structural intelligence competitors don't have
3. **Multi-layer architecture** — can monetize 3 layers separately OR bundled
4. **Founder positioning** — European, independent, solo, technical — different from US-aligned Palantir, corporate Bloomberg, consumer Polymarket
5. **Wiki as training substrate** — in 3 years, unique dataset for IPM-GPT fine-tune
6. **Sub-brand flexibility** — IMP Core/Markets/Experts/Foresight/Risk can each have independent GTM

---

## 10. Key metrics to track (monthly)

**Moat metrics:**
- Sealed predictions count (cumulative)
- Brier score by brain × regime
- Calibration certification signups (when launched)
- Graph density (edges, communities, drift events)

**Revenue metrics:**
- ARR by stream
- Customer count by tier
- Churn by tier
- Expansion revenue per customer

**Operational metrics:**
- Brief generation time (p50, p95)
- Agent cost per interaction
- Data pipeline freshness (lag time)
- User activation rate (free → Pro)

**Strategic metrics:**
- Calibration track record length
- Platform NPS
- Inbound client interest
- Competitor positioning shifts

---

## Document status

**Created:** 2026-04-18
**Version:** 1.0
**Next review:** 2026 Q3 (after Phase 5 frontend complete)
**Owner:** Founder (Ruben)
