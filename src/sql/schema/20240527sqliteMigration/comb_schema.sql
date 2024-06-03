

-- add in table to link node codes (PPARG/BMI) to onltology ids returned to API queries
drop table if exists comb_node_ontology;
create table comb_node_ontology (
  id                        INTEGER PRIMARY KEY,
  node_code                 TEXT not null,
  node_type_id              INTEGER not null,
  ontology_id               TEXT not null,
  ontology_type_id          INTEGER,
  node_name                 TEXT,
  added_by_study_id         INTEGER,
  created_at                DATE DEFAULT (DATE('now', 'localtime'))
);
-- -- indices
CREATE INDEX node_ont_node_cde_idx ON comb_node_ontology (node_code);
CREATE INDEX node_ont_node_typ_idx ON comb_node_ontology (node_type_id);
CREATE INDEX node_ont_ont_idx ON comb_node_ontology (ontology_id);

-- alter table comb_node_ontology add index node_ont_node_cde_idx (node_code);
-- alter table comb_node_ontology add index node_ont_node_typ_idx (node_type_id);
-- alter table comb_node_ontology add index node_ont_ont_idx (ontology_id);

-- add a combined node-0edge-node tables
drop table if exists comb_edge_node;
create table comb_edge_node (
  id                        INTEGER PRIMARY KEY,
  edge_id                   TEXT not null,
  source_node_id            INTEGER not null,
  target_node_id            INTEGER not null,
  edge_type_id              INTEGER not null,
  score                     REAL,
  score_text                TEXT,
  score_type_id             INTEGER,
  study_id                  INTEGER not null,
  study_secondary_id        INTEGER,
  publication_ids           TEXT,
  annotation                TEXT,
  score_translator              REAL,
  p_value                       REAL,
  beta                          REAL,
  standard_error                REAL,
  probability                   REAL,
  probability_app_bayes_factor  REAL,
  enrichment                    REAL,
  created_at                DATE DEFAULT (DATE('now', 'localtime'))
);

-- indices
CREATE INDEX comb_edg_nod_src_idx ON comb_edge_node (source_node_id);
CREATE INDEX comb_edg_nod_tgt_idx ON comb_edge_node (target_node_id);
-- CREATE INDEX comb_edg_nod_sco_idx ON comb_edge_node (edge_type_id);
-- CREATE INDEX comb_edg_nod_sco_typ_idx ON comb_edge_node (source_type_id);
CREATE INDEX comb_edg_nod_stu_idx ON comb_edge_node (study_id);


-- alter table comb_edge_node add index comb_edg_nod_src_idx (source_node_id);
-- alter table comb_edge_node add index comb_edg_nod_tgt_idx (target_node_id);
-- alter table comb_edge_node add index comb_edg_nod_sco_idx (score);
-- alter table comb_edge_node add index comb_edg_nod_sco_typ_idx (score_type_id);
-- -- 20220829 - added to help with creative query
-- alter table comb_edge_node add index comb_edg_nod_stu_idx (study_id);




-- add in sample data
-- id 39821
insert into comb_node_ontology (node_code, node_type_id, ontology_id, ontology_type_id, node_name, added_by_study_id)
values('pancreas', 11, 'UBERON:0001264', 9, 'pancreas', 1);
-- link to t2d, id 5980
insert into comb_edge_node 
(edge_id, source_node_id, target_node_id, edge_type_id, study_id,
  score, score_translator, p_value, beta, probability, probability_app_bayes_factor, publication_ids, enrichment)
values('test-edge', 39821, 5980, 6, 1, 0.75, 0.75, 0.0000000053, .125, .69, .98, "12123, 121334", 78);























-- scratch
-- sqlite example
drop table mcq_gene;
CREATE TABLE IF NOT EXISTS mcq_gene (
    id INTEGER PRIMARY KEY, 
    ontology_id TEXT, 
    query_ontology_id TEXT, 
    name TEXT,
    namer_translator TEXT,
    created_at DATE DEFAULT (DATE('now', 'localtime'))
);


-- queries
select node.node_code, curie.type_name 
from comb_lookup_type curie, comb_node_ontology node 
where node.node_type_id = curie.type_id 
and curie.type_id = 1
order by node.node_code;

