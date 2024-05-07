

-- update magma
update comb_edge_node
set score_translator = 0.15
where study_id = 1 and edge_type_id in (5, 10) 
and score <= 2.5e-6;


update comb_edge_node
set score_translator = 0.05
where study_id = 1 and edge_type_id in (5, 10) 
and score > 2.5e-6;

select * from comb_edge_node


-- update richards gene data
update comb_edge_node
set score_translator = score
where study_id = 4 and edge_type_id in (5, 10) 



-- update clingen/clinvar data
update comb_edge_node
set score_translator = 0.99
where study_id in (5, 6) and edge_type_id in (5, 10) 
and score_text = 'Definitive';

update comb_edge_node
set score_translator = 0.8
where study_id in (5, 6) and edge_type_id in (5, 10) 
and score_text = 'Strong';

update comb_edge_node
set score_translator = 0.5
where study_id in (5, 6) and edge_type_id in (5, 10) 
and score_text = 'Moderate';

update comb_edge_node
set score_translator = 0.1
where study_id in (5, 6) and edge_type_id in (5, 10) 
and score_text = 'Limited';

update comb_edge_node
set score_translator = 0.05
where study_id in (5, 6) and edge_type_id in (5, 10) 
and score_text is null;


update comb_edge_node
set score_translator = 0.25
where study_id in (5, 6) and edge_type_id in (5, 10) 
and score_text = 'Associated';

update comb_edge_node
set score_translator = 0.1
where study_id in (5, 6) and edge_type_id in (5, 10) 
and score_text = 'Related';


-- scratch 
select count(ed.id), st.study_id, st.study_name
from comb_edge_node ed, comb_study_type st
where ed.study_id = st.study_id
and score_translator is null
group by st.study_id, st.study_name;


select count(id), score_text, study_id, score_translator
from comb_edge_node
where study_id in (5, 6)
group by score_text, study_id, score_translator
order by study_id;


