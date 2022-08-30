# Creative Mode Test
The Genetics KP provides results for drug-treats-disease creative mode queries. 
The following genetic association criteria  and process used for the drugs found is:
## Selection Criteria
* find genes that are genetically associated to the disease
  * use 6 10e-6 as the max value filter
* filter those resulting genes using the pathways/gene setzs they are a part of that have a genetic assocaition with the disease
  * use 5 10e-4 as the max value filter
* any genes that pass both the above filters, return linked drugs that regulate those genes

