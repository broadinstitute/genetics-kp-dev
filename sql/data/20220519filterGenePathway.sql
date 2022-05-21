





delete from comb_edge_node edge
inner join comb_node_ontology node
where edge.score > 0.01

\

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


