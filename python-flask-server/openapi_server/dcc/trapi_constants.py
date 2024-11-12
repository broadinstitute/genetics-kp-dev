
# constants
SET_INTERPRETATION_MANY = "MANY"
SET_INTERPRETATION_ALL = "ALL"
SET_INTERPRETATION_BATCH = "BATCH"

OPERATION_LOOKUP = "lookup"

KNOWLEDGE_TYPE_INFERRED = "inferred"


# biolink
BIOLINK_ENTITY_GENE = 'biolink:Gene'
BIOLINK_ENTITY_SET = 'biolink:Set'
BIOLINK_ENTITY_DISEASE = 'biolink:Disease'
BIOLINK_ENTITY_PHENOTYPE = 'biolink:PhenotypicFeature'
BIOLINK_ENTITY_CELL = 'biolink:Cell'

BIOLINK_PREDICATE_GENETIC_ASSOCIATION = 'biolink:genetic_association'


# constants
BIOLINK_SCORE = 'biolink:score'
BIOLINK_SCORE_NOT_NORMALIZED = 'biolink:score_not_normalized'
BIOLINK_BETA = 'biolink:beta'
BIOLINK_PVALUE = 'biolink:p-value'
BIOLINK_STANDARD_ERROR = 'biolink:standard_error'
BIOLINK_PROBABILITY = 'biolink:probability'
BIOLINK_CLASSIFICATION = 'biolink:classification'
BIOLINK_PUBLICATION = 'biolink:publications'
BIOLINK_SUPPORT_GRAPH = 'biolink:support_graphs'
BIOLINK_KNOWLEDGE_LEVEL = 'biolink:knowledge_level'
BIOLINK_AGENT_TYPE = 'biolink:agent_type'
BIOLINK_ENRICHMENT = 'biolink:enrichment'
BIOLINK_ANNOTATION = 'biolink:annotation'

TYPE_VALUE_STRING = 'String'
TYPE_VALUE_DOUBLE = 'Double'
TYPE_VALUE_PUBLICATIONS = 'linkml:Uriorcurie'


KNOWLEDGE_STATS = 'statistical_association'
KNOWLEDGE_PREDICTION = 'prediction'

AGENT_COMPUTATION = "computational_model"
AGENT_PIPELINE = "data_analysis_pipeline"

INFORES_ROOT = "infores:cmap"

NAME_KNOWLEDGE_LEVEL = 'knowledge level'
NAME_AGENT_TYPE = 'agent type'
NAME_PUBLICATIONS = 'publications'
NAME_SCORE = 'score'
NAME_BETA = 'beta'
NAME_PVALUE = 'p-value'
NAME_STANDARD_ERROR = 'standard error'
NAME_PROBABILITY = 'probability'
NAME_CLASSIFICATION = 'classification'
NAME_ENRICHMENT = 'enrichment'
NAME_ANNOTATION = 'annotation'


MAP_NAME_ATTRIBUTE = {
    BIOLINK_SCORE: NAME_SCORE,
    BIOLINK_BETA: NAME_BETA,
    BIOLINK_PVALUE: NAME_PVALUE,
    BIOLINK_STANDARD_ERROR: NAME_STANDARD_ERROR, 
    BIOLINK_PROBABILITY: NAME_PROBABILITY,
    BIOLINK_CLASSIFICATION: NAME_CLASSIFICATION,
    BIOLINK_PUBLICATION: NAME_PUBLICATIONS,
    BIOLINK_ENRICHMENT: NAME_ENRICHMENT,
    BIOLINK_ANNOTATION: NAME_ANNOTATION
}

# provenance
PROVENANCE_INFORES_KP_GENETICS='infores:genetics-data-provider'
PROVENANCE_INFORES_KP_MOLEPRO='infores:molepro'
PROVENANCE_INFORES_CLINVAR='infores:clinvar'
PROVENANCE_INFORES_CLINGEN='infores:clingen'
PROVENANCE_INFORES_GENCC='infores:gencc'
PROVENANCE_INFORES_GENEBASS='infores:genebass'
PROVENANCE_INFORES_RICHARDS='infores:regl'

# ontologies
ONTOLOGY_PREFIX_EFO = "EFO"
ONTOLOGY_PREFIX_GO = "GO"
ONTOLOGY_PREFIX_HP = "HP"
ONTOLOGY_PREFIX_MESH = "MESH"
ONTOLOGY_PREFIX_MONDO = "MONDO"
ONTOLOGY_PREFIX_NCBIGENE = "NCBIGene"
ONTOLOGY_PREFIX_NCIT = "NCIT"
ONTOLOGY_PREFIX_UBERON = "UBERON"
ONTOLOGY_PREFIX_UMLS = "UMLS"

LIST_ACCEPTED_ONTOLOGIES = [ONTOLOGY_PREFIX_EFO, ONTOLOGY_PREFIX_GO, ONTOLOGY_PREFIX_HP, ONTOLOGY_PREFIX_MESH, ONTOLOGY_PREFIX_MONDO, ONTOLOGY_PREFIX_NCBIGENE, ONTOLOGY_PREFIX_NCIT,
                            ONTOLOGY_PREFIX_UBERON, ONTOLOGY_PREFIX_UMLS]



# map keys for results
KEY_EDGE_ID = 'edge_id'
KEY_ROW_ID = 'db_row_id'
KEY_SUBJECT_ID = 'subject_id'
KEY_OBJECT_ID = 'object_id'
KEY_SUBJECT_TYPE = 'subject_type'
KEY_OBJECT_TYPE = 'object_type'
KEY_EDGE_TYPE = 'edge_type'
KEY_SUBJECT_NAME = 'subject_name'
KEY_OBJECT_NAME = 'object_name'
KEY_SCORE = 'score'
KEY_SCORE_TRANSLATOR = 'score_translator'
KEY_PVALUE = 'p_value'
KEY_BETA = 'beta'
KEY_STD_ERROR = 'std_error'
KEY_PROB = 'probability'
KEY_PROB_BAYES = 'probability_bayes'
KEY_ENRICHMENT = 'enrichment'
KEY_ANNOTATION = 'annotation'
KEY_STUDY_ID = 'study_id'
KEY_PUBLICATIONS = 'publications'



# DB lookup values
DB_STUDY_ID_GENETICS = 1


