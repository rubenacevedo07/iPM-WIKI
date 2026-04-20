---
title: IMP Agent Roles
slug: imp-agent-roles
type: comparison
created: 2026-04-09
updated: 2026-04-09
confidence: high
sources:
  - raw/internal-notes/IPM_Session_Record_2026_03_27.md
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: [imp-automation-engine, imp-platform-architecture]
---

# IMP Agent Roles

*Confirmed agent division of labour as of 2026-03-27. Do not reassign roles without architectural review.*

| Agent | Role | Does NOT do |
|-------|------|-------------|
| **Claudio** (Claude AI) | Reasoning, SQL, timelines, strategy, complex logic, IMP_ENVELOPE structuring | Does not collect live data |
| **PX** (Perplexity) | Intelligence collection, research, outcome verification | Does not write deterministic ETL — returns structured narratives, Claudio converts to SQL |
| **Base44** | UI components, SQL generation, research tasks | Does not use IPM design system — outputs need design adaptation |
| **Copilot** | Code completion in existing codebase | Does not reason about architecture |
| **Claude Code** | Frontend pages in actual repo, exact existing design system | Do NOT change design system (#020304, #8B5CF6) |

## PX Workflow (correct pattern)
PX returns intelligence narrative → Claudio structures into IMP_ENVELOPE JSON → SQL generated → `process_imp_envelope()` or direct INSERT.

PX is not a deterministic ETL service. It is a reasoning and research layer. This is the designed architecture.

## AI System User UUIDs (fixed — never change)
- `imp_system`: `00000000-0000-0000-0000-000000000001`
- `Claudio`: `00000000-0000-0000-0000-000000000002`
- `PX`: `00000000-0000-0000-0000-000000000003`
- `Base44`: `00000000-0000-0000-0000-000000000004`
