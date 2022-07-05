
-- create the drug gene table in production schema
drop table if exists infe_drug_gene;
create table infe_drug_gene (
  id                        int not null auto_increment primary key,
  gene_node_id              int(9) not null,
  gene_ontology_id          varchar(20) not null,
  gene_code                 varchar(200) not null,
  drug_ontology_id          varchar(500) not null,
  drug_name                 varchar(1000),
  drug_category_biolink_id  varchar(100) not null,
  predicate_biolink_id      varchar(100) not null,
  last_updated              timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


-- indices
alter table infe_drug_gene add index infe_drug_gene_gen_id_idx (gene_node_id);



-- create the drug gene table in load schema
drop table if exists tran_upkeep.molepro_drug_gene;
create table tran_upkeep.molepro_drug_gene (
  id                        int not null auto_increment primary key,
  gene_node_id              int(9) not null,
  gene_ontology_id          varchar(20) not null,
  gene_code                 varchar(200) not null,
  drug_ontology_id          varchar(500) not null,
  drug_name                 varchar(1000),
  drug_category_biolink_id  varchar(100) not null,
  predicate_biolink_id      varchar(100) not null,
  last_updated              timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


-- create the drug gene table in load schema - only AFFECTS query
drop table if exists tran_upkeep.molepro_drug_gene_affects;
create table tran_upkeep.molepro_drug_gene_affects (
  id                        int not null auto_increment primary key,
  gene_node_id              int(9) not null,
  gene_ontology_id          varchar(20) not null,
  gene_code                 varchar(200) not null,
  drug_ontology_id          varchar(500) not null,
  drug_name                 varchar(1000),
  drug_category_biolink_id  varchar(100) not null,
  predicate_biolink_id      varchar(100) not null,
  last_updated              timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

insert into tran_upkeep.molepro_drug_gene_affects 
(gene_node_id, gene_ontology_id, gene_code, drug_ontology_id, drug_name, drug_category_biolink_id, predicate_biolink_id)
select gene_node_id, gene_ontology_id, gene_code, drug_ontology_id, drug_name, drug_category_biolink_id, predicate_biolink_id
from tran_upkeep.molepro_drug_gene;

-- create the drug gene table in load schema - only AFFECTS query
drop table if exists tran_upkeep.molepro_drug_gene_regulates;
create table tran_upkeep.molepro_drug_gene_regulates (
  id                        int not null auto_increment primary key,
  gene_node_id              int(9) not null,
  gene_ontology_id          varchar(20) not null,
  gene_code                 varchar(200) not null,
  drug_ontology_id          varchar(500) not null,
  drug_name                 varchar(1000),
  drug_category_biolink_id  varchar(100) not null,
  predicate_biolink_id      varchar(100) not null,
  last_updated              timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);




-- create the gene status table in the load schema
drop table if exists tran_upkeep.molepro_gene_status;
create table tran_upkeep.molepro_gene_status (
  id                        int not null auto_increment primary key,
  gene_node_id              int(9) not null,
  gene_ontology_id          varchar(20) not null,
  gene_code                 varchar(200) not null,
  load_status               enum('done', 'not done') default 'not done',
  last_updated              timestamp default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- indices
alter table infe_drug_gene add index infe_drug_gene_gen_id_idx (gene_node_id);

-- insert into the gene status table
insert into tran_upkeep.molepro_gene_status (gene_node_id, gene_ontology_id, gene_code)
select id, ontology_id, node_code
from comb_node_ontology
where node_type_id = 2
limit 20;



-- scratch
select * from tran_upkeep.molepro_gene_status limit 20;

select count(id), load_status from tran_upkeep.molepro_gene_status group by load_status;

select count(id) from tran_upkeep.molepro_drug_gene;

select count(id), predicate_biolink_id from tran_upkeep.molepro_drug_gene group by predicate_biolink_id order by predicate_biolink_id;
