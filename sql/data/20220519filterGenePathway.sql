
-- pathway data filtering
-- jason mentioned filtering for pValue under 0.05





delete from comb_edge_node edge
inner join comb_node_ontology node
where edge.score > 0.01

-- reload filtered magma pathway data
insert into comb_edge_node
(edge_id, source_node_id, target_node_id, edge_type_id, score, score_text, score_type_id, study_id, score_translator, study_secondary_id, publication_ids)
select distinct edge_id, source_node_id, target_node_id, edge_type_id, score, score_text, score_type_id, study_id, score_translator, study_secondary_id, publication_ids
from tran_upkeep.comb_pathway_magma_data magma_pathway
where magma_pathway.score < 0.05;


-- scratch
-- delete all the magma pathway data for reload
delete ed
from comb_edge_node ed
inner join comb_node_ontology node on ed.source_node_id = node.id
where node.node_type_id = 4
and ed.study_id = 1;

delete ed
from comb_edge_node ed
inner join comb_node_ontology node on ed.target_node_id = node.id
where node.node_type_id = 4
and ed.study_id = 1;

-- NO WORK
delete ed
from comb_edge_node ed
inner join comb_node_ontology target on ed.target_node_id = target.id, 
comb_node_ontology subject on ed.source_node_id = subject.id
where (subject.node_type_id = 4 or target.node_type_id = 4)
and ed.study_id = 1;


-- creating magma pathway data table with rows filtered by 0.05 pValue cutoff
create table tran_upkeep.comb_pathway_magma_data as 
select ed.* 
from comb_edge_node ed, comb_node_ontology target, comb_node_ontology subject
where ed.source_node_id = subject.id
and ed.target_node_id = target.id 
and (subject.node_type_id = 4 or target.node_type_id = 4)
and ed.study_id = 1
and ed.score < 0.05;
delete ed
from comb_edge_node ed
inner join comb_node_ontology node on ed.source_node_id = node.id
where node.node_type_id = 4
and ed.study_id = 1;

-- find all magma pathway/disease rows (1630538 rows in set (5.91 sec))
-- magma pathway rows filtered as less than pValue 0.05 (111152 rows in set (2.45 sec))
select count(*) 
from comb_edge_node ed, comb_node_ontology target, comb_node_ontology subject
where ed.source_node_id = subject.id
and ed.target_node_id = target.id 
and (subject.node_type_id = 4 or target.node_type_id = 4)
and ed.study_id = 1;

select count(*), subject.node_type_id, target.node_type_id
from comb_edge_node ed, comb_node_ontology target, comb_node_ontology subject
where ed.source_node_id = subject.id
and ed.target_node_id = target.id 
and (subject.node_type_id = 4 or target.node_type_id = 4)
and ed.study_id = 1
group by subject.node_type_id, target.node_type_id;

-- find duplicate rows
select count(*) from comb_edge_node a, comb_edge_node b 
where a.id != b.id and a.source_node_id = b.source_node_id and a.target_node_id = b.target_node_id
mysql> select count(*) from comb_edge_node;
+----------+
| count(*) |
+----------+
|   553909 |
+----------+
1 row in set (0.07 sec)




select count(edge.id), node.node_type_id, edge.edge_type_id, edge.score_type_id, edge.study_id
from comb_edge_node edge, comb_node_ontology node
where edge.score > -1
and node.node_type_id = 4
and edge.source_node_id = node.id
group by node.node_type_id, edge.edge_type_id, edge.score_type_id, edge.study_id;



select count(edge.id), node.node_type_id, edge.edge_type_id, edge.score_type_id, edge.study_id
from comb_edge_node edge, comb_node_ontology node
where edge.score < 0.01
and node.node_type_id = 4
and edge.source_node_id = node.id
group by node.node_type_id, edge.edge_type_id, edge.score_type_id, edge.study_id;


select count(edge.id), node.node_type_id, edge.edge_type_id, edge.score_type_id, edge.study_id
from comb_edge_node edge, comb_node_ontology node
where edge.score < 0.01
and node.node_type_id = 4
and edge.target_node_id = node.id
group by node.node_type_id, edge.edge_type_id, edge.score_type_id, edge.study_id;

select count(ed.id)
from comb_edge_node ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, 
comb_lookup_type sco_type
where ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id             
and ed.score_type_id = sco_type.type_id and ed.source_node_id = so.id and ed.target_node_id = ta.id  and ted.type_name = 'biolink:genetic_association'  
and tso.type_name = 'biolink:Pathway'  and tta.type_name = 'biolink:Disease'
and ed.score < 0.1
order by ed.score 
limit 200


-- post deletion and reinsertion of distinct rows (had 111,152 magma pathway duplicates data count; expect 1/2)


-- post magma pathway deletion
-- expect 2,150,129 - 111,152 = 2,038,977



-- 20220524 - log of operations to clean out pathways
mysql> select count(*), subject.node_type_id, target.node_type_id
    -> from comb_edge_node ed, comb_node_ontology target, comb_node_ontology subject
    -> where ed.source_node_id = subject.id
    -> and ed.target_node_id = target.id 
    -> and (subject.node_type_id = 4 or target.node_type_id = 4)
    -> and ed.study_id = 1
    -> group by subject.node_type_id, target.node_type_id;
+----------+--------------+--------------+
| count(*) | node_type_id | node_type_id |
+----------+--------------+--------------+
|    12365 |            4 |            1 |
|    31403 |            4 |            3 |
|    12365 |            1 |            4 |
|    31403 |            3 |            4 |
+----------+--------------+--------------+
4 rows in set (0.98 sec)

mysql> 


mysql> select count(*) from comb_edge_node;
+----------+
| count(*) |
+----------+
|   641445 |
+----------+
1 row in set (0.06 sec)


mysql> insert into comb_edge_node
    -> (edge_id, source_node_id, target_node_id, edge_type_id, score, score_text, score_type_id, study_id, score_translator, study_secondary_id, publication_ids)
    -> select distinct edge_id, source_node_id, target_node_id, edge_type_id, score, score_text, score_type_id, study_id, score_translator, study_secondary_id, publication_ids
    -> from tran_upkeep.comb_pathway_magma_data magma_pathway
    -> where magma_pathway.score < 0.05;
Query OK, 87536 rows affected (2.84 sec)
Records: 87536  Duplicates: 0  Warnings: 0


mysql> select count(*) from comb_edge_node;
+----------+
| count(*) |
+----------+
|   553909 |
+----------+
1 row in set (0.07 sec)


mysql> select count(*) 
    -> from comb_edge_node ed, comb_node_ontology target, comb_node_ontology subject
    -> where ed.source_node_id = subject.id
    -> and ed.target_node_id = target.id 
    -> and (subject.node_type_id = 4 or target.node_type_id = 4)
    -> and ed.study_id = 1;
+----------+
| count(*) |
+----------+
|        0 |
+----------+
1 row in set (13.75 sec)


mysql> delete ed
    -> from comb_edge_node ed
    -> inner join comb_node_ontology node on ed.target_node_id = node.id
    -> where node.node_type_id = 4
    -> and ed.study_id = 1;
Query OK, 815269 rows affected (2 min 1.36 sec)


mysql> delete ed
    -> from comb_edge_node ed
    -> inner join comb_node_ontology node on ed.source_node_id = node.id
    -> where node.node_type_id = 4
    -> and ed.study_id = 1;
Query OK, 815269 rows affected (2 min 19.98 sec)



mysql> select count(*) 
    -> from comb_edge_node ed, comb_node_ontology target, comb_node_ontology subject
    -> where ed.source_node_id = subject.id
    -> and ed.target_node_id = target.id 
    -> and (subject.node_type_id = 4 or target.node_type_id = 4)
    -> and ed.study_id = 1;
+----------+
| count(*) |
+----------+
|  1630538 |
+----------+
1 row in set (3.98 sec)

pre magma pathway data deletion
mysql> select count(*) from comb_edge_node;
mysql> select count(*) from comb_edge_node;
+----------+
| count(*) |
+----------+
|  2184447 |
+----------+
1 row in set (0.19 sec)

+----------+
| count(*) |
+----------+
|  2150129 |  -- outdate db
+----------+
1 row in set (0.16 sec)





-- mysql> desc tran_test_202204.comb_edge_node;
-- +--------------------+---------------+------+-----+-------------------+-------------------+
-- | Field              | Type          | Null | Key | Default           | Extra             |
-- +--------------------+---------------+------+-----+-------------------+-------------------+
-- | id                 | int           | NO   | PRI | NULL              | auto_increment    |
-- | edge_id            | varchar(100)  | NO   |     | NULL              |                   |
-- | source_node_id     | int           | NO   | MUL | NULL              |                   |
-- | target_node_id     | int           | NO   | MUL | NULL              |                   |
-- | edge_type_id       | int           | NO   |     | NULL              |                   |
-- | score              | double        | YES  | MUL | NULL              |                   |
-- | score_text         | varchar(50)   | YES  |     | NULL              |                   |
-- | score_type_id      | int           | NO   | MUL | NULL              |                   |
-- | study_id           | int           | NO   |     | NULL              |                   |
-- | date_created       | datetime      | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
-- | score_translator   | double        | YES  |     | NULL              |                   |
-- | study_secondary_id | int           | YES  |     | NULL              |                   |
-- | publication_ids    | varchar(1000) | YES  |     | NULL              |                   |
-- +--------------------+---------------+------+-----+-------------------+-------------------+
-- 13 rows in set (0.00 sec)

-- mysql> 



-- process
-- mysql> delete ed
--     -> from comb_edge_node ed
--     -> inner join comb_node_ontology target on ed.target_node_id = target.id
--     -> where target.node_type_id = 4
--     -> and ed.study_id = 1;
-- Query OK, 815269 rows affected (1 min 54.45 sec)

-- mysql> delete ed
--     -> from comb_edge_node ed
--     -> inner join comb_node_ontology node on ed.source_node_id = node.id
--     -> where node.node_type_id = 4
--     -> and ed.study_id = 1;
-- Query OK, 815269 rows affected (1 min 41.65 sec)

-- mysql> select count(*) 
--     -> from comb_edge_node ed, comb_node_ontology target, comb_node_ontology subject
--     -> where ed.source_node_id = subject.id
--     -> and ed.target_node_id = target.id 
--     -> and (subject.node_type_id = 4 or target.node_type_id = 4)
--     -> and ed.study_id = 1;
-- +----------+
-- | count(*) |
-- +----------+
-- |        0 |
-- +----------+
-- 1 row in set (5.64 sec)


