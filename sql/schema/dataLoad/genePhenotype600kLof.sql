

-- create table for loading pathway name to id data
drop table if exists tran_upkeep.data_600k_gene_phenotype;
create table tran_upkeep.data_600k_gene_phenotype (
  id                           int not null auto_increment primary key,
  gene_code                    varchar(250) not null,
  phenotype_code               varchar(50) not null,
  phenotype                    varchar(150) not null,
  ancestry                     varchar(50) not null,
  mask                         varchar(50) not null,
  combined_af                  double,
  std_error                    double,
  beta                         double,
  p_value                      double not null,
  date_created                 datetime DEFAULT CURRENT_TIMESTAMP
);
-- indices
alter table tran_upkeep.data_600k_gene_phenotype add index gen_phe_phe_cde_idx (phenotype_code);
alter table tran_upkeep.data_600k_gene_phenotype add index gen_phe_pval_idx (p_value);
alter table tran_upkeep.data_600k_gene_phenotype add index gen_phe_msk_idx (mask);


drop table if exists tran_upkeep.data_600k_phenotype_ontology;
create table tran_upkeep.data_600k_phenotype_ontology (
  id                           int not null auto_increment primary key,
  phenotype_ontology_id        varchar(50) not null,
  phenotype_code               varchar(50) not null,
  phenotype_translator_name    varchar(250) not null,
  phenotype_data_name          varchar(250) not null,
  has_translator_name          varchar(1) not null,
  date_created                 datetime DEFAULT CURRENT_TIMESTAMP
);
-- indices
alter table tran_upkeep.data_600k_phenotype_ontology add index phe_ont_phe_cde_idx (phenotype_code);


-- scratch 
-- find the gene/phenotypes for ontology_id
select gene.gene_code, phe.phenotype_ontology_id, gene.p_value, gene.mask, phe.phenotype_translator_name
from data_600k_gene_phenotype gene, data_600k_phenotype_ontology phe 
where gene.phenotype_code = phe.phenotype_code
and gene.p_value < 0.0025 and gene.mask = 'LoF_HC'
order by phe.phenotype_translator_name, gene.gene_code;

-- count the gene/phenotypes for ontology_id
select count(gene.id), phe.phenotype_ontology_id, phe.phenotype_translator_name
from tran_upkeep.data_600k_gene_phenotype gene, tran_upkeep.data_600k_phenotype_ontology phe 
where gene.phenotype_code = phe.phenotype_code
and gene.p_value < 0.0025 and gene.mask = 'LoF_HC'
group by phe.phenotype_ontology_id, phe.phenotype_translator_name
order by phe.phenotype_translator_name, phe.phenotype_ontology_id;
-- 496 rows in set (0.71 sec)


select count(id), mask from tran_upkeep.data_600k_gene_phenotype group by mask;


select distinct mask from tran_upkeep.data_600k_gene_phenotype;

select * from data_600k_phenotype_ontology ont1, data_600k_phenotype_ontology ont2 
where ont1.phenotype_ontology_id = ont2.phenotype_ontology_id
and ont1.id != ont2.id;

select * from data_600k_phenotype_ontology where regexp_like('[...]:[0..9]*', phenotype_ontology_id);

select id, phenotype_ontology_id, substring_index(phenotype_ontology_id, ':', 1) from data_600k_phenotype_ontology where substring_index(phenotype_ontology_id, ':', 1) > 0;


select distinct(substring_index(phenotype_ontology_id, ':', 1)) from data_600k_phenotype_ontology;

select * from data_600k_phenotype_ontology where substring_index(phenotype_ontology_id, ':', 1) = 'MP';
select * from data_600k_phenotype_ontology where substring_index(phenotype_ontology_id, ':', 1) = 'OBA';

-- 
select * from data_600k_phenotype_ontology where substring_index(phenotype_ontology_id, ':', 1) = 'UBERON';


-- change orphanet to mondo
select * from data_600k_phenotype_ontology where substring_index(phenotype_ontology_id, ':', 1) = 'Orphanet';

update data_600k_phenotype_ontology set phenotype_ontology_id = 'MONDO:0015978' where phenotype_code = 'phecode_288.0';
update data_600k_phenotype_ontology set phenotype_ontology_id = 'MONDO:0017427' where phenotype_code = 'phecode_736.0';
update data_600k_phenotype_ontology set phenotype_ontology_id = 'MONDO:0008399' where phenotype_code = 'phecode_697.0';
update data_600k_phenotype_ontology set phenotype_ontology_id = 'MONDO:0017760' where phenotype_code = 'phecode_261.2';
update data_600k_phenotype_ontology set phenotype_ontology_id = 'MONDO:0009061' where phenotype_code = 'phecode_499.0';
update data_600k_phenotype_ontology set phenotype_ontology_id = 'MONDO:0002525' where phenotype_code = 'phecode_277.5';
update data_600k_phenotype_ontology set phenotype_ontology_id = 'MONDO:0019216' where phenotype_code = 'phecode_270.0';


-- data changes
-- update data_600k_phenotype_ontology set phenotype_ontology_id = 'UMLS:C0155959' where id = 1086;
-- cysts oral tissues
-- 
-- UMLS:C0159040 from OBA:0002774
-- changes in skin texture
-- 
-- HP:0002533 replces MP:0001504
-- abnormal posture 
--
-- MONDO:0005392 replaces MP:0004174
-- curvature of spine 



