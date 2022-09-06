

-- duplicate phenotypes
select a.id, b.id, a.node_code, b.node_code, a.ontology_id, b.ontology_id, a.node_type_id, b.node_type_id, a.last_updated, b.last_updated
from comb_node_ontology a, comb_node_ontology b 
where a.node_type_id in (1, 3) and b.node_type_id in (1, 3)
and a.node_code = b.node_code and a.id != b.id;

-- duplicate pathways
select a.id, b.id, a.node_code, b.node_code, a.ontology_id, b.ontology_id, a.node_type_id, b.node_type_id, a.last_updated, b.last_updated
from comb_node_ontology a, comb_node_ontology b 
where a.ontology_id = 4 and b.ontology_id = 4
and a.node_code = b.node_code and a.id != b.id;

-- overlaping pathways and phenotypes (HP?) - none so far
select a.id, b.id, a.node_code, b.node_code, a.ontology_id, b.ontology_id, a.node_type_id, b.node_type_id, a.last_updated, b.last_updated
from comb_node_ontology a, comb_node_ontology b 
where a.ontology_id in (1, 3, 4) and b.ontology_id in (1, 3, 4)
and a.node_code = b.node_code and a.id != b.id;


