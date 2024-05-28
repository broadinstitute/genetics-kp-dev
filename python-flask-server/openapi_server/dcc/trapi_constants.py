
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

BIOLINK_PREDICATE_GENETIC_ASSOCIATION = 'biolink:genetic_association'


# constants
BIOLINK_SCORE = 'biolink:score'
BIOLINK_BETA = 'biolink:beta'
BIOLINK_PVALUE = 'biolink:p-value'
BIOLINK_STANDARD_ERROR = 'biolink:standard_error'
BIOLINK_PROBABILITY = 'biolink:probability'
BIOLINK_CLASSIFICATION = 'biolink:classification'
BIOLINK_PUBLICATION = 'biolink:publications'
BIOLINK_SUPPORT_GRAPH = 'biolink:support_graphs'
BIOLINK_KNOWLEDGE_LEVEL = 'biolink:knowledge_level'
BIOLINK_AGENT_TYPE = 'biolink:agent_type'

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


MAP_NAME_ATTRIBUTE = {
    BIOLINK_SCORE: NAME_SCORE,
    BIOLINK_BETA: NAME_BETA,
    BIOLINK_PVALUE: NAME_PVALUE,
    BIOLINK_STANDARD_ERROR: NAME_STANDARD_ERROR, 
    BIOLINK_PROBABILITY: NAME_PROBABILITY,
    BIOLINK_CLASSIFICATION: NAME_CLASSIFICATION,
    BIOLINK_PUBLICATION: NAME_PUBLICATIONS
}

# provenance
PROVENANCE_INFORES_KP_GENETICS='infores:genetics-data-provider'
PROVENANCE_INFORES_KP_MOLEPRO='infores:molepro'
PROVENANCE_INFORES_CLINVAR='infores:clinvar'
PROVENANCE_INFORES_CLINGEN='infores:clingen'
PROVENANCE_INFORES_GENCC='infores:gencc'
PROVENANCE_INFORES_GENEBASS='infores:genebass'
PROVENANCE_INFORES_RICHARDS='infores:regl'

