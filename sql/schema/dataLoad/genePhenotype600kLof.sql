

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
-- 20230213 - adding calculated probability
alter table tran_upkeep.data_600k_gene_phenotype add column probability_calculated double;

-- indices
alter table tran_upkeep.data_600k_gene_phenotype add index gen_phe_phe_cde_idx (phenotype_code);
alter table tran_upkeep.data_600k_gene_phenotype add index gen_phe_pval_idx (p_value);
alter table tran_upkeep.data_600k_gene_phenotype add index gen_phe_msk_idx (mask);


drop table if exists tran_upkeep.data_600k_phenotype_ontology;
create table tran_upkeep.data_600k_phenotype_ontology (
  id                           int not null auto_increment primary key,
  phenotype_ontology_id        varchar(50) not null,
  phenotype_code               varchar(50) not null,
  node_type                    varchar(50) not null,
  phenotype_translator_name    varchar(250) not null,
  phenotype_data_name          varchar(250) not null,
  has_translator_name          varchar(1) not null,
  date_created                 datetime DEFAULT CURRENT_TIMESTAMP
);
-- indices
alter table tran_upkeep.data_600k_phenotype_ontology add index phe_ont_phe_cde_idx (phenotype_code);






-- scratch 
-- get the 600k data that is lof and significant
select link.id, link.gene_code, phenotype.phenotype_code, phenotype.phenotype_ontology_id, 
  phenotype.node_type, phenotype.phenotype_translator_name,
  link.ancestry, link.mask, link.p_value, link.beta
from tran_upkeep.data_600k_gene_phenotype link, tran_upkeep.data_600k_phenotype_ontology phenotype 
where link.phenotype_code = phenotype.phenotype_code
and link.p_value < 0.0025 and link.mask = 'LoF_HC'
order by link.p_value;

-- get count for only negative betas
select link.id, link.gene_code, phenotype.phenotype_code, phenotype.phenotype_ontology_id as curie, 
  phenotype.node_type, substring(phenotype.phenotype_translator_name, 1, 20) as name,
  link.ancestry, link.mask, link.p_value, link.beta
from tran_upkeep.data_600k_gene_phenotype link, tran_upkeep.data_600k_phenotype_ontology phenotype 
where link.phenotype_code = phenotype.phenotype_code
and link.p_value < 0.0025 and link.mask = 'LoF_HC' and link.beta < 0
order by link.p_value;

-- EFO:0010830
-- MONDO:0021839
-- MONDO:0004975

-- get specific row
select link.id, link.gene_code, phenotype.phenotype_code, phenotype.phenotype_ontology_id, 
  phenotype.node_type, phenotype.phenotype_translator_name,
  link.ancestry, link.mask, link.p_value, link.beta
from tran_upkeep.data_600k_gene_phenotype link, tran_upkeep.data_600k_phenotype_ontology phenotype 
where link.phenotype_code = phenotype.phenotype_code
and link.id = 18113562
order by link.p_value;


-- test row ids
-- 13266554
-- 
-- count all relevant associations
select count(link.id)
from tran_upkeep.data_600k_gene_phenotype link, tran_upkeep.data_600k_phenotype_ontology phenotype 
where link.phenotype_code = phenotype.phenotype_code
and link.p_value < 0.0025 and link.mask = 'LoF_HC';


select count(link.id), link.mask
from tran_upkeep.data_600k_gene_phenotype link, tran_upkeep.data_600k_phenotype_ontology phenotype 
where link.phenotype_code = phenotype.phenotype_code
and link.p_value < 0.0025 and beta >= 0
group by mask;

-- select all relevant associations
select link.id, link.gene_code, phenotype.phenotype_code, phenotype.phenotype_ontology_id, 
phenotype.node_type, phenotype.phenotype_translator_name,
link.ancestry, link.mask, link.p_value, link.beta
from tran_upkeep.data_600k_gene_phenotype link, tran_upkeep.data_600k_phenotype_ontology phenotype 
where link.phenotype_code = phenotype.phenotype_code
and link.p_value < 0.0025 and link.mask = 'LoF_HC'
order by link.phenotype_code;


-- 
-- and phenotype.phenotype_ontology_id = 'MONDO:0004975' 


-- find the gene/phenotypes for ontology_id
select gene.gene_code, phe.phenotype_ontology_id, phe.node_type, gene.p_value, gene.mask, phe.phenotype_translator_name
from data_600k_gene_phenotype gene, data_600k_phenotype_ontology phe 
where gene.phenotype_code = phe.phenotype_code
and gene.p_value < 0.0025 and gene.mask = 'LoF_HC'
order by phe.phenotype_translator_name, gene.gene_code;

-- count the gene/phenotypes for ontology_id
select count(gene.id) as num, phe.phenotype_ontology_id, phe.node_type, phe.phenotype_translator_name
from tran_upkeep.data_600k_gene_phenotype gene, tran_upkeep.data_600k_phenotype_ontology phe 
where gene.phenotype_code = phe.phenotype_code
and gene.p_value < 0.0025 and gene.mask = 'LoF_HC' and beta < 0
group by phe.phenotype_ontology_id, phe.phenotype_translator_name, phe.node_type
order by phe.phenotype_translator_name, phe.phenotype_ontology_id;
-- 496 rows in set (0.71 sec)

-- for the 202302 relay
select count(gene.id) as num, phe.phenotype_ontology_id as curie, substring(phe.phenotype_translator_name, 1, 20) as name
from tran_upkeep.data_600k_gene_phenotype gene, tran_upkeep.data_600k_phenotype_ontology phe 
where gene.phenotype_code = phe.phenotype_code
and gene.p_value < 0.0025 and gene.mask = 'LoF_HC' and beta < 0 and phe.node_type = 'biolink:Disease'
group by phe.phenotype_ontology_id, phe.phenotype_translator_name, phe.node_type
order by phe.phenotype_translator_name, phe.phenotype_ontology_id;


select gene.gene_code, gene.p_value, gene.beta, phe.phenotype_ontology_id as curie, substring(phe.phenotype_translator_name, 1, 20) as name
from tran_upkeep.data_600k_gene_phenotype gene, tran_upkeep.data_600k_phenotype_ontology phe 
where gene.phenotype_code = phe.phenotype_code
and gene.p_value < 0.0025 and gene.mask = 'LoF_HC' and beta < 0 and phe.node_type = 'biolink:Disease'
order by phe.phenotype_translator_name, phe.phenotype_ontology_id;


select count(id), mask from tran_upkeep.data_600k_gene_phenotype group by mask;


select distinct mask from tran_upkeep.data_600k_gene_phenotype;

select * from data_600k_phenotype_ontology ont1, data_600k_phenotype_ontology ont2 
where ont1.phenotype_ontology_id = ont2.phenotype_ontology_id
and ont1.id != ont2.id;

select * from data_600k_phenotype_ontology where regexp_like('[...]:[0..9]*', phenotype_ontology_id);

select id, phenotype_ontology_id, substring_index(phenotype_ontology_id, ':', 1) from data_600k_phenotype_ontology where substring_index(phenotype_ontology_id, ':', 1) > 0;


select count(id), substring_index(phenotype_ontology_id, ':', 1) as prefix
from data_600k_phenotype_ontology
group by prefix;

select count(id) from data_600k_phenotype_ontology;



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



-- range of beta
select max(gene.beta), min(gene.beta)
from tran_upkeep.data_600k_gene_phenotype gene, tran_upkeep.data_600k_phenotype_ontology phe 
where gene.phenotype_code = phe.phenotype_code
and gene.p_value < 0.0025 and gene.mask = 'LoF_HC';
-- +----------------+----------------+
-- | max(gene.beta) | min(gene.beta) |
-- +----------------+----------------+
-- |         451.54 |          -1.49 |
-- +----------------+----------------+

select count(gene.id),
 case 
  when gene.beta between -10 and 0 then '0-less_than_0'
  when gene.beta between 0 and 25 then '1-under_25'
         when gene.beta between 25 and 50 then '2-between_25_50'
         when gene.beta between 50 and 100 then '3-between_50_100'
         when gene.beta between 100 and 9999 then '4-over_100'
    end as grp
from tran_upkeep.data_600k_gene_phenotype gene, tran_upkeep.data_600k_phenotype_ontology phe 
where gene.phenotype_code = phe.phenotype_code
and gene.p_value < 0.0025 and gene.mask = 'LoF_HC'
group by grp
order by grp;




select max(gene.beta), min(gene.beta)
from tran_upkeep.data_600k_gene_phenotype gene, tran_upkeep.data_600k_phenotype_ontology phe 
where gene.phenotype_code = phe.phenotype_code
and gene.p_value < 0.0025 and gene.mask = 'LoF_HC';


group by phe.phenotype_ontology_id, phe.phenotype_translator_name, phe.node_type
order by phe.phenotype_translator_name, phe.phenotype_ontology_id;


