---
title: Enum Types Reference — Valid DB Values
type: indicator
sources: [raw/internal-notes/IPM_SQL_Seed_Reference.docx]
related:
  - wiki/indicators/DB-ID-Reference.md
  - wiki/themes/IMP-Power-Index-System.md
created: 2026-04-09
updated: 2026-04-09
confidence: high
---

# Enum Types Reference — Valid DB Values

*PostgreSQL enums are strict — any value not in the list causes an ERROR. Use exact case.*

## PowerArchetype (PersonPowerIndex.ArchetypeCode)

| Value | Description | Example Persons |
|-------|-------------|-----------------|
| FINANCIAL | Controls capital, assets, funds | Fink, Gates, Bezos, Buffett |
| POLITICAL | Elected/appointed state power | Trump, Macron |
| COERCIVE | Military, enforcement, authoritarian control | Putin, MBS |
| INDUSTRIAL | Manufacturing, supply chain dominance | Chang (TSMC) |
| TECHNOLOGICAL | Tech platform or IP control | Huang, Altman |
| HYBRID | Multiple power dimensions simultaneously | Musk, Xi |

## EdgeType (RelationEdge.EdgeType)

| Value | Use Case |
|-------|----------|
| Supplies | Raw material or component supply |
| Manufactures | Production relationship |
| Distributes | Distribution/logistics |
| DependsOn | Critical dependency |
| Finances | Investment, funding, loans |
| Owns | Direct ownership or equity |
| Regulates | Regulatory authority |
| Sanctions | Sanctions or restrictions |
| Influences | Soft power, lobbying, cultural |
| Governs | State/regulatory governance |
| Competes | Market competition |
| Partners | Strategic partnership or JV |
| Exports | Export/trade flow |
| MilitaryConflict | Active or proxy military conflict |
| Sets | Sets policy or standards (central banks) |

## EdgeStrength (RelationEdge.Strength)

| Value | Meaning |
|-------|---------|
| Critical | Systemic dependency — removal causes collapse |
| High | Major relationship, significant influence |
| Medium | Notable but not dominant |
| Low | Minor or indirect relationship |

## NodeType (RelationEdge.SourceType / TargetType)

| Value | Table |
|-------|-------|
| Company | Companies |
| Person | Persons |
| Country | Countries |
| Commodity | Commodities |
| AssetManager | AssetManagers |
| Bank | Banks |
| ETF | Etfs |
| Sector | Sectors |

## PowerMapType (PowerMap.MapType)

| Value | Use Case |
|-------|----------|
| SupplyChain | Supply chain dependency maps |
| Geopolitical | Country/military/diplomatic maps |
| Ownership | Corporate ownership structures |
| Influence | Soft power and lobbying networks |
| MacroFinancial | Central bank, currency, debt maps |
| Custom | Default — user-defined |

## PowerMapVisibility

| Value | Meaning |
|-------|---------|
| Private | Only author can see |
| Unlisted | Link-only access |
| Public | Visible to all users |

## CanvasLayoutMode

| Value | Meaning |
|-------|---------|
| Freeform | Free positioning (default for Intelligence maps) |
| TierBased | Hierarchical tier layout |

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| 23505 UQ_Company_Ticker | Duplicate ticker | Use NULL for private companies, never 'PRIVATE' |
| 42703 column X does not exist | Using FPI/MPI/SPI abbreviations | Use FinancialScore/MilitaryScore/SoftwareScore etc. |
| 23503 FK violation | Referenced ID doesn't exist | Verify parent record before INSERT |
| 22P02 invalid input for type json | % in LIKE inside PL/pgSQL JSON context | Store pattern in TEXT variable first |
| 42710 type already exists | Migration run twice | Use CREATE TYPE IF NOT EXISTS |
