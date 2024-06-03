

-- tissue/phenotype data
drop table if exists agg_tissue_phenotype;
create table agg_tissue_phenotype (
  id             int not null auto_increment primary key,
  phenotype      varchar(100) not null,
  ancestry       varchar(50) not null,
  annotation     varchar(50) not null,
  tissue         varchar(50) not null,
  expectedSNPs   double,
  SNPs           double,
  enrichment     double,
  pValue         double,
  date_created   datetime DEFAULT CURRENT_TIMESTAMP
);


drop table if exists agg_tissue;
create table agg_tissue (
  id                      int not null auto_increment primary key,
  tissue_name             varchar(100) not null,
  tran_service_name       varchar(100),
  ontology_id             varchar(50),
  loaded_in_translator    date,
  date_created            datetime DEFAULT CURRENT_TIMESTAMP
);



-- create temp table to load data from
drop table if exists temp_load_tissue_phenotype;
create table temp_load_tissue_phenotype as
select link.phenotype, link.tissue, tis.ontology_id, link.pValue, link.annotation, link.enrichment
from agg_tissue_phenotype link, agg_tissue tis
where link.tissue = tis.tissue_name 
and link.pValue <= 0.0001;



drop table if exists temp_load_tissue_phenotype;
create table temp_load_tissue_phenotype as
select link.phenotype as phenotype_code, link.tissue as tissue_code, tis.ontology_id as tissue_id, pheno.ontology_id as phenotype_id, pheno.node_name as phenotype_name,
  link.pValue, link.annotation, link.enrichment
from agg_tissue_phenotype link, agg_tissue tis, tran_test_202303.comb_node_ontology pheno
where link.tissue = tis.tissue_name 
and pheno.node_code COLLATE utf8mb4_general_ci = link.phenotype and pheno.node_type_id in (1, 3)
and link.pValue <= 0.0001;



-- from bioindex
            -- "phenotype": "C19vNeg",
            -- "ancestry": "Mixed",
            -- "annotation": "binding_sites",
            -- "biosample": "SUDHL10",
            -- "tissue": "blood",
            -- "expectedSNPs": 0.0001074280714960866,
            -- "SNPs": -0.6135903081129854,
            -- "enrichment": -5711.63849046045,
            -- "pValue": 0.009509951103556595

-- queries
select link.phenotype, link.tissue, tis.ontology_id, link.pValue, link.annotation, link.enrichment
from agg_tissue_phenotype link, agg_tissue tis
where link.tissue = tis.tissue_name 
and link.pValue <= 0.0001;


