

-- for beta
select edge.id, subj.ontology_id as scusie, subj.node_code as snode, substring(sloo.type_name, 1, 20) as sname,
  obj.ontology_id as ocurie, obj.node_code as ocode, substring(oloo.type_name, 1, 20) as oname,
  edge.study_id, edge.beta, edge.p_value, edge.score, edge.score_translator
from comb_edge_node edge, comb_node_ontology subj, comb_node_ontology obj,
  comb_lookup_type sloo, comb_lookup_type oloo
where edge.source_node_id = subj.id and edge.target_node_id = obj.id 
and edge.beta > 0
and subj.node_type_id = sloo.type_id and obj.node_type_id = oloo.type_id
order by edge.score_translator desc
limit 200;
