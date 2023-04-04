
-- count phenotypes by type
select count(node.id), type.type_id, type.type_name
from tran_test_202209.comb_node_ontology node, tran_test_202209.comb_lookup_type type
where node.node_type_id = type.type_id and node.node_type_id in (1, 3)
group by type.type_id, type.type_name;


select count(node.id), node.node_type_id
from tran_test_202211.comb_node_ontology node
group by node.node_type_id;

-- count pathways by type
select count(id) as count, pathway_prefix 
from data_pathway where ontology_id is not null 
group by pathway_prefix;

-- count associatyion rows by study type
select count(a.id) as edge_count, b.study_id, b.study_name 
from comb_edge_node a, comb_study_type b
where a.study_id = b.study_id
group by b.study_id, b.study_name
order by b.study_id;


-- count association rows by triple types
select count(edge.id) as edge_count, source_type.type_name, target_type.type_name, edge_type.type_name
from comb_edge_node edge, comb_node_ontology source, comb_node_ontology target, comb_lookup_type edge_type,
    comb_lookup_type source_type, comb_lookup_type target_type
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
group by edge_type.type_name, source_type.type_name, target_type.type_name
order by source_type.type_name, target_type.type_name, edge_type.type_name;


-- count association rows by triple types and study
select count(edge.id) as edge_count, source_type.type_name, target_type.type_name, edge_type.type_name, study.study_id, study.study_name
from comb_edge_node edge, comb_node_ontology source, comb_node_ontology target, comb_lookup_type edge_type,
    comb_lookup_type source_type, comb_lookup_type target_type, comb_study_type study 
where edge.source_node_id = source.id and edge.target_node_id = target.id 
and source.node_type_id = source_type.type_id and target.node_type_id = target_type.type_id and edge.edge_type_id = edge_type.type_id
and edge.study_id = study.study_id
group by edge_type.type_name, source_type.type_name, target_type.type_name, study.study_id, study.study_name
order by source_type.type_name, target_type.type_name, edge_type.type_name;


-- count the rows with qualifiers
select count(id), has_qualifiers 
from comb_edge_node
group by has_qualifiers;

-- count the qualifiersaspe
select count(link.id), qualifier.id 
from comb_edge_qualifier link, comb_qualifier qualifier 
where link.qualifier_id = qualifier.id 
group by qualifier.id;



-- count nodes by ontology type
select count(a.id), b.ontology_name
from comb_node_ontology a, comb_ontology_type b
where a.ontology_type_id = b.ontology_id
group by b.ontology_name;

-- count nodes by node type
select count(a.id), b.type_name
from comb_node_ontology a, comb_lookup_type b
where a.node_type_id = b.type_id
group by b.type_name;

-- find mondo with smallest counts
select count(a.id) as edge_count, b.node_name, b.ontology_id
from comb_edge_node a, comb_node_ontology b
where a.source_node_id = b.id
    and b.ontology_id like 'MONDO%'
group by b.node_name, b.ontology_id
order by edge_count
limit 20;

-- count edges by study
select count(a.id), b.study_id, b.study_name
from comb_edge_node a, comb_study_type b
where a.study_id = b.study_id
group by b.study_id, b.study_name;

-- count edges by qualifiers
select count(a.id), a.has_qualifiers
from comb_edge_node a
group by a.has_qualifiers;


-- phenotypes by dataset
select count(distinct ed.target_node_id) as phenotype_count, st.study_name as study
from comb_edge_node ed, comb_study_type st, comb_node_ontology node
where ed.study_id = st.study_id 
and source_node_id = node.id 
and node.node_type_id = 2
group by st.study_name;


-- sample results by study
select concat(ed.edge_id, so.ontology_id, ta.ontology_id), so.ontology_id, ta.ontology_id, ed.score, sco_type.type_name, 
                so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name, ed.study_id, ed.publication_ids, ed.score_translator 
            from comb_edge_node ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type 
            where ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id 
            and ed.score_type_id = sco_type.type_id and ed.source_node_id = so.id and ed.target_node_id = ta.id 
and ed.study_id = 17
limit 10;

select         so.ontology_id, ta.ontology_id, ed.score, sco_type.type_name,         so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name, ed.study_id, 
ed.score_translator 
            from comb_edge_node ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type 
            where ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id 
            and ed.score_type_id = sco_type.type_id and ed.source_node_id = so.id and ed.target_node_id = ta.id 
and ed.study_id = 7
order by ed.score_translator desc
limit 10;


-- debug
select ontology_id from data_pathway where ontology_id is not null order by ontology_id;

select * from tran_test_202211.comb_lookup_type;



-- rows with qualifiers
select edge.id, subj.ontology_id as scusie, subj.node_code as snode, substring(sloo.type_name, 1, 20) as sname,
  obj.ontology_id as ocurie, obj.node_code as ocode, substring(oloo.type_name, 1, 20) as oname, 
  qualifier.qualifier_type as qtype, qualifier.qualifier_value as qvalue,
  edge.study_id
from comb_edge_node edge, comb_node_ontology subj, comb_node_ontology obj, comb_edge_qualifier link,
  comb_qualifier qualifier, comb_lookup_type sloo, comb_lookup_type oloo
where edge.source_node_id = subj.id and edge.target_node_id = obj.id 
and link.edge_id = edge.id and link.qualifier_id = qualifier.id
and subj.node_type_id = sloo.type_id and obj.node_type_id = oloo.type_id
order by subj.node_code, obj.node_code, qualifier.qualifier_type, qualifier.qualifier_value 
limit 2;


select edge.id, subj.ontology_id as scusie, substring(sloo.type_name, 1, 20) as sname,
  obj.ontology_id as ocurie, substring(oloo.type_name, 1, 20) as oname, 
  qualifier.qualifier_type as qtype, qualifier.qualifier_value as qvalue,
  edge.study_id
from comb_edge_node edge, comb_node_ontology subj, comb_node_ontology obj, comb_edge_qualifier link,
  comb_qualifier qualifier, comb_lookup_type sloo, comb_lookup_type oloo
where edge.source_node_id = subj.id and edge.target_node_id = obj.id 
and link.edge_id = edge.id and link.qualifier_id = qualifier.id
and subj.node_type_id = sloo.type_id and obj.node_type_id = oloo.type_id
and obj.ontology_id = 'MONDO:0004975'
order by subj.node_code, obj.node_code, qualifier.qualifier_type, qualifier.qualifier_value;

