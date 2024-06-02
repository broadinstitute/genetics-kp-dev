

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

