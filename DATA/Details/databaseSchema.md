
# Genetics KP Database Schema Information

## Edge table
```
+------------------------------+-----------+
| COLUMN_NAME                  | DATA_TYPE |
+------------------------------+-----------+
| id                           | int       |
| edge_id                      | varchar   | - edge id returned in results
| source_node_id               | int       | - FK to comb_node_ontology table
| target_node_id               | int       | - FK to comb_node_ontology table
| edge_type_id                 | int       | - FK to comb_lookup table
| score                        | double    | - (depraceted) - p_value or prob
| score_text                   | varchar   | - (deprecated) - if text score
| score_type_id                | int       | - (deprecated) - indicates p_value or prob
| study_id                     | int       | - FK to comb_study table
| date_created                 | datetime  | 
| score_translator             | double    | - prob score for translator ranking
| study_secondary_id           | int       | - FK to comb_study table
| publication_ids              | varchar   | - array of PMIDs
| has_qualifiers               | enum      | - if data is qualified (trapi 1.3)  - DEPRECATED
| p_value                      | double    |
| beta                         | double    |
| standard_error               | double    |
| probabilty                   | double    |
| probability_app_bayes_factor | double    |
+------------------------------+-----------+

```
- the score_translator will be a 0 to 1 probability
- p_value populated when available
- beta populated when available
- standard_error populated when available
- probability populated when available
- probability_app_bayes_factor populated when available
- study_id value will determine primary_knowledge_source


## Node table
```
+-------------------+-----------+
| COLUMN_NAME       | DATA_TYPE |
+-------------------+-----------+
| id                | int       |
| node_code         | varchar   | - internal DCC gene/phenotype lookup code
| node_type_id      | int       | - FK to comb_lookup, node type (gene, pheno, etc)
| ontology_id       | varchar   | - translator curie ID
| ontology_type_id  | varchar   | - FK to comb_ontology, ontology family
| node_name         | varchar   | - translator name returned
| last_updated      | datetime  |
| added_by_study_id | int       | - FK to comb_study
+-------------------+-----------+
```

