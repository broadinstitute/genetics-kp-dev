

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




-- select non null beta with disease
select concat(ed.edge_id, so.ontology_id, ta.ontology_id), 
    so.ontology_id, ta.ontology_id, ed.score, sco_type.type_name,                 
    so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name, ed.study_id, 
    ed.publication_ids, ed.score_translator, ed.id             
from comb_edge_node ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type             
where ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id             
and ed.score_type_id = sco_type.type_id and ed.source_node_id = so.id and ed.target_node_id = ta.id  and ted.type_name = 'biolink:condition_associated_with_gene'
and tso.type_name = 'biolink:PhenotypicFeature'  and tta.type_name = 'biolink:Gene'  and so.ontology_id = 'UMLS:C0424646'  and ta.ontology_id = 'NCBIGene:22955'
and ed.study_id != 18
order by ed.score_translator desc 
limit 50;

-- select non null beta with disease
select concat(ed.edge_id, so.ontology_id, ta.ontology_id), 
    so.ontology_id, ta.ontology_id, ed.score, sco_type.type_name,                 
    so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name, ed.study_id, ed.publication_ids, ed.score_translator, ed.id             
from comb_edge_node ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type             
where ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id             
and ed.score_type_id = sco_type.type_id and ed.source_node_id = so.id and ed.target_node_id = ta.id  and ted.type_name = 'biolink:condition_associated_with_gene'
and tso.type_name = 'biolink:PhenotypicFeature'  and tta.type_name = 'biolink:Gene'  and so.ontology_id in ('MONDO:0021140')  
and ed.study_id != 18
order by ed.score_translator desc 
limit 50;


-- select non null beta
select concat(ed.edge_id, so.ontology_id, ta.ontology_id), 
    so.ontology_id, ta.ontology_id, ed.score, sco_type.type_name,                 
    so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name, ed.study_id, ed.publication_ids, ed.score_translator, ed.id             
from comb_edge_node ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type             
where ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id             
and ed.score_type_id = sco_type.type_id and ed.source_node_id = so.id and ed.target_node_id = ta.id  and ted.type_name = 'biolink:condition_associated_with_gene'
and tso.type_name = 'biolink:PhenotypicFeature'  and tta.type_name = 'biolink:Gene'
and ed.study_id != 18
order by ed.score_translator desc 
limit 50;


, parameters: ['biolink:condition_associated_with_gene', 'biolink:PhenotypicFeature', 'biolink:Gene', 'MONDO:0021140']


