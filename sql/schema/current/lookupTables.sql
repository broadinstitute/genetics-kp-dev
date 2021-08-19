
-- add node/edge type lookup tables
-- table defines the accepted edge and node types
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
-- 20210513 - add in score_text 
insert into comb_lookup_type values(11, 'biolink:classification', 'attribute');
-- 20210519 - added new row type
insert into comb_lookup_type values(12, 'biolink:DiseaseOrPhenotypicFeature', 'node');


-- add study lookup tables
-- table defines where the data came from (provenance)
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
-- 20210513 - adding new provenances
insert into comb_study_type (study_id, study_name) values(5, 'ClinGen');
insert into comb_study_type (study_id, study_name) values(6, 'ClinVar');
-- 20210817 - adding the gencc study and its sub studies
insert into comb_study_type (study_id, study_name) values(7, 'genCC');
insert into comb_study_type (study_id, study_name) values(8, 'Ambry Genetics');
insert into comb_study_type (study_id, study_name) values(9, 'Genomics England PanelApp');
insert into comb_study_type (study_id, study_name) values(10, 'Illumina');
insert into comb_study_type (study_id, study_name) values(11, 'Invitae');
insert into comb_study_type (study_id, study_name) values(12, 'Myriad Women’s Health');
insert into comb_study_type (study_id, study_name) values(13, 'PanelApp Australia');
insert into comb_study_type (study_id, study_name) values(14, 'TGMI|G2P');
insert into comb_study_type (study_id, study_name) values(15, 'Franklin by Genoox');
insert into comb_study_type (study_id, study_name) values(16, 'Online Mendelian Inheritance in Man (OMIM)');


-- add ontology lookup tables
-- table defines the ontology families used in the DB
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
insert into comb_ontology_type (ontology_id, ontology_name) values(5, 'UMLS disease/phenotype');
insert into comb_ontology_type (ontology_id, ontology_name) values(6, 'HP disease/phenotype');
insert into comb_ontology_type (ontology_id, ontology_name) values(7, 'NCIT disease/phenotype');


