

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

-- all phenotypes/diseases
select node.ontology_id, node.node_code, node.node_name 
from comb_node_ontology node, comb_edge_node edge
where node.ontology_type_id in (2, 3, 5, 6, 7)
and edge.source_node_id = node.id 
and edge.study_id = 1
group by node.ontology_id, node.node_code, node.node_name 
order by node.node_code;


