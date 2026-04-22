---
title: IMP Business Model — Revenue Streams
slug: imp-business-model
type: theme
region: global
tags: [platform, business-model, revenue, imp-internal]
created: 2026-04-09
updated: 2026-04-21
confidence: high
sources: [raw/IMP_Strategy_v2_2.docx]
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: [imp-competitive-moats, imp-platform-architecture]
---

# IMP Business Model — Revenue Streams

## Summary
8 revenue streams. Breakeven at 3 Pro users ($49/month). Monthly burn $1,020. Most streams don't require new infrastructure — they unlock as the platform scales.

## Revenue Streams

| Stream | Unit Economics | Type | Notes |
|---|---|---|---|
| **Platform subscriptions** | $9–$49/mo · Free/Explorer/Analyst/Pro/Enterprise | Predictable MRR | Breakeven: 3 Pro users. Burn: $1,020/mo. |
| **Builder fees (Polymarket CLOB)** | ~0.5% of every USDC trade | Volume-based passive | Scales automatically. No competitor has this stream. |
| **Oracle SaaS** | $199/mo | B2B recurring | Weekly analyst accuracy reports for funds. |
| **IMP Briefing API** | $2,000/mo | B2B infrastructure | Live EdgeRiskScores + oracle leaderboard + composite index signals. |
| **Supply chain due diligence** | $99/report or $999/mo | Per-use + subscription | Auto-generated PDF in 30 seconds. PE firms pay $5K–$50K for consultant version. Margin 99.8%. |
| **Strategy Lab** | Included in $49/mo Pro | Feature gate | 3 runs/month at Analyst. Unlimited at Pro. |
| **Bot Marketplace** | 25% revenue share | Platform revenue | 100 bots × $49 × 100 subs × 25% = $122K/mo passive at target scale. |
| **Observatory institutional** | $10K–$100K/year | Institutional license | UN, World Bank, Gates Foundation. |
| **Data licensing** | TBD — Year 3+ | Long-term moat | 24 months of resolved predictions + calibrated graph = fine-tuning dataset. |

## Key Financial Facts
- Monthly burn: $1,020
- Breakeven: 3 Pro users at $49/month
- Revenue as of April 2026: $0 (Stripe not yet live — B-01 blocker)
- Hosting: Vercel (frontend) + Railway (backend + DB)

## Bot Marketplace Math
100 bots × $49 average × 100 subscribers × 25% IMP share = **$122K/month** passive at scale

## Exit Thesis
- Target: $300M–$1B acquisition (Year 7–9)
- Acquirers: Bloomberg, S&P, Palantir, Mastercard
- Catalyst: Correlation Discovery Engine — 24 months of validated predictions with causal graph paths
- Pre-exit fundable: $5M–$15M seed (50 users), $20M–$50M Series A (viral traction)

## DB Sync Notes
- Stripe not live as of April 2026 — no subscription enforcement yet
- `FeatureGate.MinRole` exists in DB but no tier enforcement anywhere in codebase

## Open Questions
- When does Stripe go live? (B-01 — BillingController in progress)
- Observatory: who are the first 3 institutional targets to approach?
- Data licensing: what's the minimum viable prediction dataset to start licensing conversations?
