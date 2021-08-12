

-- count associatyiopn rows by study type
select count(a.id), b.study_name 
from comb_edge_node a, comb_study_type b
where a.study_id = b.study_id
group by b.study_name;


-- count nodes by type
select count(a.id), b.ontology_name
from comb_node_ontology a, comb_ontology_type b
where a.ontology_type_id = b.ontology_id
group by b.ontology_name;


