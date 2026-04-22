---
title: DB ID Reference — Verified Entity IDs
slug: db-id-reference
type: indicator
domain: reference
scope: all
region: global
tags: [database, reference, imp-internal, entity-ids]
created: 2026-04-09
updated: 2026-04-21
confidence: high
sources: [raw/internal-notes/IPM_SQL_Seed_Reference.docx]
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: [imp-power-index-system]
---

# DB ID Reference — Verified Entity IDs

*Use these IDs when writing SQL, building wiki frontmatter db_id fields, or referencing entities in Oracle context.*

## Countries

| Country | DB ID | Country | DB ID |
|---------|-------|---------|-------|
| United States | 1 | Taiwan | 151 |
| Brazil | 4 | North Korea | 152 |
| United Kingdom | 28 | Australia | 170 |
| Germany | 29 | Pakistan | 141 |
| France | 30 | India | 140 |
| Ukraine | 65 | Japan | 149 |
| Russia | 64 | Saudi Arabia | 71 |
| Morocco | 85 | Iran | 72 |
| China | 148 | Turkey | 73 |
| Algeria | 86 | Israel | 74 |
| Canada | ~ (unverified) | | |

## Key Persons

| Person | DB ID | Archetype | PowerIndex Seeded |
|--------|-------|-----------|-------------------|
| Jensen Huang | 1 | TECHNOLOGICAL | ✅ 68 (rank 7) |
| Mark Zuckerberg | 6 | TECHNOLOGICAL | — |
| Elon Musk | 7 | HYBRID | ✅ 74 (rank 4) |
| Warren Buffett | 9 | FINANCIAL | — |
| Jamie Dimon | 12 | FINANCIAL | — |
| Sam Altman | 61 | TECHNOLOGICAL | ✅ 55 (rank 13) |
| Jeff Bezos | 66 | FINANCIAL | — |
| Bill Gates | 67 | FINANCIAL | ✅ 71 (rank 8) |
| Larry Fink | 75 | FINANCIAL | ✅ 72 (rank 5) |
| Morris Chang | 113 | INDUSTRIAL | — |
| Xi Jinping | 171 | HYBRID | ✅ 79 (rank 2) |
| Vladimir Putin | 172 | COERCIVE | ✅ 81 (rank 3) |
| Donald Trump | 173 | POLITICAL | ✅ 76 (rank 1) |
| Emmanuel Macron | 174 | POLITICAL | — |
| Mohammed bin Salman | 176 | COERCIVE | ✅ 78 (rank 6) |
| Christine Lagarde | 191 | POLITICAL | ✅ 58 (rank 11) |
| Jerome Powell | 192 | POLITICAL | ✅ 62 (rank 10) |
| Scott Bessent | 545 | FINANCIAL | ✅ 58 (rank 12) |

*Modi, Yellen — DB IDs TBD. Narendra Modi composite 64 (rank 9), Yellen composite 48 (rank 14) — seeded but IDs unconfirmed.*

## Key Companies

| Company | DB ID | Company | DB ID |
|---------|-------|---------|-------|
| NVIDIA | 1 | JPMorgan | 12 |
| Apple | 2 | ExxonMobil | 14 |
| Alphabet | 3 | ASML | 21 |
| Microsoft | 4 | TSMC | 41 |
| Amazon | 5 | Saudi Aramco | 42 |
| Meta | 6 | Samsung | 43 |
| Tesla | 7 | Goldman Sachs | 63 |
| Lockheed Martin | 68 | BlackRock | 90 |
| Intel | 85 | BASF | 115 |
| Bayer | 116 | OpenAI | 198 |

## AI System Users (UUIDs)
| Name | UUID |
|------|------|
| imp_system | 00000000-0000-0000-0000-000000000001 |
| Claudio | 00000000-0000-0000-0000-000000000002 |
| PX (Perplexity) | 00000000-0000-0000-0000-000000000003 |

## Safe ID Derivation Pattern
```sql
-- Always use this before any INSERT session
SELECT COALESCE(MAX("Id"),0)+1 AS next_id FROM public."Persons";
SELECT COALESCE(MAX("Id"),0)+1 AS next_id FROM public."Companies";
-- PowerMap has NO sequence — must use MAX(Id)+1 explicitly
SELECT COALESCE(MAX("Id"),0)+1 AS next_id FROM public."PowerMap";
```
