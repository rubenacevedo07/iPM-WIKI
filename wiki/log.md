# IMP Wiki — Activity Log
*Append-only. Never edit past entries. Format defined in CLAUDE.md.*

---

## [2026-04-22] wiki-expansion | European Companies — 6 new institution pages
- **Operation:** wiki-expansion
- **Files created:**
  - wiki/institutions/RHEINMETALL.md — German defense; €50B+ order backlog, Ukraine JV, RHM.DE conviction proxy
  - wiki/institutions/AIRBUS.md — EU aerospace; 8,500+ aircraft backlog, Boeing crisis windfall, Eurofighter surge
  - wiki/institutions/TOTALENERGIES.md — French oil major; Qatar LNG JV, Hormuz exposure, Russia Arctic write-down
  - wiki/institutions/DEUTSCHE-BANK.md — German bank; €40T derivatives book, CDS spread as EU stress barometer
  - wiki/institutions/VOLKSWAGEN.md — German auto; China share 20%→12%, CARIAD delays, plant closure crisis
  - wiki/institutions/LVMH.md — French luxury; Bernard Arnault controlling shareholder, cognac tariff risk
- **Files updated:**
  - wiki/countries/GERMANY.md — related_institutions expanded; Related Pages section added (Rheinmetall, VW, Deutsche Bank, Airbus)
  - wiki/countries/FRANCE.md — related_institutions expanded; Related Pages section added (TotalEnergies, Airbus, LVMH)
  - wiki/pending-db-sync.md — CL-DB-016 through CL-DB-022 registered in Open Flags table
  - wiki/index.md — v27, 142 pages, European Companies section added to Institutions (31→37)
- **Contradictions flagged:** none
- **DB sync needed:** yes — CL-DB-016 (ASML edges), CL-DB-017 (Rheinmetall), CL-DB-018 (Airbus), CL-DB-019 (TotalEnergies), CL-DB-020 (Deutsche Bank), CL-DB-021 (Volkswagen), CL-DB-022 (LVMH + Arnault)
- **Notes:** All 6 pages follow CLAUDE.md v3.0 schema. institution_type set to 'regulator' as placeholder for industrial companies — enum should be extended to include 'manufacturer' or 'corporation'. DB IDs all TBD pending sync. Total open DB flags now: 11 (CL-DB-012 through CL-DB-022).

---

## [2026-04-09] init | IMP Wiki v1.0 created
- **Operation:** init
- **Files created:** CLAUDE.md, wiki/index.md, wiki/log.md, wiki/overview.md — full folder structure
- **Files updated:** —
- **Contradictions flagged:** none
- **DB sync needed:** no
- **Notes:** Repo initialized. Karpathy LLM Wiki pattern adapted for IMP. Option A confirmed — separate repo from main iPM_GV codebase. Ready for first ingest.

## [2026-04-09] ingest | IMP_Strategy_v2_2.docx
- **Operation:** ingest
- **Files created:**
  - wiki/sources/IMP-Strategy-v2-2.md
  - wiki/themes/IMP-Platform-Architecture.md
  - wiki/themes/IMP-Automation-Engine.md
  - wiki/themes/IMP-Oracle-System.md
  - wiki/themes/IMP-Competitive-Moats.md
  - wiki/themes/IMP-Business-Model.md
  - wiki/themes/IMP-Power-Index-System.md
  - wiki/timelines/IMP-Phase-Roadmap.md
  - wiki/oracle/Oracle-Machine-Roster.md
  - wiki/actors/DALIO-Ray.md
- **Files updated:** wiki/index.md
- **Contradictions flagged:** none
- **DB sync needed:** no — strategy doc is documentation, not entity data
- **Notes:** First real ingest. 10 pages created from one source. IMP platform skeleton now in wiki. All 20 Oracle machine names documented. Phase roadmap captured with current blocker status. DB state gaps flagged as open questions throughout.

## [2026-04-09] ingest | IPM_SQL_Seed_Reference.docx
- **Operation:** ingest
- **Files created:**
  - wiki/sources/IPM-SQL-Seed-Reference.md
  - wiki/indicators/DB-ID-Reference.md
  - wiki/indicators/Enum-Types-Reference.md
  - wiki/actors/TRUMP-Donald.md (db_id: 173)
  - wiki/actors/XI-Jinping.md (db_id: 171)
  - wiki/actors/PUTIN-Vladimir.md (db_id: 172)
  - wiki/actors/POWELL-Jerome.md (db_id: 192)
  - wiki/actors/LAGARDE-Christine.md (db_id: 191)
  - wiki/actors/FINK-Larry.md (db_id: 75)
  - wiki/actors/MUSK-Elon.md (db_id: 7)
  - wiki/actors/HUANG-Jensen.md (db_id: 1)
  - wiki/actors/DIMON-Jamie.md (db_id: 12)
  - wiki/actors/ALTMAN-Sam.md (db_id: 61)
  - wiki/actors/MACRON-Emmanuel.md (db_id: 174)
  - wiki/actors/BUFFETT-Warren.md (db_id: 9)
  - wiki/actors/BEZOS-Jeff.md (db_id: 66)
  - wiki/actors/GATES-Bill.md (db_id: 67)
  - wiki/actors/ZUCKERBERG-Mark.md (db_id: 6)
  - wiki/actors/CHANG-Morris.md (db_id: 113)
- **Files updated:** wiki/index.md
- **Contradictions flagged:** none
- **DB sync needed:** no — document defines DB state, does not require updates to it
- **Notes:** 16 actor stubs created with verified db_ids. 2 indicator pages created (DB-ID-Reference, Enum-Types-Reference). All PersonPowerIndex seeding status documented per actor. Musk + Trump flagged as standard migration test pair.

## [2026-04-09] manual-edit | CLAUDE.md upgraded to v2.0
- **Operation:** manual-edit
- **Files created:** CLAUDE.md v2.0
- **Files updated:** —
- **Contradictions flagged:** none
- **DB sync needed:** no
- **Notes:** Upgraded all 10 page templates based on Perplexity v2 guide review. Added: region+tags frontmatter, Role and Levers section, Narrative Shift section, Key Recent Actions with dates to actor template. Added Sanctions and Legal Constraints + Key Timelines to country template. Added full institution, commodity, narrative, market-impact, scenario templates (previously missing). Added domain frontmatter + Rationale + Inputs + Calculation Logic + Maintenance Rules to indicator template. Added source priority tiers table. Added specialized ingest focus rules by source type. Added narrative drift detection and geopolitics-to-markets connection rules.

## 2026-04-09 | schema-upgrade | CLAUDE.md v3.0 + frontmatter migration
- source: uploaded files (imp-mini-claude-frontmatter-rules.md, templates)
- created: CLAUDE.md v3.0
- updated: all 17 actor pages — new frontmatter schema applied
- contradictions: none
- db-sync: no
- notes: Added slug, related_actors, related_countries, related_institutions, related_commodities, related_themes arrays to all actor pages. Added role, country fields. Upgraded CLAUDE.md to v3.0 with full frontmatter governance section, reciprocal relationship rules, deduplication rules, 11 page type templates with new schema. Source priority tiers and specialized ingest modes preserved from v2.0.

## 2026-04-09 | ingest | IPM_Session_Record_2026_03_27.md
- source: raw/internal-notes/IPM_Session_Record_2026_03_27.md
- created: wiki/sources/Session-Record-2026-03-27.md
- created: wiki/timelines/IMP-DB-State-Timeline.md
- created: wiki/themes/Chokepoint-Intelligence.md
- created: wiki/dossiers/Product-Ideas-2026-03-27.md
- created: wiki/comparisons/IMP-Agent-Roles.md
- created: wiki/countries/UNITED-STATES.md (db_id: 1)
- created: wiki/countries/CHINA.md (db_id: 148)
- created: wiki/countries/RUSSIA.md (db_id: 64)
- created: wiki/countries/TAIWAN.md (db_id: 151)
- created: wiki/countries/UKRAINE.md (db_id: 65)
- created: wiki/countries/SAUDI-ARABIA.md (db_id: 71)
- updated: wiki/index.md
- contradictions: none
- db-sync: no — source IS the DB state record
- notes: First country pages created with full new frontmatter schema. DB state timeline established as append-only reference. 7 product ideas archived in dossiers/. Agent roles comparison documented. Chokepoint intelligence theme page created with all 7 IMP chokepoints. Key pending seeds flagged: Trump/MBS/Bessent PersonPowerIndex, Aladdin node, IdeologyProfiles for Fink/Xi/MBS.

## 2026-04-09 | ingest | IPM_Project_State_2026_04_01.md
- source: raw/internal-notes/IPM_Project_State_2026_04_01.md
- created: wiki/sources/Project-State-2026-04-01.md
- created: wiki/actors/MBS.md (db_id: 176)
- created: wiki/actors/BESSENT-Scott.md (db_id: 545)
- created: wiki/actors/MODI-Narendra.md (db_id: TBD)
- created: wiki/actors/YELLEN-Janet.md (db_id: TBD)
- updated: wiki/timelines/IMP-DB-State-Timeline.md — April 1 snapshot appended
- updated: wiki/actors/TRUMP-Donald.md — score confirmed 76 rank 1
- updated: wiki/actors/GATES-Bill.md — score confirmed 71 rank 8
- updated: wiki/indicators/DB-ID-Reference.md — full 14-person ranking added, MBS=176, Bessent=545
- updated: wiki/index.md — actors table now shows full ranking
- contradictions: none — Trump score was "target 76", now confirmed 76 ✅
- db-sync: no — source IS the DB state record
- notes: Full PersonPowerIndex ranking now documented (14 persons). 4 new actor pages. C# vs DB column name map archived in DB timeline. Auth blocker (B-02) confirmed COMPLETE. B-04 (CompositeIndexSnapshots) still failing.

## 2026-04-09 | ingest | IPM_Session_Handoff_2026_04_02.md + IPM_Launch_Plan_April21.html
- source: raw/internal-notes/IPM_Session_Handoff_2026_04_02.md
- source: raw/internal-notes/IPM_Launch_Plan_April21.html
- created: wiki/sources/Session-Handoff-2026-04-02.md
- created: wiki/sources/Launch-Plan-April-21.md
- created: wiki/dossiers/Launch-Plan-April-21.md
- updated: wiki/timelines/IMP-DB-State-Timeline.md — April 2 checkpoint appended
- updated: wiki/index.md
- contradictions: none
- db-sync: yes — Launch Plan flags two DB sync needs: (1) Trump↔Powell VsOverlay divergence data needed, (2) Semiconductor PowerMap PowerMapRelation edges still empty
- notes: All 6 internal IMP project sources now ingested. Launch plan archived as dossier with 6 persona profiles and critical path deadlines. April 21 is 12 days from today — active deadline. DB timeline now covers March 27 → April 1 → April 2.

## 2026-04-09 | query | Trump-Powell IdeologyProfile divergence
- source: live DB query (IdeologyProfile table, EntityIds 173 + 192)
- created: wiki/comparisons/Trump-Powell-Divergence.md
- updated: wiki/actors/TRUMP-Donald.md — ideology scores added
- updated: wiki/actors/POWELL-Jerome.md — ideology scores added
- contradictions: none
- db-sync: no — DB is source of truth, wiki now reflects it
- notes: DSI signal = 4.25 (high tension). Highest divergence: EnvScore 9.5. Most policy-relevant: AuthScore 7.5 gap. EconScore gap only 1.0 — both economically conservative. Trump-Powell divergence is a political pressure signal, not monetary policy divergence signal. DB sync flag CL-DB-001 RESOLVED.

## 2026-04-09 | query | Powell-Lagarde IdeologyProfile divergence — EUR/USD signal
- source: live DB query (IdeologyProfile table, EntityIds 191 + 192 + 173)
- created: wiki/comparisons/Powell-Lagarde-Divergence.md
- updated: wiki/actors/LAGARDE-Christine.md — ideology scores added
- contradictions: none
- db-sync: no — DB is source of truth, wiki now reflects it
- notes: EUR/USD signal = 4.5 (strong divergence zone). EconScore gap 6.0 = primary driver (Powell conservative 4.0 vs Lagarde left-of-center -2.0). Three-way comparison documented: Trump-Lagarde divergence 9.75 = near maximum in dataset. DB sync flag CL-DB-002 RESOLVED.

## 2026-04-09 | manual-edit | Graph view wikilinks — all pages updated
- Operation: manual-edit
- Files updated: 21 actor pages + 6 country pages + 5 theme/comparison pages + 10 institution stubs created
- Contradictions flagged: none
- DB sync needed: no
- Notes: Added [[wikilink]] syntax to Related Pages sections across all pages so Obsidian Graph View shows connections. Created institution stubs for BlackRock, Federal Reserve, ECB, JPMorgan, NVIDIA, TSMC, OpenAI, US Treasury, Kremlin, OPEC+. Graph now shows: actor-actor links, actor-institution links, actor-country links, country-country links, theme cross-links, comparison-actor links.

## 2026-04-09 | manual-edit | BlackRock ownership web — graph connections built
- Operation: manual-edit
- Files created: wiki/comparisons/BlackRock-Ownership-Web.md + 12 company institution stubs (Apple, Microsoft, Amazon, Alphabet, Meta, Tesla, ExxonMobil, Lockheed Martin, Samsung, ASML, Saudi Aramco, Goldman Sachs)
- Files updated: wiki/institutions/BLACKROCK.md — full ownership wikilinks added
- Contradictions: none
- DB sync needed: yes — BlackRock→Owns→NVIDIA/TSMC/ASML/ExxonMobil/Lockheed RelationEdge rows pending
- Notes: BlackRock now connects to 15 companies in graph view. Aladdin layer documented. Invisible Hand Tracker example trace built (Hormuz closure cascade). All holdings link bidirectionally back to BLACKROCK.md. Source a 13F filing for precise stake percentages.

## 2026-04-09 | lint | First health audit
- Operation: lint
- Files created: wiki/lint-reports/2026-04-09.md
- Files updated: wiki/index.md (full rebuild), wiki/themes/IMP-Automation-Engine.md, wiki/timelines/IMP-Phase-Roadmap.md, wiki/institutions/ECB.md, wiki/institutions/META.md, wiki/institutions/AMAZON.md, wiki/institutions/MICROSOFT.md
- Contradictions flagged: none
- DB sync needed: no
- Notes: 73 pages audited. 14 orphans found (8 fixed immediately). 21 thin pages (all institution stubs — acceptable). 11 actors with empty Current Assessment + Narrative Shift (root cause: no external sources ingested yet). 8 broken wikilinks fixed (naming convention mismatch). Index rebuilt with all 22 institution pages + new comparison pages. Missing: France, Germany, India, Iran country pages. Top priority next action: ingest first external source (Fed speech or ECB transcript) to populate empty actor sections.

## 2026-04-09 | manual-edit | IMP Raw Collection Prompts added
- Operation: manual-edit
- Files created: wiki/dossiers/IMP-Raw-Collection-Prompts.md
- Notes: 10-task prompt pack for collecting external sources into raw/. Tasks cover Fed/Powell, ECB/Lagarde, IMF WEO, BIS Quarterly, BlackRock 13F, TSMC earnings, chokepoint risk, China economy, Russia oil sanctions, Trump trade policy. Source URLs included. Compatible with Claude Code (direct file write) and Claude.ai (paste output for ingest).

## 2026-04-09 | ingest | 7 external sources (Perplexity batch)
- Operation: ingest
- Sources ingested:
  - raw/transcripts/powell-fomc-2026-04.md
  - raw/central-banks/lagarde-ecb-2026-04.md
  - raw/institutions/imf-weo-2026-04.md
  - raw/markets/blackrock-13f-2025-12-31.md
  - raw/geopolitics/chokepoint-risk-2026-04.md
  - raw/geopolitics/trump-trade-policy-2026-04.md
  - raw/sanctions/russia-oil-2026-04.md
- Created: wiki/sources/ (7 summaries), wiki/market-impact/Fed-Rate-Policy-Markets.md, wiki/market-impact/Trump-Trade-War-Markets.md, wiki/narratives/Global-Macro-Regime-2026-04.md
- Updated: POWELL-Jerome.md (Current Assessment + Narrative Shift), LAGARDE-Christine.md (same), TRUMP-Donald.md (same), RUSSIA.md (Narrative Trajectory), CHINA.md (Narrative Trajectory), Chokepoint-Intelligence.md (threat scores updated)
- Contradictions: Chokepoint DB scores diverge from wiki — DB has Hormuz=10/Taiwan=8, wiki April 2026 assessment has Bab el-Mandeb=8 as highest active risk
- DB sync needed: YES — CommodityChokepoint Bab el-Mandeb threat score needs update (Houthi campaign elevated it)
- Notes: FIRST EXTERNAL SOURCE INGESTS. Actor pages now have real Current Assessment and Narrative Shift content for Powell, Lagarde, Trump. BlackRock 13F partial — full verified data requires EDGAR XML download. All 7 raw files saved in correct raw/ subfolders.

## 2026-04-09 | manual-edit | Perplexity State Report v13 created
- Operation: manual-edit
- Files created: wiki/dossiers/Perplexity-State-Report-v13.md
- Notes: Full briefing for Perplexity on wiki v13 state. Includes: inventory of 96 pages, IdeologyProfile status per actor, active DB sync flags (CL-DB-003 to CL-DB-006), 5 priority collection tasks with ready-to-paste prompts, workflow summary, health metrics.

## 2026-04-09 | ingest | 6 Perplexity templates — 4 themes + 2 timelines
- Operation: ingest
- Source: Perplexity generated page templates
- Files created:
  - wiki/themes/Energy-Chokepoints-War.md
  - wiki/themes/AI-Supply-Chain-Export-Controls.md
  - wiki/themes/Geoeconomic-Fragmentation.md
  - wiki/themes/Monetary-Policy-Weaponized-World.md
  - wiki/timelines/Global-Energy-Shipping-2019-2026.md
  - wiki/timelines/AI-Tech-Decoupling-2019-2026.md
- Contradictions: none
- DB sync needed: CL-DB-003 (Bab el-Mandeb), CL-DB-005 (PowerMapRelation semiconductor edges) referenced in new pages
- Notes: Major structural upgrade — 4 new intelligence themes created that cross-link actors, countries, institutions, and signals. Two append-only timelines covering energy/shipping and AI/tech decoupling from 2019-2026. All pages fully wikilinked into graph. Wiki now has 11 theme pages (was 7).

## 2026-04-09 | manual-edit | Prompt Pack Operativo v2.0 creado
- Operation: manual-edit
- Files created: wiki/dossiers/IMP-Prompt-Pack-Operativo-v2.md
- Notes: Pack operativo completo alineado con CLAUDE.md v3.0. 5 prioridades con prompts listos para copiar/pegar en Perplexity. P1=IdeologyProfile 9 actores con DB column names correctos. P2=6 country pages con Power Profile fields (FinancialScore/MilitaryScore etc). P3=TSMC earnings + Jensen Huang narrative. P4=BIS Quarterly. P5=Weekly refresh (Powell/Lagarde/Chokepoints). Quick reference tables incluyen DB column names y verified IDs.

## 2026-04-09 | ingest | Mission Pack v1.0 — Tasks 1-5 executed
- Operation: ingest + manual-edit
- Files created:
  - raw/ideology/ideology-profiles-2026-04.md (9 actor scores)
  - raw/ideology/ideology-seed-sql-2026-04-09.sql (ready to run in pgAdmin)
  - wiki/countries/FRANCE.md (db_id: 30)
  - wiki/countries/GERMANY.md (db_id: 29)
  - wiki/countries/INDIA.md (db_id: 140)
  - wiki/countries/IRAN.md (db_id: 72)
  - wiki/countries/ISRAEL.md (db_id: 74)
  - wiki/countries/JAPAN.md (db_id: 149)
  - raw/internal-notes/IMP-mission-weekly-ops-2026-04-09.md
- Files updated: 9 actor pages (IdeologyProfile sections), wiki/index.md
- Contradictions: none
- DB sync needed: YES
  - CL-DB-006: Run ideology-seed-sql-2026-04-09.sql for 7 actors (Modi+Yellen pending PersonId confirmation)
  - CL-DB-007: Confirm 6 new country DB IDs in Countries table
- Notes: Task 1 (IdeologyProfiles) complete with knowledge-based scoring confidence 70-85%. Task 2 (6 country pages) complete with full CLAUDE.md v3.0 schema. Tasks 3-4 (TSMC/BIS) stubs created in Mission Pack — pending Perplexity source. Task 5 (Weekly Refresh) protocol documented with ready-to-paste prompts. Mission Pack v1.0 is the operating document for weekly intelligence operations.

## 2026-04-09 | db-sync | CL-DB-005 CLOSED — Semiconductor PowerMapRelation seeded
- Operation: db-sync
- DB changes confirmed:
  - PowerMapRelation row 1: ASML → Partners → TSMC (RE 55, Critical) ✅
  - PowerMapRelation row 2: NVIDIA → DependsOn → Taiwan (RE 91, Critical) ✅
  - PowerMapRelation row 3: Jensen → Governs → NVIDIA (RE 1, Critical) ✅
  - PowerMapRelation row 4: Morris Chang → Owns → TSMC (RE 38, High) ✅
  - PowerMapRelation row 5: TSMC → Partners → Apple (RE 53, Critical) ✅
- Files updated: wiki/themes/Chokepoint-Intelligence.md, wiki/themes/AI-Supply-Chain-Export-Controls.md
- DB sync flag: CL-DB-005 CLOSED
- Notes: Semiconductor PowerMap (ID=4) now has 5 live edges. PowerMapIntelligence view will render these in frontend. Samsung and Intel nodes not in PowerMap 4 — could be added as PowerMapNode inserts if needed for demo.

## 2026-04-09 | db-sync | CL-DB-006 PENDING — IdeologyProfile SQL ready to run
- Notes: SQL ready in raw/ideology/ideology-seed-sql-2026-04-09.sql. 7 actors with confirmed DB IDs: Xi(171), MBS(176), Fink(75), Bessent(545), Huang(1), Gates(67), Altman(61). Modi and Yellen not in Persons table — need person seed first.

## 2026-04-10 | db-sync | CL-DB-006 CLOSED — IdeologyProfile 12 actors confirmed live
- Operation: db-sync
- DB rows confirmed:
  Putin(172):   Econ=-2.0 Auth=10.0 Geo=9.0  Env=7.5  Label=Authoritarian nationalist imperialist  Conf=5
  Xi(171):      Econ=2.0  Auth=9.0  Geo=3.0  Env=-3.0 Label=CCP nationalist authoritarian          Conf=5
  MBS(176):     Econ=4.0  Auth=8.5  Geo=2.0  Env=6.0  Label=Modernising authoritarian              Conf=4
  Trump(173):   Econ=5.0  Auth=7.5  Geo=-4.0 Env=8.5  Label=Nationalist-populist authoritarian     Conf=5
  Musk(7):      Econ=7.5  Auth=4.0  Geo=6.0  Env=-2.0 Label=Techno-libertarian nationalist         Conf=5
  Bessent(545): Econ=6.0  Auth=1.0  Geo=-1.0 Env=4.0  Label=Fiscal hawk nationalist                Conf=4
  Powell(192):  Econ=4.0  Auth=0.0  Geo=1.0  Env=-1.0 Label=Technocratic institutionalist          Conf=4
  Fink(75):     Econ=3.0  Auth=-2.0 Geo=5.0  Env=-4.0 Label=Liberal financial multilateralist      Conf=4
  Altman(61):   Econ=4.0  Auth=-3.0 Geo=3.0  Env=-1.0 Label=AI accelerationist techno-optimist     Conf=4
  Lagarde(191): Econ=-2.0 Auth=-3.0 Geo=4.0  Env=-5.0 Label=Liberal multilateralist               Conf=4
  Huang(1):     Econ=5.0  Auth=-3.0 Geo=4.0  Env=-1.0 Label=Techno-optimist multilateralist        Conf=4
  Gates(67):    Econ=1.0  Auth=-4.0 Geo=7.0  Env=-6.0 Label=Techno-philanthropic multilateralist   Conf=5
- Constraint discovered: IdeologyProfile.Confidence CHECK 1-5 (not 0-100) — ipm-database SKILL updated
- DB sync flag: CL-DB-006 CLOSED
- Notes: AuthScore column shown in verify is GeoScore in schema (columns: Econ, Auth, Cultural, Gender, Geo, Env, Religion). Verify output matches expected values. Musk EconScore=7.5 = highest in dataset. Gates EnvScore=-6.0 = most interventionist. Putin AuthScore=10.0 = maximum.

## 2026-04-10 | db-sync | CL-DB-003 CLOSED — Bab el-Mandeb updated to 8
- Operation: db-sync
- Confirmed chokepoint scores:
  Hormuz=10, Bab el-Mandeb=8, Taiwan Strait=8, Black Sea=8, Suez=6, Malacca=5, Panama=3
- DB sync flag: CL-DB-003 CLOSED
- Notes: Bab el-Mandeb now matches wiki assessment (Houthi campaign elevated to 8). Taiwan Strait and Black Sea also at 8 — three chokepoints at critical tier simultaneously. Panama at 3 (drought-related capacity issues, not conflict).

## 2026-04-10 | ingest | Bitcoin integration — wiki + Thread Master config
- Operation: ingest + manual-edit
- Files created:
  - wiki/commodities/BITCOIN.md — supply structure, demand, chokepoints, market impact
  - wiki/themes/Bitcoin-Macro-Regime.md — 3 regimes (A=liquidity-on, B=liquidity-off, C=macro-hedge)
  - wiki/market-impact/Bitcoin-vs-Equities-Rates.md — direct/second-order channels, affected asset classes
  - raw/internal-notes/thread-master-bitcoin-integration.js — CONFIG additions, IMP_CONTEXT bridge, compatibilityRules
- Contradictions: none
- DB sync needed: yes — Bitcoin not yet in Commodities table (db_id pending)
- Notes: Current IMP regime = Regime B (liquidity-off, Fed hawkish). Bitcoin strategy BLOCKED in Thread Master until Powell pivot or DSI deterioration triggers Regime A or C. IMP_CONTEXT object provides weekly-updatable bridge between wiki and Thread Master config. BitcoinImpBadge component shows current bias in strategy selector UI.

## 2026-04-10 | ingest | Dollar System layer — Fed + Wall Street + Pentagon + 3 indicators
- Operation: ingest
- Files created:
  - wiki/institutions/WALL-STREET.md — financial ecosystem node, Fed relationship, Pentagon link
  - wiki/institutions/PENTAGON.md — US military projection, chokepoint control, defense industrial base
  - wiki/indicators/Fed-Liquidity-Pulse.md — balance sheet Δ + RRP + TGA + BTFP → Pulse Score -10 to +10
  - wiki/indicators/USD-Hegemony-Index.md — COFER + SWIFT + DXY + trade invoicing → 0-100 score
  - wiki/indicators/US-Military-Projection.md — budget + carriers + bases + nuclear → 0-100 score
  - wiki/themes/Dollar-System-Fed-Liquidity.md — connects all 3 indicators + 3 scenarios
- Contradictions: none
- DB sync needed: Wall Street + Pentagon need Company rows seeded
- Notes: Dollar power stack documented (Pentagon→Treasury→Fed→Wall Street→Global System). Current: Fed Liquidity Pulse ~-3 to -4 (mild contraction), USD Hegemony ~72/100 (gradual erosion), US Military ~78/100 (stressed but dominant). Bitcoin regime connections wired through Fed Liquidity Pulse. Three dollar scenarios: A=gradual erosion (baseline), B=crisis (tail), C=reinvigoration.

## 2026-04-10 | db-sync | Institutions seeded as Companies — 8 new rows confirmed
- Operation: db-sync
- DB rows confirmed:
  Federal Reserve=240, ECB=241, US Treasury=242, Pentagon=243
  Wall Street=244, IMF=245, BIS=246, NATO=247
- Files updated: FEDERAL-RESERVE.md, ECB.md, US-TREASURY.md, WALL-STREET.md, PENTAGON.md (db_ids added)
- Files created: IMF.md (db_id:245), BIS.md (db_id:246)
- SQL ready: raw/ideology/institutions-relationedge-seed.sql — 13 RelationEdge INSERTs
- Notes: NodeType='Company' used for all institutions (no schema change needed). Ticker=NULL, SystemicImportanceLevel=Critical/High. ipm-database SKILL updated with institution ID map. Skill now has: Federal Reserve=240, ECB=241, Treasury=242, Pentagon=243, Wall Street=244, IMF=245, BIS=246, NATO=247.

## 2026-04-10 | ingest | AI supply chain complete — AI companies, cloud, Palantir, commodities
- Operation: ingest
- Files created:
  - wiki/institutions/PALANTIR.md
  - wiki/institutions/AWS.md
  - wiki/institutions/AZURE.md
  - wiki/institutions/GOOGLE-CLOUD.md
  - wiki/institutions/ANTHROPIC.md (db_id: 197 confirmed)
  - raw/ideology/ai-supply-chain-complete-seed.sql (companies + commodities)
  - raw/ideology/ai-supply-chain-edges.sql (25 RelationEdge INSERTs — needs IDs from Step 0)
- Files updated: wiki/themes/AI-Supply-Chain-Export-Controls.md (complete 6-layer graph added)
- DB sync needed: YES
  1. Run ai-supply-chain-complete-seed.sql Step 1 to seed companies
  2. Run Step 0 verify to get actual IDs
  3. Replace [PLTR_ID],[AWS_ID],[AZURE_ID],[GCP_ID],[AMD_ID],[ARM_ID],[HYNIX_ID],[MICRON_ID],[XAI_ID] in ai-supply-chain-edges.sql
  4. Run edges SQL
  5. Seed commodities (Step 2)
- Notes: Complete AI supply chain now documented — 6 layers from rare earths to Palantir defense AI. Meta confirmed as largest single NVIDIA buyer (350K+ H100s). OpenAI exclusively on Azure. Anthropic exclusively on AWS. xAI Colossus = 100K+ H100s. Palantir connects AI supply chain to Pentagon/CIA/Ukraine.

## 2026-04-10 | db-sync | Commodity links seed — CompanyCommodities + CommodityFacility
- Operation: db-sync
- SQL ready: raw/ideology/commodity-links-seed.sql
- CompanyCommodities new rows (18 inserts):
  TSMC(41): Silicon Wafers(50) Critical, Photoresist EUV(54) Critical, Gallium(69) High, Germanium(68) High
  Samsung(43): Silicon Wafers(50) Critical, HBM(55) Critical, NAND(48) Critical, DRAM(49) Critical
  Intel(85): Silicon Wafers(50) Critical, Photoresist EUV(54) Critical, SiC Wafers(56) High
  OpenAI(198): GPU Compute(53) Critical 95%, HBM(55) High 75%
  Anthropic(197): GPU Compute(53) Critical 90%, HBM(55) High 70%
  BlackRock(90): Brent(1) High, Gold(12) High, GPU Compute(53) High
- CommodityFacility new rows (8 inserts):
  TSMC Fab18(41)→Advanced Logic(51) Produces Critical Risk=9
  TSMC Hsinchu(407)→Silicon Wafers(50) Input Critical Risk=8
  TSMC Arizona(454)→Advanced Logic(51) Produces High Risk=4
  ASML Veldhoven(21)→Photoresist EUV(54) Input Critical Risk=7
  Samsung Pyeongtaek(43)→HBM(55) Produces Critical Risk=6
  Samsung Pyeongtaek(43)→NAND(48) Produces High Risk=5
  Intel Fab42 AZ(175)→Mature Chips(52) Produces High Risk=3
  Intel Fab34 Ireland(447)→Advanced Logic(51) Produces Medium Risk=3
- ipm-database SKILL updated with full commodity ID map (117 commodities categorized)

## 2026-04-10 | ingest | 5 scenarios created — one per domain
- Operation: ingest
- Files created:
  - wiki/scenarios/Taiwan-Strait-2026-2028.md (Semiconductor domain)
  - wiki/scenarios/Hormuz-Iran-Crisis-2026.md (Energy/Chokepoint domain)
  - wiki/scenarios/Fed-Pivot-2026.md (Monetary/Macro domain)
  - wiki/scenarios/Dollar-System-Stress-2026-2028.md (Dollar/DSI domain)
  - wiki/scenarios/AI-Race-Breakpoint-2026-2028.md (AI/Tech domain)
- Each scenario: 3 branches (A/B/C), probability estimates, market cascades, IMP DB updates triggered, cross-branch markers, Oracle relevance
- DB sync: Taiwan Branch A triggers ScenarioCascade Oil $150 template. AGI Branch A needs new ScenarioCascade template.
- Notes: Taiwan scenario directly relevant for Oliver demo (Apr 21) — SupplyRiskScore=9 on TSMC Fab 18 now has narrative context. Fed Pivot scenario wired to Thread Master Bitcoin IMP_CONTEXT. Dollar scenario documents Trump paradox (short-term USD strength vs long-term erosion).

## 2026-04-10 | db-sync | 4 SQLs completados — AI supply chain + commodities LIVE
- Operation: db-sync
- Final counts confirmed:
  RelationEdge: 1,271 (+25 new AI supply chain edges)
  CompanyCommodities: 315 (+18 new links)
  CommodityFacility: 22 (+8 fab→commodity links)
  Commodities: 121 (+4: Rare Earths/Uranium/Phosphates/Bitcoin)
- New companies seeded: Palantir(96), AMD(69), Arm Holdings(248), Mistral AI, Cohere, xAI(199)
- Key edges live: NVIDIA→SK Hynix, NVIDIA→Micron, AMD→TSMC, Arm→NVIDIA, 
  Meta→NVIDIA, OpenAI→Microsoft, Microsoft→OpenAI, Anthropic→Amazon, 
  Amazon→Anthropic, Musk→xAI, xAI→NVIDIA, Altman→OpenAI,
  Palantir→Pentagon, Palantir→Ukraine, Palantir→USA, Palantir→NVIDIA
- DB sync flags: CL-DB-008 ✅, CL-DB-009 ✅, CL-DB-010 ✅
- Skill updated: Rule 13 (setval before nextval in batch), Rule 14 (CommodityFacility UsageType enum), Rule 15 (pg_get_serial_sequence pattern)
- Still pending: CL-DB-011 (institution RelationEdges — institutions-relationedge-seed.sql)

## 2026-04-10 | db-sync | CL-DB-011 CLOSED — Institution RelationEdges confirmed live
- Operation: db-sync
- 13 edges confirmed (RE 1272-1284):
  Powell(192)→Sets→Federal Reserve(240) Critical
  Lagarde(191)→Sets→ECB(241) Critical
  Bessent(545)→Governs→US Treasury(242) Critical
  Trump(173)→Governs→Pentagon(243) Critical
  Federal Reserve(240)→Sets→USA(1) Critical
  Federal Reserve(240)→Influences→Wall Street(244) Critical
  US Treasury(242)→Sanctions→Russia(64) Critical
  US Treasury(242)→Sanctions→Iran(72) Critical
  Pentagon(243)→Governs→USA(1) Critical
  Pentagon(243)→Finances→Lockheed Martin(68) Critical
  Fink(75)→Influences→Wall Street(244) High
  ECB(241)→Sets→Germany(29) Critical
  IMF(245)→Partners→Federal Reserve(240) High
- DB sync flag: CL-DB-011 CLOSED
- Final RelationEdge count: 1,284

## 2026-04-10 | db-sync | CL-DB-004 + CL-DB-007 CLOSED
- CL-DB-007: Country IDs confirmed — France=30, Germany=29, India=140, Iran=72, Israel=74, Japan=149
- CL-DB-004: BlackRock Owns edges seeded (RE 1285-1294):
  NVIDIA(1), TSMC(41), ASML(21), ExxonMobil(14), Lockheed(68)
  Microsoft(4), Apple(2), Alphabet(3), Amazon(5), Saudi Aramco(42)
  All Strength=High except Aramco=Medium
- Final RelationEdge count: 1,294
- ALL DB SYNC FLAGS CLOSED ✅

## 2026-04-17 | dossier-ingest | 6 actor pages enriched from external dossiers
- sources:
  - raw/dossiers-external/musk-elon-dossier-2026-04.html
  - raw/dossiers-external/trump-donald-power-profile-2026-04.html
  - raw/dossiers-external/fink-larry-dossier-2026-04.html
  - raw/dossiers-external/huang-jensen-dossier-2026-04.html
  - raw/dossiers-external/gates-bill-dossier-2026-04.html
  - raw/dossiers-external/zuckerberg-mark-dossier-2026-04.html
- created (raw/): 6 HTML dossiers copied to raw/dossiers-external/ for source traceability
- updated (wiki/actors/):
  - MUSK-Elon.md — added Wealth Composition, Companies & Valuations, Global Facilities, Commodities, Strategic Alliances, Ideology & Worldview, Risk Profile, enriched Current Assessment, Narrative Shift, Key Recent Actions, Market Impact
  - TRUMP-Donald.md — added Wealth Composition, Key Properties, Crypto Empire, Wall Street Influence, Winners/Losers, Media Allies/Enemies, AI Vision, Strategic Alliances, US SWF, Dollar as Weapon, Risk Profile, enriched Current Assessment with April 2026 synthesis
  - FINK-Larry.md — added BlackRock Empire Scope, Aladdin systemic infrastructure detail, Fourth Branch argument, Historical Milestones, Strategic Alliances, Revolving Door, Ideology, Risk Profile, Current Assessment April 2026 synthesis, Key Recent Actions, enriched Market Impact channels
  - HUANG-Jensen.md — added Financial Trajectory table, CUDA Moat detail, Product Stack, China Problem geopolitical exposure, Clients/Partners, Competitors, Physical AI, Ideology, Risk Profile, Current Assessment April 2026 synthesis
  - GATES-Bill.md — added Wealth Composition, Microsoft History, BMGF Global Health, Food/Farmland, COVID Role, Epstein Files, Philanthropy, AI Vision, Political Power, Myths vs Facts, Risk Profile, Current Assessment April 2026 synthesis
  - ZUCKERBERG-Mark.md — added Meta Empire scale, AI Open Source Bet, Political Pivot Jan 2025, Antitrust battles, CZI Philanthropy, Personal Transformation, Properties, Ideology, Risk Profile, Current Assessment April 2026 synthesis
- contradictions: none material — dossier content supplements stub sections marked "populate from ingests"
- db-sync: YES — multiple DB SYNC NEEDED flags raised across all 6 pages
  - Wealth figures (EstimatedWealthUsd) for all 6 actors need verification against Persons table
  - New Company node candidates: xAI (under SpaceX), Trump Media (DJT), World Liberty Financial, iShares, Starlink, CZI, Cascade Investment subsidiaries
  - New RelationEdge candidates: US-China NVIDIA/AMD 15% revenue deal, Fink→Advises→Ukraine reconstruction, Fink→Manages→US-Infrastructure-Fund, Zuckerberg→Influences→Trump
  - Chokepoint status review: Starlink (Musk), Aladdin (Fink — flag already open), CUDA (Huang, new candidate)
  - Sovereign AI partnerships (Huang dossier): UAE, Saudi, Japan, India, France, Singapore as new NVIDIA→Supplies edges
- notes:
  - Existing IdeologyProfile tables preserved on TRUMP, FINK, HUANG, GATES — not overwritten
  - Existing DB sync notes preserved; new flags appended rather than replacing
  - Related Pages links de-duplicated across sources
  - All 6 dossiers are external HTML retained in raw/dossiers-external/ for audit trail
  - 6 source-summary pages NOT created under wiki/sources/ — dossiers are cited in each actor's Sources section directly; consider adding formal summary pages in follow-up if dossiers become canonical references

## 2026-04-20 | dossier | GPT Context Report generated
- Operation: dossier creation
- Files created: wiki/dossiers/GPT-Context-Report-2026-04-20.md
- Purpose: self-contained briefing doc for ChatGPT/GPT sessions — parallel to Perplexity-State-Report-v13
- Contents: mission, structure, IMP glossary (archetypes, edges, chokepoints), full inventory with DB IDs, open DB sync flags, recent activity, prioritized work list, frontmatter rules, what-not-to-do
- Contradictions flagged: none
- DB sync needed: no
- Notes: Stand-alone doc. Paste into ChatGPT or upload as file. Does not duplicate raw wiki pages — summarizes and indexes.

## 2026-04-21 | lint | Monthly health audit — 130 pages
- Operation: lint
- Files created: wiki/lint-reports/2026-04-21.md
- Files updated: wiki/index.md (v24 — companies/ section added, header updated to 130 pages, new lint entry)
- Findings (10 total):
  - LINT-01 [HIGH]: 12 pages on old v1 schema (missing slug, using `related:` instead of `related_*` arrays) — 6 IMP themes, IMP-Phase-Roadmap, Oracle-Machine-Roster, 2 sources, 2 indicators
  - LINT-02 [HIGH]: companies/ folder (11 pages, added 2026-04-19) absent from wiki/index.md — now fixed
  - LINT-03 [MEDIUM]: wiki/index.md header stale — now fixed (v24, 130 pages)
  - LINT-04 [MEDIUM]: 7 high-churn intel pages last updated 2026-04-09 (Powell, Lagarde, Bessent, China, Ukraine, Iran, Global-Macro-Regime narrative)
  - LINT-05 [MEDIUM]: 3 dossiers without any frontmatter (IMP-Raw-Collection-Prompts, Perplexity-State-Report-v13, IMP-Prompt-Pack-Operativo-v2)
  - LINT-06 [MEDIUM]: PALANTIR.md has db_id: TBD — confirmed 96 in DB
  - LINT-07 [LOW]: Lockheed↔Northrop edge strength drift (Competes/Partners swap) — open from 2026-04-20 dry-run
  - LINT-08 [LOW]: 42 pages with sources: [] — chronic stub gap, no new external ingests since 2026-04-09
  - LINT-09 [NULL]: depends_on field does not exist in this schema — no broken slugs of that type
  - LINT-10 [LOW]: No individual oracle context pages — only Oracle-Machine-Roster exists
- Contradictions flagged: none
- DB sync needed: YES
  - CL-DB-012: PALANTIR db_id: TBD → 96 confirmed in DB
  - CL-DB-013: Lockheed↔Northrop edge strength mismatch (Competes=High→Medium, Partners=Medium→High)
- Top 5 next ingests: (1) Powell/Fed April 2026, (2) Lagarde/ECB April 2026, (3) TSMC Q1 2026 earnings, (4) BIS Quarterly Q1 2026, (5) China MOFCOM tariff retaliation
- Notes: 57 new pages since last lint (2026-04-09). Primary schema debt is the 12 old-v1-schema pages — these predate CLAUDE.md v3.0 upgrade and need frontmatter migration. companies/ section is now indexed. GPT-Context-Report dossier is untracked in git.

## 2026-04-21 | wiki-expansion | TAIWAN, narratives, 5 actors, pending-db-sync, CLAUDE.md
- Operation: content-enrichment + new-control-file + schema-update
- Files created:
  - wiki/pending-db-sync.md — single source of truth for all open DB flags (CL-DB-012 to CL-DB-015). Closed flags preserved as audit trail. SQL patterns included.
- Files updated (CLAUDE.md):
  - Added `wiki/pending-db-sync.md` as a named control file in Section 6 with full usage rules (raise/close protocol, sequential numbering, never-delete-closed-entries)
- Files updated (actors):
  - wiki/actors/POWELL-Jerome.md — removed duplicate Narrative Shift section, expanded with tariff-era posture, Key Recent Actions populated (knowledge-based)
  - wiki/actors/LAGARDE-Christine.md — removed duplicate Narrative Shift, added tariff shock fork analysis, April 2026 pivot signal, Key Recent Actions
  - wiki/actors/XI-Jinping.md — Current Assessment + Narrative Shift + Key Recent Actions populated (rare earth controls, PBOC RRR, Taiwan exercises)
  - wiki/actors/MACRON-Emmanuel.md — full Current Assessment + Role and Levers + Narrative Shift + Key Recent Actions + Market Impact + Oracle Relevance + DB Sync Notes
  - wiki/actors/DIMON-Jamie.md — Current Assessment (US debt thesis, tariff-driven hard landing risk) + Narrative Shift + Key Recent Actions
- Files updated (countries):
  - wiki/countries/TAIWAN.md — full expansion: Strategic Summary, Power Profile (silicon shield, Jade Mountain, Lai Ching-te), Domestic Pressures, External Alignments, Sanctions, Narrative Trajectory, Market Relevance (TAIEX/TWD/semiconductor shock/defense premium), IMP-Specific Significance
- Files updated (narratives):
  - wiki/narratives/Global-Macro-Regime-2026-04.md — Added tariff shock transmission section, updated Recent Shifts for April 2026 escalation (Liberation Day tariffs, rare earths, stagflation risk formalized)
- Contradictions flagged: none
- DB sync needed: YES
  - CL-DB-015: BESSENT EstimatedWealthUsd — Key Square AUM not verified in Persons table (db_id=545)
  - CL-DB-012/013/014: carried forward (see wiki/pending-db-sync.md)
- Notes: wiki/pending-db-sync.md is now the canonical DB sync tracking file. CLAUDE.md updated to mandate its use. All future DB flags should be logged there first. Page count: 136.

## 2026-04-21 | recommendations-pass | lint + Smart Connections audit implemented
- Operation: schema-fix + content-enrichment + new-pages
- Files updated (schema — old v1 → v3.0):
  - wiki/themes/IMP-Platform-Architecture.md — slug, region, tags, related_* arrays
  - wiki/themes/IMP-Automation-Engine.md — same
  - wiki/themes/IMP-Competitive-Moats.md — same
  - wiki/themes/IMP-Oracle-System.md — same
  - wiki/themes/IMP-Power-Index-System.md — same
  - wiki/themes/IMP-Business-Model.md — same
  - wiki/timelines/IMP-Phase-Roadmap.md — same
  - wiki/oracle/Oracle-Machine-Roster.md — slug + oracle-specific fields (machine_domain, brier_trend) + related_*
  - wiki/sources/IMP-Strategy-v2-2.md — slug, source-path, related_*
  - wiki/sources/IPM-SQL-Seed-Reference.md — slug, source-path, related_*
  - wiki/indicators/DB-ID-Reference.md — slug, domain, scope, related_*
  - wiki/indicators/Enum-Types-Reference.md — slug, domain, scope, related_*
- Files updated (content):
  - wiki/institutions/PALANTIR.md — db_id: TBD → 96 (confirmed from log 2026-04-10)
  - wiki/actors/BESSENT-Scott.md — Current Assessment, Narrative Shift, Key Recent Actions populated (knowledge-based, confidence: medium)
  - wiki/countries/CHINA.md — Market Relevance expanded (FX/CNY/PBOC/equities/commodities/rates/Taiwan premium)
  - wiki/countries/RUSSIA.md — Market Relevance expanded (oil/shadow fleet/grain/ruble/frozen assets/infrastructure)
  - wiki/countries/SAUDI-ARABIA.md — Market Relevance expanded (Aramco/petrodollar/SAR peg/Vision 2030 bonds/Abqaiq risk)
  - wiki/countries/UKRAINE.md — Market Relevance expanded (grain/defense multiplier/eurobonds/frozen assets/Palantir)
  - wiki/countries/ISRAEL.md — Market Relevance expanded (ILS/TASE/defense tech/Suez/Iran premium/reconstruction)
- Files updated (frontmatter added):
  - wiki/dossiers/IMP-Raw-Collection-Prompts.md — full YAML frontmatter added
  - wiki/dossiers/Perplexity-State-Report-v13.md — full YAML frontmatter added
  - wiki/dossiers/IMP-Prompt-Pack-Operativo-v2.md — full YAML frontmatter added
- Files created (new oracle context pages):
  - wiki/oracle/MEI-LIN-ZHANG.md — China/trade war/tech decoupling/CNY domain, full context block
  - wiki/oracle/CHEN-WEI.md — Asia Pacific/semiconductors/Taiwan/PLA domain, full context block
- Files updated (index/control):
  - wiki/index.md — v25, 135 pages, oracle section updated (3 pages), lint entry updated
- Contradictions flagged: none
- DB sync needed: YES
  - CL-DB-012: PALANTIR.md db_id fixed wiki-side (96) — verify Palantir Company row exists in DB
  - CL-DB-013: Lockheed↔Northrop edge strength mismatch — still open from 2026-04-19 dry-run
  - CL-DB-014: CHINA Market Relevance now references PBOC→Influences→CNY edge and CIPS node — neither seeded in DB
- Notes: All 10 lint findings from 2026-04-21 report addressed except LINT-07 (Lockheed↔Northrop = DB-side fix, not wiki) and LINT-04 (requires external source ingests). Schema debt from 12 old-v1 pages fully cleared. 3 oracle machines now have individual context pages (Roster + Mei Lin Zhang + Chen Wei). BESSENT assessment is knowledge-based pending source ingest — flag for Perplexity collection.

## 2026-04-20 | state-snapshot | no edits today
- Operation: state-snapshot
- Files created: —
- Files updated: —
- Page count: 118 core wiki pages + 11 companies pages (129 total)
- Last material edit: 2026-04-19 (companies/ pipeline + generator scripts, not yet logged as its own entry)
- Last logged operation: 2026-04-17 (6-actor dossier enrichment)
- Sync status (wiki/companies/_sync_report.json, 2026-04-19 dry-run):
  - 9 company pages scanned, 0 missing edges, 0 missing news
  - 1 DRIFT: Lockheed Martin (068) — edge_strength vs Northrop Grumman: Competes wiki=High/db=Medium, Partners wiki=Medium/db=High
- Contradictions flagged: none
- DB sync needed: no new flags today; Lockheed↔Northrop strength drift still open from 2026-04-19 report
- Notes: Snapshot entry only — no ingest, edit, or lint performed. wiki/index.md still shows "Last updated: 2026-04-17" and does not yet reference the companies/ section added 2026-04-19.
