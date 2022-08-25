


-- create the gene/pathway link table from the upkeep schema table 
drop table if exists comb_pathway_gene;
create table comb_pathway_gene (
  id                        int not null auto_increment primary key,
  gene_node_id              int(9) not null,
  pathway_node_id           int(9) not null,
  gene_ontology_id          varchar(250) not null,                        
  pathway_ontology_id       varchar(250) not null,                        
  gene_code                 varchar(100) not null,                        
  last_updated              timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

alter table comb_pathway_gene add index comb_path_gen_path_idx (pathway_node_id);
alter table comb_pathway_gene add index comb_path_gen_gene_idx (gene_node_id);



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


-- old - joined on pathway_code
-- insert into comb_pathway_gene (gene_node_id, pathway_node_id, gene_ontology_id, pathway_ontology_id, gene_code)
-- select gene.id as gene_id, pathway.id as pathway_id, gene.ontology_id, pathway.ontology_id, gene.node_code
-- from tran_upkeep.data_pathway data_path, tran_upkeep.data_pathway_genes data_path_gene, 
--     comb_node_ontology gene, comb_node_ontology pathway
-- where data_path.id = data_path_gene.pathway_id 
--     and pathway.node_type_id = 4 and gene.node_type_id = 2
--     and data_path.pathway_code = pathway.ontology_id COLLATE utf8mb4_general_ci
--     and data_path_gene.gene_code = gene.node_code COLLATE utf8mb4_general_ci 
-- limit 20;

