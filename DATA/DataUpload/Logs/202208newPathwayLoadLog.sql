

-- steps taken
-- 1 - load new phenotypes not already in the comb_node_ontology tables
-- 2 - add new ontologies to comb_ontology_type table -> see lookupTables.sql
-- 3 - loaded new pathways that were not in the comb_node_ontology tables already -> see loadUpkeepPathwayToTranslator.sql
-- 4 - load pathway genes
-- 5 - load pathway associations
-- 6 - load gene associations



select count(edge.id), source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id
from comb_edge_node edge, comb_node_ontology source, comb_node_ontology target, comb_lookup_type edge_type,
    comb_lookup_type source_type, comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = 1
group by edge_type.type_name, source_type.type_name, target_type.type_name, edge.study_id
order by source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id;

-- post adding in new gene/phenotype assoctiations with pVaue <= 0.0025
-- added as gene subject - Records: 193414  Duplicates: 0  Warnings: 0
-- added as gene target - Records: 193414  Duplicates: 0  Warnings: 0

-- +----------------+---------------------------+---------------------------+----------------------------------------+----------+
-- | count(edge.id) | type_name                 | type_name                 | type_name                              | study_id |
-- +----------------+---------------------------+---------------------------+----------------------------------------+----------+
-- |          27166 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |         114410 | biolink:Disease           | biolink:Pathway           | biolink:genetic_association            |        1 |
-- |          27166 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        1 |
-- |         166248 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        1 |
-- |         114410 | biolink:Pathway           | biolink:Disease           | biolink:genetic_association            |        1 |
-- |         246113 | biolink:Pathway           | biolink:PhenotypicFeature | biolink:genetic_association            |        1 |
-- |         166248 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |         246113 | biolink:PhenotypicFeature | biolink:Pathway           | biolink:genetic_association            |        1 |
-- +----------------+---------------------------+---------------------------+----------------------------------------+----------+
-- 8 rows in set (6.14 sec)


-- post gene study 1 assocations deleted (both subject and target)
-- +----------------+---------------------------+---------------------------+-----------------------------+----------+
-- | count(edge.id) | type_name                 | type_name                 | type_name                   | study_id |
-- +----------------+---------------------------+---------------------------+-----------------------------+----------+
-- |         114410 | biolink:Disease           | biolink:Pathway           | biolink:genetic_association |        1 |
-- |         114410 | biolink:Pathway           | biolink:Disease           | biolink:genetic_association |        1 |
-- |         246113 | biolink:Pathway           | biolink:PhenotypicFeature | biolink:genetic_association |        1 |
-- |         246113 | biolink:PhenotypicFeature | biolink:Pathway           | biolink:genetic_association |        1 |
-- +----------------+---------------------------+---------------------------+-----------------------------+----------+
-- 4 rows in set (2.57 sec)


-- deleting gene source, expect 26,505 + 133,409 = 159,914
-- go Query OK, 211621 rows affected (33.74 sec) - assume more due to unlinked rows - GOT ORE DUE TO NODE TYPE 12 (DELETED NOW)
-- Query OK, 211621 rows affected (29.75 sec) - for gene as target in study 1

-- +----------------+---------------------------+---------------------------+----------------------------------------+----------+
-- | count(edge.id) | type_name                 | type_name                 | type_name                              | study_id |
-- +----------------+---------------------------+---------------------------+----------------------------------------+----------+
-- |          26505 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |         114410 | biolink:Disease           | biolink:Pathway           | biolink:genetic_association            |        1 |
-- |          26505 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        1 |
-- |         133409 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        1 |
-- |         114410 | biolink:Pathway           | biolink:Disease           | biolink:genetic_association            |        1 |
-- |         246113 | biolink:Pathway           | biolink:PhenotypicFeature | biolink:genetic_association            |        1 |
-- |         133409 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |         246113 | biolink:PhenotypicFeature | biolink:Pathway           | biolink:genetic_association            |        1 |
-- +----------------+---------------------------+---------------------------+----------------------------------------+----------+
-- 8 rows in set (6.56 sec)



select count(edge.id) as edge_count, source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id
from comb_edge_node edge, comb_node_ontology source, comb_node_ontology target, comb_lookup_type edge_type,
    comb_lookup_type source_type, comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
group by edge_type.type_name, source_type.type_name, target_type.type_name, edge.study_id
order by source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id;

-- post addition of pathway associations
-- +------------+---------------------------+---------------------------+----------------------------------------+----------+
-- | edge_count | type_name                 | type_name                 | type_name                              | study_id |
-- +------------+---------------------------+---------------------------+----------------------------------------+----------+
-- |      26505 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |       3824 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        4 |
-- |       1105 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        5 |
-- |       4580 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        6 |
-- |       6378 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |        7 |
-- |      12568 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |       17 |
-- |     114410 | biolink:Disease           | biolink:Pathway           | biolink:genetic_association            |        1 |
-- |      26505 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        1 |
-- |       3824 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        4 |
-- |       1112 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        5 |
-- |       4580 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        6 |
-- |       6378 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |        7 |
-- |      12568 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |       17 |
-- |     133409 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        1 |
-- |      32284 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |        4 |
-- |       4591 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |       17 |
-- |     114410 | biolink:Pathway           | biolink:Disease           | biolink:genetic_association            |        1 |
-- |     246113 | biolink:Pathway           | biolink:PhenotypicFeature | biolink:genetic_association            |        1 |
-- |     133409 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |        1 |
-- |      32284 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |        4 |
-- |       4591 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |       17 |
-- |     246113 | biolink:PhenotypicFeature | biolink:Pathway           | biolink:genetic_association            |        1 |
-- +------------+---------------------------+---------------------------+----------------------------------------+----------+
-- 22 rows in set (10.73 sec)




select count(edge.id) as edge_count, source_type.type_name, target_type.type_name, edge_type.type_name
from comb_edge_node edge, comb_node_ontology source, comb_node_ontology target, comb_lookup_type edge_type,
    comb_lookup_type source_type, comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
group by edge_type.type_name, source_type.type_name, target_type.type_name
order by source_type.type_name, target_type.type_name, edge_type.type_name;

-- post payhway insertions
-- get 360523 rows affected (32.54 sec) as pathway source
-- get 360523 rows affected (32.98 sec) as pathway target
-- +------------+---------------------------+---------------------------+----------------------------------------+
-- | edge_count | type_name                 | type_name                 | type_name                              |
-- +------------+---------------------------+---------------------------+----------------------------------------+
-- |      54960 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |
-- |     114410 | biolink:Disease           | biolink:Pathway           | biolink:genetic_association            |
-- |      54967 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |
-- |     170284 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |
-- |     114410 | biolink:Pathway           | biolink:Disease           | biolink:genetic_association            |
-- |     246113 | biolink:Pathway           | biolink:PhenotypicFeature | biolink:genetic_association            |
-- |     170284 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |
-- |     246113 | biolink:PhenotypicFeature | biolink:Pathway           | biolink:genetic_association            |
-- +------------+---------------------------+---------------------------+----------------------------------------+
-- 8 rows in set (7.84 sec)


-- post pathway association deletions
-- expected 43768 deletions for source node, same for arget node
-- +------------+---------------------------+---------------------------+----------------------------------------+
-- | edge_count | type_name                 | type_name                 | type_name                              |
-- +------------+---------------------------+---------------------------+----------------------------------------+
-- |      54960 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |
-- |      54967 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |
-- |     170284 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |
-- |     170284 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |
-- +------------+---------------------------+---------------------------+----------------------------------------+

-- pre deletion of old pathway/phenotype associations
-- +------------+---------------------------+---------------------------+----------------------------------------+
-- | edge_count | type_name                 | type_name                 | type_name                              |
-- +------------+---------------------------+---------------------------+----------------------------------------+
-- |      54960 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene |
-- |      12365 | biolink:Disease           | biolink:Pathway           | biolink:genetic_association            |
-- |      54967 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition |
-- |     170284 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition |
-- |      12365 | biolink:Pathway           | biolink:Disease           | biolink:genetic_association            |
-- |      31403 | biolink:Pathway           | biolink:PhenotypicFeature | biolink:genetic_association            |
-- |     170284 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene |
-- |      31403 | biolink:PhenotypicFeature | biolink:Pathway           | biolink:genetic_association            |
-- +------------+---------------------------+---------------------------+----------------------------------------+
-- 8 rows in set (3.22 sec)





select count(a.id), b.ontology_name, c.type_name
from comb_node_ontology a, comb_ontology_type b, comb_lookup_type c
where a.ontology_type_id = b.ontology_id
and a.node_type_id = c.type_id
group by b.ontology_name, c.type_name
order by b.ontology_name, c.type_name;



-- post new ontology and pathway load
-- +-------------+------------------------------+---------------------------+
-- | count(a.id) | ontology_name                | type_name                 |
-- +-------------+------------------------------+---------------------------+
-- |         292 | Biocarta pathway             | biolink:Pathway           |
-- |           7 | EFO disease/phenotype        | biolink:Disease           |
-- |         152 | EFO disease/phenotype        | biolink:PhenotypicFeature |
-- |       11079 | GO pathway                   | biolink:Pathway           |
-- |        5071 | HP disease/phenotype/pathway | biolink:Pathway           |
-- |          19 | HP disease/phenotype/pathway | biolink:PhenotypicFeature |
-- |         186 | Kegg pathway                 | biolink:Pathway           |
-- |        5702 | MONDO disease/phenotype      | biolink:Disease           |
-- |           2 | MONDO disease/phenotype      | biolink:PhenotypicFeature |
-- |       19500 | NCBI Gene                    | biolink:Gene              |
-- |           1 | NCIT disease/phenotype       | biolink:PhenotypicFeature |
-- |         196 | PID pathway                  | biolink:Pathway           |
-- |        1615 | Reactome pathway             | biolink:Pathway           |
-- |           5 | UMLS disease/phenotype       | biolink:PhenotypicFeature |
-- |         664 | WikiPathway pathway          | biolink:Pathway           |
-- +-------------+------------------------------+---------------------------+
-- 15 rows in set (0.14 sec)


-- post new phenotype load
-- +-------------+-------------------------+---------------------------+
-- | count(a.id) | ontology_name           | type_name                 |
-- +-------------+-------------------------+---------------------------+
-- |           7 | EFO disease/phenotype   | biolink:Disease           |
-- |         152 | EFO disease/phenotype   | biolink:PhenotypicFeature |
-- |        7279 | GO pathway              | biolink:Pathway           |
-- |          19 | HP disease/phenotype    | biolink:PhenotypicFeature |
-- |        5702 | MONDO disease/phenotype | biolink:Disease           |dvn
-- |           5 | UMLS disease/phenotype  | biolink:PhenotypicFeature |
-- +-------------+-------------------------+---------------------------+
-- 9 rows in set (0.11 sec)

-- pre new phenotype load
-- +-------------+-------------------------+---------------------------+
-- | count(a.id) | ontology_name           | type_name                 |
-- +-------------+-------------------------+---------------------------+
-- |           7 | EFO disease/phenotype   | biolink:Disease           |
-- |         148 | EFO disease/phenotype   | biolink:PhenotypicFeature |
-- |        7279 | GO pathway              | biolink:Pathway           |
-- |           3 | HP disease/phenotype    | biolink:PhenotypicFeature |
-- |        5684 | MONDO disease/phenotype | biolink:Disease           |
-- |           2 | MONDO disease/phenotype | biolink:PhenotypicFeature |
-- |       19500 | NCBI Gene               | biolink:Gene              |
-- |           1 | NCIT disease/phenotype  | biolink:PhenotypicFeature |
-- |           3 | UMLS disease/phenotype  | biolink:PhenotypicFeature |
-- +-------------+-------------------------+---------------------------+

-- post pathway load


select count(id) from comb_pathway_gene;

-- post new gene/pathway load 

-- +-----------+
-- | count(id) |
-- +-----------+
-- |   2864203 |
-- +-----------+
-- 1 row in set (0.14 sec)


-- pre new gene load
-- mysql> select count(id) from comb_pathway_gene;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |    530546 |
-- +-----------+
-- 1 row in set (0.06 sec)


