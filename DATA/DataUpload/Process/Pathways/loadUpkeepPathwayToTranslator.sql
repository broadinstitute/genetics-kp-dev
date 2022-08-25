

-- need to change all to utf8mb4_unicode_ci

-- load the pathways to the translator tables
-- only load those with ontology ids
insert into tran_test_202209.comb_node_ontology
(node_code, node_type_id, ontology_id, ontology_type_id, node_name, added_by_study_id)
select up_path.pathway_code, 4, up_path.ontology_id, ont_type.ontology_id, up_path.pathway_name, 1
from tran_upkeep.data_pathway up_path, tran_test_202209.comb_ontology_type ont_type
where SUBSTRING_INDEX(SUBSTRING_INDEX(up_path.ontology_id, ':', 1), ' ', -1) collate utf8mb4_unicode_ci = ont_type.prefix
and up_path.ontology_id collate utf8mb4_unicode_ci not in (select ontology_id from tran_test_202209.comb_node_ontology where node_type_id = 4)
and up_path.ontology_id is not null;


-- reload the genes into the comb_pathway_gene table
-- delete/drop

-- load


-- for pathway gene loading 
-- see creatPathwayGeneTable.sql in sql creative directory
-- query to populate the pathway gene table
insert into comb_pathway_gene (gene_node_id, pathway_node_id, gene_ontology_id, pathway_ontology_id, gene_code)
select gene.id as gene_id, pathway.id as pathway_id, gene.ontology_id, pathway.ontology_id, gene.node_code
from tran_upkeep.data_pathway data_path, tran_upkeep.data_pathway_genes data_path_gene, 
    comb_node_ontology gene, comb_node_ontology pathway
where data_path.id = data_path_gene.pathway_id 
    and pathway.node_type_id = 4 and gene.node_type_id = 2
    and data_path.ontology_id = pathway.ontology_id COLLATE utf8mb4_general_ci
    and data_path_gene.gene_code = gene.node_code COLLATE utf8mb4_general_ci;
    
limit 20;





-- debug
select count(up_path.pathway_code), SUBSTRING_INDEX(SUBSTRING_INDEX(up_path.ontology_id, ':', 1), ' ', -1) as prefix
from tran_upkeep.data_pathway up_path, tran_test_202209.comb_ontology_type ont_type
where SUBSTRING_INDEX(SUBSTRING_INDEX(up_path.ontology_id, ':', 1), ' ', -1) collate utf8mb4_unicode_ci = ont_type.prefix
and up_path.ontology_id collate utf8mb4_unicode_ci not in (select ontology_id from tran_test_202209.comb_node_ontology where node_type_id = 4)
group by SUBSTRING_INDEX(SUBSTRING_INDEX(up_path.ontology_id, ':', 1), ' ', -1);

select count(up_path.pathway_code)
from tran_upkeep.data_pathway up_path, tran_test_202209.comb_ontology_type ont_type
where SUBSTRING_INDEX(SUBSTRING_INDEX(up_path.ontology_id, ':', 1), ' ', -1) collate utf8mb4_unicode_ci = ont_type.prefix
and up_path.ontology_id collate utf8mb4_unicode_ci not in (select ontology_id from tran_test_202209.comb_node_ontology where node_type_id = 4);

select distinct gene_code
from tran_upkeep.data_pathway_genes up_gene, tran_upkeep.data_pathway up_pathway
where up_gene.pathway_id = up_pathway.id 
and up_pathway.ontology_id is not null
and up_gene.gene_code collate utf8mb4_unicode_ci not in (select node_code from tran_test_202209.comb_node_ontology where node_type_id = 2)
order by gene_code;
