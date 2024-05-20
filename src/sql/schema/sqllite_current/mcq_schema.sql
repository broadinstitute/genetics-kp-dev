
-- schema for the multi curie queries
-- phenotype to gene in our instance

-- phenotype tables
drop table mcq_phenotype;
CREATE TABLE IF NOT EXISTS mcq_phenotype (
    id INTEGER PRIMARY KEY, 
    ontology_id TEXT, 
    query_ontology_id TEXT, 
    name TEXT,
    namer_translator TEXT
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



-- updates
update mcq_phenotype set query_ontology_id = 'HP:0001382' where name = 'joint_stiffness';
update mcq_phenotype set query_ontology_id = 'HP:0100785' where name = 'insomnia';
update mcq_phenotype set query_ontology_id = 'HP:5200207' where name = 'decreased_concetration';
update mcq_phenotype set query_ontology_id = 'HP:5200207' where name = 'attention_function';
update mcq_phenotype set query_ontology_id = 'HP:0001252' where name = 'thigh_muscle_fat_percentage';
update mcq_phenotype set query_ontology_id = 'HP:0020221' where name = 'clonic_tonic';
update mcq_phenotype set query_ontology_id = 'HP:0032792' where name = 'clonic_tonic';
update mcq_phenotype set query_ontology_id = 'HP:0010862' where name = 'motor_delay';
update mcq_phenotype set query_ontology_id = 'HP:0002317' where name = 'gait_disturbance';
update mcq_phenotype set query_ontology_id = 'HP:0001250' where name = 'seizures';
update mcq_phenotype set query_ontology_id = 'HP:0001251' where name = 'falling_risk';
update mcq_phenotype set query_ontology_id = 'HP:0000752' where name = 'adhd';
update mcq_phenotype set query_ontology_id = 'HP:0001250' where name = 'epilepsy';
update mcq_phenotype set query_ontology_id = 'HP:0031491' where name = 'eeg';

-- update mcq_phenotype set ontology_id = '' where name = 'handedness';
-- update mcq_phenotype set ontology_id = '' where name = 'cerebellar_volume';


-- update mcq_phenotype set ontology_id = '' where name = '';


-- test
select * from mcq_phenotype;

select gene_pheno.gene, pheno.name, gene_pheno.probability
from mcq_phenotype pheno, mcq_gene_phenotype gene_pheno 
where gene_pheno.phenotype = pheno.name 
and pheno.name = 'adhd'
order by gene_pheno.probability desc 
limit 20;



select gene_pheno.gene, pheno.name, gene_pheno.probability
from mcq_phenotype pheno, mcq_gene_phenotype gene_pheno 
where gene_pheno.phenotype = pheno.name 
and pheno.name in ('adhd', 'seizures')
order by gene_pheno.probability desc 
limit 20;



-- query by curie
select gene_pheno.gene, pheno.name, pheno.query_ontology_id, gene_pheno.probability
from mcq_phenotype pheno, mcq_gene_phenotype gene_pheno 
where gene_pheno.phenotype = pheno.name 
and pheno.query_ontology_id in ('HP:0000752', 'HP:0001250')
order by gene_pheno.probability desc 
limit 20;




-- scratch
-- update mcq_phenotype set query_ontology_id = 'HP:0001382' where name = 'joint_stiffness';
-- update mcq_phenotype set query_ontology_id = 'HP:0100785' where name = 'insomnia';
-- update mcq_phenotype set query_ontology_id = 'HP:5200207' where name = 'decreased_concetration';
-- update mcq_phenotype set query_ontology_id = 'HP:5200207' where name = 'attention_function';
-- update mcq_phenotype set query_ontology_id = 'HP:0001252' where name = 'thigh_muscle_fat_percentage';
-- update mcq_phenotype set query_ontology_id = 'HP:0020221' where name = 'clonic_tonic';
-- update mcq_phenotype set query_ontology_id = 'HP:0032792' where name = 'clonic_tonic';
-- update mcq_phenotype set query_ontology_id = 'HP:0010862' where name = 'motor_delay';
-- update mcq_phenotype set query_ontology_id = 'HP:0002317' where name = 'gait_disturbance';
-- update mcq_phenotype set query_ontology_id = 'HP:0001250' where name = 'seizures';
-- update mcq_phenotype set query_ontology_id = 'HP:0001251' where name = 'falling_risk';
-- update mcq_phenotype set query_ontology_id = 'HP:0000752' where name = 'adhd';
-- update mcq_phenotype set query_ontology_id = 'HP:0001250' where name = 'epilepsy';
-- update mcq_phenotype set query_ontology_id = 'HP:0031491' where name = 'eeg';


