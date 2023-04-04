


-- delete old pathway associations
-- delete where pathway is subject
delete edge from tran_test_202211.comb_edge_node edge
inner join tran_test_202211.comb_node_ontology node on edge.source_node_id = node.id 
where node.node_type_id = 4;

-- delete where pathway is object
delete edge from tran_test_202211.comb_edge_node edge
inner join tran_test_202211.comb_node_ontology node on edge.target_node_id = node.id 
where node.node_type_id = 4;

-- insert pathway phenotype association
-- add pathway as subject
-- expecting 729207 rows in set (14.35 sec)
-- got 360523 rows in set (12.38 sec) -> fewer due to phenotypes that don't get included
-- insert with pathway as source
insert into tran_test_202211.comb_edge_node 
(edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id) 
    select concat('magma_', pathway.ontology_id, '_', phenotype.ontology_id) as edge_id, 
    6, pathway.id, phenotype.id, 
    up_path_assoc.p_value, 8, 1
    from tran_upkeep.agg_pathway_phenotype up_path_assoc, tran_test_202211.comb_node_ontology pathway, tran_test_202211.comb_node_ontology phenotype, 
      tran_upkeep.data_pathway up_path
    where up_path_assoc.pathway_code = up_path.pathway_code
    and up_path.ontology_id collate utf8mb4_unicode_ci = pathway.ontology_id and pathway.node_type_id = 4 and pathway.ontology_id is not null
    and up_path_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
    and up_path_assoc.p_value <= 0.05
    order by phenotype.node_code, pathway.node_code;

-- insert with pathway as target
insert into tran_test_202211.comb_edge_node 
(edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id) 
    select concat('magma_', phenotype.ontology_id, '_', pathway.ontology_id) as edge_id, 
    6, phenotype.id, pathway.id, 
    up_path_assoc.p_value, 8, 1
    from tran_upkeep.agg_pathway_phenotype up_path_assoc, tran_test_202211.comb_node_ontology pathway, tran_test_202211.comb_node_ontology phenotype, 
      tran_upkeep.data_pathway up_path
    where up_path_assoc.pathway_code = up_path.pathway_code
    and up_path.ontology_id collate utf8mb4_unicode_ci = pathway.ontology_id and pathway.node_type_id = 4 and pathway.ontology_id is not null
    and up_path_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
    and up_path_assoc.p_value <= 0.05
    order by phenotype.node_code, pathway.node_code;


    limit 20;

    pathway.ontology_id as path_ont, phenotype.ontology_id as pheno_ont, phenotype.node_code, pathway.node_code,
    limit 20;

    %s, 5, %s, 2, %s, (select node_type_id from comb_node_ontology where node_code = %s and node_type_id in (1, 3, 12)), %s, 8, 1)




-- scratch
select *
from comb_node_ontology path, comb_edge_node edge
where edge.source_node_id = path.id and path.node_type_id = 4
limit 20;


select substring(up_path_assoc.pathway_code, 1, 100), up_path_assoc.phenotype_code
from tran_upkeep.agg_pathway_phenotype up_path_assoc, tran_upkeep.data_pathway up_path
where up_path_assoc.pathway_code = up_path.pathway_code
and up_path_assoc.p_value <= 0.05 and up_path.ontology_id is not null
order by up_path_assoc.pathway_code, up_path_assoc.phenotype_code;
-- 738,309 rows in set (7.30 sec)

-- debugging getting 1.3 million rows vs 800k rows in upkeep associations
select up_path.id, up_path_assoc.id, substring(up_path_assoc.pathway_code, 1, 20), up_path_assoc.phenotype_code, pathway.id, pathway.ontology_id
from tran_upkeep.agg_pathway_phenotype up_path_assoc, tran_upkeep.data_pathway up_path, comb_node_ontology pathway
where up_path_assoc.pathway_code = up_path.pathway_code
and up_path.ontology_id collate utf8mb4_unicode_ci = pathway.ontology_id and pathway.node_type_id = 4 and pathway.ontology_id is not null
and up_path_assoc.p_value <= 0.05 and up_path.ontology_id is not null
order by up_path.id, up_path_assoc.id, substring(up_path_assoc.pathway_code, 1, 20), up_path_assoc.phenotype_code, pathway.id, pathway.ontology_id;
-- 2,513,199 rows in set (37.72 sec

select count(*)

select up_path.id, up_path_assoc.id, pathway.id, phenotype.id
from tran_upkeep.agg_pathway_phenotype up_path_assoc, comb_node_ontology pathway, comb_node_ontology phenotype, tran_upkeep.data_pathway up_path
where up_path_assoc.pathway_code = up_path.pathway_code
and up_path.ontology_id collate utf8mb4_unicode_ci = pathway.ontology_id and pathway.node_type_id = 4 and pathway.ontology_id is not null
and up_path_assoc.phenotype_code collate utf8mb4_unicode_ci = phenotype.node_code and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
and up_path_assoc.p_value <= 0.05
order by up_path.id, up_path_assoc.id, pathway.id, phenotype.id;





-- debugging getting 1.3 million rows vs 800k rows in upkeep associations
-- this was due to PID pathwqys all having the same ontology id, hence lots of cartesian joins
drop table if exists scratch_pathway_pheno;
create table scratch_pathway_pheno (
  id                        int not null auto_increment primary key,
  pheno_assoc_id            int(9) not null,
  pathway_id                int(9) not null,
  node_id                   int(9) not null,
  pathway_ontology_id       varchar(250) not null,                        
  pathway_code              varchar(250) not null,                        
  pheno_code                varchar(250) not null,                        
  last_updated              timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


-- expecting ~ 800k inserts
-- this is without joining on phenotypes; 1/2 of aggregator phenotypes arwe not in translator due to adj features/no ontology_id
insert into scratch_pathway_pheno
(pathway_id, pheno_assoc_id, pathway_code, pheno_code, node_id, pathway_ontology_id)

select up_path.id, up_path_assoc.id, substring(up_path_assoc.pathway_code, 1, 20), up_path_assoc.phenotype_code, pathway.id, pathway.ontology_id
from tran_upkeep.agg_pathway_phenotype up_path_assoc, tran_upkeep.data_pathway up_path, comb_node_ontology pathway
where up_path_assoc.pathway_code = up_path.pathway_code
and up_path.ontology_id collate utf8mb4_unicode_ci = pathway.ontology_id and pathway.node_type_id = 4 and pathway.ontology_id is not null
and up_path_assoc.p_value <= 0.05 and up_path.ontology_id is not null
order by up_path.id, up_path_assoc.id, substring(up_path_assoc.pathway_code, 1, 20), up_path_assoc.phenotype_code, pathway.id, pathway.ontology_id;

select * from scratch_pathway_pheno a, scratch_pathway_pheno b
where a.pathway_id = b.pathway_id and a.pheno_assoc_id = b.pheno_assoc_id and a.node_id = b.node_id
and a.id != b.id
order by a.pathway_id, a.pheno_assoc_id, a.node_id
limit 30;


alter table scratch_pathway_pheno add index scratch_1_idx (pheno_assoc_id);
alter table scratch_pathway_pheno add index scratch_2_idx (pathway_id);
alter table scratch_pathway_pheno add index scratch_3_idx (node_id);


-- 20220824 - issue with join translator pathway and data upload pathways?
select count(id) from tran_upkeep.data_pathway where ontology_id is not null;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |     18426 |
-- +-----------+
-- 1 row in set (0.01 sec)


select count(*)
from comb_node_ontology where ontology_id is not null and node_type_id = 4;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |     19103 |
-- +-----------+
-- 1 row in set (0.06 sec)

select count(*) 
from comb_node_ontology node_path, tran_upkeep.data_pathway up_path
where up_path.ontology_id is not null and node_path.node_type_id = 4
and up_path.ontology_id = node_path.ontology_id collate utf8mb4_0900_ai_ci;

select a.id, b.id, substring(a.pathway_code, 1, 20), substring(b.pathway_code, 1, 20), a.ontology_id, b.ontology_id
from tran_upkeep.data_pathway a, tran_upkeep.data_pathway b
where a.id != b.id and a.ontology_id is not null and a.ontology_id = b.ontology_id
order by substring(a.pathway_code, 1, 20), substring(b.pathway_code, 1, 20), a.ontology_id, b.ontology_id;



select distinct a.pathway_prefix
from tran_upkeep.data_pathway a, tran_upkeep.data_pathway b
where a.id != b.id and a.ontology_id is not null and a.ontology_id = b.ontology_id;

order by substring(a.pathway_code, 1, 20), substring(b.pathway_code, 1, 20), a.ontology_id, b.ontology_id;
