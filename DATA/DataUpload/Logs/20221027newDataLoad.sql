

-- steps taken
-- 1 - load new phenotypes not already in the comb_node_ontology tables
-- 2 - add new ontologies to comb_ontology_type table -> see lookupTables.sql
-- 3 - loaded new pathways that were not in the comb_node_ontology tables already -> see loadUpkeepPathwayToTranslator.sql
-- 4 - load pathway genes
-- 5 - load pathway associations
-- 6 - load gene associations



-- from the phenotype loading python script
-- 
-- got aggregator phenotype data size of 664
-- the are 6257 phenotypes/diseases in the translator db
-- the are 586 phenotypes/diseases in the upkeep db
-- 640 - disease HY3inPD
-- 660 - disease IPFSurvival
-- the are 6257 phenotypes/diseases in the translator db
-- the are 664 phenotypes/diseases in the upkeep db

-- finding ontology_id for new magma phenotypes
-- mysql> select count(id), in_translator 
--     -> from tran_upkeep.agg_aggregator_phenotype
--     -> group by in_translator;
-- +-----------+---------------+
-- | count(id) | in_translator |
-- +-----------+---------------+
-- |       259 | true          |
-- |       405 | false         |
-- +-----------+---------------+
-- 2 rows in set (0.00 sec)

-- mysql> select count(id), in_translator 
--     -> from tran_upkeep.agg_aggregator_phenotype
--     -> where ontology_id is not null
--     -> group by in_translator;
-- +-----------+---------------+
-- | count(id) | in_translator |
-- +-----------+---------------+
-- |        15 | false         |
-- +-----------+---------------+
-- 1 row in set (0.01 sec)


-- mysql> select * 
--     -> from tran_upkeep.agg_aggregator_phenotype
--     -> where ontology_id is not null
--     -> and in_translator = 'false'
--     -> order by phenotype_name;
-- +------+---------------+---------------------------------------+---------------------+---------------+---------------+---------------+---------------------+
-- | id   | phenotype_id  | phenotype_name                        | group_name          | ontology_id   | in_translator | just_added_in | last_updated        |
-- +------+---------------+---------------------------------------+---------------------+---------------+---------------+---------------+---------------------+
-- | 1206 | ASAT          | Abdominal subcutaneous adipose tissue | ANTHROPOMETRIC      | UMLS:C1563741 | false         | false         | 2022-10-28 11:21:15 |
-- | 1214 | Eczema        | Atopic dermatitis                     | IMMUNOLOGICAL       | MONDO:0004980 | false         | false         | 2022-10-28 11:21:27 |
-- | 1217 | BackPain      | Back pain                             | MUSCULOSKELETAL     | NCIT:C146739  | false         | false         | 2022-10-28 11:21:29 |
-- | 1065 | BMI_GIANT     | BMI                                   | GIANT PHENOTYPES    | NCIT:C138901  | false         | false         | 2022-10-28 11:21:30 |
-- | 1223 | DementiaInPD  | Dementia in Parkinson's disease       | NEUROLOGICAL        | UMLS:C1828079 | false         | false         | 2022-10-28 11:21:37 |
-- | 1215 | Graves        | Graves' disease                       | IMMUNOLOGICAL       | MONDO:0005364 | false         | false         | 2022-10-28 11:21:47 |
-- | 1066 | HEIGHT_GIANT  | HEIGHT                                | GIANT PHENOTYPES    | UMLS:C0489786 | false         | false         | 2022-10-28 11:21:49 |
-- |  939 | HbConc        | Hemoglobin concentration              | HEMATOLOGICAL       | UMLS:C0019029 | false         | false         | 2022-10-28 11:21:50 |
-- | 1218 | KneePain      | Knee pain                             | MUSCULOSKELETAL     | HP:0030839    | false         | false         | 2022-10-28 11:21:57 |
-- | 1201 | LacunarStroke | Lacunar stroke                        | STROKE              | HP:0032325    | false         | false         | 2022-10-28 11:21:58 |
-- | 1116 | NAFLD         | NAFLD                                 | HEPATIC             | MONDO:0013209 | false         | false         | 2022-10-28 11:22:15 |
-- | 1220 | NeckCir       | Neck circumference                    | SLEEP AND CIRCADIAN | UMLS:C2367402 | false         | false         | 2022-10-28 11:22:17 |
-- | 1216 | Pollinosis    | Pollinosis                            | IMMUNOLOGICAL       | MONDO:0005324 | false         | false         | 2022-10-28 11:22:27 |
-- | 1193 | RVSV          | Right ventricular stroke volume       | CARDIOVASCULAR      | UMLS:C1998360 | false         | false         | 2022-10-28 11:22:37 |
-- | 1219 | SCS           | Spinal canal stenosis                 | MUSCULOSKELETAL     | HP:0003416    | false         | false         | 2022-10-28 11:22:44 |
-- +------+---------------+---------------------------------------+---------------------+---------------+---------------+---------------+---------------------+
-- 15 rows in set (0.00 sec)

-- NOTE
-- remove BMI, HEIGHT, update NAFLD to more descriptive
update tran_upkeep.agg_aggregator_phenotype set phenotype_name = 'NAFLD (Nonalcoholic fatty liver disease)' where id = 1116;
update tran_upkeep.agg_aggregator_phenotype set in_translator = 'true' where id in (1065, 1066);


-- query number phenotypes in translator before the load (4 dis + 9 pheno = 13 new entries)
select count(node.id), type.type_id, type.type_name
from tran_test_202211.comb_node_ontology node, tran_test_202211.comb_lookup_type type
where node.node_type_id = type.type_id and node.node_type_id in (1, 3)
group by type.type_id, type.type_name;

-- +----------------+---------+---------------------------+
-- | count(node.id) | type_id | type_name                 |
-- +----------------+---------+---------------------------+
-- |           5787 |       1 | biolink:Disease           |
-- |            222 |       3 | biolink:PhenotypicFeature |
-- +----------------+---------+---------------------------+
-- 2 rows in set (0.01 sec)

-- query number phenotypes in translator after the load
-- +----------------+---------+---------------------------+
-- | count(node.id) | type_id | type_name                 |
-- +----------------+---------+---------------------------+
-- |           5791 |       1 | biolink:Disease           |
-- |            231 |       3 | biolink:PhenotypicFeature |
-- +----------------+---------+---------------------------+
-- 2 rows in set (0.03 sec)

-- loading new gene associations into upkeep table
select count(id) from agg_gene_phenotype;
-- before
-- +-----------+
-- | count(id) |
-- +-----------+
-- |   8943059 |
-- +-----------+
-- 1 row in set (3.40 sec)

-- after
-- +-----------+
-- | count(id) |
-- +-----------+
-- |  10020757 |
-- +-----------+
-- 1 row in set (0.51 sec)


-- drop the gene phenotype load table for speed
drop table if exists tran_upkeep.agg_gene_phenotype;
create table tran_upkeep.agg_gene_phenotype (
  id                           int not null auto_increment primary key,
  gene_code                    varchar(250) not null,
  phenotype_code               varchar(50) not null,
  gene_type                    varchar(250),
  z_stat                       double,
  p_value                      double not null,
  date_created                 datetime DEFAULT CURRENT_TIMESTAMP
);
alter table tran_upkeep.agg_gene_phenotype add index gene_phen_gene_cde_idx (gene_code);
alter table tran_upkeep.agg_gene_phenotype add index gene_phen_phen_cde_idx (phenotype_code);


-- loading new pathway phenotype associations to upkeep table
-- before
select count(id) from agg_pathway_phenotype;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |  11805087 |
-- +-----------+
-- 1 row in set (0.87 sec)

-- after
-- mysql> select count(id) from agg_pathway_phenotype;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |  13179013 |
-- +-----------+
-- 1 row in set (0.79 sec)

-- drop the pathway phenotype load table for speed
drop table if exists tran_upkeep.agg_pathway_phenotype;
create table tran_upkeep.agg_pathway_phenotype (
  id                           int not null auto_increment primary key,
  pathway_code                 varchar(250) not null,
  phenotype_code               varchar(50) not null,
  beta                         double null,
  beta_standard_error          double null,
  standard_error               double null,
  p_value                      double not null,
  date_created                 datetime DEFAULT CURRENT_TIMESTAMP
);


-- loading new phenotype phenotype associations to upkeep table
-- after
select count(id) from agg_pathway_phenotype;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |     29715 |
-- +-----------+
-- 1 row in set (0.02 sec)


-- loadign new genes/disease edges to translator table
-- pre load
select count(edge.id), source_type.type_id, source_type.type_name, target_type.type_id, target_type.type_name, edge_type.type_name, edge.study_id
from tran_test_202211.comb_edge_node edge, tran_test_202211.comb_node_ontology source, tran_test_202211.comb_node_ontology target, 
    tran_test_202211.comb_lookup_type edge_type,
    tran_test_202211.comb_lookup_type source_type, tran_test_202211.comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = 1
group by edge_type.type_name, source_type.type_id, source_type.type_name, target_type.type_id, target_type.type_name, edge.study_id
order by source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id;

-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- | count(edge.id) | type_id | type_name                 | type_id | type_name                 | type_name                              | study_id |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- |          27166 |       1 | biolink:Disease           |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |          78375 |       1 | biolink:Disease           |       4 | biolink:Pathway           | biolink:genetic_association            |        1 |
-- |          27166 |       2 | biolink:Gene              |       1 | biolink:Disease           | biolink:gene_associated_with_condition |        1 |
-- |         166248 |       2 | biolink:Gene              |       3 | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        1 |
-- |          78375 |       4 | biolink:Pathway           |       1 | biolink:Disease           | biolink:genetic_association            |        1 |
-- |         173154 |       4 | biolink:Pathway           |       3 | biolink:PhenotypicFeature | biolink:genetic_association            |        1 |
-- |         166248 |       3 | biolink:PhenotypicFeature |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |         173154 |       3 | biolink:PhenotypicFeature |       4 | biolink:Pathway           | biolink:genetic_association            |        1 |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- 8 rows in set (4.68 sec)

-- delete gene/disease edges
-- mysql> delete edge from tran_test_202211.comb_edge_node edge
--     -> inner join comb_node_ontology node on edge.source_node_id = node.id 
--     -> where node.node_type_id = 2 and edge.study_id = 1;
-- ERROR 1146 (42S02): Table 'tran_upkeep.comb_node_ontology' doesn't exist
-- mysql> delete edge from tran_test_202211.comb_edge_node edge
--     -> inner join tran_test_202211.comb_node_ontology node on edge.source_node_id = node.id 
--     -> where node.node_type_id = 2 and edge.study_id = 1;
-- Query OK, 193414 rows affected (32.16 sec)

-- mysql> delete edge from tran_test_202211.comb_edge_node edge
--     -> inner join tran_test_202211.comb_node_ontology node on edge.target_node_id = node.id 
--     -> where node.node_type_id = 2 and edge.study_id = 1;
-- Query OK, 193414 rows affected (34.03 sec)

-- edge count table
-- +----------------+---------+---------------------------+---------+---------------------------+-----------------------------+----------+
-- | count(edge.id) | type_id | type_name                 | type_id | type_name                 | type_name                   | study_id |
-- +----------------+---------+---------------------------+---------+---------------------------+-----------------------------+----------+
-- |          78375 |       1 | biolink:Disease           |       4 | biolink:Pathway           | biolink:genetic_association |        1 |
-- |          78375 |       4 | biolink:Pathway           |       1 | biolink:Disease           | biolink:genetic_association |        1 |
-- |         173154 |       4 | biolink:Pathway           |       3 | biolink:PhenotypicFeature | biolink:genetic_association |        1 |
-- |         173154 |       3 | biolink:PhenotypicFeature |       4 | biolink:Pathway           | biolink:genetic_association |        1 |
-- +----------------+---------+---------------------------+---------+---------------------------+-----------------------------+----------+
-- 4 rows in set (1.87 sec)

-- insert new gene/disease edges
-- mysql> insert into tran_test_202211.comb_edge_node 
--     -> (edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id, score_translator) 
--     ->     select concat('magma_', gene.ontology_id, '_', phenotype.ontology_id) as edge_id, 
--     ->     5, gene.id, phenotype.id, 
--     ->     up_gene_assoc.p_value, 8, 1, 0.15
--     ->     from tran_upkeep.agg_gene_phenotype up_gene_assoc, tran_test_202211.comb_node_ontology gene, tran_test_202211.comb_node_ontology phenotype
--     ->     where up_gene_assoc.gene_code collate utf8mb4_unicode_ci = gene.node_code and gene.node_type_id = 2 and gene.ontology_id is not null
--     ->     and up_gene_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
--     ->     and up_gene_assoc.p_value <= 0.0025
--     ->     order by phenotype.node_code, gene.node_code;
-- Query OK, 209612 rows affected (18.30 sec)
-- Records: 209612  Duplicates: 0  Warnings: 0

-- mysql> insert into tran_test_202211.comb_edge_node 
--     -> (edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id, score_translator) 
--     ->     select concat('magma_', phenotype.ontology_id, '_', gene.ontology_id) as edge_id, 
--     ->     10, phenotype.id, gene.id,
--     ->     up_gene_assoc.p_value, 8, 1, 0.15
--     ->     from tran_upkeep.agg_gene_phenotype up_gene_assoc, tran_test_202211.comb_node_ontology gene, tran_test_202211.comb_node_ontology phenotype
--     ->     where up_gene_assoc.gene_code collate utf8mb4_unicode_ci = gene.node_code and gene.node_type_id = 2 and gene.ontology_id is not null
--     ->     and up_gene_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
--     ->     and up_gene_assoc.p_value <= 0.0025
--     ->     order by phenotype.node_code, gene.node_code;
-- Query OK, 209612 rows affected (18.62 sec)
-- Records: 209612  Duplicates: 0  Warnings: 0


-- edge counts after gene/phenotype load 
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- | count(edge.id) | type_id | type_name                 | type_id | type_name                 | type_name                              | study_id |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- |          31140 |       1 | biolink:Disease           |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |          78375 |       1 | biolink:Disease           |       4 | biolink:Pathway           | biolink:genetic_association            |        1 |
-- |          31140 |       2 | biolink:Gene              |       1 | biolink:Disease           | biolink:gene_associated_with_condition |        1 |
-- |         178472 |       2 | biolink:Gene              |       3 | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        1 |
-- |          78375 |       4 | biolink:Pathway           |       1 | biolink:Disease           | biolink:genetic_association            |        1 |
-- |         173154 |       4 | biolink:Pathway           |       3 | biolink:PhenotypicFeature | biolink:genetic_association            |        1 |
-- |         178472 |       3 | biolink:PhenotypicFeature |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |         173154 |       3 | biolink:PhenotypicFeature |       4 | biolink:Pathway           | biolink:genetic_association            |        1 |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- 8 rows in set (4.82 sec)


-- 20221102 - fix data_pathway table as well
select id, pathway_code, ontology_id, replace(ontology_id, 'REACTOME', 'REACT') as ont_new from data_pathway where ontology_id like 'REA%';

update data_pathway set ontology_id = replace(ontology_id, 'REACTOME', 'REACT') where ontology_id like 'REA%';

-- mysql> update data_pathway set ontology_id = replace(ontology_id, 'REACTOME', 'REACT') where ontology_id like 'REA%';
-- Query OK, 1615 rows affected (0.07 sec)
-- Rows matched: 1615  Changed: 1615  Warnings: 0


-- insert new pathway/phenotype edges
-- delete old pathyway/phenotype edges
-- mysql> delete edge from tran_test_202211.comb_edge_node edge
--     -> inner join tran_test_202211.comb_node_ontology node on edge.source_node_id = node.id 
--     -> where node.node_type_id = 4;
-- Query OK, 251529 rows affected (37.32 sec)

-- mysql> delete edge from tran_test_202211.comb_edge_node edge
--     -> inner join tran_test_202211.comb_node_ontology node on edge.target_node_id = node.id 
--     -> where node.node_type_id = 4;
-- Query OK, 251529 rows affected (34.92 sec)

-- edge count 
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- | count(edge.id) | type_id | type_name                 | type_id | type_name                 | type_name                              | study_id |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- |          31140 |       1 | biolink:Disease           |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |          31140 |       2 | biolink:Gene              |       1 | biolink:Disease           | biolink:gene_associated_with_condition |        1 |
-- |         178472 |       2 | biolink:Gene              |       3 | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        1 |
-- |         178472 |       3 | biolink:PhenotypicFeature |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- +----------------+------

-- insert new pathway/phenotype edges
-- mysql> insert into tran_test_202211.comb_edge_node 
--     -> (edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id) 
--     ->     select concat('magma_', pathway.ontology_id, '_', phenotype.ontology_id) as edge_id, 
--     ->     6, pathway.id, phenotype.id, 
--     ->     up_path_assoc.p_value, 8, 1
--     ->     from tran_upkeep.agg_pathway_phenotype up_path_assoc, tran_test_202211.comb_node_ontology pathway, tran_test_202211.comb_node_ontology phenotype, 
--     ->       tran_upkeep.data_pathway up_path
--     ->     where up_path_assoc.pathway_code = up_path.pathway_code
--     ->     and up_path.ontology_id collate utf8mb4_unicode_ci = pathway.ontology_id and pathway.node_type_id = 4 and pathway.ontology_id is not null
--     ->     and up_path_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
--     ->     and up_path_assoc.p_value <= 0.05
--     ->     order by phenotype.node_code, pathway.node_code;
-- Query OK, 239891 rows affected (1 min 52.15 sec)
-- Records: 239891  Duplicates: 0  Warnings: 0

-- mysql> insert into tran_test_202211.comb_edge_node 
--     -> (edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id) 
--     ->     select concat('magma_', phenotype.ontology_id, '_', pathway.ontology_id) as edge_id, 
--     ->     6, phenotype.id, pathway.id, 
--     ->     up_path_assoc.p_value, 8, 1
--     ->     from tran_upkeep.agg_pathway_phenotype up_path_assoc, tran_test_202211.comb_node_ontology pathway, tran_test_202211.comb_node_ontology phenotype, 
--     ->       tran_upkeep.data_pathway up_path
--     ->     where up_path_assoc.pathway_code = up_path.pathway_code
--     ->     and up_path.ontology_id collate utf8mb4_unicode_ci = pathway.ontology_id and pathway.node_type_id = 4 and pathway.ontology_id is not null
--     ->     and up_path_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
--     ->     and up_path_assoc.p_value <= 0.05
--     ->     order by phenotype.node_code, pathway.node_code;
-- Query OK, 239891 rows affected (1 min 54.61 sec)
-- Records: 239891  Duplicates: 0  Warnings: 0

-- post pathway load edge counts
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- | count(edge.id) | type_id | type_name                 | type_id | type_name                 | type_name                              | study_id |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- |          31140 |       1 | biolink:Disease           |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |          80179 |       1 | biolink:Disease           |       4 | biolink:Pathway           | biolink:genetic_association            |        1 |
-- |          31140 |       2 | biolink:Gene              |       1 | biolink:Disease           | biolink:gene_associated_with_condition |        1 |
-- |         178472 |       2 | biolink:Gene              |       3 | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        1 |
-- |          80179 |       4 | biolink:Pathway           |       1 | biolink:Disease           | biolink:genetic_association            |        1 |
-- |         159712 |       4 | biolink:Pathway           |       3 | biolink:PhenotypicFeature | biolink:genetic_association            |        1 |
-- |         178472 |       3 | biolink:PhenotypicFeature |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |         159712 |       3 | biolink:PhenotypicFeature |       4 | biolink:Pathway           | biolink:genetic_association            |        1 |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- 8 rows in set (5.87 sec)






