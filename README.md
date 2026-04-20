# ipm-wiki

Intelligence narrative layer for the IMP platform.
Karpathy LLM Wiki pattern — adapted for geopolitics, macro, and power intelligence.

## What this is

The **narrative and reasoning layer** above the IMP PostgreSQL knowledge graph.
The DB owns structure, typed edges, and quantitative indexes.
This wiki owns the *why* — analyst reasoning, narrative history, contradictions, and compiled context.

## Three uses

1. **AI Analyst Avatars** — compiled actor/theme history as reasoning context
2. **Oracle report generation** — grounded, cross-referenced narrative for weekly reports
3. **Due diligence synthesis** — accumulated intelligence per entity on demand

## How to use

Read `CLAUDE.md` first. It defines all workflows.

- **Ingest:** drop a source file into `raw/`, run the ingest workflow
- **Query:** ask questions — Claude synthesizes from `wiki/` first
- **Lint:** run periodic health checks to catch drift, contradictions, and gaps

## Browse

Open this folder as an Obsidian vault. Use graph view to spot clusters and orphans.

## Rules

- `raw/` is immutable source-of-truth
- `wiki/` is compiled knowledge — maintained by Claude per `CLAUDE.md`
- `wiki/log.md` is append-only
- Every claim links to a source

---

*IMP · Intelligence Map Platform · Confidential — Solo Founder*
