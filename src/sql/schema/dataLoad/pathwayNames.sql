-- create the data
drop table if exists tran_upkeep.data_pathway;
create table tran_upkeep.data_pathway (
  id                        int not null auto_increment primary key,
  pathway_code              varchar(250) not null,                        
  pathway_name              varchar(2000) not null,                        
  pathway_updated_name      varchar(2000),             
  pathway_prefix            varchar(200),             
  systematic_name           varchar(200),             
  pmid                      varchar(200),             
  exact_source              varchar(200),             
  msig_url                  varchar(2000),             
  ontology_id               varchar(200),             
  gene_count                int(9) not null,           
  last_updated              timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


-- create indexes
create index dt_pathway_info_cde on tran_upkeep.data_pathway(pathway_code);
create index dt_pathway_ont_id on tran_upkeep.data_pathway(ontology_id);



drop table if exists tran_upkeep.data_pathway_genes;
create table tran_upkeep.data_pathway_genes (
  id                           int not null auto_increment primary key,
  pathway_id                   int(9) not null,
  gene_code                   varchar(200) not null,
  date_created              datetime DEFAULT CURRENT_TIMESTAMP
);

alter table tran_upkeep.data_pathway_genes add index path_gen_path_id_idx (pathway_id);
alter table tran_upkeep.data_pathway_genes add index path_gen_gen_cde_idx (gene_code);





-- queries
-- debug
-- count pathways by ontology id
select ontology_id from data_pathway where ontology_id is not null order by ontology_id;

-- count pathways by type
select count(id) as count, pathway_prefix 
from data_pathway where ontology_id is not null 
group by pathway_prefix;

select count(id) as count, SUBSTRING_INDEX(SUBSTRING_INDEX(ontology_id, ':', 1), ' ', -1) AS prefix
from data_pathway where ontology_id is not null 
group by prefix;

-- count pathways already in translator
select count(ontology_id) from data_pathway
where ontology_id is not null and ontology_id in (select ontology_id COLLATE utf8mb4_general_ci from tran_test_202208.comb_node_ontology where node_type_id = 4);
-- 6602 rows in set (0.07 sec)

-- count pathways already not in translator
select count(ontology_id) from data_pathway
where ontology_id is not null and ontology_id not in (select ontology_id COLLATE utf8mb4_general_ci from tran_test_202208.comb_node_ontology where node_type_id = 4);

-- count all pathway with found ontology_id
select count(id) as count
from data_pathway where ontology_id is not null; 
-- +-------+
-- | count |
-- +-------+
-- | 18426 |
-- +-------+
-- diff = 18426 - 6602 = 11824


select count(id) from tran_test_202208.comb_node_ontology where node_type_id = 4;
-- mysql> select count(id) from tran_test_202208.comb_node_ontology where node_type_id = 4;
-- +-----------+
-- | count(id) |
-- +-----------+
-- |      7279 |
-- +-----------+
-- 1 row in set (0.01 sec)

select ontology_id, node_name from tran_test_202208.comb_node_ontology where node_type_id = 4 and ontology_id  COLLATE utf8mb4_general_ci not in 
(select ontology_id from data_pathway where ontology_id is not null);
-- 677 rows in set (13.29 sec)




select *
from data_pathway pathway
where pathway.pathway_code = 'GO:0045444';


select *
from data_pathway pathway, data_pathway_genes gene
where gene.pathway_id = pathway.id 
and pathway.pathway_code = 'GO:0045444';

select *
from data_pathway pathway, data_pathway_genes gene
where gene.pathway_id = pathway.id 
and pathway.pathway_code = 'GO:0050872';

select pathway.pathway_code, gene.*
from data_pathway pathway, data_pathway_genes gene
where gene.pathway_id = pathway.id 
and pathway.pathway_code in ('GO:0009256', 'GO:0042398');



-- update node ontology table pathway data name based on loaded pathway data
select node.node_code, node_name, pathway.pathway_code, pathway.pathway_updated_name
from comb_node_ontology node, tran_upkeep.data_pathway pathway
where node.node_code COLLATE utf8mb4_general_ci = pathway.pathway_code;


update comb_node_ontology node
join tran_upkeep.data_pathway pathway on node.node_code COLLATE utf8mb4_general_ci = pathway.pathway_code
set node.node_name = pathway.pathway_updated_name
where node.node_type_id = 4;

 and  node.node_code like '%3';
