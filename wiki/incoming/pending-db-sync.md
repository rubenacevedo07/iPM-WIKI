# pending-db-sync.md — Research Pass: Palantir Political Network
# Date: 2026-04-22
# Status: OPEN — all flags below require DB action

---

## New Flags This Pass

| Flag ID | Entity | Type | SQL Hint | Status |
|---|---|---|---|---|
| CL-DB-023 | Peter Thiel — Person node | INSERT | `INSERT INTO "Persons" (name, "PowerArchetype") VALUES ('Peter Thiel', 'FINANCIAL')` | OPEN |
| CL-DB-024 | JD Vance — Person node | INSERT | `INSERT INTO "Persons" (name, "PowerArchetype", "Role") VALUES ('JD Vance', 'POLITICAL', 'Vice President')` | OPEN |
| CL-DB-025 | AfD — Institution node | INSERT | `INSERT INTO "Companies" (name, "NodeType") VALUES ('Alternative für Deutschland', 'Company')` | OPEN |
| CL-DB-026 | Thiel→Founded→Palantir | RELATION | Edge type: Founded; Strength: Critical | OPEN |
| CL-DB-027 | Thiel→Finances→Vance | RELATION | Edge type: Finances; Strength: Critical; Evidence: $15M 2022 Senate donation | OPEN |
| CL-DB-028 | Palantir→Supplies→ICE | RELATION | Edge type: Supplies; Strength: High; Product: ImmigrationOS/ICM | OPEN |
| CL-DB-029 | Musk→Influences→AfD | RELATION | Edge type: Influences; Strength: High; Evidence: Jan 2025 X Space, AfD rally appearance | OPEN |

---

## Schema Notes

- CL-DB-026: "Founded" may require new enum value — check RelationEdge type list
- CL-DB-025: AfD classified as "Company" per existing schema; note it is a political party (potential NodeType enum gap)
- CL-DB-027: "Finances" edge should carry temporal metadata: start 2016 (Mithril hire), peak 2022 ($15M)

---

## Index Updates Required

### wiki/index.md — add:
- `wiki/actors/THIEL-Peter.md` — NEW
- `wiki/actors/VANCE-JD.md` — NEW
- `wiki/themes/Tech-Power-Nexus.md` — NEW
- `wiki/dossiers/Palantir-Political-Network.md` — NEW
- `wiki/institutions/PALANTIR.md` — UPDATED (major expansion)
- `wiki/actors/MUSK-Elon.md` — PATCH PENDING (see _patches/)
- `wiki/actors/TRUMP-Donald.md` — PATCH PENDING (see _patches/)

### log.md — append:
```
2026-04-22 | Research pass: Palantir Political Network
Pages created: THIEL-Peter, VANCE-JD, Tech-Power-Nexus, Palantir-Political-Network dossier
Pages expanded: PALANTIR (major rewrite)
Patches staged: MUSK-Elon (AfD section), TRUMP-Donald (Thiel/Palantir section)
Raw notes: 4 files in raw/internal-notes/
DB flags: CL-DB-023 through CL-DB-029 (7 open)
Confidence: MEDIUM across all pages (no Priority 1-4 primary sources consulted directly; all via Priority 2-3 journalism and Priority 7 internal synthesis)
```
