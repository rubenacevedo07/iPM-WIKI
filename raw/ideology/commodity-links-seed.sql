-- ============================================================
-- CompanyCommodities + CommodityFacility SEED
-- Filling gaps identified from current 297 rows
-- Commodity IDs confirmed:
--   48=NAND, 49=DRAM, 50=Silicon Wafers, 51=Advanced Logic 3-5nm
--   52=Mature Node, 53=GPU Compute, 54=Photoresist EUV, 55=HBM
--   56=SiC Wafers, 58=Neodymium, 59=Praseodymium, 60=Dysprosium
--   68=Germanium, 69=Gallium, 1=Brent, 6=Copper, 7=Lithium
--   12=Gold, 76=LNG JKM
-- Facility IDs confirmed:
--   41=Fab 18 (TSMC Taiwan), 407=TSMC Hsinchu, 454=TSMC Arizona
--   21=Veldhoven (ASML), 43=Pyeongtaek (Samsung), 145=Samsung Suwon
--   175=Intel Fab 42 AZ, 447=Intel Fab 34 Ireland
-- ============================================================

BEGIN;

-- ── TSMC CompanyCommodities ──────────────────────────────────
INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 41, 50, 'Critical', 95.00, 'Long-Term', 'Very Low',
  'TSMC consumes silicon wafers as primary fab input — N3/N2 requires ultra-pure 300mm wafers'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=41 AND "CommodityId"=50);

INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 41, 54, 'Critical', 90.00, 'Long-Term', 'Very Low',
  'TSMC requires EUV-grade photoresist from JSR/Shin-Etsu for sub-7nm patterning'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=41 AND "CommodityId"=54);

INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 41, 69, 'High', 70.00, 'Long-Term', 'Low',
  'Gallium used in compound semiconductors and III-V layers in advanced nodes — China controls 80% supply'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=41 AND "CommodityId"=69);

INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 41, 68, 'High', 65.00, 'Long-Term', 'Low',
  'Germanium used in optical fiber and advanced semiconductor substrates — China 60% supply'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=41 AND "CommodityId"=68);

-- ── Samsung CompanyCommodities ───────────────────────────────
INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 43, 50, 'Critical', 90.00, 'Long-Term', 'Very Low',
  'Samsung fab primary input — DRAM/NAND/Logic all require silicon wafers'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=43 AND "CommodityId"=50);

INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 43, 55, 'Critical', 85.00, 'Long-Term', 'Low',
  'Samsung is #1 HBM producer — SK Hynix competitor. HBM3E for NVIDIA B100/B200'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=43 AND "CommodityId"=55);

INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 43, 48, 'Critical', 80.00, 'Long-Term', 'Low',
  'Samsung largest NAND Flash producer globally — 30%+ market share'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=43 AND "CommodityId"=48);

INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 43, 49, 'Critical', 85.00, 'Long-Term', 'Low',
  'Samsung #1 DRAM producer globally — 43%+ market share'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=43 AND "CommodityId"=49);

-- ── Intel CompanyCommodities ─────────────────────────────────
INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 85, 50, 'Critical', 95.00, 'Long-Term', 'Very Low',
  'Intel IDM — owns fabs, consumes silicon wafers directly. 300mm wafers for 18A node'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=85 AND "CommodityId"=50);

INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 85, 54, 'Critical', 88.00, 'Long-Term', 'Very Low',
  'Intel requires EUV photoresist for 7nm/5nm/18A nodes — same supply chain as TSMC'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=85 AND "CommodityId"=54);

INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 85, 56, 'High', 60.00, 'Long-Term', 'Medium',
  'SiC wafers for Intel power management ICs and automotive chips'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=85 AND "CommodityId"=56);

-- ── OpenAI CompanyCommodities ────────────────────────────────
INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 198, 53, 'Critical', 95.00, 'Long-Term', 'Very Low',
  'OpenAI GPT-4/o1 training runs on NVIDIA H100/H200 clusters on Azure — existential GPU dependency'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=198 AND "CommodityId"=53);

INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 198, 55, 'High', 75.00, 'Long-Term', 'Low',
  'HBM3 memory in H100 GPUs critical for OpenAI model training throughput'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=198 AND "CommodityId"=55);

-- ── Anthropic CompanyCommodities ─────────────────────────────
INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 197, 53, 'Critical', 90.00, 'Long-Term', 'Very Low',
  'Anthropic Claude training on AWS Trainium + NVIDIA H100 — GPU compute existential dependency'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=197 AND "CommodityId"=53);

INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 197, 55, 'High', 70.00, 'Long-Term', 'Low',
  'HBM memory in training clusters critical for Claude model quality'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=197 AND "CommodityId"=55);

-- ── ASML additional rare materials ───────────────────────────
INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 21, 72, 'Critical', 75.00, 'Long-Term', 'Very Low',
  'Hafnium used in high-k dielectric layers in EUV systems — no substitute'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=21 AND "CommodityId"=72);

-- ── BlackRock commodity exposures ────────────────────────────
INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 90, 1, 'High', 8.00, 'ETF/Fund', 'Low',
  'BlackRock iShares oil ETFs + direct equity exposure via XOM, CVX holdings'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=90 AND "CommodityId"=1);

INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 90, 12, 'High', 5.00, 'ETF/Fund', 'Low',
  'BlackRock iShares Gold ETF (IAU) — $30B+ AUM'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=90 AND "CommodityId"=12);

INSERT INTO public."CompanyCommodities"
  ("Id","CompanyId","CommodityId","DependencyLevel","ExposurePercentage","ContractType","SubstitutionRisk","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 90, 53, 'High', 12.00, 'ETF/Fund', 'Low',
  'BlackRock IBIT (Bitcoin ETF $50B+) + NVIDIA equity = largest GPU Compute financial exposure'
FROM public."CompanyCommodities"
WHERE NOT EXISTS (SELECT 1 FROM public."CompanyCommodities" WHERE "CompanyId"=90 AND "CommodityId"=53);

COMMIT;

-- ============================================================
-- CommodityFacility SEED — linking fabs to their key commodities
-- ============================================================
BEGIN;

-- TSMC Fab 18 (Taiwan, FacilityId=41) → Advanced Logic Chips (51)
INSERT INTO public."CommodityFacility"
  ("Id","CommodityId","FacilityId","UsageType","DependencyLevel","SupplyRiskScore","SourceCountryId","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 51, 41, 'Produces', 'Critical', 9, 151,
  'TSMC Fab 18 = primary N3/N5 advanced logic production. Taiwan Strait risk=8/10'
FROM public."CommodityFacility"
WHERE NOT EXISTS (SELECT 1 FROM public."CommodityFacility" WHERE "CommodityId"=51 AND "FacilityId"=41);

-- TSMC Hsinchu (FacilityId=407) → Silicon Wafers (50) input
INSERT INTO public."CommodityFacility"
  ("Id","CommodityId","FacilityId","UsageType","DependencyLevel","SupplyRiskScore","SourceCountryId","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 50, 407, 'Input', 'Critical', 8, 151,
  'TSMC Hsinchu consumes 300mm silicon wafers — primary fab campus'
FROM public."CommodityFacility"
WHERE NOT EXISTS (SELECT 1 FROM public."CommodityFacility" WHERE "CommodityId"=50 AND "FacilityId"=407);

-- TSMC Arizona (FacilityId=454) → Advanced Logic Chips (51) produces
INSERT INTO public."CommodityFacility"
  ("Id","CommodityId","FacilityId","UsageType","DependencyLevel","SupplyRiskScore","SourceCountryId","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 51, 454, 'Produces', 'High', 4, 1,
  'TSMC Arizona Fab 21 — N4 node, US-based production for strategic customers'
FROM public."CommodityFacility"
WHERE NOT EXISTS (SELECT 1 FROM public."CommodityFacility" WHERE "CommodityId"=51 AND "FacilityId"=454);

-- ASML Veldhoven (FacilityId=21) → Photoresist EUV (54) input
INSERT INTO public."CommodityFacility"
  ("Id","CommodityId","FacilityId","UsageType","DependencyLevel","SupplyRiskScore","SourceCountryId","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 54, 21, 'Input', 'Critical', 7, 33,
  'ASML Veldhoven EUV machines require EUV photoresist — single-source supply chain'
FROM public."CommodityFacility"
WHERE NOT EXISTS (SELECT 1 FROM public."CommodityFacility" WHERE "CommodityId"=54 AND "FacilityId"=21);

-- Samsung Pyeongtaek (FacilityId=43) → HBM (55) produces
INSERT INTO public."CommodityFacility"
  ("Id","CommodityId","FacilityId","UsageType","DependencyLevel","SupplyRiskScore","SourceCountryId","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 55, 43, 'Produces', 'Critical', 6, 150,
  'Samsung Pyeongtaek — HBM3/HBM3E production for AI GPU market'
FROM public."CommodityFacility"
WHERE NOT EXISTS (SELECT 1 FROM public."CommodityFacility" WHERE "CommodityId"=55 AND "FacilityId"=43);

-- Samsung Pyeongtaek (FacilityId=43) → NAND Flash (48) produces
INSERT INTO public."CommodityFacility"
  ("Id","CommodityId","FacilityId","UsageType","DependencyLevel","SupplyRiskScore","SourceCountryId","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 48, 43, 'Produces', 'High', 5, 150,
  'Samsung Pyeongtaek largest NAND fab — V-NAND production'
FROM public."CommodityFacility"
WHERE NOT EXISTS (SELECT 1 FROM public."CommodityFacility" WHERE "CommodityId"=48 AND "FacilityId"=43);

-- Intel Fab 42 Arizona (FacilityId=175) → Mature Node Chips (52) produces
INSERT INTO public."CommodityFacility"
  ("Id","CommodityId","FacilityId","UsageType","DependencyLevel","SupplyRiskScore","SourceCountryId","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 52, 175, 'Produces', 'High', 3, 1,
  'Intel Fab 42 Arizona — 7nm/5nm production, transitioning to 18A'
FROM public."CommodityFacility"
WHERE NOT EXISTS (SELECT 1 FROM public."CommodityFacility" WHERE "CommodityId"=52 AND "FacilityId"=175);

-- Intel Fab 34 Ireland (FacilityId=447) → Advanced Logic (51) produces
INSERT INTO public."CommodityFacility"
  ("Id","CommodityId","FacilityId","UsageType","DependencyLevel","SupplyRiskScore","SourceCountryId","Notes")
SELECT COALESCE(MAX("Id"),0)+1, 51, 447, 'Produces', 'Medium', 3, 38,
  'Intel Fab 34 Ireland — Intel 4 node (7nm equiv), European advanced logic production'
FROM public."CommodityFacility"
WHERE NOT EXISTS (SELECT 1 FROM public."CommodityFacility" WHERE "CommodityId"=51 AND "FacilityId"=447);

COMMIT;

-- VERIFY
SELECT COUNT(*) as total_company_commodities FROM public."CompanyCommodities";
SELECT COUNT(*) as total_commodity_facilities FROM public."CommodityFacility";

-- Show new entries
SELECT cc."CompanyId", c."Name" AS company,
  cm."Name" AS commodity, cm."Category",
  cc."DependencyLevel", cc."ExposurePercentage", cc."SubstitutionRisk"
FROM public."CompanyCommodities" cc
JOIN public."Companies" c ON c."Id" = cc."CompanyId"
JOIN public."Commodities" cm ON cm."Id" = cc."CommodityId"
WHERE cc."CompanyId" IN (41,43,85,198,197,90)
ORDER BY c."Name", cm."Category";
