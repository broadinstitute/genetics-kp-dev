
-- delete old 600k gene/phenotype associations
delete edge from tran_test_202303.comb_edge_node edge
where edge.study_id = 18;


-- insert the new rows
insert into tran_test_202303.comb_edge_node 
(edge_id, source_node_id, target_node_id, edge_type_id, score, score_type_id, study_id, has_qualifiers)
values(concat('600k_', %s, '_', %s), %s, %s, %s, %s, 8, %s, 'Y')

-- insert 600k associations with gene as subject 
insert into tran_test_202303.comb_edge_node 
(edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id, score_translator, 
    p_value, probability_app_bayes_factor, beta, standard_error) 
  select concat('600k_', gene.ontology_id, '_', phenotype.ontology_id) as edge_id, 
    5, gene.id, phenotype.id, 
    up_gene_assoc.p_value, 8, 18, up_gene_assoc.probability_calculated, 
    up_gene_assoc.p_value, up_gene_assoc.probability_calculated, up_gene_assoc.beta, up_gene_assoc.std_error
    from tran_upkeep.data_600k_gene_phenotype up_gene_assoc, tran_upkeep.data_600k_phenotype_ontology up_pheno, 
      tran_test_202303.comb_node_ontology gene, tran_test_202303.comb_node_ontology phenotype
    where up_gene_assoc.gene_code collate utf8mb4_unicode_ci = gene.node_code and gene.node_type_id = 2 and gene.ontology_id is not null
    and up_gene_assoc.phenotype_code = up_pheno.phenotype_code and up_gene_assoc.mask = 'LoF_HC'
    and up_pheno.phenotype_ontology_id collate utf8mb4_unicode_ci = phenotype.ontology_id and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
    and up_gene_assoc.probability_calculated >= 0.1;
    -- order by phenotype.node_code, gene.node_code;


-- insert 600k associations with gene as object
insert into tran_test_202303.comb_edge_node 
(edge_id, edge_type_id, source_node_id, target_node_id, score, score_type_id, study_id, score_translator, 
    p_value, probability_app_bayes_factor, beta, standard_error) 
  select concat('600k_', phenotype.ontology_id, '_',  gene.ontology_id) as edge_id, 
    10, phenotype.id, gene.id,
    up_gene_assoc.p_value, 8, 18, up_gene_assoc.probability_calculated, 
    up_gene_assoc.p_value, up_gene_assoc.probability_calculated, up_gene_assoc.beta, up_gene_assoc.std_error
    from tran_upkeep.data_600k_gene_phenotype up_gene_assoc, tran_upkeep.data_600k_phenotype_ontology up_pheno, 
      tran_test_202303.comb_node_ontology gene, tran_test_202303.comb_node_ontology phenotype
    where up_gene_assoc.gene_code collate utf8mb4_unicode_ci = gene.node_code and gene.node_type_id = 2 and gene.ontology_id is not null
    and up_gene_assoc.phenotype_code = up_pheno.phenotype_code and up_gene_assoc.mask = 'LoF_HC'
    and up_pheno.phenotype_ontology_id collate utf8mb4_unicode_ci = phenotype.ontology_id and phenotype.node_type_id in (1, 3) and phenotype.ontology_id is not null
    and up_gene_assoc.probability_calculated >= 0.1;




-- scratch
select up_gene_assoc.id, up_gene_assoc.gene_code, up_pheno.phenotype_ontology_id, 
  up_gene_assoc.p_value, up_gene_assoc.probability_calculated, up_gene_assoc.beta, up_gene_assoc.std_error
  from tran_upkeep.data_600k_gene_phenotype up_gene_assoc, tran_upkeep.data_600k_phenotype_ontology up_pheno
  where up_gene_assoc.phenotype_code = up_pheno.phenotype_code and up_gene_assoc.mask = 'LoF_HC'
  and up_pheno.phenotype_ontology_id is not null
  and up_gene_assoc.probability_calculated >= 0.1;
