

drop table if exists tran_upkeep.data_genebass_gene_phenotype;
create table tran_upkeep.data_genebass_gene_phenotype (
  id                        int not null auto_increment primary key,
  gene                      varchar(100) not null,                          -- gene_symbol
  gene_ncbi_id              varchar(100),                             -- FROM JOINED LOOKUP TABLE
  phenotype_genebass        varchar(1000),                                  -- disease_title
  phenotype_ontology_id     varchar(100),                                   -- disease_curie
  phenotype_genepro_name    varchar(1000),                            -- FROM JOINED LOOKUP TABLE OR NODE NORMALIZER
  gene_genepro_id           int(9),
  phenotype_genepro_id      int(9),
  pheno_num_genebass        int(9),
  pheno_coding_genebass     int(9),
  pvalue                    double,                                    -- 
  standard_error            double,                                    -- 
  beta                      double,                                    -- 
  abf                       double,                                    -- approximate bayes factor
  probability               double,                                    -- probability from abf using prior 0.05
  score_genepro             double                                    -- classification calculated
);


alter table tran_upkeep.data_genebass_gene_phenotype add index geneb_gene_cde_idx (gene);


-- update data 
update tran_upkeep.data_genebass_gene_phenotype gb
      join tran_test_202303.comb_node_ontology node on node.node_code COLLATE utf8mb4_general_ci = gb.gene
      set gb.gene_ncbi_id = node.ontology_id 
      where gb.probability > 0.10 and node.node_type_id = 2 and gb.gene_ncbi_id is null;
