

from logging import log
import six
import copy
import os
import time 
import yaml 

from openapi_server.models.message import Message
from openapi_server.models.knowledge_graph import KnowledgeGraph
from openapi_server.models.edge import Edge
from openapi_server.models.node import Node
from openapi_server.models.query import Query
from openapi_server.models.q_edge import QEdge
from openapi_server.models.q_node import QNode
from openapi_server.models.query_graph import QueryGraph
from openapi_server.models.qualifier import Qualifier
from openapi_server.models.result import Result
from openapi_server.models.edge_binding import EdgeBinding
from openapi_server.models.node_binding import NodeBinding
from openapi_server.models.response import Response
from openapi_server.models.attribute import Attribute
from openapi_server.models.analysis import Analysis
from openapi_server.models.retrieval_source import RetrievalSource
from openapi_server.models.resource_role_enum import ResourceRoleEnum
from openapi_server.models.auxiliary_graph import AuxiliaryGraph
from openapi_server.models.response import Response
from openapi_server.models.response_workflow import ResponseWorkflow
from openapi_server.models.response_message import ResponseMessage

from openapi_server.models.message_query_graph import MessageQueryGraph
from openapi_server.models.message_knowledge_graph import MessageKnowledgeGraph


from openapi_server import util
from openapi_server.dcc.creative_model import CreativeResult, CreativeEdge, CreativeNode
import openapi_server.dcc.trapi_constants as trapi_constants

from openapi_server.dcc.utils import translate_type, get_curie_synonyms, get_logger, build_pubmed_ids, get_normalize_curies
from openapi_server.dcc.genetics_model import GeneticsModel, NodeOuput, EdgeOuput
import openapi_server.dcc.query_builder as qbuilder
import openapi_server.dcc.trapi_extract as textract

# set up the logger
logger = get_logger("trapi_utils")

# read trapi and biolink versions
VERSION_BIOLINK = 0.1
VERSION_TRAPI = 1.0
with open("./openapi_server/openapi/openapi.yaml", "r") as stream:
    try:
        map_openapi = yaml.safe_load(stream)
        VERSION_BIOLINK = map_openapi.get('info').get('x-translator').get('biolink-version')
        VERSION_TRAPI = map_openapi.get('info').get('x-trapi').get('version')
        # print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)
logger.info("Using biolink version: {} and trapi version: {}".format(VERSION_BIOLINK, VERSION_TRAPI))

# query set interpretation
SET_INTERPRETATION_BATCH = 'BATCH'
SET_INTERPRETATION_ALL = 'ALL'
SET_INTERPRETATION_MANY = 'MANY'

# infores
PROVENANCE_INFORES_KP_GENETICS='infores:genetics-data-provider'
PROVENANCE_INFORES_KP_MOLEPRO='infores:molepro'
PROVENANCE_INFORES_CLINVAR='infores:clinvar'
PROVENANCE_INFORES_CLINGEN='infores:clingen'
PROVENANCE_INFORES_GENCC='infores:gencc'
PROVENANCE_INFORES_GENEBASS='infores:genebass'
PROVENANCE_INFORES_RICHARDS='infores:regl'

# new source structure
SOURCE_AGGREGATOR_KP_GENETICS = RetrievalSource(
    resource_id=PROVENANCE_INFORES_KP_GENETICS,
    resource_role=ResourceRoleEnum.AGGREGATOR_KNOWLEDGE_SOURCE,
    source_record_urls=['https://github.com/broadinstitute/genetics-kp-dev/blob/master/DATA/Details/geneticsKp.md'],
    upstream_resource_ids=[])
SOURCE_PRIMARY_KP_GENETICS = RetrievalSource(
    resource_id=PROVENANCE_INFORES_KP_GENETICS,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://github.com/broadinstitute/genetics-kp-dev/blob/master/DATA/Details/magmaData.md'],
    upstream_resource_ids=[])
SOURCE_PRIMARY_KP_MOLEPRO = RetrievalSource(
    resource_id=PROVENANCE_INFORES_KP_MOLEPRO,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://github.com/broadinstitute/molecular-data-provider'],
    upstream_resource_ids=[])
SOURCE_PRIMARY_RICHARDS = RetrievalSource(
    resource_id=PROVENANCE_INFORES_RICHARDS,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://github.com/broadinstitute/genetics-kp-dev/blob/master/DATA/Details/richardsList.md'],
    upstream_resource_ids=[])
SOURCE_PRIMARY_CLINVAR = RetrievalSource(
    resource_id=PROVENANCE_INFORES_CLINVAR,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://www.ncbi.nlm.nih.gov/clinvar/'],
    upstream_resource_ids=[])
SOURCE_PRIMARY_CLINGEN = RetrievalSource(
    resource_id=PROVENANCE_INFORES_CLINGEN,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://clinicalgenome.org/'],
    upstream_resource_ids=[])
SOURCE_PRIMARY_GENCC = RetrievalSource(
    resource_id=PROVENANCE_INFORES_GENCC,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://thegencc.org/'],
    upstream_resource_ids=[])
SOURCE_PRIMARY_GENCC = RetrievalSource(
    resource_id=PROVENANCE_INFORES_GENEBASS,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://genebass.org/'],
    upstream_resource_ids=[])
SOURCE_PRIMARY_GENEBASS = RetrievalSource(
    resource_id=PROVENANCE_INFORES_GENEBASS,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://genebass.org/'],
    upstream_resource_ids=[])
SOURCE_PRIMARY_600k = RetrievalSource(
    resource_id=PROVENANCE_INFORES_KP_GENETICS,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://github.com/broadinstitute/genetics-kp-dev/blob/master/DATA/Details/Ellinor600k.md'],
    upstream_resource_ids=[])


# build map for study types
MAP_SOURCE = {1: SOURCE_PRIMARY_KP_GENETICS, 4: SOURCE_PRIMARY_RICHARDS, 5: SOURCE_PRIMARY_CLINGEN, 6: SOURCE_PRIMARY_CLINVAR, 7: SOURCE_PRIMARY_GENCC, 
              17: SOURCE_PRIMARY_GENEBASS, 18: SOURCE_PRIMARY_600k, 99:SOURCE_PRIMARY_KP_MOLEPRO}

# methods
def get_biolink_version(log=False):
    ''' 
    returns the biolink version
    '''
    return VERSION_BIOLINK

def get_trapi_version(log=False):
    ''' 
    returns the trapi version
    '''
    return VERSION_TRAPI

def build_attribute(value, value_type, name_original=None, id_source=None, log=False):
    '''
    builds an attribute and returns it 
    '''
    # initialization and defaults
    type_value = None
    source = None
    attribute_result = []
    attribute_name = name_original

    # get the name if not defined
    if not attribute_name:
        attribute_name = trapi_constants.MAP_NAME_ATTRIBUTE.get(value_type)

    # set the type
    if value_type in [trapi_constants.BIOLINK_BETA, trapi_constants.BIOLINK_PROBABILITY, trapi_constants.BIOLINK_PVALUE, trapi_constants.BIOLINK_STANDARD_ERROR, 
                        trapi_constants.BIOLINK_SCORE]:
        type_value = trapi_constants.TYPE_VALUE_DOUBLE
    elif value_type in [trapi_constants.BIOLINK_CLASSIFICATION, trapi_constants.BIOLINK_AGENT_TYPE, trapi_constants.BIOLINK_KNOWLEDGE_LEVEL]:
        type_value = trapi_constants.TYPE_VALUE_STRING
    elif value_type in [trapi_constants.BIOLINK_PUBLICATION]:
        type_value = trapi_constants.TYPE_VALUE_PUBLICATIONS

    # set the source of the data
    # - if score or probability, this is generated by genetics kp
    # - if not and have source id, then that is the source
    if value_type in [trapi_constants.BIOLINK_SCORE, trapi_constants.BIOLINK_PROBABILITY]:
        source = MAP_SOURCE.get(1).resource_id
    elif id_source:
        source = MAP_SOURCE.get(id_source).resource_id

    # build and return the attribute
    attribute_result = Attribute(attribute_type_id=value_type, attribute_source=source, original_attribute_name=attribute_name, value=value, attributes=[], value_type_id=type_value)
    return attribute_result


# def build_attribute_list(name_original, value, value_type, id_source=None, log=False):
#     '''
#     builds a new attribute and returns it; applies new fields based on data
#     '''
#     # initialization and defaults
#     type_value = None
#     source = None
#     list_result = []
#     agent_type = None
#     knowledge_level = None

#     # set the type
#     if value_type in [at_utils.BIOLINK_BETA, at_utils.BIOLINK_PROBABILITY, at_utils.BIOLINK_PVALUE, at_utils.BIOLINK_STANDARD_ERROR, 
#                         at_utils.BIOLINK_SCORE]
#         type_value = at_utils.TYPE_VALUE_DOUBLE
#     elif value_type in [at_utils.BIOLINK_CLASSIFICATION]:
#         type_value = at_utils.TYPE_VALUE_STRING

#     # set the source of the data
#     # - if score or probability, this is generated by genetics kp
#     # - if not and have source id, then that is the source
#     if value_type in [at_utils.BIOLINK_SCORE, at_utils.BIOLINK_PROBABILITY]:
#         source = MAP_SOURCE.get(1).resource_id
#     elif id_source:
#         source = MAP_SOURCE.get(id_source).resource_id

#     # build the main attribute
#     attribute_main = Attribute(attribute_type_id=value_type, attribute_source=source, original_attribute_name=name_original, value=value, attributes=[], value_type_id=type_value)
#     list_result.append(attribute_main)

#     # add agent type if type is compued/stats
#     if type_value in [at_utils.BIOLINK_SCORE, at_utils.BIOLINK_PROBABILITY]:
#         # if score/probability that we applied resoning to, then computational model and prediction
#         agent_type = at_utils.AGENT_COMPUTATION
#         knowledge_level = at_utils.KNOWLEDGE_PREDICTION
#     elif value_type in [at_utils.BIOLINK_BETA, at_utils.BIOLINK_PVALUE, at_utils.BIOLINK_STANDARD_ERROR, at_utils.BIOLINK_PVALUE]:
#         # if results come from straight computation but no reasoning, then stat assoc/pipeline
#         agent_type = at_utils.AGENT_PIPELINE
#         knowledge_level = at_utils.KNOWLEDGE_STATS
        
#     if agent_type:
#         att_agent = Attribute(attribute_type_id=at_utils.BIOLINK_AGENT_TYPE, original_attribute_name=at_utils.NAME_AGENT_TYPE, value=agent_type, attributes=[], 
#                               value_type_id=at_utils.TYPE_VALUE_STRING, attribute_source=MAP_SOURCE.get(1).resource_id)
#         list_result.append(att_agent)

#     if knowledge_level:
#         att_knowledge = Attribute(attribute_type_id=at_utils.BIOLINK_KNOWLEDGE_LEVEL, original_attribute_name=at_utils.NAME_KNOWLEDGE_LEVEL, value=knowledge_level, attributes=[], 
#                               value_type_id=at_utils.TYPE_VALUE_STRING, attribute_source=MAP_SOURCE.get(1).resource_id)
#         list_result.append(att_knowledge)

#     # return
#     return list_result


def create_list_attributes14(edge_element :CreativeEdge):
    ''' 
    creates a list fo attributes for the edge
    '''
    list_attributes = []

    # add in pvalue if applicable
    if edge_element.score:
        list_attributes.append(Attribute(original_attribute_name='pvalue', value=edge_element.score, attribute_type_id='biolink:p_value', attributes=[]))

    # return
    return list_attributes

def build_results_creative14(results_list, query_graph):
    """ build the trapi v1.0 response from the genetics model """
    # build the empty collections
    results = []
    knowledge_graph = KnowledgeGraph(nodes={}, edges={})
    nodes = {}
    # edges = {}

    # 1.4 - add auxiliary_graphs map at the message level
    auxiliary_graphs = {}

    # only returning for affects inferred predicate

    # loop through the results
    creative_result: CreativeResult
    for index, creative_result in enumerate(results_list):
        # DEBUG
        # if index > 0:
        #     print("{} - BREAK".format(index))
        #     break

        # initialize
        edge_binding_map = {}
        node_binding_map = {}
        list_aux_graph_edges = []
        # 1.4 - for each result, 
        # inferred edges go into auxiliary graph and referenced back to 


        #  - add all nodes to knowledge_graph/nodes map
        #  - create creative edge with drug/disease relationship
        #  - add all other edges to knowledge_graph/edges map, along with creative edge
        #  - create auxiliary_graphs map entry with all supporting edges
        #  - add in auxiliary_graphs entry above as biolink:support_graphs attribute to the creative edge
        #  - only add drug and disease nodes in node bindings
        #  - in analyses, only add creative edge in edge_bindings
        #  - in analyses, add genetics_kp as resource_id with score of gene probability
        # TODO - possible cleanup: add query_id to subject/object node bindings


        # source lists

        # add all the edges for this result
        edge_element :CreativeEdge

        # create the creative edge
        edge_creative: Edge = Edge(predicate=creative_result.predicate, subject=creative_result.drug.id, object=creative_result.disease.id, sources=[SOURCE_PRIMARY_KP_GENETICS],
                                   attributes=[], qualifiers=[])
        edge_creative_id = "{}_creative".format(index)
        knowledge_graph.edges[edge_creative_id] = edge_creative

        # add in drug_gene edge
        edge_element = creative_result.drug_gene
        edge_drug_gene: Edge = Edge(predicate=edge_element.predicate, subject=edge_element.subject.id, object=edge_element.target.id, 
                                    attributes=create_list_attributes14(edge_element), sources=[SOURCE_PRIMARY_KP_MOLEPRO, SOURCE_AGGREGATOR_KP_GENETICS], qualifiers=[])
        knowledge_graph.edges[edge_element.edge_id] = edge_drug_gene
        list_aux_graph_edges.append(edge_element.edge_id)

        # add in gene_disease edge
        edge_element = creative_result.gene_disease
        edge_gene_disease: Edge = Edge(predicate=edge_element.predicate, subject=edge_element.subject.id, object=edge_element.target.id, 
                                       attributes=create_list_attributes14(edge_element), sources=[SOURCE_PRIMARY_KP_GENETICS], qualifiers=[])
        knowledge_graph.edges[edge_element.edge_id] = edge_gene_disease
        score_result = edge_element.probability
        list_aux_graph_edges.append(edge_element.edge_id)

        # add in gene_pathway edge
        edge_element = creative_result.pathway_gene
        edge_gene_pathway: Edge = Edge(predicate=edge_element.predicate, subject=edge_element.subject.id, object=edge_element.target.id, 
                                       attributes=create_list_attributes14(edge_element), sources=[SOURCE_PRIMARY_KP_GENETICS], qualifiers=[])
        knowledge_graph.edges[edge_element.edge_id] = edge_gene_pathway
        list_aux_graph_edges.append(edge_element.edge_id)

        # add in pathway_disease edge
        edge_element = creative_result.pathway_disease
        edge_pathway_disease: Edge = Edge(predicate=edge_element.predicate, subject=edge_element.subject.id, object=edge_element.target.id, attributes=create_list_attributes14(edge_element), sources=[SOURCE_PRIMARY_KP_GENETICS])
        knowledge_graph.edges[edge_element.edge_id] = edge_pathway_disease
        list_aux_graph_edges.append(edge_element.edge_id)

        # create auxiliary_graphs map entry with all supporting edges
        graph_aux = AuxiliaryGraph(edges=list_aux_graph_edges, attributes=[])
        graph_aux_id = "{}_graph_aux".format(index)
        auxiliary_graphs[graph_aux_id] = graph_aux

        # add in auxiliary_graphs entry above as biolink:support_graphs attribute to the creative edge
        attribute_creative = Attribute(attribute_type_id="biolink:support_graphs", value=[graph_aux_id], attributes=[])
        edge_creative.attributes = [attribute_creative]

        # in analyses, only add creative edge in edge_bindings
        edge_binding = EdgeBinding(id=edge_creative_id, attributes=[])
        edge_binding_map[creative_result.edge_key] = [edge_binding]

        # add all nodes to knowledge_graph/nodes map
        for edge_element in creative_result.list_edges:
            node = Node(name=edge_element.subject.name, categories=[edge_element.subject.category], attributes=[])
            knowledge_graph.nodes[edge_element.subject.id] = node
            node = Node(name=edge_element.target.name, categories=[edge_element.target.category], attributes=[])
            knowledge_graph.nodes[edge_element.target.id] = node

        # only add drug and disease nodes in node bindings
        source_binding = NodeBinding(id=edge_element.subject.id, attributes=[])
        target_binding = NodeBinding(id=edge_element.target.id, attributes=[])
        node_binding_map[edge_element.subject.query_node_binding_key] = [source_binding]
        node_binding_map[edge_element.target.query_node_binding_key] = [target_binding]

        # add the analysis
        # in analyses, add genetics_kp as resource_id with score of gene probability
        # analysis = Analysis(resource_id=PROVENANCE_INFORES_KP_GENETICS, edge_bindings=edge_binding_map, score=score_result)
        analysis = Analysis(resource_id=PROVENANCE_INFORES_KP_GENETICS, edge_bindings=edge_binding_map, score=None, support_graphs=[], attributes=[])

        # add the bindings to the result
        results.append(Result(node_binding_map, analyses=[analysis]))

    # build out the message
    message = Message(results=results, query_graph=query_graph, knowledge_graph=knowledge_graph, auxiliary_graphs=auxiliary_graphs)
    results_response = Response(message = message, schema_version=VERSION_TRAPI, biolink_version=VERSION_BIOLINK, logs=[])

    # return
    return results_response


def build_results(results_list: list, query_graph) -> Response:
    """ build the trapi v1.0 response from the genetics model """
    # build the empty collections
    results = []
    knowledge_graph = KnowledgeGraph(nodes={}, edges={})
    nodes = {}
    edges = {}

    # loop through the results
    edge_element: EdgeOuput
    for edge_element in results_list:
        # get the nodes
        source = edge_element.source_node
        target = edge_element.target_node
        # print("edge element: {}".format(edge_element))

        # add the edge
        # build the provenance data
        list_sources = get_retrieval_source_list(list_study_id=[edge_element.study_type_id])

        # add in the attributes
        list_attributes = []
        # add in the pvalue/probability if applicable
        # 20230404 - OLD SCHEMA
        # if edge_element.score_translator:
        #     attributes.append(Attribute(original_attribute_name='probability', value=edge_element.score_translator, attribute_type_id='biolink:probability'))

        if edge_element.score is not None:
            # OLD - pre score translator data
            # if edge_element.score_type == 'biolink:probability':
            #     attributes.append(Attribute(original_attribute_name='probability', value=edge_element.score, attribute_type_id=edge_element.score_type))

            # add p_value or classification if available
            if edge_element.score_type == 'biolink:classification':
                # list_attributes.append(Attribute(original_attribute_name='classification', value=edge_element.score, attribute_type_id=edge_element.score_type, attributes=[]))
                list_attributes.append(build_attribute(name_original=trapi_constants.NAME_CLASSIFICATION, value=edge_element.score, value_type=trapi_constants.BIOLINK_CLASSIFICATION, id_source=edge_element.study_type_id))
            elif edge_element.score_type == 'biolink:p_value':
                # list_attributes.append(Attribute(original_attribute_name='pValue', value=edge_element.score, attribute_type_id=edge_element.score_type, attributes=[]))
                list_attributes.append(build_attribute(name_original=trapi_constants.NAME_PVALUE, value=edge_element.score, value_type=trapi_constants.BIOLINK_PVALUE, id_source=edge_element.study_type_id))
            # print("added attributes: {}".format(attributes))

        # 20230404 - NEW SCHEMA
        if edge_element.score_translator:
            # list_attributes.append(Attribute(original_attribute_name='score', value=edge_element.score_translator, attribute_type_id='biolink:score', attributes=[]))
            list_attributes.append(build_attribute(name_original=trapi_constants.NAME_SCORE, value=edge_element.score_translator, value_type=trapi_constants.BIOLINK_SCORE, id_source=edge_element.study_type_id))
        if edge_element.beta:
            # list_attributes.append(Attribute(original_attribute_name='beta', value=edge_element.beta, attribute_type_id='biolink:beta', attributes=[]))
            list_attributes.append(build_attribute(name_original=trapi_constants.NAME_BETA, value=edge_element.beta, value_type=trapi_constants.BIOLINK_BETA, id_source=edge_element.study_type_id))
        if edge_element.standard_error:
            # list_attributes.append(Attribute(original_attribute_name='standard_error', value=edge_element.standard_error, attribute_type_id='biolink:standard_error', attribute_source=[]))
            list_attributes.append(build_attribute(name_original=trapi_constants.NAME_STANDARD_ERROR, value=edge_element.standard_error, value_type=trapi_constants.BIOLINK_STANDARD_ERROR, id_source=edge_element.study_type_id))
        if edge_element.p_value:
            # attributes.append(Attribute(original_attribute_name='p_value', value=edge_element.score_translator, attribute_type_id='biolink:p_value'))
            list_attributes.append(build_attribute(name_original=trapi_constants.NAME_PVALUE, value=edge_element.p_value, value_type=trapi_constants.BIOLINK_PVALUE, id_source=edge_element.study_type_id))
        if edge_element.probability:
            # list_attributes.append(Attribute(original_attribute_name='probability', value=edge_element.probability, attribute_type_id='biolink:probability', attributes=[]))
            list_attributes.append(build_attribute(name_original=trapi_constants.NAME_PROBABILITY, value=edge_element.probability, value_type=trapi_constants.BIOLINK_PROBABILITY, id_source=edge_element.study_type_id))

        # publications
        if edge_element.publication_ids:
            list_publication = build_pubmed_ids(edge_element.publication_ids)
            if (list_publication):
                # pub_source = None
                # using sources to get infores; gets rid of old provenance attributes
                # if MAP_PROVENANCE.get(edge_element.study_type_id):
                #     pub_source = MAP_PROVENANCE.get(edge_element.study_type_id).value
                # if MAP_SOURCE.get(edge_element.study_type_id):
                #     pub_source = MAP_SOURCE.get(edge_element.study_type_id).resource_id
                # list_attributes.append(Attribute(original_attribute_name='publication', value=list_publication, 
                #     attribute_type_id='biolink:has_supporting_publications', value_type_id='biolink:publications', attribute_source=pub_source, attributes=[]))
                list_attributes.append(build_attribute(name_original=trapi_constants.NAME_PUBLICATIONS, value=list_publication, value_type=trapi_constants.BIOLINK_PUBLICATION, id_source=edge_element.study_type_id))

        # 20240423 - add in agent type and knowledge level
        list_attributes.append(build_attribute(name_original=trapi_constants.NAME_AGENT_TYPE, value=trapi_constants.AGENT_PIPELINE, value_type=trapi_constants.BIOLINK_AGENT_TYPE, id_source=1))
        list_attributes.append(build_attribute(name_original=trapi_constants.NAME_KNOWLEDGE_LEVEL, value=trapi_constants.KNOWLEDGE_STATS, value_type=trapi_constants.BIOLINK_KNOWLEDGE_LEVEL, id_source=1))

        # 20230213 - add qualifiers
        list_qualifiers = []
        if edge_element.list_qualifiers:
            for row_qualifier in edge_element.list_qualifiers:
                list_qualifiers.append(Qualifier(qualifier_type_id=row_qualifier['id'], qualifier_value=row_qualifier['value']))

        # build the edge
        edge = Edge(predicate=translate_type(edge_element.predicate, False), subject=source.curie, object=target.curie, attributes=list_attributes, 
                    qualifiers=list_qualifiers, sources=list_sources)
        knowledge_graph.edges[edge_element.id] = edge
        edges[(source.node_key, target.node_key)] = edge

        # add the subject node
        node = Node(name=source.name, categories=[translate_type(source.category, False)], attributes=[])
        nodes[source.node_key] = node           
        knowledge_graph.nodes[source.curie] = node

        # add the target node
        node = Node(name=target.name, categories=[translate_type(target.category, False)], attributes=[])
        nodes[target.node_key] = node           
        knowledge_graph.nodes[target.curie] = node

        # build the bindings
        source_binding = NodeBinding(id=source.curie, query_id=source.query_curie, attributes=[])
        edge_binding = EdgeBinding(id=edge_element.id, attributes=[])
        target_binding = NodeBinding(id=target.curie, query_id=target.query_curie, attributes=[])

        # add to the maps
        edge_map = {edge_element.edge_key: [edge_binding]}
        analysis = Analysis(resource_id=PROVENANCE_INFORES_KP_GENETICS, edge_bindings=edge_map, score=edge_element.score_translator, support_graphs=[], attributes=[])
        nodes_map = {source.node_key: [source_binding], target.node_key: [target_binding]}
        results.append(Result(node_bindings=nodes_map,  analyses=[analysis]))

    # build out the message
    # BUG line below if use wrong message type
    # response_message: Message = Message(results=results, query_graph=query_graph, knowledge_graph=knowledge_graph)
    response_message: ResponseMessage = build_response_message(query_graph=query_graph, knowledge_graph=knowledge_graph, results=results)
    results_response: Response = Response(message = response_message, schema_version=VERSION_TRAPI, biolink_version=VERSION_BIOLINK, logs=[])

    # return
    return results_response






##################################################################
# TODO - write unit test
def get_retrieval_source_list(list_study_id=None, log=False):
    '''
    will create the source retrieval list for the study id given
    '''
    list_sources = []

    # add genetics KP as aggregator 
    source_aggregator = copy.deepcopy(SOURCE_AGGREGATOR_KP_GENETICS)
    list_sources.append(source_aggregator)
    list_primary_ids = []

    # add in the primary source
    for study_id in list_study_id:
        source_primary = MAP_SOURCE.get(study_id)
        if source_primary:
            list_primary_ids.append(source_primary.resource_id)
            list_sources.append(source_primary)

    # add the primary sources to the aggregator source
    if list_primary_ids and len(list_primary_ids) > 0:
        source_aggregator.upstream_resource_ids = list_primary_ids

    # return
    return list_sources


def build_edge_knowledge_graph(predicate, key_subject: str, key_object: str, list_attributes=[], list_sources=[], log=False):
    '''
    will build a KG graph edge from the given nodes
    '''
    # initialize
    map_edge = {}
    edge = None
    list_qualifiers = []

    # get the name
    if log:
        logger.info("got subject:{} and object: {}".format(key_subject, key_object))
    key_edge = key_subject + '--' + key_object

    # build the edge object
    edge = Edge(predicate=predicate, subject=key_subject, object=key_object, attributes=list_attributes, qualifiers=list_qualifiers, sources=list_sources)

    # return the key/value pair
    return key_edge, edge

def build_node_knowledge_graph(ontology_id, name, list_categories, list_attributes=[], log=False):
    '''
    wild buid a KG graph node  
    '''
    # initialize
    node = Node(name=ontology_id, categories=list_categories, attributes=list_attributes)

    # return the node
    return node


def build_knowledge_graph(map_edges, map_nodes, log=False):
    '''
    build a result knowledge graph 
    '''
    # log
    if log:
        logger.info("got nodes: {}".format(map_nodes))
        logger.info("got edges: {}".format(map_edges))

    # build the data
    knowledge_graph = KnowledgeGraph(nodes=map_nodes, edges=map_edges)
    # knowledge_graph = KnowledgeGraph(nodes={}, edges={})

    # return
    return knowledge_graph


def build_response_workflow(log=False):
    '''
    builds the response workflow
    '''
    return ResponseWorkflow()


def build_response_message(query_graph: MessageQueryGraph, knowledge_graph: MessageKnowledgeGraph = None, results: list = [], log=False):
    '''
    builds a response message
    '''
    return ResponseMessage(results=results, query_graph=query_graph, knowledge_graph=knowledge_graph)


def build_response_result(query: Query, edge_key, subject_id, object_id, scoring_method=None,
                 score=None, edge_resource=trapi_constants.PROVENANCE_INFORES_KP_GENETICS, log=False):
    ''' 
    builds a result for the query response
    '''
    # initialize
    map_edges = {}
    map_nodes = {}

    # build the edge binding
    edge_binding: EdgeBinding = EdgeBinding(id=edge_key, attributes=[])
    key_temp, _ = textract.get_queryedge_key_edge(trapi_query=query)
    map_edges[key_temp] = edge_binding

    # build the node bindings
    subject_binding: NodeBinding = NodeBinding(id=subject_id, attributes=[]) 
    key_temp, _ = textract.get_querygraph_key_node(trapi_query=query, is_subject=True)
    map_nodes[key_temp] = subject_binding
    object_binding: NodeBinding = NodeBinding(id=object_id, attributes=[]) 
    key_temp, _ = textract.get_querygraph_key_node(trapi_query=query, is_subject=False)
    map_nodes[key_temp] = object_binding

    # build the analysis
    analysis: Analysis = Analysis(resource_id=edge_resource, score=score, support_graphs=[], attributes=[], scoring_method=scoring_method, edge_bindings=map_edges)

    # build the result
    result: Result = Result(analyses=analysis, node_bindings=map_nodes)

    # return
    return result


