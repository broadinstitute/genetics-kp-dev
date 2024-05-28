

-- create table for loading pathway name to id data
drop table if exists tran_upkeep.agg_phenotype_phenotype;
create table tran_upkeep.agg_phenotype_phenotype (
  id                           int not null auto_increment primary key,
  phenotype_subj_code          varchar(50) not null,
  phenotype_obj_code           varchar(50) not null,
  ancestry                     varchar(250),
  rg                           double,
  standard_error               double,
  p_value                      double not null,
  date_created                 datetime DEFAULT CURRENT_TIMESTAMP
);




alter table tran_upkeep.agg_phenotype_phenotype add index phen_phen_subj_cde_idx (phenotype_subj_code);
alter table tran_upkeep.agg_phenotype_phenotype add index phen_phen_obj_cde_idx (phenotype_obj_code);



-- update node ontolgy pathway rowsbased on download names




-- queries 
