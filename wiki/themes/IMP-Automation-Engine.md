---
title: IMP Automation Engine — Perplexity + Claude + n8n
slug: imp-automation-engine
type: theme
region: global
tags: [platform, automation, imp-internal, n8n, perplexity]
created: 2026-04-09
updated: 2026-04-21
confidence: high
sources: [raw/IMP_Strategy_v2_2.docx]
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: [imp-platform-architecture, imp-oracle-system]
---

# IMP Automation Engine — Perplexity + Claude + n8n

## Summary
The engine that makes IMP self-sustaining. Three systems, one protocol: IMP_ENVELOPE v1. Runs continuously without human intervention after setup. Monday 8AM cron refreshes everything. Event-driven updates fire within minutes of a geopolitical trigger.

## IMP_ENVELOPE v1 Protocol
Unified JSON contract governing all data flowing between Perplexity, Claude, and PostgreSQL. One master PostgreSQL function `process_imp_envelope(JSONB)` handles all insertions and routes by mission type.

| Mission Type | Maps To | Trigger |
|---|---|---|
| `entities` | Countries, Companies, Persons, Commodities | Manual or Perplexity entity research |
| `signals` | NewsEvents + EdgeRiskScore update | Perplexity news pull / GDELT ingest |
| `timelines` | Timeline + Branch A/B structures | Perplexity event → Claude creates timeline |
| `analyst_predictions` | AnalystPredictions table | Monday cron |
| `risk_impact` | EdgeRiskScore, SupplyChainImpact, ResolutionImpactLog | Event-driven on news insert |
| `composite_index` | CompositeIndexSnapshots — all 10 indexes | Weekly batch + event-driven |

## Monday 8AM Weekly Cron — 11 Nodes
1. **PX:** Collect analyst predictions last 14 days → JSON array
2. **CL:** Validate + assign machine_name + link to graph edges → cleaned envelope
3. **PG:** `process_imp_envelope()` → batch insert
4. **PG:** Query pending predictions past resolution date
5. **PX:** Check each outcome → true/false + source URL
6. **CL:** Verify outcome + confidence
7. **PG:** `resolve_prediction()` → Brier scores auto-calculated
8. **PG:** Query AnalystLeaderboard VIEW → ranked machines
9. **CL:** Generate weekly Oracle report narrative
10. **API:** HTTP POST → IMP API → publish to dashboard
11. **EMAIL:** Digest → all subscribers

## Event-Driven Cascade (sub-5-minute latency target)
Trigger: GDELT GoldsteinScale < −7 OR Perplexity-detected critical event

Chain: `NewsEvent INSERT → Claude entity extraction → NewsEventEdge rows → EdgeRiskScore recalculate → CompositeRiskIndex update → SignalR push`

Example cascades:
- Iran strike detected → signals envelope → EdgeRiskScore update → portfolio alerts
- Fed rate decision → NewsEvent → entity extraction → EdgeRiskScore → TradeSignal → SignalR
- GDELT GoldsteinScale < −7 → direct NewsEvent INSERT → full pipeline fires

## Extended Enterprise Stack
- **Firecrawl / Apify:** structured scraping of central bank sites, regulatory filings, parliamentary transcripts → raw HTML → Claude converts to IMP_ENVELOPE
- **Whisper API / AssemblyAI:** podcast and video transcript extraction at scale (Real Vision, Macro Voices, Bloomberg podcasts)
- **pgvector:** semantic search across 18 months of accumulated intelligence. Natural language query over structured history.
- **GDELT:** GoldsteinScale-triggered event detection, direct NewsEvent INSERT

## DB Sync Notes
- `process_imp_envelope()` is the single insertion point — all automation flows through it
- `CompositeIndexSnapshots` table was empty as of April 2026 — snapshot job not yet running (B-04 blocker)

## Open Questions
- When does GDELT ingest go live? (Phase 2 goal)
- n8n workflow: is the Monday cron built yet or still pending?
- Firecrawl/Apify integration status?

- [[../comparisons/IMP-Agent-Roles]]
