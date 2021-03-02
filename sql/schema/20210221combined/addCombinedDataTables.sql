

-- add a combined node-0edge-node tables
drop table if exists comb_node_edge;
create table comb_node_edge (
  id                        int not null auto_increment primary key,
  edge_id                   varchar(100) not null,
  source_code               varchar(50) not null,
  target_code               varchar(50) not null,
  edge_type_id              int(3) not null,
  score                     double,
  score_type_id             int(3) not null,
  study_id                  int(3) not null
);

-- add in table to link node codes (PPARG/BMI) to onltology ids returned to API queries
drop table if exists comb_node_ontology;
create table comb_node_ontology (
  id                        int not null auto_increment primary key,
  node_code                 varchar(50) not null,
  node_type_id              int(3) not null,
  ontology_id               varchar(50) not null,
  ontology_type_id          int(3) not null,
  node_name                 varchar(1000)
);


-- add node/edge type lookup tables
drop table if exists comb_lookup_type;
create table comb_lookup_type (
  type_id                   int not null primary key,
  type_name                 varchar(100) not null,
  type_family               enum('node', 'edge', 'attribute')
);

insert into comb_lookup_type values(1, 'biolink:Disease', 'node');
insert into comb_lookup_type values(2, 'biolink:Gene', 'node');
insert into comb_lookup_type values(3, 'biolink:PhenotypicFeature', 'node');
insert into comb_lookup_type values(4, 'biolink:Pathway', 'node');
insert into comb_lookup_type values(5, 'biolink:gene_associated_with_condition', 'edge');
insert into comb_lookup_type values(6, 'biolink:genetic_association', 'edge');
insert into comb_lookup_type values(7, 'biolink:symbol', 'attribute');
insert into comb_lookup_type values(8, 'biolink:p_value', 'attribute');
insert into comb_lookup_type values(9, 'biolink:probability', 'attribute');
-- insert into comb_lookup_type values(1, 'biolink:condition_associated_with_gene', 'edge');
-- insert into comb_lookup_type values(1, 'biolink:condition_associated_with_gene', 'edge');
-- insert into comb_lookup_type values(1, 'biolink:condition_associated_with_gene', 'edge');
-- insert into comb_lookup_type values(1, 'biolink:condition_associated_with_gene', 'edge');

-- add study lookup tables
drop table if exists comb_study_type;
create table comb_study_type (
  study_id                  int not null primary key,
  study_name                varchar(100) not null,
  publication               varchar(4000),
  description               varchar(4000)
);

insert into comb_study_type (study_id, study_name) values(1, 'Magma');
insert into comb_study_type (study_id, study_name) values(2, 'ABC');
insert into comb_study_type (study_id, study_name) values(3, 'Integrated Genetics');
insert into comb_study_type (study_id, study_name) values(4, 'Richards Effector Gene');

-- add ontology lookup tables
drop table if exists comb_ontology_type;
create table comb_ontology_type (
  ontology_id               int not null primary key,
  ontology_name             varchar(100) not null,
  url                       varchar(4000),
  description               varchar(4000)
);

insert into comb_ontology_type (ontology_id, ontology_name) values(1, 'NCBI Gene');
insert into comb_ontology_type (ontology_id, ontology_name) values(2, 'MONDO disease/phenotype');
insert into comb_ontology_type (ontology_id, ontology_name) values(3, 'EFO disease/phenotype');
insert into comb_ontology_type (ontology_id, ontology_name) values(4, 'GO pathway');









-- INSERTS ---
-- insert the genes
insert into comb_node_ontology (node_code, node_type_id, ontology_id, ontology_type_id, node_name)
select gene, 2, ncbi_id, 1, gene from gene_lookup;

-- insert the phenotype/diseases
-- mondo disease
insert into comb_node_ontology (node_code, node_type_id, ontology_id, ontology_type_id, node_name)
select phenotype_code, 1, mondo_id, 2, phenotype from phenotype_lookup where mondo_id is not null and category='Disease';
-- mondo phenotype
insert into comb_node_ontology (node_code, node_type_id, ontology_id, ontology_type_id, node_name)
select phenotype_code, 3, mondo_id, 2, phenotype from phenotype_lookup where mondo_id is not null and category in ('Phenotype', 'Measurement');
-- efo disease
insert into comb_node_ontology (node_code, node_type_id, ontology_id, ontology_type_id, node_name)
select phenotype_code, 1, efo_id, 3, phenotype from phenotype_lookup where efo_id is not null and category='Disease';
-- efo phenotype
insert into comb_node_ontology (node_code, node_type_id, ontology_id, ontology_type_id, node_name)
select phenotype_code, 3, efo_id, 3, phenotype from phenotype_lookup where efo_id is not null and category in ('Phenotype', 'Measurement');

-- insert richards data
insert into comb_node_edge (edge_id, source_code, target_code, edge_type_id, score, score_type_id, study_id)
select id, gene_name, phenotype_name, 5, probability, 9, 4
from richards_gene;

-- https://stackoverflow.com/questions/3164505/mysql-insert-record-if-not-exists-in-table




-- TODO
-- indexes
-- flipped query
-- only on object


-- SCRATCH ---
-- sample p_value query
    -- # the data return order is:
    -- # edge_id
    -- # source ontology code
    -- # target ontology code
    -- # score
    -- # score_type
    -- # source name
    -- # target name
    -- # edge type
    -- # source type
    -- # target type

select ed.edge_id, so.ontology_id, ta.ontology_id, score, sco_type.type_name, so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name
from comb_node_edge ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type 
where ed.source_code = so.node_code and ed.target_code = ta.node_code and ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id 
and ed.score_type_id = sco_type.type_id and sco_type.type_name = 'biolink:probability'
order by score desc limit 10;


select ed.* from comb_node_edge ed, comb_node_ontology so where ed.source_code = so.node_code and so.ontology_id = 'NCBIGene:1803';

-- Richards phenotypes
-- 
-- mysql> select distinct target_code from comb_node_edge;
-- +-------------+
-- | target_code |
-- +-------------+
-- | dbilirubin  |
-- | ldl         |
-- | ebmd        |
-- | glucose     |
-- | dbp         |
-- | lowtsh      |
-- | calcium     |
-- | rbc         |
-- | t2d         |
-- | sbp         |
-- | tg          |
-- | height      |
-- +-------------+
-- 12 rows in set (0.02 sec)

