
-- DESIGN
-- for phenotypes/disease, needed a unique code for each; since not all ontologies cover all entries, but our DCC codes do
-- the join will be done on the DCC phenotype/disease code
-- same for gene

-- add a combined node-0edge-node tables
drop table if exists comb_node_edge;
create table comb_node_edge (
  id                        int not null auto_increment primary key,
  edge_id                   varchar(100) not null,
  source_code               varchar(50) not null,
  target_code               varchar(50) not null,
  edge_type_id              int(3) not null,
  source_type_id            int(3) not null,
  target_type_id            int(3) not null,
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
-- indices
alter table comb_node_ontology add index node_ont_node_cde_idx (node_code);
alter table comb_node_ontology add index node_ont_node_typ_idx (node_type_id);
alter table comb_node_ontology add index node_ont_ont_idx (ontology_id);

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
insert into comb_lookup_type values(10, 'biolink:condition_associated_with_gene', 'edge');
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

-- fix '-' with ':' for onltology IDs
update comb_node_ontology set ontology_id = replace(ontology_id, '_', ':');

-- insert the pathways
-- GO pathways
insert into comb_node_ontology (node_code, node_type_id, ontology_id, ontology_type_id, node_name)
select distinct PATHWAY, 4, PATHWAY, 4, PATHWAY from MAGMA_PATHWAYS;


-- add a combined node-0edge-node tables
drop table if exists comb_node_edge;
create table comb_node_edge (
  id                        int not null auto_increment primary key,
  edge_id                   varchar(100) not null,
  source_code               varchar(50) not null,
  target_code               varchar(50) not null,
  edge_type_id              int(3) not null,
  source_type_id            int(3) not null,
  target_type_id            int(3) not null,
  score                     double,
  score_type_id             int(3) not null,
  study_id                  int(3) not null
);
-- add indices
alter table comb_node_edge add index comb_nod_edg_src_cde_idx (source_code);
alter table comb_node_edge add index comb_nod_edg_tgt_cde_idx (target_code);
alter table comb_node_edge add index comb_nod_edg_edg_typ_idx (edge_type_id);
alter table comb_node_edge add index comb_nod_edg_src_typ_idx (source_type_id);
alter table comb_node_edge add index comb_nod_edg_tgt_typ_idx (target_type_id);
alter table comb_node_edge add index comb_nod_edg_sco_idx (score);
alter table comb_node_edge add index comb_nod_edg_sco_typ_idx (score_type_id);
-- alter table comb_node_edge add foreign key (source_code) references comb_node_ontology(node_code);
-- alter table comb_node_edge add foreign key (target_code) references comb_node_ontology(node_code);
-- alter table comb_node_edge add foreign key (edge_type_id) references comb_lookup_type(type_id);
-- alter table comb_node_edge add foreign key (source_type_id) references comb_node_ontology(node_type_id);
-- alter table comb_node_edge add foreign key (target_type_id) references comb_node_ontology(node_type_id);


-- EDGE DATA
-- insert richards data - disease
insert into comb_node_edge (edge_id, source_code, target_code, edge_type_id, source_type_id, target_type_id, score, score_type_id, study_id)
select id, gene_name, phenotype_name, 5, 2, 1, probability, 9, 4
from richards_gene where category = 'disease';
-- insert richards data - phenotype
insert into comb_node_edge (edge_id, source_code, target_code, edge_type_id, source_type_id, target_type_id, score, score_type_id, study_id)
select id, gene_name, phenotype_name, 5, 2, 3, probability, 9, 4
from richards_gene where category = 'phenotypic_feature';
-- fix richards data phenotype codes
update comb_node_edge set target_code = 'Thyroid' where target_code = 'lowtsh' and edge_id like 'RC_GENES%';
update comb_node_edge set target_code = 'BILIRUBIN' where target_code = 'dbilirubin' and edge_id like 'RC_GENES%';
update comb_node_edge set target_code = 'LDL' where target_code = 'ldl' and edge_id like 'RC_GENES%';
update comb_node_edge set target_code = 'T2D' where target_code = 't2d' and edge_id like 'RC_GENES%';
update comb_node_edge set target_code = 'eBMD' where target_code = 'ebmd' and edge_id like 'RC_GENES%';
update comb_node_edge set target_code = 'DBP' where target_code = 'dbp' and edge_id like 'RC_GENES%';
update comb_node_edge set target_code = 'Ca' where target_code = 'calcium' and edge_id like 'RC_GENES%';
update comb_node_edge set target_code = 'RedCount' where target_code = 'rbc' and edge_id like 'RC_GENES%';
update comb_node_edge set target_code = 'SBP' where target_code = 'sbp' and edge_id like 'RC_GENES%';
update comb_node_edge set target_code = 'TG' where target_code = 'tg' and edge_id like 'RC_GENES%';
update comb_node_edge set target_code = 'HEIGHT' where target_code = 'height' and edge_id like 'RC_GENES%';
update comb_node_edge set target_code = 'FG' where target_code = 'glucose' and edge_id like 'RC_GENES%';

-- insert magma pathway data - disease
insert into comb_node_edge (edge_id, source_code, target_code, edge_type_id, source_type_id, target_type_id, score, score_type_id, study_id)
select pa.ID, pa.PATHWAY, co.node_code, 6, 4, 1, pa.PVALUE, 8, 1
from MAGMA_PATHWAYS pa, comb_node_ontology co where pa.DISEASE = co.ontology_id and co.node_type_id = 1 and CATEGORY = 'disease';
-- insert magma pathway data - phenotype
insert into comb_node_edge (edge_id, source_code, target_code, edge_type_id, source_type_id, target_type_id, score, score_type_id, study_id)
select pa.ID, pa.PATHWAY, co.node_code, 6, 4, 3, pa.PVALUE, 8, 1
from MAGMA_PATHWAYS pa, comb_node_ontology co where pa.DISEASE = co.ontology_id and co.node_type_id = 3 and CATEGORY = 'phenotypic_feature';

-- insert integrated genetics gene data - disease
insert into comb_node_edge (edge_id, source_code, target_code, edge_type_id, source_type_id, target_type_id, score, score_type_id, study_id)
select pa.ID, ge.node_code, co.node_code, 5, 2, 1, pa.SCORE, 9, 3
from SCORE_GENES pa, comb_node_ontology co, comb_node_ontology ge 
where pa.DISEASE = co.ontology_id and co.node_type_id = 1 and pa.GENE = ge.ontology_id and ge.node_type_id = 2 and CATEGORY = 'disease';
-- insert integrated genetics gene data - phenotype
insert into comb_node_edge (edge_id, source_code, target_code, edge_type_id, source_type_id, target_type_id, score, score_type_id, study_id)
select pa.ID, ge.node_code, co.node_code, 5, 2, 3, pa.SCORE, 9, 3
from SCORE_GENES pa, comb_node_ontology co, comb_node_ontology ge  
where pa.DISEASE = co.ontology_id and co.node_type_id = 3 and pa.GENE = ge.ontology_id and ge.node_type_id = 2 and CATEGORY = 'phenotypic_feature';

-- insert magma gene data - disease
insert into comb_node_edge (edge_id, source_code, target_code, edge_type_id, source_type_id, target_type_id, score, score_type_id, study_id)
select concat('magma_gene_',id), gene, phenotype_code, 5, 2, 1, p_value, 8, 1
from magma_gene_phenotype where biolink_category = 'biolink:Disease';
-- insert magma gene data - phenotype
insert into comb_node_edge (edge_id, source_code, target_code, edge_type_id, source_type_id, target_type_id, score, score_type_id, study_id)
select concat('magma_gene_',id), gene, phenotype_code, 5, 2, 3, p_value, 8, 1
from magma_gene_phenotype where biolink_category = 'biolink:PhenotypicFeature';

-- insert the reverse data
insert into comb_node_edge (edge_id, source_code, target_code, edge_type_id, source_type_id, target_type_id, score, score_type_id, study_id)
select edge_id, target_code, source_code, if(edge_type_id = 5, 10, edge_type_id), target_type_id, source_type_id, score, score_type_id, study_id
from comb_node_edge;
limit 3;

-- https://stackoverflow.com/questions/3164505/mysql-insert-record-if-not-exists-in-table




-- TODO
-- indexes
-- flipped query
-- DONE - only on object
-- add in pathways

drop table if exists com_node_edge_backup;
create table comb_node_edge_backup as select * from comb_node_edge;

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
and ed.score_type_id = sco_type.type_id and ed.source_type_id = so.node_type_id and ed.target_type_id = ta.node_type_id and sco_type.type_name = 'biolink:probability'
order by score desc limit 10;


select ed.* from comb_node_edge ed, comb_node_ontology so where ed.source_code = so.node_code and so.ontology_id = 'NCBIGene:1803';

-- edges by combination type
select count(ed.edge_id), sco_type.type_name as score_type, ted.type_name as edge, tso.type_name as source, tta.type_name as target, study.study_name
from comb_node_edge ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type, comb_study_type study
where ed.source_code = so.node_code and ed.target_code = ta.node_code and ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id 
and ed.score_type_id = sco_type.type_id and ed.source_type_id = so.node_type_id and ed.target_type_id = ta.node_type_id and ed.study_id = study.study_id
group by sco_type.type_name, ted.type_name, tso.type_name, tta.type_name, study.study_name;

select * 
from comb_node_edge ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type 
where ed.source_code = so.node_code and ed.target_code = ta.node_code and ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id 
and ed.score_type_id = sco_type.type_id and tso.type_name = 'biolink:Disease' and tta.type_name = 'biolink:Gene';

-- edge by id
select concat(ed.edge_id, so.ontology_id, ta.ontology_id), so.ontology_id, ta.ontology_id, ed.score, sco_type.type_name, 
so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name         
from comb_node_edge ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type         
where ed.source_code = so.node_code and ed.target_code = ta.node_code and ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id         
and ed.score_type_id = sco_type.type_id and ed.source_type_id = so.node_type_id and ed.target_type_id = ta.node_type_id  
and ed.edge_id = 67587;

-- and ted.type_name = %s  and tso.type_name = %s  and tta.type_name = %s  and sco_type.type_name = %s  and so.ontology_id = %s  
-- order by ed.score limit 5000

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

