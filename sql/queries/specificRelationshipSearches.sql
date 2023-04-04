
select * from comb_lookup_type;

select * from comb_node_ontology where ontology_id = 'NCBIGene:1017';

-- all edges by node type
-- pathway to gene
select * from comb_node_ontology subj, comb_node_ontology obj, comb_edge_node edge 
where subj.id = edge.source_node_id and obj.id = edge.target_node_id
and obj.node_type_id = 4
and subj.ontology_id = 'NCBIGene:1017'
order by obj.ontology_id;

-- disease to kegg pathway
select subj.ontology_id, obj.ontology_id, edge.score 
from comb_node_ontology subj, comb_node_ontology obj, comb_edge_node edge 
where subj.id = edge.source_node_id and obj.id = edge.target_node_id
and obj.node_type_id = 4 and obj.ontology_type_id = 11
order by obj.ontology_id;


-- all edges by node type
select subj.ontology_id, subj.node_type_id, obj.ontology_id, obj.node_type_id
from comb_node_ontology subj, comb_node_ontology obj, comb_edge_node edge 
where subj.id = edge.source_node_id and obj.id = edge.target_node_id
and subj.ontology_id = 'NCBIGene:169026'
order by obj.node_type_id, obj.ontology_id;



select subj.ontology_id, subj.node_type_id, obj.ontology_id, obj.node_type_id
from comb_node_ontology subj, comb_node_ontology obj, comb_edge_node edge 
where subj.id = edge.source_node_id and obj.id = edge.target_node_id
and obj.node_type_id = 4 and subj.node_type_id = 1
order by obj.node_type_id, obj.ontology_id;
