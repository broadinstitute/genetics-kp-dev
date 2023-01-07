


select ontology_id, node_name
from tran_test_202209.comb_node_ontology node_new
where node_new.node_type_id in (1, 3)
and node_new.ontology_id not in (select ontology_id from tran_test_202112.comb_node_ontology)
order by node_new.node_name;



select ontology_id, node_name
from tran_test_202209.comb_node_ontology node_new
where node_new.node_type_id in (1, 3)
and node_new.ontology_id in (select ontology_id from tran_test_202107.comb_node_ontology)
order by node_new.node_name;



select count(id) from comb_node_ontology where node_type_id in (1, 3);

