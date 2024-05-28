


-- create temp tables
drop table if exists tran_scratch.comb_node_reactome_20220901;
create table tran_scratch.comb_node_reactome_20220901 as 
select * from comb_node_ontology where ontology_type_id = 9;


-- alter table to add new ontology id
alter table tran_scratch.comb_node_reactome_20220901 add new_ontology_id varchar(50);

-- populate new column
update tran_scratch.comb_node_reactome_20220901 set new_ontology_id = replace(ontology_id, 'REACTOME', 'REACT');

-- test join table
select co.id, co.ontology_id, new.new_ontology_id
from comb_node_ontology co, tran_scratch.comb_node_reactome_20220901 new 
where co.id = new.id;

-- update production translator table
update comb_node_ontology tran
join tran_scratch.comb_node_reactome_20220901 upda on tran.id = upda.id
set tran.ontology_id = upda.new_ontology_id;

-- verify
select id, node_code, ontology_id from comb_node_ontology where ontology_type_id = 9;

-- debug
select * from comb_node_ontology 
where ontology_type_id = 9 and ontology_id not like 'REAC%';

select id, ontology_id, new_ontology_id from tran_scratch.comb_node_reactome_20220901;


select id, node_code ontology_id, new_ontology_id from tran_scratch.comb_node_reactome_20220901 where new_ontology_id like '%381340';


select edge.id, subject.node_name as disease, substring(target.node_name, 1, 50) pathway, edge.score as pvalue
from comb_node_ontology subject, comb_node_ontology target, comb_edge_node edge
where subject.id = edge.source_node_id and target.id = edge.target_node_id 
and target.ontology_id = 'REACT:R-HSA-381340'
order by score;


select edge.id, subject.node_name as disease, substring(target.node_name, 1, 50) as pathway, edge.score as pvalue
from comb_node_ontology subject, comb_node_ontology target, comb_edge_node edge
where subject.id = edge.source_node_id and target.id = edge.target_node_id 
and subject.ontology_id = 'MONDO:0005148' and target.node_type_id = 4 and target.ontology_type_id in (4, 13, 9)
order by score;



select count(edge.id), type.ontology_name
from comb_node_ontology subject, comb_ontology_type type, comb_edge_node edge
where subject.id = edge.source_node_id and subject.ontology_type_id = type.ontology_id and subject.node_type_id = 4
group by type.ontology_name;



-- 20221102 - fix data_pathway table as well
select id, pathway_code, ontology_id, replace(ontology_id, 'REACTOME', 'REACT') as ont_new from data_pathway where ontology_id like 'REA%';

update data_pathway set ontology_id = replace(ontology_id, 'REACTOME', 'REACT') where ontology_id like 'REA%';

-- mysql> update data_pathway set ontology_id = replace(ontology_id, 'REACTOME', 'REACT') where ontology_id like 'REA%';
-- Query OK, 1615 rows affected (0.07 sec)
-- Rows matched: 1615  Changed: 1615  Warnings: 0



