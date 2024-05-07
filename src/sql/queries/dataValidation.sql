


-- find all go pathways not in the node table
select * 
from tran_upkeep.data_pathway pathway
where lower(pathway.pathway_code) like 'go%' 
and pathway_code not in (select ontology_id COLLATE utf8mb4_general_ci from comb_node_ontology where node_type_id = 4);

-- other way
select * 
from comb_node_ontology
where node_type_id = 4
and ontology_id COLLATE utf8mb4_general_ci not in (select pathway_code from tran_upkeep.data_pathway);


-- find all duplicate genes
select * 
from comb_node_ontology a, comb_node_ontology b
where a.node_type_id = 2 and b.node_type_id = 2 
and a.ontology_id = b.ontology_id and a.id != b.id 

