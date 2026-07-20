



-- count edges
-- 1,116,058 edges with UMLS/NCIT
SELECT
    count(edge_id)
FROM comb_edge_node ed
JOIN comb_node_ontology so ON ed.source_node_id = so.id
JOIN comb_node_ontology ta ON ed.target_node_id = ta.id
JOIN comb_lookup_type ted ON ed.edge_type_id   = ted.type_id
JOIN comb_lookup_type tso ON so.node_type_id   = tso.type_id
JOIN comb_lookup_type tta ON ta.node_type_id   = tta.type_id
JOIN comb_lookup_type sco_type ON ed.score_type_id = sco_type.type_id
WHERE ed.study_id = 1;

-- 922,724 edges w/o UMLS/NCIT
SELECT
    count(edge_id)
FROM comb_edge_node ed
JOIN comb_node_ontology so ON ed.source_node_id = so.id
JOIN comb_node_ontology ta ON ed.target_node_id = ta.id
JOIN comb_lookup_type ted ON ed.edge_type_id   = ted.type_id
JOIN comb_lookup_type tso ON so.node_type_id   = tso.type_id
JOIN comb_lookup_type tta ON ta.node_type_id   = tta.type_id
JOIN comb_ontology_type oso ON so.ontology_type_id   = oso.ontology_id
JOIN comb_ontology_type ota ON ta.ontology_type_id   = ota.ontology_id
JOIN comb_lookup_type sco_type ON ed.score_type_id = sco_type.type_id
WHERE ed.study_id = 1 and oso.ontology_id not in (5, 7) and ota.ontology_id not in (5, 7);



-- count edges by type of relationships by ontology
SELECT
    count(edge_id), oso.ontology_id, oso.ontology_name, ota.ontology_id, ota.ontology_name
FROM comb_edge_node ed
JOIN comb_node_ontology so ON ed.source_node_id = so.id
JOIN comb_node_ontology ta ON ed.target_node_id = ta.id
JOIN comb_lookup_type ted ON ed.edge_type_id   = ted.type_id
JOIN comb_lookup_type tso ON so.node_type_id   = tso.type_id
JOIN comb_lookup_type tta ON ta.node_type_id   = tta.type_id
JOIN comb_ontology_type oso ON so.ontology_type_id   = oso.ontology_id
JOIN comb_ontology_type ota ON ta.ontology_type_id   = ota.ontology_id
JOIN comb_lookup_type sco_type ON ed.score_type_id = sco_type.type_id
WHERE ed.study_id = 1 and oso.ontology_id not in (5, 7) and ota.ontology_id not in (5, 7)
GROUP BY oso.ontology_id, oso.ontology_name, ota.ontology_id, ota.ontology_name;




SELECT
    CONCAT(ed.edge_id, so.ontology_id, ta.ontology_id) AS edge_id,
    so.ontology_id  AS subject_id,
    ta.ontology_id  AS object_id,
    ed.score        AS score,
    sco_type.type_name AS score_type,
    so.node_name    AS subject_name,
    ta.node_name    AS object_name,
    ted.type_name   AS predicate,
    tso.type_name   AS subject_category,
    tta.type_name   AS object_category,
    ed.study_id     AS study_id,
    ed.publication_ids AS publication_ids,
    ed.score_translator AS score_translator,
    ed.id           AS internal_id
FROM comb_edge_node ed
JOIN comb_node_ontology so ON ed.source_node_id = so.id
JOIN comb_node_ontology ta ON ed.target_node_id = ta.id
JOIN comb_lookup_type ted ON ed.edge_type_id   = ted.type_id
JOIN comb_lookup_type tso ON so.node_type_id   = tso.type_id
JOIN comb_lookup_type tta ON ta.node_type_id   = tta.type_id
JOIN comb_lookup_type sco_type ON ed.score_type_id = sco_type.type_id
WHERE ed.study_id = 1;




-- all data
-- +----------------+
-- | count(edge_id) |
-- +----------------+
-- |        1116058 |
-- +----------------+
-- 1 row in set (7.02 sec)


-- taking out UMLS
