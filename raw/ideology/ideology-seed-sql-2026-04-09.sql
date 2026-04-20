-- ============================================================
-- IdeologyProfile SEED — 9 actors
-- Generated: 2026-04-09 | Source: Knowledge-based scoring
-- Confidence: 70-85% — pending Perplexity source verification
-- Run in pgAdmin against Railway PostgreSQL
-- ============================================================
-- FIRST: verify these EntityIds exist in Persons table
SELECT "Id", "Name", "LastName"
FROM public."Persons"
WHERE "Id" IN (171, 176, 75, 545, 1, 67, 61)
ORDER BY "Id";
-- Note: Modi and Yellen IDs are TBD — seed after confirming their Persons.Id

-- CHECK: existing IdeologyProfile rows to avoid duplicates
SELECT "EntityId", "LabelPrimary"
FROM public."IdeologyProfile"
WHERE "EntityType" = 'PERSON'
  AND "EntityId" IN (171, 176, 75, 545, 1, 67, 61)
ORDER BY "EntityId";

-- INSERT: 7 actors with confirmed DB IDs
BEGIN;

INSERT INTO public."IdeologyProfile"
  ("Id", "EntityType", "EntityId", "EconScore", "AuthScore", "CulturalScore",
   "GenderScore", "GeoScore", "EnvScore", "ReligionScore",
   "LabelPrimary", "Confidence", "ValidFrom", "Notes")
SELECT
  COALESCE(MAX("Id"),0)+1,
  'PERSON', 171,
  2.0, 9.0, 7.0, 6.0, 3.0, -3.0, -5.0,
  'CCP nationalist authoritarian', 80,
  '2026-04-09'::date,
  'Knowledge-based scoring from public record. Pending Perplexity source verification.'
FROM public."IdeologyProfile"
WHERE NOT EXISTS (
  SELECT 1 FROM public."IdeologyProfile"
  WHERE "EntityType"='PERSON' AND "EntityId"=171
);

INSERT INTO public."IdeologyProfile"
  ("Id", "EntityType", "EntityId", "EconScore", "AuthScore", "CulturalScore",
   "GenderScore", "GeoScore", "EnvScore", "ReligionScore",
   "LabelPrimary", "Confidence", "ValidFrom", "Notes")
SELECT
  COALESCE(MAX("Id"),0)+1,
  'PERSON', 176,
  4.0, 8.5, 5.0, 3.0, 2.0, 6.0, 4.0,
  'Modernising authoritarian', 75,
  '2026-04-09'::date,
  'Knowledge-based scoring from public record.'
FROM public."IdeologyProfile"
WHERE NOT EXISTS (
  SELECT 1 FROM public."IdeologyProfile"
  WHERE "EntityType"='PERSON' AND "EntityId"=176
);

INSERT INTO public."IdeologyProfile"
  ("Id", "EntityType", "EntityId", "EconScore", "AuthScore", "CulturalScore",
   "GenderScore", "GeoScore", "EnvScore", "ReligionScore",
   "LabelPrimary", "Confidence", "ValidFrom", "Notes")
SELECT
  COALESCE(MAX("Id"),0)+1,
  'PERSON', 75,
  3.0, -2.0, -1.0, -2.0, 5.0, -4.0, -1.0,
  'Liberal financial multilateralist', 80,
  '2026-04-09'::date,
  'Knowledge-based scoring from public record.'
FROM public."IdeologyProfile"
WHERE NOT EXISTS (
  SELECT 1 FROM public."IdeologyProfile"
  WHERE "EntityType"='PERSON' AND "EntityId"=75
);

INSERT INTO public."IdeologyProfile"
  ("Id", "EntityType", "EntityId", "EconScore", "AuthScore", "CulturalScore",
   "GenderScore", "GeoScore", "EnvScore", "ReligionScore",
   "LabelPrimary", "Confidence", "ValidFrom", "Notes")
SELECT
  COALESCE(MAX("Id"),0)+1,
  'PERSON', 545,
  6.0, 1.0, 4.0, 2.0, -1.0, 4.0, 1.0,
  'Fiscal hawk nationalist', 70,
  '2026-04-09'::date,
  'Knowledge-based scoring from public record.'
FROM public."IdeologyProfile"
WHERE NOT EXISTS (
  SELECT 1 FROM public."IdeologyProfile"
  WHERE "EntityType"='PERSON' AND "EntityId"=545
);

INSERT INTO public."IdeologyProfile"
  ("Id", "EntityType", "EntityId", "EconScore", "AuthScore", "CulturalScore",
   "GenderScore", "GeoScore", "EnvScore", "ReligionScore",
   "LabelPrimary", "Confidence", "ValidFrom", "Notes")
SELECT
  COALESCE(MAX("Id"),0)+1,
  'PERSON', 1,
  5.0, -3.0, -2.0, -1.0, 4.0, -1.0, -2.0,
  'Techno-optimist multilateralist', 75,
  '2026-04-09'::date,
  'Knowledge-based scoring from public record.'
FROM public."IdeologyProfile"
WHERE NOT EXISTS (
  SELECT 1 FROM public."IdeologyProfile"
  WHERE "EntityType"='PERSON' AND "EntityId"=1
);

INSERT INTO public."IdeologyProfile"
  ("Id", "EntityType", "EntityId", "EconScore", "AuthScore", "CulturalScore",
   "GenderScore", "GeoScore", "EnvScore", "ReligionScore",
   "LabelPrimary", "Confidence", "ValidFrom", "Notes")
SELECT
  COALESCE(MAX("Id"),0)+1,
  'PERSON', 67,
  1.0, -4.0, -3.0, -3.0, 7.0, -6.0, -3.0,
  'Techno-philanthropic multilateralist', 85,
  '2026-04-09'::date,
  'Knowledge-based scoring from public record.'
FROM public."IdeologyProfile"
WHERE NOT EXISTS (
  SELECT 1 FROM public."IdeologyProfile"
  WHERE "EntityType"='PERSON' AND "EntityId"=67
);

INSERT INTO public."IdeologyProfile"
  ("Id", "EntityType", "EntityId", "EconScore", "AuthScore", "CulturalScore",
   "GenderScore", "GeoScore", "EnvScore", "ReligionScore",
   "LabelPrimary", "Confidence", "ValidFrom", "Notes")
SELECT
  COALESCE(MAX("Id"),0)+1,
  'PERSON', 61,
  4.0, -3.0, -2.0, -2.0, 3.0, -1.0, -2.0,
  'AI accelerationist techno-optimist', 70,
  '2026-04-09'::date,
  'Knowledge-based scoring from public record.'
FROM public."IdeologyProfile"
WHERE NOT EXISTS (
  SELECT 1 FROM public."IdeologyProfile"
  WHERE "EntityType"='PERSON' AND "EntityId"=61
);

COMMIT;

-- VERIFY
SELECT
  p."Name" || ' ' || COALESCE(p."LastName",'') AS person,
  ip."EconScore", ip."AuthScore", ip."GeoScore", ip."EnvScore",
  ip."LabelPrimary", ip."Confidence"
FROM public."IdeologyProfile" ip
JOIN public."Persons" p ON p."Id" = ip."EntityId"
WHERE ip."EntityType" = 'PERSON'
  AND ip."EntityId" IN (171, 176, 75, 545, 1, 67, 61, 173, 192, 191, 7)
ORDER BY ip."AuthScore" DESC;

-- NOTE: Modi and Yellen require PersonId lookup first:
-- SELECT "Id", "Name", "LastName" FROM public."Persons"
-- WHERE "Name" ILIKE '%Modi%' OR "Name" ILIKE '%Yellen%';
-- Then run separate INSERTs with confirmed IDs.
