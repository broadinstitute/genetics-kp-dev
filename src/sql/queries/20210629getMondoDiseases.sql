

select ontology_id, node_code, node_name 
from comb_node_ontology
where ontology_id like 'MONDO%'
order by node_code;

-- just mondo
select node.ontology_id, node.node_code, node.node_name 
from comb_node_ontology node, comb_edge_node edge
where node.ontology_id like 'MONDO%'
and edge.source_node_id = node.id 
and edge.study_id = 1
group by node.ontology_id, node.node_code, node.node_name 
order by node.node_code;

-- all magma phenotypes/diseases for genes
select snode.ontology_id, snode.node_code, snode.node_name 
from comb_node_ontology snode, comb_edge_node edge, comb_node_ontology tnode
where snode.ontology_type_id in (2, 3, 5, 6, 7, 8)
and edge.source_node_id = snode.id 
and edge.target_node_id = tnode.id 
and tnode.ontology_type_id in (1)
and edge.study_id = 1
group by snode.ontology_id, snode.node_code, snode.node_name 
order by snode.node_code;

-- all magma phenotypes/diseases for pathways
select snode.ontology_id, snode.node_code, snode.node_name 
from comb_node_ontology snode, comb_edge_node edge, comb_node_ontology tnode
where snode.ontology_type_id in (2, 3, 5, 6, 7, 8)
and edge.source_node_id = snode.id 
and edge.target_node_id = tnode.id 
and tnode.ontology_type_id in (4)
and edge.study_id = 1
group by snode.ontology_id, snode.node_code, snode.node_name 
order by snode.node_code;



-- scratch 
select snode.ontology_id, snode.node_code, snode.node_name, tnode.ontology_id 
from comb_node_ontology snode, comb_edge_node edge, comb_node_ontology tnode
where snode.ontology_type_id in (2, 3, 5, 6, 7, 8)
and edge.source_node_id = snode.id 
and edge.target_node_id = tnode.id 
and tnode.ontology_type_id in (4)
and edge.study_id = 1
group by snode.ontology_id, snode.node_code, snode.node_name, tnode.ontology_id
order by snode.node_code;
