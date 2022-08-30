



select concat(path_disease.id, '_', gene_disease.id, '_', drug_gene.id, '_', pathway_gene.id) as result_id,
    pathway.ontology_id as pathway, pathway.node_name as pathway_name, 
    gene.ontology_id as gene, gene.node_name as gene_name,
    disease.ontology_id as disease, disease.node_name as disease_name,
    path_disease.score as pathway_score, gene_disease.score as gene_score, 
    drug_gene.drug_ontology_id as drug, drug_gene.drug_name, drug_gene.drug_category_biolink_id as drug_category,
    drug_gene.predicate_biolink_id as gene_drug_predicate,
    drug_gene.id as drug_gene_row_id, gene_disease.id as gene_disease_row_id, 
    pathway_gene.id as path_gene_row_id, path_disease.id as path_disease_row_id
from comb_edge_node path_disease, comb_edge_node gene_disease, 
    comb_node_ontology pathway, comb_node_ontology gene,
    comb_node_ontology disease,
    comb_pathway_gene pathway_gene,
    infe_drug_gene drug_gene
where path_disease.source_node_id = pathway.id and path_disease.target_node_id = disease.id 
    and gene_disease.source_node_id = gene.id and gene_disease.target_node_id = disease.id
    and pathway.node_type_id = 4 and gene.node_type_id = 2 and disease.node_type_id = 1
    and path_disease.score < 0.0005 and (gene_disease.score < 0.000006 or gene_disease.score_translator > 0.7)
    and pathway_gene.gene_node_id = gene.id and pathway_gene.pathway_node_id = pathway.id
    and gene.id = drug_gene.gene_node_id
     and disease.ontology_id in (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  
order by path_disease.score, gene_disease.score  limit 500

-- 20220826 - changes to make query faster in light of new pathway data
-- + add node ontology_id index - need to ontolgy in query
-- * add edge score_translator index, NO, only use magma
-- - add edge study_id index
-- + changed scroe translator to 0.7 from 0.1 (could exclude to magma study only an not use this)
-- + changed pathway assoc pvalue limit to 0.0005 from 0.005

-- hypertension MONDO:0005044
-- , parameters: ['MONDO:0029132', 'MONDO:0005044', 'MONDO:0007211', 'MONDO:0007772', 'MONDO:0017147', 'MONDO:0024533', 'MONDO:0014135', 'MONDO:0008078', 'MONDO:0008347', 'MONDO:0013817', 'MONDO:0020854', 'MONDO:0012266', 'MONDO:0001134', 'MONDO:0009937', 'MONDO:0015924', 'MONDO:0018975', 'MONDO:0020607', 'MONDO:0013782', 'MONDO:0011309', 'MONDO:0009025', 'MONDO:0013777', 'MONDO:0013781', 'MONDO:0007781', 'MONDO:0008678', 'MONDO:0013778', 'MONDO:0017148']

-- revisit after gene association upload
-- MONDO:005300
-- parameters: ['MONDO:0005443', 'MONDO:0005016', 'MONDO:0005300']



select concat(path_disease.id, '_', gene_disease.id, '_', drug_gene.id, '_', pathway_gene.id) as result_id,
    pathway.ontology_id as pathway, pathway.node_name as pathway_name, 
    gene.ontology_id as gene, gene.node_name as gene_name,
    disease.ontology_id as disease, disease.node_name as disease_name,
    path_disease.score as pathway_score, gene_disease.score as gene_score, 
    drug_gene.drug_ontology_id as drug, drug_gene.drug_name, drug_gene.drug_category_biolink_id as drug_category,
    drug_gene.predicate_biolink_id as gene_drug_predicate,
    drug_gene.id as drug_gene_row_id, gene_disease.id as gene_disease_row_id, 
    pathway_gene.id as path_gene_row_id, path_disease.id as path_disease_row_id
from comb_edge_node path_disease, comb_edge_node gene_disease, 
    comb_node_ontology pathway, comb_node_ontology gene,
    comb_node_ontology disease,
    comb_pathway_gene pathway_gene,
    infe_drug_gene drug_gene
where path_disease.source_node_id = pathway.id and path_disease.target_node_id = disease.id 
    and gene_disease.source_node_id = gene.id and gene_disease.target_node_id = disease.id
    and pathway.node_type_id = 4 and gene.node_type_id = 2 
    and path_disease.score < 0.00005 and gene_disease.score < 0.000006 
    and pathway_gene.gene_node_id = gene.id and pathway_gene.pathway_node_id = pathway.id
    and gene.id = drug_gene.gene_node_id
     and disease.ontology_id in ('MONDO:0029132', 'MONDO:0005044', 'MONDO:0007211', 'MONDO:0007772', 'MONDO:0017147', 'MONDO:0024533', 'MONDO:0014135', 
     'MONDO:0008078', 'MONDO:0008347', 'MONDO:0013817', 'MONDO:0020854', 'MONDO:0012266', 'MONDO:0001134', 'MONDO:0009937', 'MONDO:0015924', 
     'MONDO:0018975', 'MONDO:0020607', 'MONDO:0013782', 'MONDO:0011309', 'MONDO:0009025', 'MONDO:0013777', 'MONDO:0013781', 'MONDO:0007781', 
     'MONDO:0008678', 'MONDO:0013778', 'MONDO:0017148');
order by path_disease.score, gene_disease.score;

    -- and pathway.node_type_id = 4 and gene.node_type_id = 2 and disease.node_type_id = 1
    -- and path_disease.score < 0.0005 and gene_disease.score < 0.000006 and gene_disease.study_id = 1  
    -- and path_disease.score < 0.0005 and (gene_disease.score < 0.000006 or gene_disease.score_translator > 0.7)


-- count edges based on pathway assocaitions
select count(path_disease.id)
from comb_edge_node path_disease, comb_node_ontology pathway 
where path_disease.source_node_id = pathway.id and pathway.node_type_id = 4
and path_disease.score < 0.0005;


-- for 0.0005, get 234 diseases, 8582 pathways
-- for 0.00005, get 219 diseases, 4735 pathways

select count(distinct path_disease.source_node_id)
from comb_edge_node path_disease, comb_node_ontology pathway 
where path_disease.source_node_id = pathway.id and pathway.node_type_id = 4
and path_disease.score < 0.00005;

select count(distinct path_disease.target_node_id)
from comb_edge_node path_disease, comb_node_ontology pathway 
where path_disease.source_node_id = pathway.id and pathway.node_type_id = 4
and path_disease.score < 0.00005;


select path_disease.id, gene_disease.id, pathway.ontology_id, gene.ontology_id, disease.ontology_id, gene_disease.score, path_disease.score
from comb_edge_node path_disease, comb_edge_node gene_disease, 
    comb_node_ontology pathway, comb_node_ontology gene,
    comb_node_ontology disease,
    comb_pathway_gene pathway_gene
where path_disease.source_node_id = pathway.id and path_disease.target_node_id = disease.id 
    and gene_disease.source_node_id = gene.id and gene_disease.target_node_id = disease.id
    and pathway.node_type_id = 4 and gene.node_type_id = 2 
    and path_disease.score < 0.000006 and gene_disease.score < 0.000006 and gene_disease.study_id = 1  
    and pathway_gene.gene_node_id = gene.id and pathway_gene.pathway_node_id = pathway.id
     and disease.ontology_id in ('MONDO:0029132', 'MONDO:0005044', 'MONDO:0007211', 'MONDO:0007772', 'MONDO:0017147', 'MONDO:0024533', 'MONDO:0014135', 
     'MONDO:0008078', 'MONDO:0008347', 'MONDO:0013817', 'MONDO:0020854', 'MONDO:0012266', 'MONDO:0001134', 'MONDO:0009937', 'MONDO:0015924', 
     'MONDO:0018975', 'MONDO:0020607', 'MONDO:0013782', 'MONDO:0011309', 'MONDO:0009025', 'MONDO:0013777', 'MONDO:0013781', 'MONDO:0007781', 
     'MONDO:0008678', 'MONDO:0013778', 'MONDO:0017148')
order by gene_disease.score, path_disease.score;



