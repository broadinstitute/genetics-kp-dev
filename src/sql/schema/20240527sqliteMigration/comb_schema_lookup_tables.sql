

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
insert into comb_lookup_type (type_id, type_name, type_family) values(11, 'biolink:Cell', 'node');



-- add study lookup tables
drop table if exists comb_study_type;
create table comb_study_type (
  study_id                  INTEGER PRIMARY KEY,
  study_name                TEXT not null,
  publication               TEXT,
  description               TEXT,
  created_at                DATE DEFAULT (DATE('now', 'localtime'))
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
insert into comb_study_type (study_id, study_name) values(19, 'Magma tissue');



-- add ontology lookup tables
drop table if exists comb_ontology_type;
create table comb_ontology_type (
  ontology_id               INTEGER PRIMARY KEY,
  ontology_name             TEXT not null,
  prefix                    TEXT not null,
  url                       TEXT,
  description               TEXT,
  created_at                DATE DEFAULT (DATE('now', 'localtime'))
);


insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(1, 'NCBI Gene', 'NBCIGene');
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(2, 'MONDO disease/phenotype', 'MONDO');
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(3, 'EFO disease/phenotype', 'EFO');
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(4, 'GO pathway', 'GO');
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(5, 'UMLS disease/phenotype', 'UMLS');
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(6, 'HP disease/phenotype', 'HP');
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(7, 'NCIT disease/phenotype', 'NCIT');
-- 20210908 - adding MESH
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(8, 'MESH disease/phenotype', 'MESH');
-- 20240530 - adding UBERON for tissues
insert into comb_ontology_type (ontology_id, ontology_name, prefix) values(9, 'UBERON cell', 'UBERON');




