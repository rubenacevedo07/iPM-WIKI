# n8n Setup — IMP Wiki Perplexity Collector

## Prerequisites

1. **n8n running in Docker** (via `C:\Users\ruben\Desktop\Docker Auto\docker-compose.yml`)
   - UI: http://localhost:5678
   - Container name: `dockerauto-n8n-1`
2. **Perplexity API key** — https://www.perplexity.ai/settings/api
   - Sonar Pro: ~$3 per 1000 searches; a single research run uses ~1-3 calls

---

## Architecture

Five-node linear workflow that writes the research note directly to the Windows filesystem via the Docker volume mount (no `docker cp`, no `readWriteFile` node):

```
Manual Trigger → Set Inputs → Build Request → Perplexity Sonar API → Format & Save
```

The final node uses `fs.writeFileSync` inside an n8n Code node to write to `/wiki/raw/internal-notes/{slug}-research-{date}.md`, which maps to `C:\Users\ruben\source\repos\iPM-WIKI\raw\internal-notes\` on the host.

### Why not the `readWriteFile` node
n8n 2.17.5's `readWriteFile` node has a writability-check bug that rejects any non-existent target file, including `/tmp/`. We bypass it with a Code node using Node's built-in `fs` module.

### Required docker-compose config
```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    user: root
    ports:
      - "5678:5678"
    environment:
      - NODE_FUNCTION_ALLOW_BUILTIN=fs,path,os
      - NODE_FUNCTION_ALLOW_EXTERNAL=*
    volumes:
      - C:/Users/ruben/source/repos/iPM-WIKI:/wiki
```

`NODE_FUNCTION_ALLOW_BUILTIN` is what unblocks `require('fs')` inside Code nodes — without it the task runner sandbox refuses it.

---

## One-Time Setup

### Step 1 — Import the workflow

1. In n8n: **Workflows → Import from File**
2. Select: `n8n/perplexity-research-collector.json`
3. Open the imported workflow
4. Click the **Perplexity Sonar API** node → set the `Authorization` header to `Bearer YOUR_KEY`
5. Save

---

## How to Use It

**Step 1** — Ask Claude to generate a research prompt:
> "Pre-flight for [entity] — generate a Perplexity prompt"

**Step 2** — Open the **Set Inputs** node in n8n:
- `entity` → the entity slug (e.g., `KARP-Alex`)
- `prompt` → paste Claude's prompt
- `recency_filter` → `day` / `week` / `month` / `year` (default: `year`)

**Step 3** — Click **Test Workflow**

**Step 4** — Workflow runs (~15-30 s). The **Format & Save** node output shows:
```json
{
  "status": "success",
  "entity": "KARP-Alex",
  "filename": "karp-alex-research-2026-04-22.md",
  "host_path": "C:\\Users\\ruben\\source\\repos\\iPM-WIKI\\raw\\internal-notes\\karp-alex-research-2026-04-22.md",
  "bytes": 8234,
  "next_step": "Tell Claude: ingest raw/internal-notes/karp-alex-research-2026-04-22.md"
}
```

**Step 5** — Tell Claude exactly what `next_step` says:
> "ingest raw/internal-notes/karp-alex-research-2026-04-22.md"

Done.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | API key wrong or missing | Set `Authorization: Bearer pplx-...` on Perplexity Sonar API node |
| `429 Too Many Requests` | Rate limit hit | Wait 60s and retry; or upgrade Perplexity plan |
| `require is not defined` / `Cannot find module 'fs'` | `NODE_FUNCTION_ALLOW_BUILTIN` missing | Add env vars to docker-compose, `docker compose up -d --force-recreate n8n` |
| `EACCES: permission denied, open '/wiki/...'` | Container not running as root OR volume mount missing | Confirm `user: root` and volume in docker-compose |
| `process is not defined` | n8n task runner sandboxes `process` | Don't reference `process.*` in Code nodes — use only `fs`, `path` |
| Empty content returned | Prompt too long or model timeout | Split prompt into two runs; reduce max_tokens |
| Citations missing | API returned none | Normal for some queries; `return_citations: true` is set in Build Request |

---

## Workflow Nodes — What Each Does

| Node | Type | Purpose |
|------|------|---------|
| Manual Trigger | Trigger | You start it manually each time |
| Set Inputs | Set | Where you paste entity name + research prompt |
| Build Request | Code | Assembles the Perplexity request body |
| Perplexity Sonar API | HTTP Request | Calls `sonar-pro` with your prompt |
| Format & Save | Code | Wraps output in Priority 7 header format and writes the `.md` file to `/wiki/raw/internal-notes/` |

---

## Perplexity Model Options

| Model | Cost | Best for |
|-------|------|---------|
| `sonar-pro` | ~$3/1K requests | Deep research, citations, longer output — **use this** |
| `sonar` | ~$1/1K requests | Faster/cheaper, shorter output |
| `sonar-reasoning-pro` | ~$8/1K requests | Complex multi-step reasoning; overkill for wiki research |

Change the model in the **Build Request** node (`body.model` field).
