
-- create table
drop table if exists agg_aggregator_phenotype;
create table agg_aggregator_phenotype (
  id                        int not null auto_increment primary key,
  phenotype_id              varchar(100) not null,
  phenotype_name            varchar(500),
  group_name                varchar(500),
  ontology_id               varchar(100),
  in_translator             enum('true', 'false') default 'false',
  just_added_in             enum('true', 'false') default 'false',
  last_updated              timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

alter table agg_aggregator_phenotype add unique index u_phenotype_id_idx (phenotype_id);




-- insert new phenotypes into the comb_node_ontology table
-- new phenotypes from magma are determined based on the aggregator phenotype code, not the ontology_id
insert into tran_test_202211.comb_node_ontology
(node_code, node_type_id, ontology_id, ontology_type_id, node_name, added_by_study_id)
select up_phenotype.phenotype_id, 
(case when SUBSTRING_INDEX(SUBSTRING_INDEX(up_phenotype.ontology_id, ':', 1), ':', -1) = 'MONDO' then 1 else 3 end) as node_type,
up_phenotype.ontology_id, ont_type.ontology_id, up_phenotype.phenotype_name, 1
from tran_upkeep.agg_aggregator_phenotype up_phenotype, tran_test_202211.comb_ontology_type ont_type 
where up_phenotype.ontology_id is not null and up_phenotype.in_translator = 'false' 
and SUBSTRING_INDEX(SUBSTRING_INDEX(up_phenotype.ontology_id, ':', 1), ':', -1) collate utf8mb4_unicode_ci = ont_type.prefix
and up_phenotype.phenotype_id collate utf8mb4_unicode_ci not in (select node_code from tran_test_202209.comb_node_ontology where node_type_id in (1, 3));

-- and up_phenotype.id not in (479, 480);

-- select up_phenotype.id,  up_phenotype.phenotype_id, 



-- workflow
-- step 01 - run the loadAggregatorPhentypes.py python script - loads all the phenotypes into a cleaned table

-- step 02 - set to true the upkeep phenotypes that are in the translator for magma calculations already (use DCC phenotype code for comparison)
update tran_upkeep.agg_aggregator_phenotype set in_translator = 'true'
where phenotype_id COLLATE utf8mb4_general_ci in (
  select node_code from tran_test_202211.comb_node_ontology where node_type_id in (1, 3)
);





-- one off updates
-- add magma as the source study for previous phenotypes
update tran_test_202209.comb_node_ontology
set added_by_study_id = 1
where node_type_id in (1, 3)
and node_code in (select phenotype_id collate utf8mb4_unicode_ci from tran_upkeep.agg_aggregator_phenotype);

select id, node_code, node_name from tran_test_202209.comb_node_ontology
where node_type_id in (1, 3)
and node_code in (select phenotype_id collate utf8mb4_unicode_ci from tran_upkeep.agg_aggregator_phenotype);



-- debug
select count(id) from agg_aggregator_phenotype;

-- see how many of the upkeep phenotypes are in stranslator already
select count(id), in_translator 
from tran_upkeep.agg_aggregator_phenotype
where ontology_id is not null
group by in_translator;

-- see how many of the upkeep phenotypes are in stranslator already
select count(id), in_translator 
from tran_upkeep.agg_aggregator_phenotype
group by in_translator;

select * 
from tran_upkeep.agg_aggregator_phenotype
where ontology_id is not null
and in_translator = 'false'
order by phenotype_name;


select id, phenotype_id, phenotype_name, ontology_id, in_translator, just_added_in
from tran_upkeep.agg_aggregator_phenotype
where ontology_id is null and in_translator = 'false'
order by phenotype_name;


select id, substring(node_code, 1, 20), node_type_id, ontology_id, substring(node_name, 1, 20), added_by_study_id
from tran_test_202209.comb_node_ontology 
where node_type_id in (1, 3) and added_by_study_id = 1
order by node_name, ontology_id;

-- find duplicate aggregator code entries
select a.id, b.id, a.node_code, b.node_code, a.node_type_id, b.node_type_id, a.ontology_id, b.ontology_id, a.last_updated, b.last_updated
from comb_node_ontology a, comb_node_ontology b 
where a.node_type_id in (1, 3) and b.node_type_id in (1, 3)
and a.node_code = b.node_code and a.id != b.id;

-- 20220829 - have node type 12 disease/phenotypes in comb_node_ontology linked to edges
-- node type 12 non existent; all have null ontology_id
-- most likely loaded old aggregator codes that had no ontologies
-- deleting them from db, as well as their edges
-- ADDING THEM TO TRAN_SCRATCH SCHEMA
select * from comb_node_ontology where node_type_id = 12 order by node_code;
select * from comb_node_ontology where node_type_id = 12 and ontology_id is not null order by node_code;
create table tran_scratch.comb_node_ontology_20220829_type_12 as select * from comb_node_ontology where node_type_id = 12 order by node_code;
delete from comb_node_ontology where node_type_id = 12;
