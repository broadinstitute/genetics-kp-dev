
# Genetics Knowledge Provider - Data Upload/Refresh 
The data is reloaded everytime new phenotype association statistics are calculated in the aggregator

# Data to upload
The data is uploaded to a staging schema, then transformed and loaded into the translator schema node/edges tables
The staging schema is tran_upkeep


## Data Upkeep Tables (from which the translator application comb_* tables get loaded)

### Phenotypes
* `agg_phenotype` - will contain the phenotypes loaded from the bioindex/aggregator API

### Pathways
* `data_pathway` - data loaded from the msigdb files (current;y c2 and c5)
* `data_pathway_genes` - data loaded from the the msigdb files (currently c2 and c5)
* `agg_pathway_phenotype` - will contain the data loaded from the aggregator S3 magma process output
* `calc_pathway_similarity` - used to store computed pathway similarity measures (deprecated due to having all pathway data)

### Genes
* `agg_gene_phenotype` - will contain the data loaded from the aggregator S3 magma process output

### Drugs
* `molepro_drug_gene` - data downloaded from molepro that has the gene/drug/predicate triples for selected predicates
* `molepro_gene_status` - used to track the upload of the molepro drug/gene data to the translator schema tables

## Data Load/Refresh Process
### Phenotypes
* load the new phenotypes and find the ontology ids for what you can (agg_phenotype)
* mark the phenotypes already in translator (determined by the phenotype code, not ontology_id)
* find the ontology_id for the ones not already in translator (have no ontology_id)
* load the new phenotypes with ontology IDs not already in translator for magma (by phenotype code) into translator

### Pathways
* load the new pathways into translator (if updated)
* load the pathway/phenotype magma associations from S3 into the upkeep table
* refresh (delete/insert) the pathway/phenotype magma associations
  * cutoff is for loading is is pValue less than 0.05

### Genes (magma)
* refresh the upkeep gene/phenotype magma method associations (agg_gene_phenotype_magma)
* refresh (delete/insert) the translator db gene/phenotype magma associations
  * cutoff is for loading is is pValue less than 0.0025

### Genes (pigean)
* refresh the upkeep gene/phenotype pigean method associations (agg_gene_phenotype_pigean)


### Tissues
* load into the upkeep db the new tissues and find the ontology ids for what you can (agg_tissue)
* refresh the upkeep db tissue/phenotype associations (agg_tissue_phenotype)
