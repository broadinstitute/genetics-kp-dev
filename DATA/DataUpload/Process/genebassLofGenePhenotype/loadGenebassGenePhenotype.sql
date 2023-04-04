

-- reports pre load, post load
select count(edge.id) as edge_count, source_type.type_name, target_type.type_name, edge_type.type_name, study.study_name, study.study_id
from comb_edge_node edge, comb_node_ontology source, comb_node_ontology target, comb_lookup_type edge_type,
    comb_lookup_type source_type, comb_lookup_type target_type, comb_study_type study
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = study.study_id and study.study_id = 17
group by edge_type.type_name, source_type.type_name, target_type.type_name, study.study_name
order by source_type.type_name, target_type.type_name, edge_type.type_name;


-- delete from production tables 
delete from comb_edge_node where study_id = 17;

-- load data 
-- only load with probability > 0.15 
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


-- history 
-- 20230303 - reload of genebass with pValue, beta, abf prob, standard error  
-- pre deletion
-- +------------+---------------------------+---------------------------+----------------------------------------+------------+----------+
-- | edge_count | type_name                 | type_name                 | type_name                              | study_name | study_id |
-- +------------+---------------------------+---------------------------+----------------------------------------+------------+----------+
-- |      12568 | biolink:Disease           | biolink:Gene              | biolink:condition_associated_with_gene | GeneBass   |       17 |
-- |      12568 | biolink:Gene              | biolink:Disease           | biolink:gene_associated_with_condition | GeneBass   |       17 |
-- |       4591 | biolink:Gene              | biolink:PhenotypicFeature | biolink:gene_associated_with_condition | GeneBass   |       17 |
-- |       4591 | biolink:PhenotypicFeature | biolink:Gene              | biolink:condition_associated_with_gene | GeneBass   |       17 |
-- +------------+---------------------------+---------------------------+----------------------------------------+------------+----------+
-- post deletion

-- post reload 







-- scratch
select distinct concat('genebass_', gb.id), so.id, ta.id, 10, gb.probability, 9, 17, gb.probability,
    gb.pvalue, gb.beta, gb.standard_error, gb.probability
from tran_upkeep.data_genebass_gene_phenotype gb, comb_node_ontology so, comb_node_ontology ta
where gb.gene_ncbi_id COLLATE utf8mb4_unicode_ci = ta.ontology_id
and gb.phenotype_ontology_id COLLATE utf8mb4_unicode_ci = so.ontology_id 
and ta.node_type_id = 2 and so.node_type_id in (1, 3) 
and gb.probability >= 0.15;


select gb.id, gb.probability, gb.pvalue, gb.beta, gb.standard_error, gb.gene_ncbi_id, gb.phenotype_ontology_id
from tran_upkeep.data_genebass_gene_phenotype gb 
where gb.probability > 0.15 
limit 30;

select gb.id, gb.probability, gb.pvalue, gb.beta, gb.standard_error, gb.gene_ncbi_id, gb.phenotype_ontology_id
from tran_dataload.data_genebass_gene_phenotype_good_prob gb 
where gb.probability > 0.15 
limit 30;


update tran_upkeep.data_genebass_gene_phenotype gb
      join tran_test_202303.comb_node_ontology node on node.node_code COLLATE utf8mb4_general_ci = gb.gene
      set gb.gene_ncbi_id = node.ontology_id 
      where gb.probability > 0.50 and node.node_type_id = 2 and gb.gene_ncbi_id is null;
