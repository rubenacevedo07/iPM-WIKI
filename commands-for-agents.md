# IMP Wiki — Commands for Agents
*How to use AI models with this wiki system · v1.0 · 2026-04-22*
*Companion to CLAUDE.md. Read both before starting any session.*

---

## 1. What This File Is

This document defines the operating protocol for using AI agents (Claude, Perplexity, ChatGPT, Gemini, Grok, DeepSeek) with the IMP LLM Wiki. It answers three questions:

1. **What to do before generating any research prompt** — which files to read, in what order
2. **Which model to use for what** — each model's role in the pipeline and how to adapt prompts for each
3. **How to improve the overall function** — gaps and upgrade paths

The wiki has two pipeline scripts that matter here:
- `ipm_wiki_generator.py` — DB → `wiki/companies/` auto-pages (keyed on `entity_id`)
- `ipm_wiki_to_graph.py` — `wiki/companies/` → DB drift sync (reads `entity_id`)

Hand-crafted pages (`wiki/actors/`, `wiki/institutions/`, `wiki/themes/`, etc.) use `db_id` and are **invisible to both scripts**. They reach the DB only via manual SQL in `wiki/pending-db-sync.md`. Keep this separation in mind when deciding where to invest research effort.

---

## 2. The Standard Workflow

Every research session follows this sequence. Do not skip steps.

```
STEP 1 — PRE-FLIGHT (always Claude)
  Ask Claude to read: wiki/index.md + target page(s) + wiki/log.md (last entries)
  Claude produces: a targeted research prompt for the external model

STEP 2 — RESEARCH (Perplexity / ChatGPT / Gemini / Grok)
  Feed the Claude-generated prompt to the appropriate model
  Collect structured output

STEP 3 — RAW FILE DEPOSIT
  Save research output as raw/internal-notes/topic-YYYY-MM.md (Priority 7)
  Do not edit existing raw/ files

STEP 4 — INGEST (Claude)
  Tell Claude: "ingest raw/internal-notes/topic-YYYY-MM.md"
  Claude reads CLAUDE.md + index.md + raw file → creates/updates wiki pages

STEP 5 — HOUSEKEEPING (Claude, automatic on ingest)
  wiki/log.md appended
  wiki/index.md updated
  wiki/pending-db-sync.md flags raised if DB sync needed
```

### The Pre-Flight Command

Every session starts with this instruction to Claude:

> "Before we research [topic/entity], read the relevant wiki files and generate a research prompt for [target model]."

Claude will read:

| File | Purpose |
|------|---------|
| `wiki/index.md` | What pages exist — prevents duplicating covered ground |
| `wiki/actors/NAME.md` or relevant page | What's already known — Open Questions become research targets |
| `wiki/log.md` (last 3 entries) | What was recently ingested — avoids repeating same sources |
| `CLAUDE.md` sections 3–4 | Schema and section structure — prompt maps to these |
| Closely related pages | Network context for reciprocal links |

The output is a prompt that specifies:
- Exactly which sections need filling
- What's already known (so the model doesn't repeat it)
- What source tier to prioritize (Priority 1 speeches > Priority 4 sell-side > Priority 7 analyst notes)
- What format to return results in (maps to CLAUDE.md page sections)

---

## 3. Model Roster — Roles and Adaptations

### Claude (Anthropic) — Wiki Maintainer
**Role:** The only model that writes to the wiki. All ingest, schema compliance, cross-referencing, lint, SQL flag generation, and reciprocal link maintenance goes through Claude.

**Best for:**
- Ingest operations (raw → wiki pages)
- Schema-compliant page creation and updates
- Lint passes (`wiki/lint-reports/`)
- Generating pending-db-sync SQL
- Cross-referencing and contradiction detection
- Producing research prompts for other models

**How to prompt Claude for this wiki:**
- Always say "read CLAUDE.md first" if starting a new conversation (or put CLAUDE.md in context)
- For ingest: `"Ingest raw/internal-notes/FILENAME.md per CLAUDE.md section 5.1"`
- For lint: `"Run a health check per CLAUDE.md section 5.4"`
- For pre-flight: `"Read wiki/index.md + wiki/actors/NAME.md + wiki/log.md and generate a Perplexity prompt to fill the Open Questions"`

**What Claude cannot do:** real-time web search, current prices, live news. Use Perplexity for that.

---

### Perplexity — Primary Research Engine
**Role:** Real-time web research with citations. Best source for Priority 1–5 material (speeches, sanctions, IMF reports, sell-side, think tanks).

**Best for:**
- Current actor positions, recent speeches, press conferences
- Contract values, regulatory filings, sanctions package details
- Think tank reports (CSIS, CFR, RAND, Bruegel)
- Market data, commodity prices, company financials
- News events for the `## Key Recent Actions` and `## Recent Moves` sections

**Adaptation needed — give Perplexity this structure in the prompt:**

```
Research task: [entity/topic]

Return results organized by these sections:
1. Summary (2-4 sentences: who/what and why it matters)
2. Key Recent Actions (bullet list with dates: YYYY-MM-DD: event)
3. Narrative Shift (what changed in language/posture vs 6 months ago)
4. Market Impact (which assets, which direction, which mechanism)
5. Open Questions (what remains unclear or unconfirmed)

Priority: cite sources with URL and date. Flag if information is unconfirmed.
Prioritize: official statements > laws/filings > IMF/BIS/World Bank > market research > think tanks > media.
Avoid: speculative commentary without sourcing.
```

**Prompt prefix to add every time:**
> "This is for an intelligence wiki. Provide structured, dated, source-cited output. Flag uncertainty levels (confirmed / likely / unconfirmed)."

---

### ChatGPT / GPT-4o — Synthesis and Dossier Writing
**Role:** Long-form synthesis, scenario generation, dossier writing, comparison tables. Better than Perplexity for structuring existing information but cannot search the live web reliably.

**Best for:**
- Drafting dossier pages (`wiki/dossiers/`) from multiple source notes
- Writing scenario pages (`wiki/scenarios/`)
- Narrative pages (`wiki/narratives/`) — synthesizing how a story has evolved
- Comparison tables (e.g., Trump vs Powell divergence)
- Rewriting thin pages into full CLAUDE.md-compliant pages

**Adaptation needed:** GPT-4o will drift from schema without explicit constraints. Always paste the relevant CLAUDE.md section into the prompt.

```
You are writing a wiki page for an intelligence platform. Use EXACTLY this structure:

[paste the relevant CLAUDE.md section 4.X template]

Constraints:
- No bullet points in Summary — use prose
- Dates must be YYYY-MM-DD format
- Confidence must be: low / medium / high / conflicted
- Do not invent facts — mark gaps as "source needed"
- Return only the markdown page, no explanation
```

**What GPT-4o cannot do:** reliably follow schema across a long page without drift. Always have Claude review and clean up GPT-4o output before ingesting.

---

### Gemini 1.5 Pro / 2.0 Flash — Multi-Document Analysis
**Role:** Large context window (1M+ tokens) makes it uniquely useful for cross-wiki analysis — feeding it many pages simultaneously to find contradictions, orphans, or narrative drift.

**Best for:**
- Lint-style passes: feed it 20+ wiki pages, ask it to find contradictions
- Coverage gap analysis: feed it the full index + all actor pages, ask what's missing
- Relationship mapping: find all pages that reference an entity and check consistency
- Processing long primary source documents (full IMF WEO, BIS Annual Report) that exceed other models' context

**Adaptation needed:** Gemini handles long context well but output structure needs explicit instruction.

```
You are reviewing an intelligence wiki. I am providing [N] wiki pages.

Task: [specific lint/analysis task]

Return a structured report with:
- Contradictions found (Page A says X, Page B says Y)
- Orphaned references (mentioned but no page exists)
- Stale sections (section exists but has placeholder text)
- Missing links (entity referenced but not in related_* field)

Format: markdown table per category. One row per finding.
```

**Do not use Gemini to write wiki pages** — it does not know the CLAUDE.md schema and will invent plausible-looking but non-compliant frontmatter.

---

### Grok (xAI) — Narrative and Social Signal Detection
**Role:** X/Twitter intelligence. Tracks what public figures say on X, detects narrative shifts in real time, surfaces public positioning that official sources lag.

**Best for:**
- `## Narrative Shift` section content — detecting changes in language, tone, new emphasis
- Tracking what an actor says publicly on X (statements, thread summaries)
- Early warning on narrative pivots before they appear in official documents
- AfD-style political intervention tracking (Musk on X, Thiel network statements)

**Adaptation needed:** Grok is less structured than Perplexity. Prompt it toward specific output:

```
Search X for statements by [actor] from [date range].

Identify:
1. Key claims or positions stated (with direct quotes where available)
2. Changes from prior stated positions (narrative shift)
3. Topics avoided or conspicuously absent
4. Reactions or responses from key counterparts

Return as a chronological list: YYYY-MM-DD | @handle | quote/summary | significance
```

**Caveat:** Grok has a potential bias toward amplifying content favorable to Musk-aligned figures. Cross-check Grok narrative findings with Perplexity or primary sources before ingesting.

---

### DeepSeek — China and Technical Deep Dives
**Role:** Strong on Chinese-language sources, PBOC policy, PLA doctrine, CCP official language. Also useful for technical/quantitative analysis (economic models, financial calculations).

**Best for:**
- China-related pages: XI-Jinping, PBOC, CHINA country page, rare earths, semiconductor supply chain
- Reading Chinese official documents (Five-Year Plans, PBOC statements, NPC resolutions)
- Technical financial modeling (yield curve analysis, commodity pricing models)
- Cross-checking Western analyst interpretations of Chinese policy against Chinese-language originals

**Adaptation needed:** DeepSeek needs explicit schema instructions like ChatGPT. Also:

```
Note: This output will be ingested into an intelligence wiki. Separate:
(a) confirmed facts with source
(b) analyst interpretation — label as "assessment"
(c) speculation — label as "hypothesis"

For China-specific content, distinguish:
- Official CCP/PRC stated position
- Observed behavior (may differ from stated position)
- Western analyst interpretation
```

**Do not use DeepSeek for US domestic politics** — it has documented blind spots on that domain.

---

## 4. Quick Reference — Model Selection

| Task | Primary model | Backup |
|------|--------------|--------|
| Pre-flight read + prompt generation | Claude | — |
| Real-time actor research (speeches, actions) | Perplexity | Grok |
| Dossier / synthesis writing | Claude (after Perplexity feed) | ChatGPT |
| Scenario generation | Claude | ChatGPT |
| Narrative shift / X signals | Grok | Perplexity |
| China / PBOC / PLA content | DeepSeek | Perplexity |
| Multi-page lint / contradiction check | Gemini | Claude |
| Long primary document processing | Gemini | Claude |
| Schema-compliant page writing | Claude | — |
| DB sync SQL generation | Claude | — |

---

## 5. Ways to Improve This Function

### Short term (manual, no new infrastructure)

**5.1 Standardize the raw note format**
Current raw notes (Priority 7) have inconsistent structure — some have headers, some don't. Create a template:
```markdown
# [topic]-[YYYY-MM].md
## Priority: 7 — Internal Research Note
## Compiled: YYYY-MM-DD
## Sources used: [list]
## Confidence: [low/medium/high per claim]
---
## [Section per CLAUDE.md page type]
```
This makes Claude's ingest faster and reduces schema errors on the resulting wiki pages.

**5.2 One-shot pre-flight macro**
Create a saved prompt (in your AI client of choice) that automatically instructs the model to read the standard pre-flight file set. This eliminates the "I forgot to say read index.md first" problem.

**5.3 Per-model prompt templates**
Save the Perplexity, ChatGPT, and Grok prompt templates from Section 3 above as text snippets (in Raycast, Alfred, or your clipboard manager). Copy-paste rather than re-derive each session.

---

### Medium term (light automation)

**5.4 n8n → Perplexity → raw/internal-notes/ pipeline**
Connect n8n (already in the IMP stack) to Perplexity's API. On a schedule or trigger:
1. n8n sends a pre-built research prompt for a target entity
2. Perplexity returns structured output
3. n8n saves the result to `raw/internal-notes/auto-ENTITY-YYYY-MM-DD.md`
4. Claude ingest is triggered manually or via webhook

This turns the manual research loop into a semi-automated collection pipeline.

**5.5 Lint on schedule**
Add a Claude Code scheduled task (or n8n cron) that runs `wiki/lint-reports/` generation weekly. The lint output highlights which pages are stale, which open questions are oldest, and which entities are mentioned but have no page — driving the research priority queue automatically.

**5.6 Perplexity Space for IMP Wiki**
Create a Perplexity Space seeded with `CLAUDE.md` + `wiki/index.md` + `wiki/overview.md`. Queries inside the Space automatically have wiki context, so research prompts don't need to re-explain the schema every time. Refresh the Space after major wiki updates.

---

### Long term (structural upgrades)

**5.7 Extend ipm_wiki_to_graph.py to read hand-crafted pages**
Currently the sync script only reads `wiki/companies/` (keyed on `entity_id`). A future version should also read `wiki/actors/`, `wiki/institutions/`, etc. (keyed on `db_id`). This would close the gap where hand-crafted intelligence pages can only reach the DB via manual SQL.

Required changes:
- Add `db_id` as an accepted alternative to `entity_id` in `parse_frontmatter()`
- Add Person and Country resolution (currently only Company→Company edges are supported)
- Add `related_actors`, `related_institutions` frontmatter fields as edge sources

**5.8 ipm_wiki_to_graph.py: fix hardcoded TargetType='Company'**
The INSERT in `sync_wiki_page()` hardcodes `TargetType='Company'`. Person and Country targets cannot be synced. Fix requires resolving target type from entity name lookup.

**5.9 Embed wiki pages for semantic search**
Run all `wiki/` markdown files through an embedding model (OpenAI `text-embedding-3-large` or Voyage AI) and store vectors in a local FAISS index or pgvector. This enables:
- "Which pages are most related to [new entity]?" before creating a page
- Duplicate detection before ingest
- Semantic search across the wiki for Oracle context generation

**5.10 Oracle context auto-generation**
Build a prompt template that, for any Oracle machine, automatically pulls:
- All `related_actors` pages for that machine's domain
- Relevant `wiki/themes/` and `wiki/narratives/` pages
- The `wiki/oracle/{machine-slug}.md` page
Then feeds this to Claude to produce the context block. Currently done manually; could be a one-command operation.

---

## 6. Common Mistakes to Avoid

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| Skip pre-flight reads | Research prompt is generic; ingest creates duplicate or incomplete pages | Always run pre-flight first |
| Write directly to wiki without ingest | Skips log.md, index.md, pending-db-sync.md updates | Always route through Claude ingest |
| Use Gemini to write wiki pages | Non-compliant frontmatter, invented schema fields | Gemini = analysis only; Claude = writing |
| Trust Grok on Musk/xAI narrative | Potential amplification bias | Cross-check with Perplexity |
| Use `entity_id` in hand-crafted pages | Confuses with auto-generated companies/ pages | Hand-crafted = `db_id`; auto-generated = `entity_id` |
| SQL with wrong column names | DB INSERT fails silently in pending-db-sync | Use `SourceId`/`TargetId`/`SourceType`/`TargetType` (confirmed via ipm_wiki_to_graph.py) |
| Create pages in `wiki/incoming/` | Orphaned staging files, schema bugs, no index entry | Write directly to target directory via Claude |

---

*IMP LLM Wiki · commands-for-agents.md v1.0 · 2026-04-22 · Confidential — Solo Founder*
