

-- create table for loading pathway name to id data
drop table if exists tran_upkeep.agg_gene_phenotype_pigean;
create table tran_upkeep.agg_gene_phenotype_pigean (
  id                           int not null auto_increment primary key,
  gene_code                    varchar(250) not null,
  phenotype_code               varchar(250) not null,
  score_huge                   double,
  prob_combined                double,
  date_created                 datetime DEFAULT CURRENT_TIMESTAMP
);

alter table tran_upkeep.agg_gene_phenotype_pigean add index gene_phen_gene_pig_cde_idx (gene_code);
alter table tran_upkeep.agg_gene_phenotype_pigean add index gene_phen_phen_pig_cde_idx (phenotype_code);



-- update node ontolgy pathway rowsbased on download names




-- queries 
select count(id) from tran_upkeep.agg_gene_phenotype;

select count(id) from tran_upkeep.agg_gene_phenotype where abf_probability_combined > 0.15 order by abf_probability_combined desc;

select id, gene_code, phenotype_code, p_value, app_bayes_factor_combined, abf_probability_combined
from tran_upkeep.agg_gene_phenotype 
where abf_probability_combined > 0.5 
order by gene_code, abf_probability_combined desc;

-- to build the gene table
drop table if exists tran_upkeep.agg_gene_phenotype;
create table tran_upkeep.agg_gene as
select node_code, ontology_id from tran_test_202303.comb_node_ontology where node_type_id = 2;


