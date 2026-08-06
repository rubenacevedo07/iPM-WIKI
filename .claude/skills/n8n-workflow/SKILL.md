---
name: n8n-workflow
description: Create or modify n8n workflows for the IMP Wiki (perplexity collectors, data ingests, webhooks). Use when the user asks to build a new n8n workflow, add a node, debug a workflow, or integrate a new data source. Contains hard-won knowledge about n8n 2.17.5 bugs and sandbox constraints — do NOT infer from generic n8n docs.
---

# n8n Workflow Skill — IMP Wiki

This project runs **self-hosted n8n 2.17.5** inside Docker to collect research notes from external APIs (Perplexity today, others later) and drop them into `raw/` for Claude to ingest. The runtime has several non-obvious constraints that generic n8n docs will mislead you on.

Always read this file before creating or modifying any workflow JSON.

---

## Environment facts (verified 2026-04-22)

| Fact | Value |
|---|---|
| n8n version | 2.17.5 (self-hosted Docker) |
| Container name | `dockerauto-n8n-1` |
| Compose file | `C:\Users\ruben\Desktop\Docker Auto\docker-compose.yml` |
| UI URL | http://localhost:5678 |
| Process user inside container | `root` |
| Volume mount | `C:/Users/ruben/source/repos/iPM-WIKI:/wiki` |
| Wiki writable path inside container | `/wiki/raw/...` → Windows `C:\Users\ruben\source\repos\iPM-WIKI\raw\...` |

Required env vars on the n8n service (already set — do not remove):
```yaml
environment:
  - NODE_FUNCTION_ALLOW_BUILTIN=fs,path,os
  - NODE_FUNCTION_ALLOW_EXTERNAL=*
```

If either env var is missing, Code nodes lose `require()` and the whole pattern below collapses.

---

## Hard rules (do NOT violate)

### ❌ Never use the `readWriteFile` (Read/Write File) node
Versions 1 AND 1.1 both have a writability-check bug at `write.operation.ts:130`: `fs.access(path, W_OK)` fails for any non-existent target file, including `/tmp/`. `overwrite: true` does NOT bypass the check. `user: root` does NOT help. Not fixable from config. **Use a Code node with `fs.writeFileSync` instead.**

### ❌ Never assume `executeCommand` node exists
`n8n-nodes-base.executeCommand` is not available in 2.17.5. Importing a workflow that references it fails with "Unrecognized node type."

### ❌ Never reference `process.*` in Code nodes
The task runner sandbox does NOT expose `process`. `process.cwd()`, `process.getuid()`, `process.env.*`, etc. all throw `process is not defined`. Use n8n expressions (`$env.VAR_NAME`) or hard-code.

### ❌ Never use `$helpers.prepareBinaryData` or similar helpers
The task runner sandbox does NOT inject `$helpers`. Build binaries manually with `Buffer.from(content).toString('base64')` if you must — but prefer writing files directly via `fs`.

### ❌ Never burn API credits to debug file I/O
Always create an isolated test workflow (Manual Trigger → Code node doing the file operation only) **before** wiring it into a workflow that calls a paid API.

### ✅ DO use Code node + `fs.writeFileSync` for all file output
Write directly under `/wiki/...` and the file appears on the Windows host via the bind mount. No `docker cp`, no intermediate `/tmp/` dance.

### ✅ DO use `$('NodeName').item.json` to read upstream nodes
NOT `$node["NodeName"].json` (deprecated) or `$json` (only refers to current input item).

---

## What's available inside a Code node (n8n 2.17.5 task runner)

| Available | Not available |
|---|---|
| `require('fs')` (with env var) | `process` |
| `require('path')` (with env var) | `$helpers` |
| `require('os')` (with env var) | `$binary` writes (use fs instead) |
| `Buffer` | `executeCommand` node |
| `$input.all()`, `$input.item`, `$input.first()` | Top-level `await` |
| `$('OtherNode').item.json` | |
| `$('OtherNode').all()` | |
| `$env.VAR_NAME` (reads container env) | |
| `DateTime` (Luxon), `$jmespath`, `$now`, `$today` | |

---

## Canonical workflow template

Use this as the starting point for any new collector. It's the pattern that currently runs in `n8n/perplexity-research-collector.json`.

```json
{
  "name": "Descriptive Workflow Name",
  "nodes": [
    {
      "parameters": {},
      "id": "node-0001",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [240, 340]
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            { "id": "f1", "name": "entity",         "value": "DEFAULT_VALUE", "type": "string" },
            { "id": "f2", "name": "prompt",         "value": "...",           "type": "string" },
            { "id": "f3", "name": "recency_filter", "value": "year",          "type": "string" }
          ]
        },
        "options": {}
      },
      "id": "node-0002",
      "name": "Set Inputs",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [460, 340]
    },
    {
      "parameters": {
        "jsCode": "// Build the outbound API request body here\nconst inputs = $('Set Inputs').item.json;\nconst body = { /* API-specific payload */ };\nreturn [{ json: { ...inputs, requestBody: JSON.stringify(body) }}];"
      },
      "id": "node-0003",
      "name": "Build Request",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [680, 340]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.example.com/endpoint",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            { "name": "Authorization", "value": "Bearer REPLACE_WITH_YOUR_KEY" },
            { "name": "Content-Type",  "value": "application/json" }
          ]
        },
        "sendBody": true,
        "contentType": "raw",
        "rawContentType": "application/json",
        "body": "={{ $json.requestBody }}",
        "options": { "timeout": 90000 }
      },
      "id": "node-0004",
      "name": "API Call",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [920, 340]
    },
    {
      "parameters": {
        "jsCode": "const fs = require('fs');\nconst path = require('path');\n\nconst inputs = $('Set Inputs').item.json;\nconst apiResponse = $('API Call').item.json;\n\n// 1. Extract and shape content\nconst content = apiResponse.choices?.[0]?.message?.content || 'ERROR: No content';\n\n// 2. Compute filename\nconst today = new Date().toISOString().split('T')[0];\nconst entitySlug = inputs.entity.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');\nconst filename = `${entitySlug}-research-${today}.md`;\n\n// 3. Assemble the final markdown\nconst rawNote = [\n  `# ${inputs.entity} — Research Note`,\n  `## Compiled: ${today}`,\n  ``,\n  `---`,\n  ``,\n  content\n].join('\\n');\n\n// 4. Write to /wiki/raw/<folder>/\nconst targetDir = '/wiki/raw/internal-notes';\nconst targetPath = path.join(targetDir, filename);\nfs.mkdirSync(targetDir, { recursive: true });\nfs.writeFileSync(targetPath, rawNote, 'utf-8');\nconst bytes = fs.statSync(targetPath).size;\n\nreturn [{ json: {\n  status: 'success',\n  filename,\n  host_path: `C:\\\\Users\\\\ruben\\\\source\\\\repos\\\\iPM-WIKI\\\\raw\\\\internal-notes\\\\${filename}`,\n  bytes,\n  next_step: `Tell Claude: ingest raw/internal-notes/${filename}`\n}}];"
      },
      "id": "node-0005",
      "name": "Format & Save",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [1160, 340]
    }
  ],
  "pinData": {},
  "connections": {
    "Manual Trigger":  { "main": [[{ "node": "Set Inputs",    "type": "main", "index": 0 }]] },
    "Set Inputs":      { "main": [[{ "node": "Build Request", "type": "main", "index": 0 }]] },
    "Build Request":   { "main": [[{ "node": "API Call",      "type": "main", "index": 0 }]] },
    "API Call":        { "main": [[{ "node": "Format & Save", "type": "main", "index": 0 }]] }
  },
  "active": false,
  "settings": { "executionOrder": "v1" },
  "versionId": "",
  "meta": {},
  "tags": []
}
```

### Connection rule
`connections` is keyed by **node NAME** (not id). Every node must appear as a key if it has outputs. Double-nested array `[[ { node, type, index } ]]` — the outer array is output index, inner is parallel connections.

---

## Where research notes go

| Source type | Target folder |
|---|---|
| Perplexity / LLM research | `raw/internal-notes/` |
| Central bank speeches, minutes | `raw/central-banks/` |
| IMF / BIS / World Bank | `raw/institutions/` |
| OFAC / sanctions | `raw/sanctions/` |
| Think tanks (CSIS, CFR, Bruegel) | `raw/think-tanks/` |
| Transcripts (speeches, interviews) | `raw/transcripts/` |
| Market research / sell-side | `raw/market-research/` |
| Commodity reports (IEA, OPEC) | `raw/commodities/` |

Full tier list in `CLAUDE.md` section 5.1. The workflow should write to the folder matching the source's priority tier.

---

## Standard header for ingested files

Every file written by a workflow should start with Priority/Status/Compiled headers so Claude's ingest picks up the right tier. Template:

```markdown
# {ENTITY} — Research Note
## Internal Research Note — Priority 7 Source
## Status: hypothesis pending corroboration by Priority 1-4 sources
## Compiled: YYYY-MM-DD
## Model: {provider} {model} | Tokens: {count}

---

{content}

---

## Citations
{numbered list}

---

## Original Prompt
{verbatim prompt}
```

Adjust the Priority line per source tier (1 = official, 7 = internal). See `CLAUDE.md` section 5.1.

---

## Diagnostic commands

Run these (from PowerShell, not Git Bash — Git Bash rewrites `/tmp/` to Windows paths) before assuming a workflow is broken:

```powershell
# Is n8n up?
Invoke-WebRequest "http://localhost:5678/healthz" -UseBasicParsing

# Are the env vars loaded?
docker exec dockerauto-n8n-1 env | Select-String "NODE_FUNCTION"

# Can root write to /wiki inside the container?
docker exec dockerauto-n8n-1 sh -c 'touch /wiki/raw/internal-notes/.probe && rm /wiki/raw/internal-notes/.probe && echo OK'

# Does the file appear on Windows?
Test-Path "C:\Users\ruben\source\repos\iPM-WIKI\raw\internal-notes\{filename}"

# Restart n8n after docker-compose changes
Push-Location "C:\Users\ruben\Desktop\Docker Auto"; docker compose up -d --force-recreate n8n; Pop-Location
```

---

## Debugging playbook

**Symptom: `The file "..." is not writable` in a readWriteFile node**
→ Replace the node with a Code node using `fs.writeFileSync`. This bug is not fixable.

**Symptom: `require is not defined` in Code node**
→ `NODE_FUNCTION_ALLOW_BUILTIN` is missing. Check `docker exec dockerauto-n8n-1 env | grep NODE_FUNCTION`. Add it to docker-compose and `--force-recreate`.

**Symptom: `process is not defined`**
→ Remove all `process.*` references. Sandbox doesn't expose it.

**Symptom: `Unrecognized node type: n8n-nodes-base.executeCommand`**
→ Don't use this node in 2.17.5. Shell commands must go through an HTTP webhook to the host or be replaced by a `fs`-based Code node.

**Symptom: Workflow imports but fails to run with "Authorization missing"**
→ The HTTP Request node's Authorization header value is a literal placeholder. Replace `REPLACE_WITH_YOUR_KEY` with `Bearer pplx-...` (or equivalent) in the n8n UI after import.

**Symptom: File written inside container but not visible on Windows**
→ Check volume mount: `docker inspect dockerauto-n8n-1 | Select-String -Context 5 "Mounts"`. Must show `/wiki` bind-mounted from `C:/Users/ruben/source/repos/iPM-WIKI`.

---

## Isolation test pattern

Before wiring a new API into a workflow, ALWAYS test the output path in isolation. Template for a test workflow (`n8n/test-{feature}.json`):

```
Manual Trigger → Code node
```

Code node:
```js
const fs = require('fs');
const path = require('path');

const targets = ['/tmp/probe.md', '/wiki/raw/internal-notes/probe.md'];
const results = [];

for (const p of targets) {
  const r = { path: p };
  try {
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, `probe ${new Date().toISOString()}`, 'utf-8');
    r.ok = true;
    r.bytes = fs.statSync(p).size;
  } catch (e) {
    r.ok = false;
    r.error = `${e.code || ''} ${e.message}`.trim();
  }
  results.push(r);
}

return [{ json: { results } }];
```

Run it, pipe results back to Claude, then swap into the real workflow. Delete the test JSON after.

---

## Checklist when creating a new workflow

When the user asks for a new workflow, go through this list:

1. [ ] Identify source type → pick `raw/<folder>/` target
2. [ ] Identify API endpoint, auth method, request shape
3. [ ] Write the workflow JSON from the canonical template above
4. [ ] Inline the prompt / request params in the `Set Inputs` node (or accept them via webhook body if triggered externally)
5. [ ] Verify `Format & Save` writes to `/wiki/raw/<correct-folder>/`
6. [ ] Verify Priority/Status header matches source tier (see `CLAUDE.md` 5.1)
7. [ ] Connections keyed by node **name**, not id
8. [ ] Placeholder key in HTTP node as `Bearer REPLACE_WITH_YOUR_KEY` (never commit real keys)
9. [ ] Save the JSON under `n8n/<descriptive-name>.json`
10. [ ] Tell the user exactly what to do: import in UI, set API key, Test Workflow, report back the Format & Save output
11. [ ] After first successful run, tell the user `ingest raw/<folder>/<filename>` so Claude picks it up

---

## Anti-patterns seen in this repo's history

These were tried and burned time. Don't repeat them:

- Using `readWriteFile` node with `typeVersion: 1.1` and `overwrite: true` — still fails.
- Mounting host paths as `:ro` read-only — the volume IS writable; the bug is elsewhere.
- Adding `chown node:node /wiki` in docker-compose — container runs as root, ownership is not the issue.
- Using `$helpers.prepareBinaryData` in Code nodes — task runner doesn't inject it.
- Using `console.log()` + `docker logs` to extract output — works but fragile; `fs.writeFileSync` is cleaner.
- Writing to `/tmp/` then `docker cp` to host — unnecessary once `NODE_FUNCTION_ALLOW_BUILTIN` is set and the volume mount works.
- Exposing n8n via ngrok without auth — security hole; n8n runs localhost-only by design here.
