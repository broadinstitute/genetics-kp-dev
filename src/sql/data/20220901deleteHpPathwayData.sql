


-- delete edges
-- delete edges with HP patwhay source
delete edge from comb_edge_node edge
inner join comb_node_ontology source on edge.source_node_id = source.id 
where source.node_type_id = 4 and source.ontology_type_id = 6;

-- delete edges with HP patwhay target
delete edge from comb_edge_node edge
inner join comb_node_ontology target on edge.target_node_id = target.id 
where target.node_type_id = 4 and target.ontology_type_id = 6;

-- delete pathwway/gene links
delete link from comb_pathway_gene link
inner join comb_node_ontology pathway on link.pathway_node_id = pathway.id
where pathway.node_type_id = 4 and pathway.ontology_type_id = 6;

-- delete pathways
delete from comb_node_ontology node 
where node.node_type_id = 4 and node.ontology_type_id = 6;


-- debug
-- count of pathway edges per ontology type
select count(edge.id), type.ontology_name, type.ontology_id
from comb_node_ontology subject, comb_ontology_type type, comb_edge_node edge
where subject.id = edge.source_node_id and subject.ontology_type_id = type.ontology_id and subject.node_type_id = 4
group by type.ontology_name, type.ontology_id;

-- AFTER
-- +----------------+---------------------+-------------+
-- | count(edge.id) | ontology_name       | ontology_id |
-- +----------------+---------------------+-------------+
-- |         196169 | GO pathway          |           4 |
-- |           6146 | Biocarta pathway    |          10 |
-- |           4118 | Kegg pathway        |          11 |
-- |          28996 | Reactome pathway    |           9 |
-- |          16100 | WikiPathway pathway |          13 |
-- +----------------+---------------------+-------------+
-- 5 rows in set (0.59 sec)

-- BEFORE
-- +----------------+------------------------------+-------------+
-- | count(edge.id) | ontology_name                | ontology_id |
-- +----------------+------------------------------+-------------+
-- |         196169 | GO pathway                   |           4 |
-- |         108994 | HP disease/phenotype/pathway |           6 |
-- |           6146 | Biocarta pathway             |          10 |
-- |           4118 | Kegg pathway                 |          11 |
-- |          28996 | Reactome pathway             |           9 |
-- |          16100 | WikiPathway pathway          |          13 |
-- +----------------+------------------------------+-------------+
-- 6 rows in set (0.80 sec)


-- count pathways by ontology type
select count(node.id), type.ontology_id, type.ontology_name
from comb_node_ontology node, comb_ontology_type type
where node.node_type_id = 4 and node.ontology_type_id = type.ontology_id
group by type.ontology_id, type.ontology_name;

-- +-----------+-------------+------------------------------+
-- | count(id) | ontology_id | ontology_name                |
-- +-----------+-------------+------------------------------+
-- |     11079 |           4 | GO pathway                   |
-- |      5071 |           6 | HP disease/phenotype/pathway |
-- |       292 |          10 | Biocarta pathway             |
-- |       186 |          11 | Kegg pathway                 |
-- |      1615 |           9 | Reactome pathway             |
-- |       664 |          13 | WikiPathway pathway          |
-- +-----------+-------------+------------------------------+
-- 6 rows in set (0.05 sec)

-- count gene/pathway links by ontology type
select count(pgene.id), type.ontology_id, type.ontology_name
from comb_node_ontology node, comb_ontology_type type, comb_pathway_gene pgene
where node.node_type_id = 4 and node.ontology_type_id = type.ontology_id and pgene.pathway_node_id = node.id
group by type.ontology_id, type.ontology_name;

-- AFTER
-- +-----------------+-------------+---------------------+
-- | count(pgene.id) | ontology_id | ontology_name       |
-- +-----------------+-------------+---------------------+
-- |          783015 |           4 | GO pathway          |
-- |            4769 |          10 | Biocarta pathway    |
-- |           12384 |          11 | Kegg pathway        |
-- |           81792 |           9 | Reactome pathway    |
-- |           28640 |          13 | WikiPathway pathway |
-- +-----------------+-------------+---------------------+
-- 5 rows in set (3.67 sec)


-- BEFORE
-- +----------------+-------------+------------------------------+
-- | count(node.id) | ontology_id | ontology_name                |
-- +----------------+-------------+------------------------------+
-- |         783015 |           4 | GO pathway                   |
-- |         396579 |           6 | HP disease/phenotype/pathway |
-- |           4769 |          10 | Biocarta pathway             |
-- |          12384 |          11 | Kegg pathway                 |
-- |          81792 |           9 | Reactome pathway             |
-- |          28640 |          13 | WikiPathway pathway          |
-- +----------------+-------------+------------------------------+
-- 6 rows in set (3.43 sec)

-- count pathways by ontology types
select count(pathway.id), type.ontology_id, type.ontology_name, node_type.type_id, node_type.type_name
from comb_node_ontology pathway, comb_ontology_type type, comb_lookup_type node_type
where pathway.node_type_id = 4 and pathway.ontology_type_id = type.ontology_id and pathway.node_type_id = node_type.type_id
group by type.ontology_id, type.ontology_name, node_type.type_id, node_type.type_name;

-- AFTER
-- +-------------------+-------------+---------------------+---------+-----------------+
-- | count(pathway.id) | ontology_id | ontology_name       | type_id | type_name       |
-- +-------------------+-------------+---------------------+---------+-----------------+
-- |             11079 |           4 | GO pathway          |       4 | biolink:Pathway |
-- |               292 |          10 | Biocarta pathway    |       4 | biolink:Pathway |
-- |               186 |          11 | Kegg pathway        |       4 | biolink:Pathway |
-- |              1615 |           9 | Reactome pathway    |       4 | biolink:Pathway |
-- |               664 |          13 | WikiPathway pathway |       4 | biolink:Pathway |
-- +-------------------+-------------+---------------------+---------+-----------------+
-- 5 rows in set (0.06 sec)



-- BEFORE
-- +-------------------+-------------+------------------------------+---------+-----------------+
-- | count(pathway.id) | ontology_id | ontology_name                | type_id | type_name       |
-- +-------------------+-------------+------------------------------+---------+-----------------+
-- |             11079 |           4 | GO pathway                   |       4 | biolink:Pathway |
-- |              5071 |           6 | HP disease/phenotype/pathway |       4 | biolink:Pathway |
-- |               292 |          10 | Biocarta pathway             |       4 | biolink:Pathway |
-- |               186 |          11 | Kegg pathway                 |       4 | biolink:Pathway |
-- |              1615 |           9 | Reactome pathway             |       4 | biolink:Pathway |
-- |               664 |          13 | WikiPathway pathway          |       4 | biolink:Pathway |
-- +-------------------+-------------+------------------------------+---------+-----------------+
-- 6 rows in set (0.08 sec)


select node_code, ontology_id, ontology_id 
from comb_node_ontology where node_type_id = 4 and ontology_type_id = 6
order by node_code;


-- delete edges
-- HP pathway source
-- mysql> delete edge from comb_edge_node edge
--     -> inner join comb_node_ontology source on edge.source_node_id = source.id 
--     -> where source.node_type_id = 4 and source.ontology_type_id = 6;
-- Query OK, 108994 rows affected (11.34 sec)


-- HP pathway target
-- mysql> delete edge from comb_edge_node edge
--     -> inner join comb_node_ontology target on edge.target_node_id = target.id 
--     -> where target.node_type_id = 4 and target.ontology_type_id = 6;
-- Query OK, 108994 rows affected (13.27 sec)

-- delete pathwway/gene links
-- mysql> delete link from comb_pathway_gene link
--     -> inner join comb_node_ontology pathway on link.pathway_node_id = pathway.id
--     -> where pathway.node_type_id = 4 and pathway.ontology_type_id = 6;
-- Query OK, 396579 rows affected (17.48 sec)

-- delete HP pathways
-- mysql> delete from comb_node_ontology node 
--     -> where node.node_type_id = 4 and node.ontology_type_id = 6;
-- Query OK, 5071 rows affected (0.38 sec)




