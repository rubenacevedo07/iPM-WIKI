-- ============================================================
-- PowerMapRelation SEED — Semiconductor PowerMap (ID=4)
-- Closes: CL-DB-005
-- Run in pgAdmin against Railway PostgreSQL
-- ============================================================

-- STEP 1: See what nodes exist on PowerMap 4
-- Run this first and paste results back
SELECT
    pmn."Id"       AS node_id,
    pmn."NodeType",
    pmn."NodeId",
    CASE pmn."NodeType"
        WHEN 'Company' THEN (SELECT "Name" FROM public."Companies" WHERE "Id" = pmn."NodeId")
        WHEN 'Person'  THEN (SELECT "Name" FROM public."Persons"  WHERE "Id" = pmn."NodeId")
        WHEN 'Country' THEN (SELECT "Name" FROM public."Countries" WHERE "Id" = pmn."NodeId")
    END AS entity_name
FROM public."PowerMapNode" pmn
WHERE pmn."PowerMapId" = 4
ORDER BY pmn."NodeType", pmn."NodeId";

-- STEP 2: Find canonical RelationEdge IDs for semiconductor edges
-- (NVIDIA=1, ASML=21, TSMC=41, Samsung=43, Intel=85)
SELECT
    re."Id"         AS edge_id,
    re."SourceType",
    re."SourceId",
    re."TargetType",
    re."TargetId",
    re."EdgeType",
    re."Strength",
    re."Label"
FROM public."RelationEdge" re
WHERE (
    (re."SourceType" = 'Company' AND re."SourceId" IN (1,21,41,43,85))
    OR
    (re."TargetType" = 'Company' AND re."TargetId" IN (1,21,41,43,85))
)
AND re."IsDeleted" = false
ORDER BY re."SourceId", re."TargetId";

-- STEP 3: Check current PowerMapRelation state (should be 0)
SELECT COUNT(*) AS existing_relations
FROM public."PowerMapRelation" pmr
JOIN public."PowerMapNode" pmn ON pmn."Id" = pmr."SourceNodeId"
WHERE pmn."PowerMapId" = 4;

-- ============================================================
-- STEP 4: INSERT PowerMapRelation rows
-- Run AFTER confirming node_ids from Step 1 and edge_ids from Step 2
-- Replace node_id values below with actual IDs from Step 1 output
-- ============================================================

-- Template — replace [SOURCE_NODE_ID], [TARGET_NODE_ID], [EDGE_ID]
-- with actual values from steps above:

/*
BEGIN;

-- Edge 1: TSMC → Supplies → NVIDIA (DependsOn/Supplies relationship)
INSERT INTO public."PowerMapRelation"
    ("Id", "PowerMapId", "RelationEdgeId", "SourceNodeId", "TargetNodeId",
     "IsUserDrawn", "CustomLabel", "CreatedAt")
SELECT
    COALESCE(MAX("Id"),0)+1,
    4,
    [RELATEDGE_ID_TSMC_NVIDIA],
    [POWERMAP_NODE_ID_TSMC],
    [POWERMAP_NODE_ID_NVIDIA],
    false,
    'TSMC → Manufactures → NVIDIA GPUs',
    now()
FROM public."PowerMapRelation";

-- Edge 2: ASML → Supplies → TSMC (EUV lithography)
INSERT INTO public."PowerMapRelation"
    ("Id", "PowerMapId", "RelationEdgeId", "SourceNodeId", "TargetNodeId",
     "IsUserDrawn", "CustomLabel", "CreatedAt")
SELECT
    COALESCE(MAX("Id"),0)+1,
    4,
    [RELATEDGE_ID_ASML_TSMC],
    [POWERMAP_NODE_ID_ASML],
    [POWERMAP_NODE_ID_TSMC],
    false,
    'ASML → Supplies EUV → TSMC',
    now()
FROM public."PowerMapRelation";

-- Edge 3: NVIDIA → DependsOn → TSMC
INSERT INTO public."PowerMapRelation"
    ("Id", "PowerMapId", "RelationEdgeId", "SourceNodeId", "TargetNodeId",
     "IsUserDrawn", "CustomLabel", "CreatedAt")
SELECT
    COALESCE(MAX("Id"),0)+1,
    4,
    [RELATEDGE_ID_NVIDIA_TSMC],
    [POWERMAP_NODE_ID_NVIDIA],
    [POWERMAP_NODE_ID_TSMC],
    false,
    'NVIDIA → DependsOn → TSMC (critical)',
    now()
FROM public."PowerMapRelation";

COMMIT;
*/

-- ============================================================
-- STEP 5: If RelationEdge rows for TSMC↔NVIDIA etc DON'T EXIST
-- in Step 2 results, create them first:
-- ============================================================

/*
BEGIN;

-- NVIDIA → DependsOn → TSMC (if missing)
INSERT INTO public."RelationEdge"
    ("Id", "SourceType", "SourceId", "TargetType", "TargetId",
     "EdgeType", "Strength", "Label", "Description", "IsVerified", "IsDeleted")
SELECT
    COALESCE(MAX("Id"),0)+1,
    'Company', 1,
    'Company', 41,
    'DependsOn', 'Critical',
    'NVIDIA → DependsOn → TSMC',
    'NVIDIA fabless — 100% dependent on TSMC for leading-edge GPU production (N4/N3 nodes). SubstitutionLatencyMonths=36+.',
    true, false
FROM public."RelationEdge"
WHERE NOT EXISTS (
    SELECT 1 FROM public."RelationEdge"
    WHERE "SourceType"='Company' AND "SourceId"=1
      AND "TargetType"='Company' AND "TargetId"=41
      AND "EdgeType"='DependsOn'
);

-- ASML → Supplies → TSMC (if missing)
INSERT INTO public."RelationEdge"
    ("Id", "SourceType", "SourceId", "TargetType", "TargetId",
     "EdgeType", "Strength", "Label", "Description", "IsVerified", "IsDeleted")
SELECT
    COALESCE(MAX("Id"),0)+1,
    'Company', 21,
    'Company', 41,
    'Supplies', 'Critical',
    'ASML → Supplies EUV → TSMC',
    'ASML sole supplier of EUV lithography machines. No EUV = no sub-7nm chips. SubstitutionLatencyMonths=120.',
    true, false
FROM public."RelationEdge"
WHERE NOT EXISTS (
    SELECT 1 FROM public."RelationEdge"
    WHERE "SourceType"='Company' AND "SourceId"=21
      AND "TargetType"='Company' AND "TargetId"=41
      AND "EdgeType"='Supplies'
);

-- TSMC → Manufactures → NVIDIA (if missing)
INSERT INTO public."RelationEdge"
    ("Id", "SourceType", "SourceId", "TargetType", "TargetId",
     "EdgeType", "Strength", "Label", "Description", "IsVerified", "IsDeleted")
SELECT
    COALESCE(MAX("Id"),0)+1,
    'Company', 41,
    'Company', 1,
    'Manufactures', 'Critical',
    'TSMC → Manufactures → NVIDIA H100/B100',
    'TSMC N4/N3 nodes produce NVIDIA AI GPUs. CoWoS packaging also TSMC. Total NVIDIA dependency on TSMC is existential.',
    true, false
FROM public."RelationEdge"
WHERE NOT EXISTS (
    SELECT 1 FROM public."RelationEdge"
    WHERE "SourceType"='Company' AND "SourceId"=41
      AND "TargetType"='Company' AND "TargetId"=1
      AND "EdgeType"='Manufactures'
);

-- Taiwan → Governs → TSMC (country context)
INSERT INTO public."RelationEdge"
    ("Id", "SourceType", "SourceId", "TargetType", "TargetId",
     "EdgeType", "Strength", "Label", "Description", "IsVerified", "IsDeleted")
SELECT
    COALESCE(MAX("Id"),0)+1,
    'Country', 151,
    'Company', 41,
    'Governs', 'Critical',
    'Taiwan → Governs → TSMC',
    'TSMC HQ in Hsinchu, Taiwan. Taiwan Strait conflict = existential risk to global AI supply chain.',
    true, false
FROM public."RelationEdge"
WHERE NOT EXISTS (
    SELECT 1 FROM public."RelationEdge"
    WHERE "SourceType"='Country' AND "SourceId"=151
      AND "TargetType"='Company' AND "TargetId"=41
      AND "EdgeType"='Governs'
);

-- USA → Regulates → NVIDIA (export controls)
INSERT INTO public."RelationEdge"
    ("Id", "SourceType", "SourceId", "TargetType", "TargetId",
     "EdgeType", "Strength", "Label", "Description", "IsVerified", "IsDeleted")
SELECT
    COALESCE(MAX("Id"),0)+1,
    'Country', 1,
    'Company', 1,
    'Regulates', 'High',
    'USA → Regulates → NVIDIA (export controls)',
    'BIS export controls restrict NVIDIA GPU exports to China. US determines NVIDIA China addressable market.',
    true, false
FROM public."RelationEdge"
WHERE NOT EXISTS (
    SELECT 1 FROM public."RelationEdge"
    WHERE "SourceType"='Country' AND "SourceId"=1
      AND "TargetType"='Company' AND "TargetId"=1
      AND "EdgeType"='Regulates'
);

COMMIT;
*/

-- ============================================================
-- VERIFICATION after all steps complete:
-- ============================================================
SELECT
    pmr."Id",
    pmr."CustomLabel",
    src_entity.name AS source_entity,
    tgt_entity.name AS target_entity,
    re."EdgeType",
    re."Strength"
FROM public."PowerMapRelation" pmr
JOIN public."PowerMapNode" src_pmn ON src_pmn."Id" = pmr."SourceNodeId"
JOIN public."PowerMapNode" tgt_pmn ON tgt_pmn."Id" = pmr."TargetNodeId"
JOIN public."RelationEdge" re ON re."Id" = pmr."RelationEdgeId"
JOIN LATERAL (
    SELECT CASE src_pmn."NodeType"
        WHEN 'Company' THEN (SELECT "Name" FROM public."Companies" WHERE "Id"=src_pmn."NodeId")
        WHEN 'Country' THEN (SELECT "Name" FROM public."Countries" WHERE "Id"=src_pmn."NodeId")
        WHEN 'Person'  THEN (SELECT "Name" FROM public."Persons"  WHERE "Id"=src_pmn."NodeId")
    END AS name
) src_entity ON true
JOIN LATERAL (
    SELECT CASE tgt_pmn."NodeType"
        WHEN 'Company' THEN (SELECT "Name" FROM public."Companies" WHERE "Id"=tgt_pmn."NodeId")
        WHEN 'Country' THEN (SELECT "Name" FROM public."Countries" WHERE "Id"=tgt_pmn."NodeId")
        WHEN 'Person'  THEN (SELECT "Name" FROM public."Persons"  WHERE "Id"=tgt_pmn."NodeId")
    END AS name
) tgt_entity ON true
WHERE src_pmn."PowerMapId" = 4
ORDER BY pmr."Id";
