

-- steps taken
-- 1 - load new phenotypes not already in the comb_node_ontology tables
-- 2 - add new ontologies to comb_ontology_type table -> see lookupTables.sql
-- 3 - loaded new pathways that were not in the comb_node_ontology tables already -> see loadUpkeepPathwayToTranslator.sql
-- 4 - load pathway genes
-- 5 - load magma gene associations
-- 6 - load magma pathway associations
-- 7 - reload genebass gene associations
-- 8 - reload 600k gene associations


-- 1 - load new phenotypes not already in the comb_node_ontology tables
--
-- finding ontology_id for new magma phenotypes
select count(id), in_translator 
from tran_upkeep.agg_aggregator_phenotype
group by in_translator;
-- +-----------+---------------+
-- | count(id) | in_translator |
-- +-----------+---------------+
-- |       274 | true          |
-- |       454 | false         |
-- +-----------+---------------+
-- 2 rows in set (0.01 sec)


select count(id), in_translator 
from tran_upkeep.agg_aggregator_phenotype
where ontology_id is not null
group by in_translator;
-- +-----------+---------------+
-- | count(id) | in_translator |
-- +-----------+---------------+
-- |        15 | false         |
-- +-----------+---------------+
-- 1 row in set (0.01 sec)

select id, phenotype_id, phenotype_name, ontology_id, in_translator
from tran_upkeep.agg_aggregator_phenotype
where ontology_id is not null;

-- +------+-------------------+---------------------------------------+---------------+---------------+
-- | id   | phenotype_id      | phenotype_name                        | ontology_id   | in_translator |
-- +------+-------------------+---------------------------------------+---------------+---------------+
-- | 1505 | HDL2chol          | HDL2 cholesterol                      | UMLS:C0018667 | false         |
-- | 1506 | HDL3chol          | HDL3 cholesterol                      | UMLS:C0018668 | false         |
-- | 1729 | BMI_GIANT         | BMI                                   | NCIT:C138901  | false         |
-- | 1730 | HEIGHT_GIANT      | HEIGHT                                | UMLS:C0489786 | false         |
-- | 1756 | THR               | Total hip replacement                 | UMLS:C0040508 | false         |
-- | 1757 | TKR               | Total knee replacement                | UMLS:C0086511 | false         |
-- | 1778 | nonHDL            | Non-HDL cholesterol                   | UMLS:C0729627 | false         |
-- | 1817 | HP-0001939        | Abnormality of metabolism/homeostasis | HP:0001939    | false         |
-- | 1851 | RVEF              | Right ventricular ejection fraction   | UMLS:C0428781 | false         |
-- | 1919 | Cardiomyopathy    | Hypertrophic cardiomyopathy           | MONDO:0005045 | false         |
-- | 1940 | BasoPerc          | Basophil percentage                   | UMLS:C1171402 | false         |
-- | 1942 | DirectBilirubin   | Direct bilirubin                      | UMLS:C0236556 | false         |
-- | 1943 | EosinPerc         | Eosinophil percentage                 | UMLS:C1171399 | false         |
-- | 1948 | ImReticuloFrac    | Immature reticulocyte fraction        | UMLS:C1446165 | false         |
-- | 1950 | LymphoPerc        | Lymphocyte percentage                 | UMLS:C1171404 | false         |
-- | 1952 | MeanSpheredVol    | Mean sphered cell volume              | UMLS:C2360306 | false         |
-- | 1953 | MonoPerc          | Monocyte percentage                   | UMLS:C1171403 | false         |
-- | 1954 | NeutroPerc        | Neutrophil percentage                 | UMLS:C1171400 | false         |
-- | 1955 | NucleatedRedCount | Nucleated red blood cell count        | UMLS:C0455282 | false         |
-- | 1957 | Phosphate         | Phosphate                             | UMLS:C1601799 | false         |
-- | 1959 | PlatDistWidth     | Platelet distribution width           | UMLS:C1318035 | false         |
-- | 1960 | ReticuloCount     | Reticulocyte count                    | UMLS:C1318442 | false         |
-- | 1961 | ReticuloPerc      | Reticulocyte percentage               | UMLS:C1167975 | false         |
-- | 1962 | SHBG              | Sex hormone binding globulin (SHBG)   | UMLS:C0036883 | false         |
-- | 1963 | Testosterone      | Testosterone                          | UMLS:C4721537 | false         |
-- | 1978 | PulseRate         | Pulse rate                            | UMLS:C0232117 | false         |
-- +------+-------------------+---------------------------------------+---------------+---------------+
-- 26 rows in set (0.00 sec)

-- remove GIANT BMI, HEIGHT
update tran_upkeep.agg_aggregator_phenotype set in_translator = 'true' where id in (1729, 1730);


-- new phenotypes from magma are determined based on the aggregator phenotype code, not the ontology_id
insert into tran_test_202303.comb_node_ontology
(node_code, node_type_id, ontology_id, ontology_type_id, node_name, added_by_study_id)
select up_phenotype.phenotype_id, 
(case when SUBSTRING_INDEX(SUBSTRING_INDEX(up_phenotype.ontology_id, ':', 1), ':', -1) = 'MONDO' then 1 else 3 end) as node_type,
up_phenotype.ontology_id, ont_type.ontology_id, up_phenotype.phenotype_name, 1
from tran_upkeep.agg_aggregator_phenotype up_phenotype, tran_test_202303.comb_ontology_type ont_type 
where up_phenotype.ontology_id is not null and up_phenotype.in_translator = 'false' 
and SUBSTRING_INDEX(SUBSTRING_INDEX(up_phenotype.ontology_id, ':', 1), ':', -1) collate utf8mb4_unicode_ci = ont_type.prefix
and up_phenotype.phenotype_id collate utf8mb4_unicode_ci not in (select node_code from tran_test_202303.comb_node_ontology where node_type_id in (1, 3));


-- 2 - add new ontologies to comb_ontology_type table -> see lookupTables.sql
-- NOT NEEDED since no new ontologies

-- 3 - loaded new pathways that were not in the comb_node_ontology tables already -> see loadUpkeepPathwayToTranslator.sql
-- NOT NEEDED since no new pathways

-- 4 - load pathway genes
-- NOT NEEDED since no new pathways


-- 5 - load gene associations
-- pre load
select count(edge.id), source_type.type_id, source_type.type_name, target_type.type_id, target_type.type_name, edge_type.type_name, edge.study_id
from tran_test_202303.comb_edge_node edge, tran_test_202303.comb_node_ontology source, tran_test_202303.comb_node_ontology target, 
    tran_test_202303.comb_lookup_type edge_type,
    tran_test_202303.comb_lookup_type source_type, tran_test_202303.comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = 1
group by edge_type.type_name, source_type.type_id, source_type.type_name, target_type.type_id, target_type.type_name, edge.study_id
order by source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id;
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
-- 8 rows in set (5.58 sec)

-- delete old gene associations
-- delete where gene node type is subject or object and study is magma
delete edge from tran_test_202303.comb_edge_node edge
inner join tran_test_202303.comb_node_ontology node on edge.source_node_id = node.id 
where node.node_type_id = 2 and edge.study_id = 1;
-- Query OK, 209612 rows affected (35.02 sec)

delete edge from tran_test_202303.comb_edge_node edge
inner join tran_test_202303.comb_node_ontology node on edge.target_node_id = node.id 
where node.node_type_id = 2 and edge.study_id = 1;
-- Query OK, 209612 rows affected (36.88 sec)

-- +----------------+---------+---------------------------+---------+---------------------------+-----------------------------+----------+
-- | count(edge.id) | type_id | type_name                 | type_id | type_name                 | type_name                   | study_id |
-- +----------------+---------+---------------------------+---------+---------------------------+-----------------------------+----------+
-- |          80179 |       1 | biolink:Disease           |       4 | biolink:Pathway           | biolink:genetic_association |        1 |
-- |          80179 |       4 | biolink:Pathway           |       1 | biolink:Disease           | biolink:genetic_association |        1 |
-- |         159712 |       4 | biolink:Pathway           |       3 | biolink:PhenotypicFeature | biolink:genetic_association |        1 |
-- |         159712 |       3 | biolink:PhenotypicFeature |       4 | biolink:Pathway           | biolink:genetic_association |        1 |
-- +----------------+---------+---------------------------+---------+---------------------------+-----------------------------+----------+
-- 4 rows in set (4.38 sec)

-- load new gene associations
-- add edge where gene node type is subject
insert into tran_test_202303.comb_edge_node 
(edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id, score_translator, p_value, probability_app_bayes_factor) 
    select concat('magma_', gene.ontology_id, '_', phenotype.ontology_id) as edge_id, 
    5, gene.id, phenotype.id, 
    up_gene_assoc.p_value, 8, 1, up_gene_assoc.abf_probability_combined, up_gene_assoc.p_value, up_gene_assoc.abf_probability_combined
    from tran_upkeep.agg_gene_phenotype up_gene_assoc, tran_test_202303.comb_node_ontology gene, tran_test_202303.comb_node_ontology phenotype
    where up_gene_assoc.gene_code collate utf8mb4_unicode_ci = gene.node_code and gene.node_type_id = 2 and gene.ontology_id is not null
    and up_gene_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
--    and up_gene_assoc.p_value <= 0.0025
    and up_gene_assoc.abf_probability_combined >= 0.1
    order by phenotype.node_code, gene.node_code;
-- Query OK, 291459 rows affected (28.55 sec)
-- Records: 291459  Duplicates: 0  Warnings: 0

-- add edge where gene node type is object
insert into tran_test_202303.comb_edge_node 
(edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id, score_translator, p_value, probability_app_bayes_factor) 
    select concat('magma_', phenotype.ontology_id, '_', gene.ontology_id) as edge_id, 
    10, phenotype.id, gene.id,
    up_gene_assoc.p_value, 8, 1, up_gene_assoc.abf_probability_combined, up_gene_assoc.p_value, up_gene_assoc.abf_probability_combined
    from tran_upkeep.agg_gene_phenotype up_gene_assoc, tran_test_202303.comb_node_ontology gene, tran_test_202303.comb_node_ontology phenotype
    where up_gene_assoc.gene_code collate utf8mb4_unicode_ci = gene.node_code and gene.node_type_id = 2 and gene.ontology_id is not null
    and up_gene_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
--    and up_gene_assoc.p_value <= 0.0025
    and up_gene_assoc.abf_probability_combined >= 0.1
    order by phenotype.node_code, gene.node_code;
-- Query OK, 291459 rows affected (37.34 sec)
-- Records: 291459  Duplicates: 0  Warnings: 0

-- post load 
select count(edge.id), source_type.type_id, source_type.type_name, target_type.type_id, target_type.type_name, edge_type.type_name, edge.study_id
from tran_test_202303.comb_edge_node edge, tran_test_202303.comb_node_ontology source, tran_test_202303.comb_node_ontology target, 
    tran_test_202303.comb_lookup_type edge_type,
    tran_test_202303.comb_lookup_type source_type, tran_test_202303.comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = 1
group by edge_type.type_name, source_type.type_id, source_type.type_name, target_type.type_id, target_type.type_name, edge.study_id
order by source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id;
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- | count(edge.id) | type_id | type_name                 | type_id | type_name                 | type_name                              | study_id |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- |          30900 |       1 | biolink:Disease           |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |          80179 |       1 | biolink:Disease           |       4 | biolink:Pathway           | biolink:genetic_association            |        1 |
-- |          30900 |       2 | biolink:Gene              |       1 | biolink:Disease           | biolink:gene_associated_with_condition |        1 |
-- |         260559 |       2 | biolink:Gene              |       3 | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        1 |
-- |          80179 |       4 | biolink:Pathway           |       1 | biolink:Disease           | biolink:genetic_association            |        1 |
-- |         159712 |       4 | biolink:Pathway           |       3 | biolink:PhenotypicFeature | biolink:genetic_association            |        1 |
-- |         260559 |       3 | biolink:PhenotypicFeature |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |         159712 |       3 | biolink:PhenotypicFeature |       4 | biolink:Pathway           | biolink:genetic_association            |        1 |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- 8 rows in set (8.72 sec)


select count(id) from tran_upkeep.agg_pathway_phenotype2;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |  13179013 |
-- +-----------+
-- 1 row in set (0.83 sec)


-- 6 - load magma pathway associations
-- pre load
select count(edge.id), source_type.type_id, source_type.type_name, target_type.type_id, target_type.type_name, edge_type.type_name, edge.study_id
from tran_test_202303.comb_edge_node edge, tran_test_202303.comb_node_ontology source, tran_test_202303.comb_node_ontology target, 
    tran_test_202303.comb_lookup_type edge_type,
    tran_test_202303.comb_lookup_type source_type, tran_test_202303.comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = 1
group by edge_type.type_name, source_type.type_id, source_type.type_name, target_type.type_id, target_type.type_name, edge.study_id
order by source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id;

-- delete where pathway is subject
delete edge from tran_test_202303.comb_edge_node edge
inner join tran_test_202303.comb_node_ontology node on edge.source_node_id = node.id 
where node.node_type_id = 4;

-- delete where pathway is object
delete edge from tran_test_202303.comb_edge_node edge
inner join tran_test_202303.comb_node_ontology node on edge.target_node_id = node.id 
where node.node_type_id = 4;

-- post deletion
select count(edge.id), source_type.type_id, source_type.type_name, target_type.type_id, target_type.type_name, edge_type.type_name, edge.study_id
from tran_test_202303.comb_edge_node edge, tran_test_202303.comb_node_ontology source, tran_test_202303.comb_node_ontology target, 
    tran_test_202303.comb_lookup_type edge_type,
    tran_test_202303.comb_lookup_type source_type, tran_test_202303.comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = 1
group by edge_type.type_name, source_type.type_id, source_type.type_name, target_type.type_id, target_type.type_name, edge.study_id
order by source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id;

-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- | count(edge.id) | type_id | type_name                 | type_id | type_name                 | type_name                              | study_id |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- |          30900 |       1 | biolink:Disease           |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |          30900 |       2 | biolink:Gene              |       1 | biolink:Disease           | biolink:gene_associated_with_condition |        1 |
-- |         260559 |       2 | biolink:Gene              |       3 | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        1 |
-- |         260559 |       3 | biolink:PhenotypicFeature |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- 4 rows in set (3.69 sec)

-- insert 
-- insert with pathway as subject
insert into tran_test_202303.comb_edge_node 
(edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id) 
    select concat('magma_', pathway.ontology_id, '_', phenotype.ontology_id) as edge_id, 
    6, pathway.id, phenotype.id, 
    up_path_assoc.p_value, 8, 1
    from tran_upkeep.agg_pathway_phenotype2 up_path_assoc, tran_test_202303.comb_node_ontology pathway, tran_test_202303.comb_node_ontology phenotype, 
      tran_upkeep.data_pathway up_path
    where up_path_assoc.pathway_code = up_path.pathway_code
    and up_path.ontology_id collate utf8mb4_unicode_ci = pathway.ontology_id and pathway.node_type_id = 4 and pathway.ontology_id is not null
    and up_path_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
    and up_path_assoc.p_value <= 0.05
    order by phenotype.node_code, pathway.node_code;

-- insert with pathway as target
insert into tran_test_202303.comb_edge_node 
(edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id) 
    select concat('magma_', phenotype.ontology_id, '_', pathway.ontology_id) as edge_id, 
    6, phenotype.id, pathway.id, 
    up_path_assoc.p_value, 8, 1
    from tran_upkeep.agg_pathway_phenotype2 up_path_assoc, tran_test_202303.comb_node_ontology pathway, tran_test_202303.comb_node_ontology phenotype, 
      tran_upkeep.data_pathway up_path
    where up_path_assoc.pathway_code = up_path.pathway_code
    and up_path.ontology_id collate utf8mb4_unicode_ci = pathway.ontology_id and pathway.node_type_id = 4 and pathway.ontology_id is not null
    and up_path_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
    and up_path_assoc.p_value <= 0.05
    order by phenotype.node_code, pathway.node_code;

-- post deletion
select count(edge.id), source_type.type_id, source_type.type_name, target_type.type_id, target_type.type_name, edge_type.type_name, edge.study_id
from tran_test_202303.comb_edge_node edge, tran_test_202303.comb_node_ontology source, tran_test_202303.comb_node_ontology target, 
    tran_test_202303.comb_lookup_type edge_type,
    tran_test_202303.comb_lookup_type source_type, tran_test_202303.comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = 1
group by edge_type.type_name, source_type.type_id, source_type.type_name, target_type.type_id, target_type.type_name, edge.study_id
order by source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id;


-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- | count(edge.id) | type_id | type_name                 | type_id | type_name                 | type_name                              | study_id |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- |          30900 |       1 | biolink:Disease           |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |          76404 |       1 | biolink:Disease           |       4 | biolink:Pathway           | biolink:genetic_association            |        1 |
-- |          30900 |       2 | biolink:Gene              |       1 | biolink:Disease           | biolink:gene_associated_with_condition |        1 |
-- |         260559 |       2 | biolink:Gene              |       3 | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        1 |
-- |          76404 |       4 | biolink:Pathway           |       1 | biolink:Disease           | biolink:genetic_association            |        1 |
-- |         190166 |       4 | biolink:Pathway           |       3 | biolink:PhenotypicFeature | biolink:genetic_association            |        1 |
-- |         260559 |       3 | biolink:PhenotypicFeature |       2 | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |         190166 |       3 | biolink:PhenotypicFeature |       4 | biolink:Pathway           | biolink:genetic_association            |        1 |
-- +----------------+---------+---------------------------+---------+---------------------------+----------------------------------------+----------+
-- 8 rows in set (7.10 sec)



-- 7 - reload genebass gene associations
-- reports pre load
select count(edge.id) as edge_count, source_type.type_name, target_type.type_name, edge_type.type_name, study.study_name, study.study_id
from tran_test_202303.comb_edge_node edge, tran_test_202303.comb_node_ontology source, tran_test_202303.comb_node_ontology target, tran_test_202303.comb_lookup_type edge_type,
    tran_test_202303.comb_lookup_type source_type, tran_test_202303.comb_lookup_type target_type, tran_test_202303.comb_study_type study
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = study.study_id and study.study_id = 17
group by edge_type.type_name, source_type.type_name, target_type.type_name, study.study_name
order by source_type.type_name, target_type.type_name, edge_type.type_name;
-- +------------+---------------------------+---------------------------+----------------------------------------+------------+----------+
-- | edge_count | type_name                 | type_name                 | type_name                              | study_name | study_id |
-- +------------+---------------------------+---------------------------+----------------------------------------+------------+----------+
-- |      12568 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene | GeneBass   |       17 |
-- |      12568 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition | GeneBass   |       17 |
-- |       4591 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition | GeneBass   |       17 |
-- |       4591 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene | GeneBass   |       17 |
-- +------------+---------------------------+---------------------------+----------------------------------------+------------+----------+
-- 4 rows in set (0.22 sec)

-- delete from production tables 
delete from tran_test_202303.comb_edge_node where study_id = 17;

-- reports post deletion
-- Empty set (0.01 sec)

-- insert genebass
-- only load with probability > 0.10
-- insert gene/disease rows
-- edge type 5: gene/disease, score type 9: probability, study_id 17: genebass
insert into tran_test_202303.comb_edge_node 
(edge_id, source_node_id, target_node_id, edge_type_id, score, score_type_id, study_id, score_translator,
    p_value, beta, standard_error, probability_app_bayes_factor)
select distinct concat('genebass_', gb.id), gene.id, phenotype.id, 5, gb.probability, 9, 17, gb.probability,
    gb.pvalue, gb.beta, gb.standard_error, gb.probability
from tran_upkeep.data_genebass_gene_phenotype gb, tran_test_202303.comb_node_ontology phenotype, tran_test_202303.comb_node_ontology gene
where gb.gene_ncbi_id COLLATE utf8mb4_unicode_ci = gene.ontology_id
and gb.phenotype_ontology_id COLLATE utf8mb4_unicode_ci = phenotype.ontology_id 
and gene.node_type_id = 2 and phenotype.node_type_id in (1, 3)
and gb.probability >= 0.10;

-- insert disease/gene rows
-- edge type 10: disease/gene, score type 9: probability, study_id 17: genebass
insert into tran_test_202303.comb_edge_node 
(edge_id, source_node_id, target_node_id, edge_type_id, score, score_type_id, study_id, score_translator, 
    p_value, beta, standard_error, probability_app_bayes_factor)
select distinct concat('genebass_', gb.id), phenotype.id, gene.id, 10, gb.probability, 9, 17, gb.probability,
    gb.pvalue, gb.beta, gb.standard_error, gb.probability
from tran_upkeep.data_genebass_gene_phenotype gb, tran_test_202303.comb_node_ontology phenotype, tran_test_202303.comb_node_ontology gene
where gb.gene_ncbi_id COLLATE utf8mb4_unicode_ci = gene.ontology_id
and gb.phenotype_ontology_id COLLATE utf8mb4_unicode_ci = phenotype.ontology_id 
and gene.node_type_id = 2 and phenotype.node_type_id in (1, 3) 
and gb.probability >= 0.10;

-- post load
-- +------------+---------------------------+---------------------------+----------------------------------------+------------+----------+
-- | edge_count | type_name                 | type_name                 | type_name                              | study_name | study_id |
-- +------------+---------------------------+---------------------------+----------------------------------------+------------+----------+
-- |      19922 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene | GeneBass   |       17 |
-- |      19922 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition | GeneBass   |       17 |
-- |       6839 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition | GeneBass   |       17 |
-- |       6839 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene | GeneBass   |       17 |
-- +------------+---------------------------+---------------------------+----------------------------------------+------------+----------+
-- 4 rows in set (0.26 sec)


-- 8 - reload 600k gene associations
-- delete old 600k gene/phenotype associations
delete edge from tran_test_202303.comb_edge_node edge
where edge.study_id = 18;


-- insert the new rows
insert into tran_test_202303.comb_edge_node 
(edge_id, source_node_id, target_node_id, edge_type_id, score, score_type_id, study_id, has_qualifiers)
values(concat('600k_', %s, '_', %s), %s, %s, %s, %s, 8, %s, 'Y')

-- insert 600k associations with gene as subject 
insert into tran_test_202303.comb_edge_node 
(edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id, score_translator, 
    p_value, probability_app_bayes_factor, beta, standard_error) 
  select concat('600k_', gene.ontology_id, '_', phenotype.ontology_id) as edge_id, 
    5, gene.id, phenotype.id, 
    up_gene_assoc.p_value, 8, 18, up_gene_assoc.probability_calculated, 
    up_gene_assoc.p_value, up_gene_assoc.probability_calculated, up_gene_assoc.beta, up_gene_assoc.std_error
    from tran_upkeep.data_600k_gene_phenotype up_gene_assoc, tran_upkeep.data_600k_phenotype_ontology up_pheno, 
      tran_test_202303.comb_node_ontology gene, tran_test_202303.comb_node_ontology phenotype
    where up_gene_assoc.gene_code collate utf8mb4_unicode_ci = gene.node_code and gene.node_type_id = 2 and gene.ontology_id is not null
    and up_gene_assoc.phenotype_code = up_pheno.phenotype_code and up_gene_assoc.mask = 'LoF_HC'
    and up_pheno.phenotype_ontology_id collate utf8mb4_unicode_ci = phenotype.ontology_id and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
    and up_gene_assoc.probability_calculated >= 0.1;
    -- order by phenotype.node_code, gene.node_code;


-- insert 600k associations with gene as object
insert into tran_test_202303.comb_edge_node 
(edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id, score_translator, 
    p_value, probability_app_bayes_factor, beta, standard_error) 
  select concat('600k_', phenotype.ontology_id, '_',  gene.ontology_id) as edge_id, 
    10, phenotype.id, gene.id,
    up_gene_assoc.p_value, 8, 18, up_gene_assoc.probability_calculated, 
    up_gene_assoc.p_value, up_gene_assoc.probability_calculated, up_gene_assoc.beta, up_gene_assoc.std_error
    from tran_upkeep.data_600k_gene_phenotype up_gene_assoc, tran_upkeep.data_600k_phenotype_ontology up_pheno, 
      tran_test_202303.comb_node_ontology gene, tran_test_202303.comb_node_ontology phenotype
    where up_gene_assoc.gene_code collate utf8mb4_unicode_ci = gene.node_code and gene.node_type_id = 2 and gene.ontology_id is not null
    and up_gene_assoc.phenotype_code = up_pheno.phenotype_code and up_gene_assoc.mask = 'LoF_HC'
    and up_pheno.phenotype_ontology_id collate utf8mb4_unicode_ci = phenotype.ontology_id and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
    and up_gene_assoc.probability_calculated >= 0.1;






-- reports
-- count association rows by triple types and study
select count(edge.id) as edge_count, source_type.type_name, target_type.type_name, edge_type.type_name, study.study_id, study.study_name
from tran_test_202303.comb_edge_node edge, tran_test_202303.comb_node_ontology source, tran_test_202303.comb_node_ontology target, tran_test_202303.comb_lookup_type edge_type,
    tran_test_202303.comb_lookup_type source_type, tran_test_202303.comb_lookup_type target_type, tran_test_202303.comb_study_type study 
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = study.study_id
group by edge_type.type_name, source_type.type_name, target_type.type_name, study.study_id, study.study_name
order by study.study_id, study.study_name, source_type.type_name, target_type.type_name, edge_type.type_name;

-- after magma gene, 600k reload
-- +------------+---------------------------+---------------------------+----------------------------------------+----------+------------------------+
-- | edge_count | type_name                 | type_name                 | type_name                              | study_id | study_name             |
-- +------------+---------------------------+---------------------------+----------------------------------------+----------+------------------------+
-- |      30900 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        1 | Magma                  |
-- |      80179 | biolink:Disease           | biolink:Pathway           | biolink:genetic_association            |        1 | Magma                  |
-- |      30900 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        1 | Magma                  |
-- |     260559 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        1 | Magma                  |
-- |      80179 | biolink:Pathway           | biolink:Disease           | biolink:genetic_association            |        1 | Magma                  |
-- |     159712 | biolink:Pathway           | biolink:PhenotypicFeature | biolink:genetic_association            |        1 | Magma                  |
-- |     260559 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |        1 | Magma                  |
-- |     159712 | biolink:PhenotypicFeature | biolink:Pathway           | biolink:genetic_association            |        1 | Magma                  |
-- |       3824 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        4 | Richards Effector Gene |
-- |       3824 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        4 | Richards Effector Gene |
-- |      32284 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        4 | Richards Effector Gene |
-- |      32284 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |        4 | Richards Effector Gene |
-- |       1105 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        5 | ClinGen                |
-- |       1112 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        5 | ClinGen                |
-- |       4580 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        6 | ClinVar                |
-- |       4580 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        6 | ClinVar                |
-- |       6378 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        7 | genCC                  |
-- |       6378 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        7 | genCC                  |
-- |      12568 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |       17 | GeneBass               |
-- |      12568 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |       17 | GeneBass               |
-- |       4591 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |       17 | GeneBass               |
-- |       4591 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |       17 | GeneBass               |
-- |     751282 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |       18 | 600k Ellinor           |
-- |     751282 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |       18 | 600k Ellinor           |
-- |     335001 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |       18 | 600k Ellinor           |
-- |     335001 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |       18 | 600k Ellinor           |
-- +------------+---------------------------+---------------------------+----------------------------------------+----------+------------------------+
-- 26 rows in set (53.79 sec)

-- +------------+---------------------------+---------------------------+----------------------------------------+----------+------------------------+
-- | edge_count | type_name                 | type_name                 | type_name                              | study_id | study_name             |
-- +------------+---------------------------+---------------------------+----------------------------------------+----------+------------------------+
-- |      30900 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        1 | Magma                  |
-- |      76404 | biolink:Disease           | biolink:Pathway           | biolink:genetic_association            |        1 | Magma                  |
-- |      30900 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        1 | Magma                  |
-- |     260559 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        1 | Magma                  |
-- |      76404 | biolink:Pathway           | biolink:Disease           | biolink:genetic_association            |        1 | Magma                  |
-- |     190166 | biolink:Pathway           | biolink:PhenotypicFeature | biolink:genetic_association            |        1 | Magma                  |
-- |     260559 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |        1 | Magma                  |
-- |     190166 | biolink:PhenotypicFeature | biolink:Pathway           | biolink:genetic_association            |        1 | Magma                  |
-- |       3824 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        4 | Richards Effector Gene |
-- |       3824 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        4 | Richards Effector Gene |
-- |      32284 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        4 | Richards Effector Gene |
-- |      32284 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |        4 | Richards Effector Gene |
-- |       1105 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        5 | ClinGen                |
-- |       1112 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        5 | ClinGen                |
-- |       4580 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        6 | ClinVar                |
-- |       4580 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        6 | ClinVar                |
-- |       6378 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        7 | genCC                  |
-- |       6378 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        7 | genCC                  |
-- |      19922 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |       17 | GeneBass               |
-- |      19922 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |       17 | GeneBass               |
-- |       6839 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |       17 | GeneBass               |
-- |       6839 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |       17 | GeneBass               |
-- |     751282 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |       18 | 600k Ellinor           |
-- |     751282 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |       18 | 600k Ellinor           |
-- |     335001 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |       18 | 600k Ellinor           |
-- |     335001 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |       18 | 600k Ellinor           |
-- +------------+---------------------------+---------------------------+----------------------------------------+----------+------------------------+
-- 26 rows in set (39.85 sec)



