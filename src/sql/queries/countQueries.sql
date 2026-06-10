

-- count types of relationships
select count(edge.id) as edge_count, source_type.type_name as source_type, target_type.type_name as target_type, edge_type.type_name as edge_type
from comb_edge_node edge, comb_node_ontology source, comb_node_ontology target, comb_lookup_type edge_type,
    comb_lookup_type source_type, comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
group by edge_type.type_name, source_type.type_name, target_type.type_name
order by source_type.type_name, target_type.type_name, edge_type.type_name;

-- count by ontology type
select count(edge.id) as edge_count, source_type.ontology_name as source_type, target_type.ontology_name as target_type, 
    edge_type.type_name as edge_type
from comb_edge_node edge, comb_node_ontology source, comb_node_ontology target, comb_lookup_type edge_type,
    comb_ontology_type source_type, comb_ontology_type target_type
where edge.source_node_id = source.id 
and edge.target_node_id = target.id 
and source.ontology_type_id = source_type.ontology_id 
and target.ontology_type_id = target_type.ontology_id 
and edge.edge_type_id = edge_type.type_id
group by edge_type.type_name, source_type.ontology_name, target_type.ontology_name
order by source_type.ontology_name, target_type.ontology_name, edge_type.type_name;


