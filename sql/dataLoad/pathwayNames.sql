

-- create table for loading pathway name to id data
drop table if exists tran_upkeep.load_pathway;
create table tran_upkeep.load_pathway (
  id                           int not null auto_increment primary key,
  pathway_code                 varchar(250) not null,
  pathway_name                 varchar(2000) not null,
  pathway_updated_name         varchar(2000) not null
);




drop table if exists tran_upkeep.load_pathway_genes;
create table tran_upkeep.load_pathway_genes (
  id                           int not null auto_increment primary key,
  pathway_id                   int(9) not null,
  gene_code                   varchar(200) not null,
  date_created              datetime DEFAULT CURRENT_TIMESTAMP
);

alter table tran_upkeep.load_pathway_genes add index path_gen_path_id_idx (pathway_id);



-- update node ontolgy pathway rowsbased on download names




-- queries 
