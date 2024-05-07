

-- create table for loading pathway name to id data
drop table if exists tran_upkeep.agg_pathway_phenotype2;
create table tran_upkeep.agg_pathway_phenotype2 (
  id                           int not null auto_increment primary key,
  pathway_code                 varchar(250) not null,
  phenotype_code               varchar(50) not null,
  beta                         double null,
  beta_standard_error          double null,
  standard_error               double null,
  p_value                      double not null,
  date_created                 datetime DEFAULT CURRENT_TIMESTAMP
);




alter table tran_upkeep.agg_pathway_phenotype add index path_phen_path_cde_idx (pathway_code);
alter table tran_upkeep.agg_pathway_phenotype add index path_phen_phen_cde_idx (phenotype_code);



-- update node ontolgy pathway rowsbased on download names



-- old
-- create table tran_upkeep.agg_pathway_phenotype (
--   id                           int not null auto_increment primary key,
--   pathway_code                 varchar(250) not null,
--   pathway_name                 varchar(2000) not null,
--   pathway_updated_name         varchar(2000) not null,
--   phenotype_code               varchar(50) not null,
--   number_genes                 int(9) not null,
--   beta                         double not null,
--   beta_standard_error          double not null,
--   standard_error               double not null,
--   p_value                      double not null,
--   date_created                 datetime DEFAULT CURRENT_TIMESTAMP
-- );


-- queries 
select id, pathway_code, phenotype_code, p_value
from tran_upkeep.agg_pathway_phenotype
where p_value < 0.05
order by p_value desc;

