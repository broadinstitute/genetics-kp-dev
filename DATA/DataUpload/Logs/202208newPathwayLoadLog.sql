

-- steps taken
-- 1 - add new ontologies to comb_ontology_type table -> see lookupTables.sql
-- 2 - loaded new pathways that were not in the comb_node_ontology tables already -> see loadUpkeepPathwayToTranslator.sql
-- TODO 3 - load pathway genes
-- TODO 4 - load new phenotypes not already in the comb_node_ontology tables
-- TODO 5 - load pathway associations
-- TODO 6 - load gene associations

select count(a.id), b.ontology_name, c.type_name
from comb_node_ontology a, comb_ontology_type b, comb_lookup_type c
where a.ontology_type_id = b.ontology_id
and a.node_type_id = c.type_id
group by b.ontology_name, c.type_name
order by b.ontology_name, c.type_name;

-- pre pathway load
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

