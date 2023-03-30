

-- create table for loading pathway name to id data
drop table if exists tran_upkeep.agg_gene_phenotype;
create table tran_upkeep.agg_gene_phenotype (
  id                           int not null auto_increment primary key,
  gene_code                    varchar(250) not null,
  phenotype_code               varchar(50) not null,
  gene_type                    varchar(250),
  z_stat                       double,
  p_value                      double not null,
  date_created                 datetime DEFAULT CURRENT_TIMESTAMP
);


-- adding approximate bayes factor
alter table tran_upkeep.agg_gene_phenotype add column app_bayes_factor_common double;
alter table tran_upkeep.agg_gene_phenotype add column app_bayes_factor_rare double;
alter table tran_upkeep.agg_gene_phenotype add column app_bayes_factor_combined double;
alter table tran_upkeep.agg_gene_phenotype add column abf_probability_common double;
alter table tran_upkeep.agg_gene_phenotype add column abf_probability_rare double;
alter table tran_upkeep.agg_gene_phenotype add column abf_probability_combined double;



alter table tran_upkeep.agg_gene_phenotype add index gene_phen_gene_cde_idx (gene_code);
alter table tran_upkeep.agg_gene_phenotype add index gene_phen_phen_cde_idx (phenotype_code);



-- update node ontolgy pathway rowsbased on download names




-- queries 
select count(id) from tran_upkeep.agg_gene_phenotype;

select * from tran_upkeep.agg_gene_phenotype where abf_probability_combined > 0.15 order by abf_probability_combined desc;

select id, gene_code, phenotype_code, p_value, app_bayes_factor_combined, abf_probability_combined
from tran_upkeep.agg_gene_phenotype 
where abf_probability_combined > 0.5 
order by gene_code, abf_probability_combined desc;



