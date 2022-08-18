

-- count pathways by type
select count(id) as count, pathway_prefix 
from data_pathway where ontology_id is not null 
group by pathway_prefix;

-- count associatyion rows by study type
select count(a.id) as edge_count, b.study_name 
from comb_edge_node a, comb_study_type b
where a.study_id = b.study_id
group by b.study_name;


-- count nodes by type
select count(a.id), b.ontology_name
from comb_node_ontology a, comb_ontology_type b
where a.ontology_type_id = b.ontology_id
group by b.ontology_name;

-- find mondo with smallest counts
select count(a.id) as edge_count, b.node_name, b.ontology_id
from comb_edge_node a, comb_node_ontology b
where a.source_node_id = b.id
    and b.ontology_id like 'MONDO%'
group by b.node_name, b.ontology_id
order by edge_count
limit 20;


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
