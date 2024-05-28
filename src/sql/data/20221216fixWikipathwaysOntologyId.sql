

-- create temp tables
drop table if exists tran_scratch.comb_node_wikipathways_20221216;
create table tran_scratch.comb_node_wikipathways_20221216 as 
select * from comb_node_ontology where ontology_type_id = 13;


-- alter table to add new ontology id
alter table tran_scratch.comb_node_wikipathways_20221216 add new_ontology_id varchar(50);

-- populate new column
update tran_scratch.comb_node_wikipathways_20221216 
set new_ontology_id = concat('WIKIPATHWAYS:', SUBSTRING_INDEX(ontology_id, ':', 1), SUBSTRING_INDEX(SUBSTRING_INDEX(ontology_id, ':', 2), ':', -1));


-- check
select ontology_id, new_ontology_id from tran_scratch.comb_node_wikipathways_20221216;


-- update main table
update comb_node_ontology tran
join tran_scratch.comb_node_wikipathways_20221216 upda on tran.id = upda.id
set tran.ontology_id = upda.new_ontology_id;


-- scratch
select ontology_id, 
concat('WIKIPATHWAYS:', SUBSTRING_INDEX(ontology_id, ':', 1), SUBSTRING_INDEX(SUBSTRING_INDEX(ontology_id, ':', 2), ':', -1)) as new_id 
from tran_scratch.comb_node_wikipathways_20221216;


select ontology_id, SUBSTRING_INDEX(ontology_id, ':', 1) as one, SUBSTRING_INDEX(SUBSTRING_INDEX(ontology_id, ':', 2), ':', -1) as two from tran_scratch.comb_node_wikipathways_20221216;

select ontology_id, SUBSTRING_INDEX(SUBSTRING_INDEX(ontology_id, ':', 1), ':', -1) as new_id from tran_scratch.comb_node_wikipathways_20221216;

select ontology_id, new_ontology_id from tran_scratch.comb_node_wikipathways_20221216;


select node_name , ontology_id from comb_node_ontology where ontology_type_id = 13;

select node_name , ontology_id from comb_node_ontology where node_type_id = 4 order by ontology_id ;


-- scratch
select SUBSTRING_INDEX(ontology_id, ':', 1) from comb_node_ontology;
