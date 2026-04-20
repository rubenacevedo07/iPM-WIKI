-- ============================================================
-- RelationEdge SEED — Institutional connections
-- Federal Reserve(240), ECB(241), Treasury(242), Pentagon(243)
-- Wall Street(244), IMF(245), BIS(246), NATO(247)
-- ============================================================

-- STEP 1: Check current max RelationEdge Id
SELECT COALESCE(MAX("Id"),0)+1 AS next_id FROM public."RelationEdge";

-- STEP 2: Verify institution company rows exist
SELECT "Id","Name" FROM public."Companies"
WHERE "Id" IN (240,241,242,243,244,245,246,247)
ORDER BY "Id";

-- STEP 3: INSERT key institutional edges
BEGIN;

-- Powell (192) → Sets → Federal Reserve (240)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Person',192,'Company',240,'Sets','Critical',
  'Powell Sets Fed monetary policy',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Person' AND "SourceId"=192
  AND "TargetType"='Company' AND "TargetId"=240 AND "EdgeType"='Sets');

-- Lagarde (191) → Sets → ECB (241)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Person',191,'Company',241,'Sets','Critical',
  'Lagarde Sets ECB monetary policy',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Person' AND "SourceId"=191
  AND "TargetType"='Company' AND "TargetId"=241 AND "EdgeType"='Sets');

-- Bessent (545) → Governs → US Treasury (242)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Person',545,'Company',242,'Governs','Critical',
  'Bessent Secretary of Treasury',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Person' AND "SourceId"=545
  AND "TargetType"='Company' AND "TargetId"=242 AND "EdgeType"='Governs');

-- Trump (173) → Governs → Pentagon (243)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Person',173,'Company',243,'Governs','Critical',
  'Trump Commander in Chief → Pentagon',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Person' AND "SourceId"=173
  AND "TargetType"='Company' AND "TargetId"=243 AND "EdgeType"='Governs');

-- Federal Reserve (240) → Sets → USA financial conditions (Country 1)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',240,'Country',1,'Sets','Critical',
  'Fed Sets US monetary conditions',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=240
  AND "TargetType"='Country' AND "TargetId"=1 AND "EdgeType"='Sets');

-- Federal Reserve (240) → Influences → Wall Street (244)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',240,'Company',244,'Influences','Critical',
  'Fed rate policy drives Wall Street risk pricing',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=240
  AND "TargetType"='Company' AND "TargetId"=244 AND "EdgeType"='Influences');

-- US Treasury (242) → Sanctions → Russia (Country 64)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',242,'Country',64,'Sanctions','Critical',
  'OFAC/Treasury Russia sanctions regime',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=242
  AND "TargetType"='Country' AND "TargetId"=64 AND "EdgeType"='Sanctions');

-- US Treasury (242) → Sanctions → Iran (Country 72)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',242,'Country',72,'Sanctions','Critical',
  'OFAC/Treasury Iran comprehensive sanctions',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=242
  AND "TargetType"='Country' AND "TargetId"=72 AND "EdgeType"='Sanctions');

-- Pentagon (243) → Governs → USA military power (Country 1)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',243,'Country',1,'Governs','Critical',
  'Pentagon directs US military forces',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=243
  AND "TargetType"='Country' AND "TargetId"=1 AND "EdgeType"='Governs');

-- Pentagon (243) → Finances → Lockheed Martin (Company 68)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',243,'Company',68,'Finances','Critical',
  'Pentagon largest Lockheed customer — F-35, THAAD, HIMARS',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=243
  AND "TargetType"='Company' AND "TargetId"=68 AND "EdgeType"='Finances');

-- Fink (75) → Governs → Wall Street (244)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Person',75,'Company',244,'Influences','High',
  'Fink BlackRock CEO — largest single Wall Street influence',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Person' AND "SourceId"=75
  AND "TargetType"='Company' AND "TargetId"=244 AND "EdgeType"='Influences');

-- ECB (241) → Sets → EU monetary conditions (Germany=29 as proxy)
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',241,'Country',29,'Sets','Critical',
  'ECB Sets eurozone monetary conditions',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=241
  AND "TargetType"='Country' AND "TargetId"=29 AND "EdgeType"='Sets');

-- IMF (245) → Regulates → Global financial stability
INSERT INTO public."RelationEdge"
  ("Id","SourceType","SourceId","TargetType","TargetId","EdgeType","Strength","Label","IsVerified","IsDeleted")
SELECT COALESCE(MAX("Id"),0)+1,'Company',245,'Company',240,'Partners','High',
  'IMF-Fed coordination on global financial stability',true,false
FROM public."RelationEdge"
WHERE NOT EXISTS (SELECT 1 FROM public."RelationEdge"
  WHERE "SourceType"='Company' AND "SourceId"=245
  AND "TargetType"='Company' AND "TargetId"=240 AND "EdgeType"='Partners');

COMMIT;

-- VERIFY — count new edges and show them
SELECT
  re."Id",
  re."SourceType", re."SourceId",
  re."TargetType", re."TargetId",
  re."EdgeType", re."Strength", re."Label"
FROM public."RelationEdge" re
WHERE (
  (re."SourceType"='Company' AND re."SourceId" IN (240,241,242,243,244,245,246,247))
  OR (re."TargetType"='Company' AND re."TargetId" IN (240,241,242,243,244,245,246,247))
  OR (re."SourceType"='Person' AND re."SourceId" IN (191,192,545,173,75)
      AND re."TargetType"='Company' AND re."TargetId" IN (240,241,242,243,244))
)
AND re."IsDeleted"=false
ORDER BY re."Id";
