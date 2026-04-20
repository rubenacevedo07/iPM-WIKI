-- ============================================================
-- AI Supply Chain Complete Seed
-- Layer 1: AI Companies (consumers of chips)
-- Layer 2: Cloud Infrastructure (middleware)
-- Layer 3: Palantir connections
-- Layer 4: Key commodities
-- ============================================================

-- STEP 0: Check what already exists
SELECT "Id","Name","Ticker" FROM public."Companies"
WHERE "Name" ILIKE ANY(ARRAY[
  '%Palantir%','%Anthropic%','%Mistral%','%Cohere%','%xAI%',
  '%DeepMind%','%Snowflake%','%Databricks%','%Oracle%',
  '%AMD%','%Arm Holdings%','%SK Hynix%','%Micron%',
  '%AWS%','%Azure%','%Google Cloud%'
]) ORDER BY "Name";

SELECT "Id","Name" FROM public."Commodities" ORDER BY "Id" LIMIT 50;

-- ============================================================
-- STEP 1: SEED NEW COMPANIES
-- ============================================================
BEGIN;

-- AI FRONTIER LABS
INSERT INTO public."Companies" ("Id","Name","Ticker","SystemicImportanceLevel","IsChokepoint","SoftwareDependencyScore","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Palantir Technologies','PLTR','High',false,85,1
FROM public."Companies" WHERE NOT EXISTS (SELECT 1 FROM public."Companies" WHERE "Name"='Palantir Technologies');

INSERT INTO public."Companies" ("Id","Name","Ticker","SystemicImportanceLevel","IsChokepoint","SoftwareDependencyScore","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'xAI',NULL,'High',false,75,1
FROM public."Companies" WHERE NOT EXISTS (SELECT 1 FROM public."Companies" WHERE "Name"='xAI');

INSERT INTO public."Companies" ("Id","Name","Ticker","SystemicImportanceLevel","IsChokepoint","SoftwareDependencyScore","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Mistral AI',NULL,'Medium',false,60,30
FROM public."Companies" WHERE NOT EXISTS (SELECT 1 FROM public."Companies" WHERE "Name"='Mistral AI');

INSERT INTO public."Companies" ("Id","Name","Ticker","SystemicImportanceLevel","IsChokepoint","SoftwareDependencyScore","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Cohere',NULL,'Medium',false,55,28
FROM public."Companies" WHERE NOT EXISTS (SELECT 1 FROM public."Companies" WHERE "Name"='Cohere');

-- CLOUD INFRASTRUCTURE
INSERT INTO public."Companies" ("Id","Name","Ticker","SystemicImportanceLevel","IsChokepoint","SoftwareDependencyScore","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Amazon Web Services',NULL,'Critical',true,95,1
FROM public."Companies" WHERE NOT EXISTS (SELECT 1 FROM public."Companies" WHERE "Name"='Amazon Web Services');

INSERT INTO public."Companies" ("Id","Name","Ticker","SystemicImportanceLevel","IsChokepoint","SoftwareDependencyScore","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Microsoft Azure',NULL,'Critical',true,95,1
FROM public."Companies" WHERE NOT EXISTS (SELECT 1 FROM public."Companies" WHERE "Name"='Microsoft Azure');

INSERT INTO public."Companies" ("Id","Name","Ticker","SystemicImportanceLevel","IsChokepoint","SoftwareDependencyScore","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Google Cloud',NULL,'Critical',true,92,1
FROM public."Companies" WHERE NOT EXISTS (SELECT 1 FROM public."Companies" WHERE "Name"='Google Cloud');

-- CHIP ECOSYSTEM (missing nodes)
INSERT INTO public."Companies" ("Id","Name","Ticker","SystemicImportanceLevel","IsChokepoint","SoftwareDependencyScore","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'AMD','AMD','High',false,70,1
FROM public."Companies" WHERE NOT EXISTS (SELECT 1 FROM public."Companies" WHERE "Ticker"='AMD');

INSERT INTO public."Companies" ("Id","Name","Ticker","SystemicImportanceLevel","IsChokepoint","SoftwareDependencyScore","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Arm Holdings','ARM','High',true,88,28
FROM public."Companies" WHERE NOT EXISTS (SELECT 1 FROM public."Companies" WHERE "Ticker"='ARM');

INSERT INTO public."Companies" ("Id","Name","Ticker","SystemicImportanceLevel","IsChokepoint","SoftwareDependencyScore","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'SK Hynix','000660.KS','High',true,80,74
FROM public."Companies" WHERE NOT EXISTS (SELECT 1 FROM public."Companies" WHERE "Name"='SK Hynix');

INSERT INTO public."Companies" ("Id","Name","Ticker","SystemicImportanceLevel","IsChokepoint","SoftwareDependencyScore","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Micron Technology','MU','High',false,72,1
FROM public."Companies" WHERE NOT EXISTS (SELECT 1 FROM public."Companies" WHERE "Ticker"='MU');

COMMIT;

-- VERIFY new companies
SELECT "Id","Name","Ticker","SystemicImportanceLevel","SoftwareDependencyScore"
FROM public."Companies"
WHERE "Name" IN (
  'Palantir Technologies','xAI','Mistral AI','Cohere',
  'Amazon Web Services','Microsoft Azure','Google Cloud',
  'AMD','Arm Holdings','SK Hynix','Micron Technology'
)
ORDER BY "Name";

-- ============================================================
-- STEP 2: SEED COMMODITIES
-- Run after confirming what already exists
-- ============================================================
BEGIN;

-- Energy commodities
INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Crude Oil (Brent)','barrel',true,NULL
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name" ILIKE '%Brent%');

INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Natural Gas','MMBtu',true,NULL
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name"='Natural Gas');

INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'LNG','MMBtu',true,NULL
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name"='LNG');

-- Metals / Strategic materials
INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Gold','troy oz',true,NULL
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name"='Gold');

INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Copper','metric ton',true,NULL
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name"='Copper');

INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Lithium','metric ton',true,NULL
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name"='Lithium');

INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Rare Earth Elements','metric ton',true,148
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name" ILIKE '%Rare Earth%');

INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Silicon Wafers','unit',true,NULL
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name"='Silicon Wafers');

INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Uranium','kg',true,NULL
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name"='Uranium');

-- Agricultural
INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Wheat','metric ton',true,NULL
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name"='Wheat');

INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Corn','metric ton',false,NULL
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name"='Corn');

INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Phosphates','metric ton',true,85
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name"='Phosphates');

-- Digital/Crypto
INSERT INTO public."Commodities" ("Id","Name","Unit","IsStrategic","CountryId")
SELECT COALESCE(MAX("Id"),0)+1,'Bitcoin','BTC',true,NULL
FROM public."Commodities" WHERE NOT EXISTS (SELECT 1 FROM public."Commodities" WHERE "Name"='Bitcoin');

COMMIT;

-- VERIFY commodities
SELECT "Id","Name","Unit","IsStrategic" FROM public."Commodities" ORDER BY "Id";
