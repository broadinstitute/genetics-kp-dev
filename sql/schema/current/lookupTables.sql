
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
-- 20210908 - adding genebess/uk biobank
insert into comb_study_type (study_id, study_name) values(17, 'GeneBass');
-- 20230208 - adding 600k ellinor study
insert into comb_study_type (study_id, study_name) values(18, '600k Ellinor');


-- add ontology lookup tables
-- table defines the ontology families used in the DB
drop table if exists comb_ontology_type;
create table comb_ontology_type (
  ontology_id               int not null primary key,
  ontology_name             varchar(100) not null,
  url                       varchar(4000),
  description               varchar(4000)
);
alter table comb_ontology_type add prefix varchar(10);


insert into comb_ontology_type (ontology_id, ontology_name) values(1, 'NCBI Gene');
insert into comb_ontology_type (ontology_id, ontology_name) values(2, 'MONDO disease/phenotype');
insert into comb_ontology_type (ontology_id, ontology_name) values(3, 'EFO disease/phenotype');
insert into comb_ontology_type (ontology_id, ontology_name) values(4, 'GO pathway');
insert into comb_ontology_type (ontology_id, ontology_name) values(5, 'UMLS disease/phenotype');
insert into comb_ontology_type (ontology_id, ontology_name) values(6, 'HP disease/phenotype');
insert into comb_ontology_type (ontology_id, ontology_name) values(7, 'NCIT disease/phenotype');
-- 20210908 - adding MESH
insert into comb_ontology_type (ontology_id, ontology_name) values(8, 'MESH disease/phenotype');

-- add prefixes
update comb_ontology_type set prefix='NCBIGene' where ontology_id = 1;
update comb_ontology_type set prefix='MONDO' where ontology_id = 2;
update comb_ontology_type set prefix='EFO' where ontology_id = 3;
update comb_ontology_type set prefix='GO' where ontology_id = 4;
update comb_ontology_type set prefix='UMLS' where ontology_id = 5;
update comb_ontology_type set prefix='HP' where ontology_id = 6;
update comb_ontology_type set prefix='NCIT' where ontology_id = 7;
update comb_ontology_type set prefix='MESH' where ontology_id = 8;

-- 20220817 - add new pathways
update comb_ontology_type set ontology_name='HP disease/phenotype/pathway' where ontology_id = 6;
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(9, 'Reactome pathway', 'REACTOME');
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(10, 'Biocarta pathway', 'BIOCARTA');
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(11, 'Kegg pathway', 'KEGG');
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(12, 'PID pathway', 'PID');
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(13, 'WikiPathway pathway', 'WP');
-- 20230209- adding orphanet, uberon 
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(14, 'Orphanet phenotype', 'Orphanet');
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(15, 'Orphanet phenotype', 'Orphanet');


-- 20220817 
-- mysql> select * from comb_ontology_type;
-- +-------------+------------------------------+------+-------------+----------+
-- | ontology_id | ontology_name                | url  | description | prefix   |
-- +-------------+------------------------------+------+-------------+----------+
-- |           1 | NCBI Gene                    | NULL | NULL        | NCBIGene |
-- |           2 | MONDO disease/phenotype      | NULL | NULL        | MONDO    |
-- |           3 | EFO disease/phenotype        | NULL | NULL        | EFO      |
-- |           4 | GO pathway                   | NULL | NULL        | GO       |
-- |           5 | UMLS disease/phenotype       | NULL | NULL        | UMLS     |
-- |           6 | HP disease/phenotype/pathway | NULL | NULL        | HP       |
-- |           7 | NCIT disease/phenotype       | NULL | NULL        | NCIT     |
-- |           8 | MESH disease/phenotype       | NULL | NULL        | MESH     |
-- |           9 | Reactome pathway             | NULL | NULL        | REACTOME |
-- |          10 | Biocarta pathway             | NULL | NULL        | BIOCARTA |
-- |          11 | Kegg pathway                 | NULL | NULL        | KEGG     |
-- |          12 | PID pathway                  | NULL | NULL        | PID      |
-- |          13 | WikiPathway pathway          | NULL | NULL        | WP       |
-- +-------------+------------------------------+------+-------------+----------+
-- 13 rows in set (0.00 sec



-- create qualifier table
drop table if exists comb_qualifier;
create table comb_qualifier (
  id                        varchar(50) not null primary key,
  qualifier_type            varchar(50) not null,
  qualifier_value           varchar(50) not null,
  date_created              datetime DEFAULT CURRENT_TIMESTAMP
);


-- create qualifiers
-- aspect qualifiers
insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('subject_aspect_activity', 'subject_aspect_qualifier', 'activity');

insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('subject_aspect_severity', 'subject_aspect_qualifier', 'severity');

-- direction qualifiers
insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('subject_direction_increased', 'subject_direction_qualifier', 'increased');

insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('subject_direction_decreased', 'subject_direction_qualifier', 'decreased');

insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('object_direction_increased', 'object_direction_qualifier', 'increased');

insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('object_direction_decreased', 'object_direction_qualifier', 'decreased');

-- predicate qualifier
insert into comb_qualifier (id, qualifier_type, qualifier_value) 
values('qualified_predicate_causes', 'qualified_predicate', 'causes');



