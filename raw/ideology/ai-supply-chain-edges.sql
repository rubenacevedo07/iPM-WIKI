-- ============================================================
-- RelationEdge SEED — AI Supply Chain Complete
-- Run AFTER ai-supply-chain-complete-seed.sql Step 1
-- Replace IDs below with actual values from VERIFY query
-- ============================================================

-- KNOWN IDs (confirmed):
-- NVIDIA=1, Microsoft=4, Amazon=5, Meta=6, Alphabet=3
-- OpenAI=198, Anthropic=197, TSMC=41, ASML=21, Samsung=43, Intel=85
-- Federal Reserve=240, Pentagon=243

-- GET IDs for new companies first:
SELECT "Id","Name" FROM public."Companies"
WHERE "Name" IN (
  'Palantir Technologies','xAI','Mistral AI','Cohere',
  'Amazon Web Services','Microsoft Azure','Google Cloud',
  'AMD','Arm Holdings','SK Hynix','Micron Technology'
) ORDER BY "Name";

-- ============================================================
-- Then replace [PLTR_ID], [AWS_ID], [AZURE_ID], [GCP_ID],
-- [AMD_ID], [ARM_ID], [HYNIX_ID], [MICRON_ID], [XAI_ID]
-- with actual IDs from query above before running
-- ============================================================

BEGIN;

-- ── LAYER 1: CHIP ECOSYSTEM COMPLETIONS ──────────────────────

-- NVIDIA → DependsOn → SK Hynix (HBM memory for H100/B100)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',1,'Company',[HYNIX_ID],'DependsOn','Critical',
  'NVIDIA H100/B100 requires SK Hynix HBM3 memory — CoWoS packaging bottleneck',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=1
  AND "TargetType"='Company' AND "TargetId"=[HYNIX_ID] AND "EdgeType"='DependsOn');

-- NVIDIA → DependsOn → Micron (HBM alternative)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',1,'Company',[MICRON_ID],'DependsOn','High',
  'NVIDIA uses Micron HBM as secondary memory supplier',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=1
  AND "TargetType"='Company' AND "TargetId"=[MICRON_ID] AND "EdgeType"='DependsOn');

-- Arm Holdings → Supplies → NVIDIA (chip architecture)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',[ARM_ID],'Company',1,'Supplies','High',
  'ARM architecture licenses used in NVIDIA Grace CPU and networking chips',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=[ARM_ID]
  AND "TargetType"='Company' AND "TargetId"=1 AND "EdgeType"='Supplies');

-- AMD → Competes → NVIDIA (AI GPU market)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',[AMD_ID],'Company',1,'Competes','High',
  'AMD MI300X/MI350 vs NVIDIA H100/B100 — AI accelerator market',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=[AMD_ID]
  AND "TargetType"='Company' AND "TargetId"=1 AND "EdgeType"='Competes');

-- ── LAYER 2: CLOUD → GPU DEPENDENCY ──────────────────────────

-- AWS → DependsOn → NVIDIA
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',[AWS_ID],'Company',1,'DependsOn','Critical',
  'AWS P4/P5 instances run NVIDIA H100/A100 — AI cloud infrastructure',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=[AWS_ID]
  AND "TargetType"='Company' AND "TargetId"=1 AND "EdgeType"='DependsOn');

-- Microsoft Azure → DependsOn → NVIDIA
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',[AZURE_ID],'Company',1,'DependsOn','Critical',
  'Azure NDv5 instances run NVIDIA H100 — OpenAI exclusive GPU allocation',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=[AZURE_ID]
  AND "TargetType"='Company' AND "TargetId"=1 AND "EdgeType"='DependsOn');

-- Google Cloud → DependsOn → NVIDIA + TPU (partial)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',[GCP_ID],'Company',1,'DependsOn','High',
  'Google Cloud A3 instances run NVIDIA H100 — also building TPU alternative',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=[GCP_ID]
  AND "TargetType"='Company' AND "TargetId"=1 AND "EdgeType"='DependsOn');

-- AWS → Owns → Amazon (parent)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',5,'Company',[AWS_ID],'Owns','Critical',
  'Amazon owns AWS — cloud subsidiary',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=5
  AND "TargetType"='Company' AND "TargetId"=[AWS_ID] AND "EdgeType"='Owns');

-- Microsoft → Owns → Azure
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',4,'Company',[AZURE_ID],'Owns','Critical',
  'Microsoft owns Azure cloud platform',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=4
  AND "TargetType"='Company' AND "TargetId"=[AZURE_ID] AND "EdgeType"='Owns');

-- Alphabet → Owns → Google Cloud
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',3,'Company',[GCP_ID],'Owns','Critical',
  'Alphabet owns Google Cloud platform',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=3
  AND "TargetType"='Company' AND "TargetId"=[GCP_ID] AND "EdgeType"='Owns');

-- ── LAYER 3: AI COMPANIES → CLOUD DEPENDENCY ─────────────────

-- OpenAI → DependsOn → Microsoft Azure (exclusive compute deal)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',198,'Company',[AZURE_ID],'DependsOn','Critical',
  'OpenAI runs entirely on Azure — $10B+ Microsoft compute deal',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=198
  AND "TargetType"='Company' AND "TargetId"=[AZURE_ID] AND "EdgeType"='DependsOn');

-- Microsoft → Finances → OpenAI ($13B investment)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',4,'Company',198,'Finances','Critical',
  'Microsoft $13B investment in OpenAI — 49% stake',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=4
  AND "TargetType"='Company' AND "TargetId"=198 AND "EdgeType"='Finances');

-- Anthropic → DependsOn → AWS (primary cloud + $4B Amazon investment)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',197,'Company',[AWS_ID],'DependsOn','Critical',
  'Anthropic primary cloud on AWS — Amazon $4B investment + Trainium chips',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=197
  AND "TargetType"='Company' AND "TargetId"=[AWS_ID] AND "EdgeType"='DependsOn');

-- Amazon → Finances → Anthropic
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',5,'Company',197,'Finances','Critical',
  'Amazon $4B investment in Anthropic — AWS preferred cloud + Alexa AI',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=5
  AND "TargetType"='Company' AND "TargetId"=197 AND "EdgeType"='Finances');

-- xAI → DependsOn → AWS + NVIDIA (100K H100 cluster)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',[XAI_ID],'Company',1,'DependsOn','Critical',
  'xAI Colossus cluster — 100K+ NVIDIA H100/H200 GPUs',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=[XAI_ID]
  AND "TargetType"='Company' AND "TargetId"=1 AND "EdgeType"='DependsOn');

-- Musk (7) → Governs → xAI
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Person',7,'Company',[XAI_ID],'Governs','Critical',
  'Musk founder and CEO of xAI',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Person' AND "SourceId"=7
  AND "TargetType"='Company' AND "TargetId"=[XAI_ID] AND "EdgeType"='Governs');

-- Sam Altman (61) → Governs → OpenAI
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Person',61,'Company',198,'Governs','Critical',
  'Sam Altman CEO OpenAI',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Person' AND "SourceId"=61
  AND "TargetType"='Company' AND "TargetId"=198 AND "EdgeType"='Governs');

-- Meta → DependsOn → NVIDIA (largest single GPU buyer)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',6,'Company',1,'DependsOn','Critical',
  'Meta largest single NVIDIA GPU buyer — 350K+ H100s for Llama training',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=6
  AND "TargetType"='Company' AND "TargetId"=1 AND "EdgeType"='DependsOn');

-- ── LAYER 4: PALANTIR CONNECTIONS ────────────────────────────

-- Palantir → Partners → Pentagon (largest customer)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',[PLTR_ID],'Company',243,'Partners','Critical',
  'Palantir Maven Smart System — DoD primary AI/data analytics contract',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=[PLTR_ID]
  AND "TargetType"='Company' AND "TargetId"=243 AND "EdgeType"='Partners');

-- Palantir → Partners → US Intelligence Community (CIA, NSA)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',[PLTR_ID],'Country',1,'Partners','Critical',
  'Palantir Gotham — CIA, NSA, US intelligence community primary analytics platform',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=[PLTR_ID]
  AND "TargetType"='Country' AND "TargetId"=1
  AND "EdgeType"='Partners' AND "Label" ILIKE '%CIA%');

-- Palantir → Partners → Ukraine (battlefield AI)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',[PLTR_ID],'Country',65,'Partners','High',
  'Palantir providing AI targeting and logistics to Ukraine military',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=[PLTR_ID]
  AND "TargetType"='Country' AND "TargetId"=65 AND "EdgeType"='Partners');

-- Palantir → DependsOn → AWS (runs on cloud)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',[PLTR_ID],'Company',[AWS_ID],'DependsOn','High',
  'Palantir AIP runs on AWS and Azure cloud infrastructure',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=[PLTR_ID]
  AND "TargetType"='Company' AND "TargetId"=[AWS_ID] AND "EdgeType"='DependsOn');

-- Palantir → DependsOn → NVIDIA (GPU compute for AI platform)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',[PLTR_ID],'Company',1,'DependsOn','High',
  'Palantir AIP uses NVIDIA GPUs for AI inference and analytics',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=[PLTR_ID]
  AND "TargetType"='Company' AND "TargetId"=1 AND "EdgeType"='DependsOn');

-- Palantir → Competes → Anthropic/OpenAI (enterprise AI)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',[PLTR_ID],'Company',197,'Competes','Medium',
  'Palantir AIP vs Anthropic Claude for enterprise/government AI deployment',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=[PLTR_ID]
  AND "TargetType"='Company' AND "TargetId"=197 AND "EdgeType"='Competes');

COMMIT;

-- VERIFY all new edges
SELECT re."Id", re."SourceType", re."SourceId",
  CASE re."SourceType"
    WHEN 'Company' THEN (SELECT "Name" FROM public."Companies" WHERE "Id"=re."SourceId")
    WHEN 'Person'  THEN (SELECT "Name" FROM public."Persons"  WHERE "Id"=re."SourceId")
  END AS source_name,
  re."TargetType", re."TargetId",
  CASE re."TargetType"
    WHEN 'Company' THEN (SELECT "Name" FROM public."Companies" WHERE "Id"=re."TargetId")
    WHEN 'Country' THEN (SELECT "Name" FROM public."Countries" WHERE "Id"=re."TargetId")
  END AS target_name,
  re."EdgeType", re."Strength"
FROM public."RelationEdge" re
WHERE re."Id" > 1246  -- new edges only
AND re."IsDeleted"=false
ORDER BY re."Id";
