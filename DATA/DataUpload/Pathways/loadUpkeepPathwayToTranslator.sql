

-- need to change all to utf8mb4_unicode_ci

-- load the pathways to the translator tables
insert into tran_test_202209.comb_node_ontology
(node_code, node_type_id, ontology_id, ontology_type_id, node_name, added_by_study_id)
select up_path.pathway_code, 4, up_path.ontology_id, ont_type.ontology_id, up_path.pathway_name, 1
from tran_upkeep.data_pathway up_path, tran_test_202209.comb_ontology_type ont_type
where SUBSTRING_INDEX(SUBSTRING_INDEX(up_path.ontology_id, ':', 1), ' ', -1) collate utf8mb4_unicode_ci = ont_type.prefix
and up_path.ontology_id collate utf8mb4_unicode_ci not in (select ontology_id from tran_test_202209.comb_node_ontology where node_type_id = 4);


-- reload the genes into the comb_pathway_gene table
-- delete/drop

-- load






-- debug
select count(up_path.pathway_code), SUBSTRING_INDEX(SUBSTRING_INDEX(up_path.ontology_id, ':', 1), ' ', -1) as prefix
from tran_upkeep.data_pathway up_path, tran_test_202209.comb_ontology_type ont_type
where SUBSTRING_INDEX(SUBSTRING_INDEX(up_path.ontology_id, ':', 1), ' ', -1) collate utf8mb4_unicode_ci = ont_type.prefix
and up_path.ontology_id collate utf8mb4_unicode_ci not in (select ontology_id from tran_test_202209.comb_node_ontology where node_type_id = 4)
group by SUBSTRING_INDEX(SUBSTRING_INDEX(up_path.ontology_id, ':', 1), ' ', -1);

select count(up_path.pathway_code)
from tran_upkeep.data_pathway up_path, tran_test_202209.comb_ontology_type ont_type
where SUBSTRING_INDEX(SUBSTRING_INDEX(up_path.ontology_id, ':', 1), ' ', -1) collate utf8mb4_unicode_ci = ont_type.prefix
and up_path.ontology_id collate utf8mb4_unicode_ci not in (select ontology_id from tran_test_202209.comb_node_ontology where node_type_id = 4);
