


-- mysql> select * from data_600k_phenotype_ontology where substring_index(phenotype_ontology_id, ':', 1) = 'Orphanet';
-- +-----+-----------------------+----------------+-------------------------------------------------------------------+-----------------------------------------------------------------+---------------------+---------------------+
-- | id  | phenotype_ontology_id | phenotype_code | phenotype_translator_name                                         | phenotype_data_name                                             | has_translator_name | date_created        |
-- +-----+-----------------------+----------------+-------------------------------------------------------------------+-----------------------------------------------------------------+---------------------+---------------------+
-- | 227 | Orphanet:183681       | phecode_288.0  | functional neutrophil defect                                      | Diseases of white blood cells                                   | Y                   | 2023-02-02 12:05:23 |
-- | 228 | Orphanet:294944       | phecode_736.0  | congenital deformities of limbs                                   | Other acquired deformities of limbs                             | Y                   | 2023-02-02 12:05:23 |
-- | 229 | Orphanet:797          | phecode_697.0  | sarcoidosis                                                       | Sarcoidosis                                                     | Y                   | 2023-02-02 12:05:23 |
-- | 290 | Orphanet:309833       | phecode_261.2  | disorder of other vitamins and cofactors metabolism and transport | Vitamin B-complex deficiencies                                  | Y                   | 2023-02-02 12:05:23 |
-- | 408 | Orphanet:586          | phecode_499.0  | cystic fibrosis                                                   | Cystic fibrosis                                                 | Y                   | 2023-02-02 12:05:23 |
-- | 484 | Orphanet:309005       | phecode_277.5  | inherited lipid metabolism disorder                               | Other disorders of lipoid metabolism                            | Y                   | 2023-02-02 12:05:23 |
-- | 494 | Orphanet:79166        | phecode_270.0  | inborn disorder of amino acid absorption and transport            | Disorders of protein plasma/amino-acid transport and metabolism | Y                   | 2023-02-02 12:05:23 |
-- +-----+-----------------------+----------------+-------------------------------------------------------------------+-----------------------------------------------------------------+---------------------+---------------------+
-- 7 rows in set (0.00 sec)

-- test insert
-- | 227 | Orphanet:183681       | phecode_288.0  | functional neutrophil defect                                      | Diseases of white blood cells                                   | Y                   | 2023-02-02 12:05:23 |
select * from comb_node_ontology where ontology_id = 'MONDO:0015978';





