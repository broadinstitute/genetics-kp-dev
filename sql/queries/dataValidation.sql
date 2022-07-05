


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


