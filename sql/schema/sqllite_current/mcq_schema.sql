
-- schema for the multi curie queries
-- phenotype to gene in our instance

-- phenotype tables
drop table mcq_phenotype;
CREATE TABLE IF NOT EXISTS mcq_phenotype (
    id INTEGER PRIMARY KEY, 
    name TEXT
);




