


-- magma
-- find number of low pvalues with prob < 0.15
select count(id) from agg_gene_phenotype
where p_value < 0.00005 and abf_probability_combined < 0.10;

-- just low prob
select count(id) from agg_gene_phenotype
where abf_probability_combined > 0.10;