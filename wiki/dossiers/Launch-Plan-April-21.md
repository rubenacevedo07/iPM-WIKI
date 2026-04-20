---
title: IMP Launch Plan — April 21, 2026
slug: launch-plan-april-21-dossier
type: dossier
created: 2026-04-09
updated: 2026-04-09
confidence: high
sources:
  - raw/internal-notes/IPM_Launch_Plan_April21.html
related_actors: []
related_countries: []
related_institutions: []
related_commodities: []
related_themes: [imp-business-model, imp-competitive-moats]
---

# IMP Launch Plan — April 21, 2026

**Deadline: April 21. Today: April 9. 12 days remaining.**

Strategy: not a product launch — a recruitment round. 6 specific people, 6 personalized demos, no generic pitch. Stripe activates May 1 after structured feedback collected.

---

## The 6 Personas

### Ian — EUR/USD Prop Trader
- **Demo:** Sherman EUR/USD Morning Brief with Trump↔Powell divergence, ECB/Fed ideology gap, DSI signal
- **Value prop:** IPM helps Ian pass his prop firm challenge with structural macro context at entry time
- **Role:** Beta tester — prop challenge passer
- **Key seed needed:** Trump↔Powell VsOverlay data (Day 3, Apr 8)

### Oliver — Celonis (Enterprise Supply Chain)
- **Demo:** Semiconductor PowerMap — TSMC/NVIDIA/ASML with substitution latencies
- **Value prop:** IPM's external power intelligence complements Celonis's internal process intelligence
- **Role:** Enterprise door opener — warm introductions to Celonis clients
- **Key seed needed:** Semiconductor PowerMap data (Day 3, Apr 8)
- **Connection:** [[../dossiers/Product-Ideas-2026-03-27.md]] — Idea 5 (Celonis partnership)

### Jessica — Education / Learning
- **Demo:** IPM Academy concept, personalized learning journey
- **Value prop:** IPM as an intelligence learning platform
- **Role:** Academy designer — first learning journey architect

### Ling — Asia Markets / Product Manager
- **Demo:** Asia entity overlays — China, Japan, Hong Kong, Singapore profiles
- **Value prop:** IPM's Asia coverage as a PM tool for US campaign design
- **Role:** US campaign designer
- **Key seed needed:** Asia entity data check (Day 12, Apr 17)

### Nano — Expert / Trader
- **Demo:** Expert Marketplace — Brier score credential, subscriber monetization
- **Value prop:** "On eToro your analysis is free. On IPM your subscribers pay."
- **Role:** First Expert Marketplace expert
- **Joint session with Christian**

### Christian — Expert / Trader
- Same as Nano — joint session
- **Role:** First Expert Marketplace expert

---

## Critical Path Items (active deadlines)

| Date | Deliverable | Owner | Status |
|------|-------------|-------|--------|
| Apr 8 | Trump↔Powell VsOverlay + Semiconductor PowerMap seeded | Claudio SQL | ⏳ |
| Apr 8 | Sherman EUR/USD Morning Brief live | Claude Code | ⏳ |
| Apr 17 | Asia entity data check (Japan, China, HK, Singapore) | Claudio SQL | ⏳ |
| Apr 18 | Personal invitations sent to all 6 | O07 | ⏳ |
| Apr 19 | Final QA + rehearsal | O07 | ⏳ |
| Apr 21 | PRESENTATION DAY | O07 | ⏳ |
| May 1 | Stripe goes live | Claudio | ⏳ (blocked B-01) |

---

## DB Sync Flags

**DB SYNC NEEDED:** Trump↔Powell VsOverlay data — IdeologyProfile axis divergence scores required. Powell IdeologyProfile ✅ seeded. Trump IdeologyProfile ✅ seeded. Need divergence calculation on axis 3 (monetary conservatism) and axis 5 (interventionism).

**DB SYNC NEEDED:** Semiconductor PowerMap — PowerMapRelation edges for TSMC/NVIDIA/ASML nodes with SubstitutionLatencyMonths values need to be wired (PowerMapRelation table was empty as of 2026-03-27).
