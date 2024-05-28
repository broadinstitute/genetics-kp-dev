

-- add in table to link node codes (PPARG/BMI) to onltology ids returned to API queries
drop table if exists comb_node_ontology;
create table comb_node_ontology (
  id                        INTEGER PRIMARY KEY,
  node_code                 TEXT not null,
  node_type_id              INTEGER not null,
  ontology_id               TEXT not null,
  ontology_type_id          INTEGER not null,
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

-- add node/edge type lookup tables
drop table if exists comb_lookup_type;
create table comb_lookup_type (
  type_id                   INTEGER PRIMARY KEY,
  type_name                 TEXT not null,
  type_family               TEXT CHECK(type_family IN ('node', 'edge', 'attribute')),
  created_at                DATE DEFAULT (DATE('now', 'localtime'))
);

insert into comb_lookup_type (type_id, type_name, type_family) values(1, 'biolink:Disease', 'node');
insert into comb_lookup_type (type_id, type_name, type_family) values(2, 'biolink:Gene', 'node');
insert into comb_lookup_type (type_id, type_name, type_family) values(3, 'biolink:PhenotypicFeature', 'node');
insert into comb_lookup_type (type_id, type_name, type_family) values(4, 'biolink:Pathway', 'node');
insert into comb_lookup_type (type_id, type_name, type_family) values(5, 'biolink:gene_associated_with_condition', 'edge');
insert into comb_lookup_type (type_id, type_name, type_family) values(6, 'biolink:genetic_association', 'edge');
insert into comb_lookup_type (type_id, type_name, type_family) values(7, 'biolink:symbol', 'attribute');
insert into comb_lookup_type (type_id, type_name, type_family) values(8, 'biolink:p_value', 'attribute');
insert into comb_lookup_type (type_id, type_name, type_family) values(9, 'biolink:probability', 'attribute');
insert into comb_lookup_type (type_id, type_name, type_family) values(10, 'biolink:condition_associated_with_gene', 'edge');


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

