


-- using the new druge_gene table and the new pathway genes table
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
    and path_disease.score < 0.005 and (gene_disease.score < 0.000006 or gene_disease.score_translator > 0.1)
    and disease.ontology_id = 'MONDO:0004975'
    and pathway_gene.gene_node_id = gene.id and pathway_gene.pathway_node_id = pathway.id
    and gene.ontology_id = drug_gene.gene_ontology_id
    order by path_disease.score, gene_disease.score
    limit 500;


-- DEBUG
select concat(path_disease.id, '_', gene_disease.id, '_', drug_gene.id, '_', pathway_gene.id) as result_id,
    gene.ontology_id as gene, gene.node_name as gene_name,
    disease.ontology_id as disease, disease.node_name as disease_name
from comb_edge_node path_disease, comb_edge_node gene_disease, 
    comb_node_ontology pathway, comb_node_ontology gene,
    comb_node_ontology disease,
    comb_pathway_gene pathway_gene,
    infe_drug_gene drug_gene
where path_disease.source_node_id = pathway.id and path_disease.target_node_id = disease.id 
    and gene_disease.source_node_id = gene.id and gene_disease.target_node_id = disease.id
    and pathway.node_type_id = 4 and gene.node_type_id = 2 and disease.node_type_id = 1
    and path_disease.score < 0.005 and (gene_disease.score < 0.000006 or gene_disease.score_translator > 0.1)
    and disease.ontology_id = 'MONDO:0004975'
    and pathway_gene.gene_node_id = gene.id and pathway_gene.pathway_node_id = pathway.id
    and gene.ontology_id = drug_gene.gene_ontology_id
    order by path_disease.score, gene_disease.score
    limit 500;


-- using the new pathway genes table
select pathway.ontology_id as pathway, gene.ontology_id as gene, disease.ontology_id as disease,
    path_disease.score as pathway_score, gene_disease.score as gene_score
from comb_edge_node path_disease, comb_edge_node gene_disease, 
    comb_node_ontology pathway, comb_node_ontology gene,
    comb_node_ontology disease,
    comb_pathway_gene pathway_gene
where path_disease.source_node_id = pathway.id and path_disease.target_node_id = disease.id 
    and gene_disease.source_node_id = gene.id and gene_disease.target_node_id = disease.id
    and pathway.node_type_id = 4 and gene.node_type_id = 2 and disease.node_type_id = 1
    and path_disease.score < 0.005 and gene_disease.score < 0.000006
    and disease.ontology_id = 'MONDO:0004975'
    and pathway_gene.gene_node_id = gene.id and pathway_gene.pathway_node_id = pathway.id
    order by path_disease.score, gene_disease.score
    limit 500;


-- adding in pathways and genes
select pathway.ontology_id as pathway, gene.ontology_id as gene, disease.ontology_id as disease,
    path_disease.score as pathway_score, gene_disease.score as gene_score
from comb_edge_node path_disease, comb_edge_node gene_disease, 
    comb_node_ontology pathway, comb_node_ontology gene,
    comb_node_ontology disease,
    tran_upkeep.data_pathway_genes as pathway_gene, tran_upkeep.data_pathway data_path
where path_disease.source_node_id = pathway.id and path_disease.target_node_id = disease.id 
    and gene_disease.source_node_id = gene.id and gene_disease.target_node_id = disease.id
    and pathway.node_type_id = 4 and gene.node_type_id = 2 and disease.node_type_id = 1
    and path_disease.score < 0.05 and gene_disease.score < 0.000006
    and disease.ontology_id = 'MONDO:0005148'
    and pathway_gene.pathway_id = data_path.id and data_path.pathway_code = pathway.ontology_id COLLATE utf8mb4_general_ci
    and pathway_gene.gene_code = gene.node_code COLLATE utf8mb4_general_ci
    order by gene_disease.score, path_disease.score
    limit 5;

-- select data
select pathway.ontology_id as pathway, gene.ontology_id as gene, disease.ontology_id as disease,
    path_disease.score as pathway_score, gene_disease.score as gene_score
from comb_edge_node path_disease, comb_edge_node gene_disease, 
    comb_node_ontology pathway, comb_node_ontology gene,
    comb_node_ontology disease
where path_disease.source_node_id = pathway.id and path_disease.target_node_id = disease.id 
    and gene_disease.source_node_id = gene.id and gene_disease.target_node_id = disease.id
    and pathway.node_type_id = 4 and gene.node_type_id = 2 and disease.node_type_id = 1
    and path_disease.score < 0.05 and gene_disease.score < 0.000006
    and disease.ontology_id = 'MONDO:0005148'
    order by gene_disease.score, path_disease.score
    limit 5;








-- 
