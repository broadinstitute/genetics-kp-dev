
-- schema for the multi curie queries
-- phenotype to gene in our instance

-- phenotype tables
drop table mcq_phenotype;
CREATE TABLE IF NOT EXISTS mcq_phenotype (
    id INTEGER PRIMARY KEY, 
    name TEXT
);


-- gene/phenotype data table
drop table mcq_gene_phenotype;
CREATE TABLE IF NOT EXISTS mcq_gene_phenotype (
    id INTEGER PRIMARY KEY, 
    phenotype TEXT,
    gene TEXT,
    probability REAL,
    created_at DATE DEFAULT (DATE('now', 'localtime'))
);



