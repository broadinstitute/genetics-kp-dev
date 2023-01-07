

select count(id), in_translator, just_added_in 
from agg_aggregator_phenotype 
group by in_translator, just_added_in;



select count(id), in_translator, just_added_in 
from agg_aggregator_phenotype 
where ontology_id is not null
group by in_translator, just_added_in;


select * from tran_upkeep.agg_aggregator_phenotype
where in_translator = 'false' and ontology_id is not null
order by phenotype_name;


select * from comb_node_ontology
where ontology_id collate utf8mb4_unicode_ci in (
    select ontology_id from tran_upkeep.agg_aggregator_phenotype
    where in_translator = 'false' and ontology_id is not null
);


select distinct ontology_id as curie, node_name as phenotype
from comb_node_ontology
where ontology_id collate utf8mb4_unicode_ci in (
    select ontology_id from tran_upkeep.agg_aggregator_phenotype
    where in_translator = 'false' and ontology_id is not null
)
order by node_name;



-- 20221011
+---------------+-----------------------------------------------------+
| curie         | phenotype                                           |
+---------------+-----------------------------------------------------+
| HP:0025354    | Abnormal cellular phenotype                         |
| MONDO:0005570 | Abnormality of blood and blood-forming tissues      |
| HP:0000152    | Abnormality of head or neck                         |
| HP:0040064    | Abnormality of limbs                                |
| HP:0001197    | Abnormality of prenatal development or birth        |
| HP:0000769    | Abnormality of the breast                           |
| MONDO:0004995 | Abnormality of the cardiovascular system            |
| HP:0025031    | Abnormality of the digestive system                 |
| HP:0000598    | Abnormality of the ear                              |
| MONDO:0005151 | Abnormality of the endocrine system                 |
| MONDO:0005328 | Abnormality of the eye                              |
| MONDO:0021145 | Abnormality of the genitourinary system             |
| HP:0002715    | Abnormality of the immune system                    |
| HP:0001574    | Abnormality of the integument                       |
| HP:0033127    | Abnormality of the musculoskeletal system           |
| MONDO:0020022 | Abnormality of the nervous system                   |
| HP:0002086    | Abnormality of the respiratory system               |
| HP:0045027    | Abnormality of the thoracic cavity                  |
| HP:0001608    | Abnormality of the voice                            |
| MONDO:0004995 | Any cardiovascular disease                          |
| MONDO:0005130 | Celiac disease                                      |
| MONDO:0005300 | Chronic kidney disease                              |
| MONDO:0005155 | Cirrhosis                                           |
| HP:0025142    | Constitutional symptom                              |
| MONDO:0005300 | End-stage renal disease                             |
| UMLS:C0409936 | Finger osteoarthritis                               |
| MONDO:0005406 | Gestational diabetes                                |
| HP:0001507    | Growth abnormality                                  |
| UMLS:C0263746 | Hand osteoarthritis                                 |
| EFO:0009289   | Left ventricular mass                               |
| EFO:0010556   | Left ventricular mass to end-diastolic volume ratio |
| MONDO:0007488 | Lewy body dementia                                  |
| HP:0012594    | Macroalbuminuria                                    |
| HP:0012594    | Microalbuminuria                                    |
| MONDO:0004910 | Mitral valve prolapse                               |
| MONDO:0021079 | Neoplasm                                            |
| MONDO:0005386 | Peripheral artery disease                           |
| EFO:0005192   | Red blood cell distribution width                   |
| MONDO:0008383 | Rheumatoid arthritis                                |
| EFO:0004831   | RR interval                                         |
| MONDO:0006630 | Spine osteoarthritis                                |
| MONDO:0007915 | Systemic lupus erythematosus                        |
| MONDO:0007915 | systemic lupus erythematosus (disease)              |
| MONDO:0012893 | Thumb osteoarthritis                                |
+---------------+-----------------------------------------------------+


