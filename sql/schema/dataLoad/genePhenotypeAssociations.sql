

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




alter table tran_upkeep.agg_gene_phenotype add index gene_phen_gene_cde_idx (gene_code);
alter table tran_upkeep.agg_gene_phenotype add index gene_phen_phen_cde_idx (phenotype_code);



-- update node ontolgy pathway rowsbased on download names




-- queries 
