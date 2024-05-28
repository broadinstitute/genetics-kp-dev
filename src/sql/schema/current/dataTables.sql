

-- define new edge table
-- this table handles the edges (node to node relationships)
drop table if exists comb_edge_node;
create table comb_edge_node (
  id                        int not null auto_increment primary key,
  edge_id                   varchar(100) not null,
  source_node_id            int(3) not null,
  target_node_id            int(3) not null,
  edge_type_id              int(3) not null,
  score                     double,
  score_text                varchar(50),
  score_type_id             int(3) not null,
  study_id                  int(3) not null,
  date_created              datetime DEFAULT CURRENT_TIMESTAMP
);

-- indices
alter table comb_edge_node add index comb_edg_nod_src_idx (source_node_id);
alter table comb_edge_node add index comb_edg_nod_tgt_idx (target_node_id);
alter table comb_edge_node add index comb_edg_nod_sco_idx (score);
alter table comb_edge_node add index comb_edg_nod_sco_typ_idx (score_type_id);
-- 20220829 - added to help with creative query
alter table comb_edge_node add index comb_edg_nod_stu_idx (study_id);

-- 20210817 - add in translator score, secondary provenance
alter table comb_edge_node add score_translator double;
alter table comb_edge_node add study_secondary_id int(3) null;
alter table comb_edge_node add publication_ids varchar(1000) null;

-- 20230208 - add flag if has qualifiers indicating 2nd query 
alter table comb_edge_node add column has_qualifiers enum('N', 'Y') default 'N';

-- 20230303 - add specific probability, beta, abf, p_value (eventually deprecate score)
alter table comb_edge_node add p_value double;
alter table comb_edge_node add beta double;
alter table comb_edge_node add standard_error double;
alter table comb_edge_node add probabilty double;
alter table comb_edge_node add probability_app_bayes_factor double;


-- create qualifier link table
drop table if exists comb_edge_qualifier;
create table comb_edge_qualifier (
  id                        int not null auto_increment primary key,
  edge_id                   int(9) not null,
  qualifier_id              varchar(50) not null,
  study_id                  int(3) not null,
  date_created              datetime DEFAULT CURRENT_TIMESTAMP
);

-- indices
alter table comb_edge_qualifier add index comb_edg_qua_edg_idx (edge_id);


-- add in table to link node codes (PPARG/BMI) to onltology ids returned to API queries
-- this table handles the nodes included in our graph
drop table if exists comb_node_ontology;
create table comb_node_ontology (
  id                        int not null auto_increment primary key,
  node_code                 varchar(50) not null,
  node_type_id              int(3) not null,
  ontology_id               varchar(50) not null,
  ontology_type_id          int(3) not null,
  node_name                 varchar(1000)
);

-- indices
alter table comb_node_ontology add index node_ont_node_cde_idx (node_code);
alter table comb_node_ontology add index node_ont_node_typ_idx (node_type_id);
alter table comb_node_ontology add index node_ont_ont_idx (ontology_id);

-- 20210519 - make ontology_id nullable for adding in new phenotypes
alter table comb_node_ontology modify ontology_id varchar(50) null;
alter table comb_node_ontology modify ontology_type_id varchar(50) null;

-- alter node ontology table
alter table comb_node_ontology add last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- 20210817 - add in which study added in node for history
alter table comb_node_ontology add added_by_study_id int(3);

-- 20210817 - increase disease name
alter table comb_node_ontology modify node_code varchar(500) not null;




-- curie cache table
drop table if exists comb_cache_curie;
create table comb_cache_curie (
  id                        int not null auto_increment primary key,
  node_curie_id             varchar(100) not null,
  node_name                 varchar(1000),
  node_synonym_id           varchar(100) not null,
  date_created              datetime DEFAULT CURRENT_TIMESTAMP
);
alter table comb_cache_curie add index comb_cac_cur_idx (node_curie_id);


-- new cached curie table 
-- add index on searched synonym 
drop table if exists comb_cache_ancestor_curie;
create table comb_cache_ancestor_curie (
  id                        int not null auto_increment primary key,
  genepro_node_id,          int(9) not null,
  genepro_curie_id          varchar(100) not null,
  parent_curie_id           varchar(100) not null,
  parent_node_name          varchar(1000),
  date_created              datetime DEFAULT CURRENT_TIMESTAMP
);
alter table comb_cache_ancestor_curie add index comb_cac_anc_cur_nod_idx (genepro_node_id);
alter table comb_cache_ancestor_curie add index comb_cac_anc_cur_par_idx (parent_curie_id);


