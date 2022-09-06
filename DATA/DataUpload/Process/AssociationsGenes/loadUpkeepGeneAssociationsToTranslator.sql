

-- delete old gene associations
-- delete where gene is subject or object
delete edge from comb_edge_node edge
inner join comb_node_ontology node on edge.source_node_id = node.id 
where node.node_type_id = 2 and edge.study_id = 1;

delete edge from comb_edge_node edge
inner join comb_node_ontology node on edge.target_node_id = node.id 
where node.node_type_id = 2 and edge.study_id = 1;

-- insert gene phenotype association
-- add gene as subject
insert into comb_edge_node 
(edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id, score_translator) 
    select concat('magma_', gene.ontology_id, '_', phenotype.ontology_id) as edge_id, 
    5, gene.id, phenotype.id, 
    up_gene_assoc.p_value, 8, 1, 0.15
    from tran_upkeep.agg_gene_phenotype up_gene_assoc, comb_node_ontology gene, comb_node_ontology phenotype
    where up_gene_assoc.gene_code collate utf8mb4_unicode_ci = gene.node_code and gene.node_type_id = 2 and gene.ontology_id is not null
    and up_gene_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
    and up_gene_assoc.p_value <= 0.0025
    order by phenotype.node_code, gene.node_code;

-- add gene as pathway
insert into comb_edge_node 
(edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id, score_translator) 
    select concat('magma_', phenotype.ontology_id, '_', gene.ontology_id) as edge_id, 
    10, phenotype.id, gene.id,
    up_gene_assoc.p_value, 8, 1, 0.15
    from tran_upkeep.agg_gene_phenotype up_gene_assoc, comb_node_ontology gene, comb_node_ontology phenotype
    where up_gene_assoc.gene_code collate utf8mb4_unicode_ci = gene.node_code and gene.node_type_id = 2 and gene.ontology_id is not null
    and up_gene_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
    and up_gene_assoc.p_value <= 0.0025
    order by phenotype.node_code, gene.node_code;




-- queries
select count(distinct gene_code) from agg_gene_phenotype;

select count(distinct gene_code) from agg_gene_phenotype where p_value < 0.05;

select count(id) from tran_upkeep.agg_gene_phenotype where p_value < 0.05;

select count(id) from agg_gene_phenotype;



select count(id) from tran_upkeep.agg_gene_phenotype where p_value <= 0.0025;



select max(score), source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id
from comb_edge_node edge, comb_node_ontology source, comb_node_ontology target, comb_lookup_type edge_type,
    comb_lookup_type source_type, comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = 1
group by edge_type.type_name, source_type.type_name, target_type.type_name, edge.study_id
order by source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id;

select count(edge.id), source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id
from comb_edge_node edge, comb_node_ontology source, comb_node_ontology target, comb_lookup_type edge_type,
    comb_lookup_type source_type, comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = 1
group by edge_type.type_name, source_type.type_name, target_type.type_name, edge.study_id
order by source_type.type_name, target_type.type_name, edge_type.type_name, edge.study_id;



select (edge.id) from comb_edge_node edge, comb_node_ontology node 
where edge.source_node_id = node.id 
and node.node_type_id = 2 and edge.study_id = 1;

select (edge.id) from comb_edge_node edge, comb_node_ontology node 
where edge.target_node_id = node.id 
and node.node_type_id = 2 and edge.study_id = 1;

select count(edge.id) number, subject.node_type_id as subject, target.node_type_id as target, edge.edge_type_id as edge_type, edge.study_id as study
from comb_edge_node edge, comb_node_ontology subject, comb_node_ontology target 
where edge.source_node_id = subject.id and edge.target_node_id = target.id 
and target.node_type_id = 2 and edge.study_id = 1
group by subject.node_type_id, target.node_type_id, edge.edge_type_id, edge.study_id;



select edge.id number, subject.node_type_id as subject, target.node_type_id as target, edge.edge_type_id as edge_type, edge.study_id as study,
subject.ontology_id
from comb_edge_node edge, comb_node_ontology subject, comb_node_ontology target 
where edge.source_node_id = subject.id and edge.target_node_id = target.id 
and target.node_type_id = 2 and edge.study_id = 1 and subject.node_type_id = 12
group by subject.node_type_id, target.node_type_id, edge.edge_type_id, edge.study_id;



-- get count edge/source/target types, not join on lookup table to see any weird >11 types
select count(edge.id) as edge_count, source.node_type_id as stype, target.node_type_id as ttype, edge.edge_type_id as etype, edge.study_id
from comb_edge_node edge, comb_node_ontology source, comb_node_ontology target
where edge.source_node_id = source.id and edge.target_node_id = target.id 
group by source.node_type_id, target.node_type_id, edge.edge_type_id, edge.study_id
order by source.node_type_id, target.node_type_id, edge.edge_type_id, edge.study_id;
