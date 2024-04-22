

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

from openapi_server import util
from openapi_server.dcc.creative_model import CreativeResult, CreativeEdge, CreativeNode

from openapi_server.dcc.utils import translate_type, get_curie_synonyms, get_logger, build_pubmed_ids, get_normalize_curies
from openapi_server.dcc.genetics_model import GeneticsModel, NodeOuput, EdgeOuput
import openapi_server.dcc.query_builder as qbuilder

# set up the logger
log = get_logger("trapi_utils")

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
log.info("Using biolink version: {} and trapi version: {}".format(VERSION_BIOLINK, VERSION_TRAPI))


# infores
PROVENANCE_INFORES_KP_GENETICS='infores:genetics-data-provider'
PROVENANCE_INFORES_KP_MOLEPRO='infores:molepro'
PROVENANCE_INFORES_CLINVAR='infores:clinvar'
PROVENANCE_INFORES_CLINGEN='infores:clingen'
PROVENANCE_INFORES_GENCC='infores:gencc'
PROVENANCE_INFORES_GENEBASS='infores:genebass'
PROVENANCE_INFORES_RICHARDS='infores:regl'

# provenance attributes
# aggregator sources
PROVENANCE_AGGREGATOR_KP_GENETICS = Attribute(value = PROVENANCE_INFORES_KP_GENETICS,
    attribute_type_id = 'biolink:aggregator_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://translator.broadinstitute.org/genetics_provider/trapi/v1.3',
    description = 'The Genetics Data Provider KP from NCATS Translator',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS,
    attributes=[])

# primary sources
PROVENANCE_PRIMARY_KP_GENETICS = Attribute(value = PROVENANCE_INFORES_KP_GENETICS,
    attribute_type_id = 'biolink:primary_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://github.com/broadinstitute/genetics-kp-dev/blob/master/DATA/Details/magmaData.md',
    description = 'The Genetics Data Provider KP from NCATS Translator',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS, 
    attributes=[])
PROVENANCE_PRIMARY_RICHARDS = Attribute(value = PROVENANCE_INFORES_RICHARDS,
    attribute_type_id = 'biolink:primary_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://github.com/broadinstitute/genetics-kp-dev/blob/master/DATA/Details/richardsList.md',
    description = 'The Richards Algorith Effector Gene List',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS,
    attributes=[])
PROVENANCE_PRIMARY_CLINVAR = Attribute(value = PROVENANCE_INFORES_CLINVAR,
    attribute_type_id = 'biolink:primary_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://www.ncbi.nlm.nih.gov/clinvar/',
    description = 'ClinVar is a freely accessible, public archive of reports of the relationships among human variations and phenotypes',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS,
    attributes=[])
PROVENANCE_PRIMARY_CLINGEN = Attribute(value = PROVENANCE_INFORES_CLINGEN,
    attribute_type_id = 'biolink:primary_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://clinicalgenome.org/',
    description = 'ClinGen is a NIH-funded resource dedicated to building a central resource that defines the clinical relevance of genes and variants for use in precision medicine and research',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS,
    attributes=[])
PROVENANCE_PRIMARY_GENCC = Attribute(value = PROVENANCE_INFORES_GENCC,
    attribute_type_id = 'biolink:primary_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://thegencc.org/',
    description = 'The GenCC DB provides information pertaining to the validity of gene-disease relationships, with a current focus on Mendelian diseases',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS,
    attributes=[])
PROVENANCE_PRIMARY_GENEBASS = Attribute(value = PROVENANCE_INFORES_GENEBASS,
    attribute_type_id = 'biolink:primary_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://genebass.org/',
    description = 'Genebass is a resource of exome-based association statistics, made available to the public. The dataset encompasses 3,817 phenotypes with gene-based and single-variant testing across 281,852 individuals with exome sequence data from the UK Biobank.',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS,
    attributes=[])

# new source structure
SOURCE_AGGREGATOR_KP_GENETICS = RetrievalSource(
    resource_id=PROVENANCE_INFORES_KP_GENETICS,
    resource_role=ResourceRoleEnum.AGGREGATOR_KNOWLEDGE_SOURCE,
    source_record_urls=['https://github.com/broadinstitute/genetics-kp-dev/blob/master/DATA/Details/geneticsKp.md'])
SOURCE_PRIMARY_KP_GENETICS = RetrievalSource(
    resource_id=PROVENANCE_INFORES_KP_GENETICS,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://github.com/broadinstitute/genetics-kp-dev/blob/master/DATA/Details/magmaData.md'])
SOURCE_PRIMARY_KP_MOLEPRO = RetrievalSource(
    resource_id=PROVENANCE_INFORES_KP_MOLEPRO,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://github.com/broadinstitute/molecular-data-provider'])
SOURCE_PRIMARY_RICHARDS = RetrievalSource(
    resource_id=PROVENANCE_INFORES_RICHARDS,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://github.com/broadinstitute/genetics-kp-dev/blob/master/DATA/Details/richardsList.md'])
SOURCE_PRIMARY_CLINVAR = RetrievalSource(
    resource_id=PROVENANCE_INFORES_CLINVAR,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://www.ncbi.nlm.nih.gov/clinvar/'])
SOURCE_PRIMARY_CLINGEN = RetrievalSource(
    resource_id=PROVENANCE_INFORES_CLINGEN,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://clinicalgenome.org/'])
SOURCE_PRIMARY_GENCC = RetrievalSource(
    resource_id=PROVENANCE_INFORES_GENCC,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://thegencc.org/'])
SOURCE_PRIMARY_GENCC = RetrievalSource(
    resource_id=PROVENANCE_INFORES_GENEBASS,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://genebass.org/'])
SOURCE_PRIMARY_GENEBASS = RetrievalSource(
    resource_id=PROVENANCE_INFORES_GENEBASS,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://genebass.org/'])
SOURCE_PRIMARY_600k = RetrievalSource(
    resource_id=PROVENANCE_INFORES_KP_GENETICS,
    resource_role=ResourceRoleEnum.PRIMARY_KNOWLEDGE_SOURCE,
    source_record_urls=['https://github.com/broadinstitute/genetics-kp-dev/blob/master/DATA/Details/Ellinor600k.md'])


# build map for study types
MAP_PROVENANCE = {1: PROVENANCE_PRIMARY_KP_GENETICS, 4: PROVENANCE_PRIMARY_RICHARDS, 5: PROVENANCE_PRIMARY_CLINGEN, 6: PROVENANCE_PRIMARY_CLINVAR, 7: PROVENANCE_PRIMARY_GENCC, 17: PROVENANCE_PRIMARY_GENEBASS}
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

def build_results_creative(results_list, query_graph):
    """ build the trapi v1.0 response from the genetics model """
    # build the empty collections
    results = []
    knowledge_graph = KnowledgeGraph(nodes={}, edges={})
    nodes = {}
    # edges = {}

    # loop through the results
    creative_result: CreativeResult
    for creative_result in results_list:
        # initialize
        edge_binding_map = {}
        node_binding_map = {}
        # add all the edges for this result
        edge_element :CreativeEdge
        for edge_element in creative_result.list_edges:

            # build the provenance data
            list_sources = get_retrieval_source_list(list_study_id=[1, 99])
            list_attributes = []

            # add in the pvalue/probability if applicable
            if edge_element.score:
                list_attributes.append(Attribute(original_attribute_name='pvalue', value=edge_element.score, attribute_type_id='biolink:p_value', attributes=[]))

            # build the edge
            edge = Edge(predicate=edge_element.predicate, subject=edge_element.subject.id, object=edge_element.target.id, attributes=list_attributes, sources=list_sources)
            knowledge_graph.edges[edge_element.edge_id] = edge
            # edges[(source.node_key, target.node_key)] = edge

            # add the subject node
            if not nodes.get(edge_element.subject.id):
                node = Node(name=edge_element.subject.name, categories=[edge_element.subject.category], attributes=None)
                nodes[edge_element.subject.query_node_binding_key] = node           
                knowledge_graph.nodes[edge_element.subject.id] = node

            # add the target node
            if not nodes.get(edge_element.target.id):
                node = Node(name=edge_element.target.name, categories=[edge_element.target.category], attributes=None)
                nodes[edge_element.target.query_node_binding_key] = node           
                knowledge_graph.nodes[edge_element.target.id] = node

            # build the bindings
            # TODO - trapi 1.3
            # TODO - source_binding = NodeBinding(id=source.curie, query_id=source.query_curie)
            # TODO - target_binding = NodeBinding(id=target.curie, query_id=target.query_curie)
            source_binding = NodeBinding(id=edge_element.subject.id)
            edge_binding = EdgeBinding(id=edge_element.edge_id)
            target_binding = NodeBinding(id=edge_element.target.id)
            edge_binding_map[edge_element.query_edge_binding_key] = [edge_binding]
            node_binding_map[edge_element.subject.query_node_binding_key] = [source_binding]
            node_binding_map[edge_element.target.query_node_binding_key] = [target_binding]

        # add the analysis
        analysis = Analysis(resource_id=PROVENANCE_INFORES_KP_GENETICS, edge_bindings=edge_binding_map, support_graphs=[], attributes=[])

        # add the bindings to the result
        results.append(Result(node_binding_map, analyses=[analysis]))

    # build out the message
    message = Message(results=results, query_graph=query_graph, knowledge_graph=knowledge_graph)
    results_response = Response(message = message, schema_version=VERSION_TRAPI, biolink_version=VERSION_BIOLINK)

    # return
    return results_response

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
        edge_creative: Edge = Edge(predicate=creative_result.predicate, subject=creative_result.drug.id, object=creative_result.disease.id, sources=[SOURCE_PRIMARY_KP_GENETICS])
        edge_creative_id = "{}_creative".format(index)
        knowledge_graph.edges[edge_creative_id] = edge_creative

        # add in drug_gene edge
        edge_element = creative_result.drug_gene
        edge_drug_gene: Edge = Edge(predicate=edge_element.predicate, subject=edge_element.subject.id, object=edge_element.target.id, attributes=create_list_attributes14(edge_element), sources=[SOURCE_PRIMARY_KP_MOLEPRO, SOURCE_AGGREGATOR_KP_GENETICS])
        knowledge_graph.edges[edge_element.edge_id] = edge_drug_gene
        list_aux_graph_edges.append(edge_element.edge_id)

        # add in gene_disease edge
        edge_element = creative_result.gene_disease
        edge_gene_disease: Edge = Edge(predicate=edge_element.predicate, subject=edge_element.subject.id, object=edge_element.target.id, attributes=create_list_attributes14(edge_element), sources=[SOURCE_PRIMARY_KP_GENETICS])
        knowledge_graph.edges[edge_element.edge_id] = edge_gene_disease
        score_result = edge_element.probability
        list_aux_graph_edges.append(edge_element.edge_id)

        # add in gene_pathway edge
        edge_element = creative_result.pathway_gene
        edge_gene_pathway: Edge = Edge(predicate=edge_element.predicate, subject=edge_element.subject.id, object=edge_element.target.id, attributes=create_list_attributes14(edge_element), sources=[SOURCE_PRIMARY_KP_GENETICS])
        knowledge_graph.edges[edge_element.edge_id] = edge_gene_pathway
        list_aux_graph_edges.append(edge_element.edge_id)

        # add in pathway_disease edge
        edge_element = creative_result.pathway_disease
        edge_pathway_disease: Edge = Edge(predicate=edge_element.predicate, subject=edge_element.subject.id, object=edge_element.target.id, attributes=create_list_attributes14(edge_element), sources=[SOURCE_PRIMARY_KP_GENETICS])
        knowledge_graph.edges[edge_element.edge_id] = edge_pathway_disease
        list_aux_graph_edges.append(edge_element.edge_id)

        # create auxiliary_graphs map entry with all supporting edges
        graph_aux = AuxiliaryGraph(edges=list_aux_graph_edges)
        graph_aux_id = "{}_graph_aux".format(index)
        auxiliary_graphs[graph_aux_id] = graph_aux

        # add in auxiliary_graphs entry above as biolink:support_graphs attribute to the creative edge
        attribute_creative = Attribute(attribute_type_id="biolink:support_graphs", value=[graph_aux_id], attributes=[])
        edge_creative.attributes = [attribute_creative]

        # in analyses, only add creative edge in edge_bindings
        edge_binding = EdgeBinding(id=edge_creative_id)
        edge_binding_map[creative_result.edge_key] = [edge_binding]

        # add all nodes to knowledge_graph/nodes map
        for edge_element in creative_result.list_edges:
            node = Node(name=edge_element.subject.name, categories=[edge_element.subject.category], attributes=None)
            knowledge_graph.nodes[edge_element.subject.id] = node
            node = Node(name=edge_element.target.name, categories=[edge_element.target.category], attributes=None)
            knowledge_graph.nodes[edge_element.target.id] = node

        # only add drug and disease nodes in node bindings
        source_binding = NodeBinding(id=edge_element.subject.id)
        target_binding = NodeBinding(id=edge_element.target.id)
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
    results_response = Response(message = message, schema_version=VERSION_TRAPI, biolink_version=VERSION_BIOLINK)



    # # ########################## OLD 1.3
    # # loop through the results
    # creative_result: CreativeResult
    # for index, creative_result in enumerate(results_list):

    #     for edge_element in creative_result.list_edges:

    #         # build the provenance data
    #         list_sources = get_retrieval_source_list(list_study_id=[1, 99])
    #         list_attributes = []

    #         # add in the pvalue/probability if applicable
    #         if edge_element.score:
    #             list_attributes.append(Attribute(original_attribute_name='pvalue', value=edge_element.score, attribute_type_id='biolink:p_value'))

    #         # build the edge
    #         edge = Edge(predicate=edge_element.predicate, subject=edge_element.subject.id, object=edge_element.target.id, attributes=list_attributes, sources=list_sources)
    #         knowledge_graph.edges[edge_element.edge_id] = edge
    #         # edges[(source.node_key, target.node_key)] = edge

    #         # add the subject node
    #         if not nodes.get(edge_element.subject.id):
    #             node = Node(name=edge_element.subject.name, categories=[edge_element.subject.category], attributes=None)
    #             nodes[edge_element.subject.query_node_binding_key] = node           
    #             knowledge_graph.nodes[edge_element.subject.id] = node

    #         # add the target node
    #         if not nodes.get(edge_element.target.id):
    #             node = Node(name=edge_element.target.name, categories=[edge_element.target.category], attributes=None)
    #             nodes[edge_element.target.query_node_binding_key] = node           
    #             knowledge_graph.nodes[edge_element.target.id] = node

    #         # build the bindings
    #         # TODO - trapi 1.3
    #         # TODO - source_binding = NodeBinding(id=source.curie, query_id=source.query_curie)
    #         # TODO - target_binding = NodeBinding(id=target.curie, query_id=target.query_curie)
    #         source_binding = NodeBinding(id=edge_element.subject.id)
    #         edge_binding = EdgeBinding(id=edge_element.edge_id)
    #         target_binding = NodeBinding(id=edge_element.target.id)
    #         edge_binding_map[edge_element.query_edge_binding_key] = [edge_binding]
    #         node_binding_map[edge_element.subject.query_node_binding_key] = [source_binding]
    #         node_binding_map[edge_element.target.query_node_binding_key] = [target_binding]

    #     # add the analysis
    #     analysis = Analysis(resource_id=PROVENANCE_INFORES_KP_GENETICS, edge_bindings=edge_binding_map)

    #     # add the bindings to the result
    #     results.append(Result(node_binding_map, analyses=[analysis]))

    # # build out the message
    # message = Message(results=results, query_graph=query_graph, knowledge_graph=knowledge_graph, auxiliary_graphs=auxiliary_graphs)
    # results_response = Response(message = message, schema_version=VERSION_TRAPI, biolink_version=VERSION_BIOLINK)

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
                list_attributes.append(Attribute(original_attribute_name='classification', value=edge_element.score, attribute_type_id=edge_element.score_type, attributes=[]))
            elif edge_element.score_type == 'biolink:p_value':
                list_attributes.append(Attribute(original_attribute_name='pValue', value=edge_element.score, attribute_type_id=edge_element.score_type, attributes=[]))
            # print("added attributes: {}".format(attributes))

        # 20230404 - NEW SCHEMA
        if edge_element.score_translator:
            list_attributes.append(Attribute(original_attribute_name='score', value=edge_element.score_translator, attribute_type_id='biolink:score', attributes=[]))
        if edge_element.beta:
            list_attributes.append(Attribute(original_attribute_name='beta', value=edge_element.beta, attribute_type_id='biolink:beta', attributes=[]))
        if edge_element.standard_error:
            list_attributes.append(Attribute(original_attribute_name='standard_error', value=edge_element.standard_error, attribute_type_id='biolink:standard_error', attribute_source=[]))
        # if edge_element.p_value:
        #     attributes.append(Attribute(original_attribute_name='p_value', value=edge_element.score_translator, attribute_type_id='biolink:p_value'))
        if edge_element.probability:
            list_attributes.append(Attribute(original_attribute_name='probability', value=edge_element.probability, attribute_type_id='biolink:probability', attributes=[]))

        # publications
        if edge_element.publication_ids:
            list_publication = build_pubmed_ids(edge_element.publication_ids)
            if (list_publication):
                pub_source = None
                if MAP_PROVENANCE.get(edge_element.study_type_id):
                    pub_source = MAP_PROVENANCE.get(edge_element.study_type_id).value
                list_attributes.append(Attribute(original_attribute_name='publication', value=list_publication, 
                    attribute_type_id='biolink:has_supporting_publications', value_type_id='biolink:Publication', attribute_source=pub_source, attributes=[]))

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
        node = Node(name=source.name, categories=[translate_type(source.category, False)], attributes=None)
        nodes[source.node_key] = node           
        knowledge_graph.nodes[source.curie] = node

        # add the target node
        node = Node(name=target.name, categories=[translate_type(target.category, False)], attributes=None)
        nodes[target.node_key] = node           
        knowledge_graph.nodes[target.curie] = node

        # build the bindings
        # trapi 1.3
        # source_binding = NodeBinding(id=source.curie)
        source_binding = NodeBinding(id=source.curie, query_id=source.query_curie)
        edge_binding = EdgeBinding(id=edge_element.id)
        # trapi 1.3
        # target_binding = NodeBinding(id=target.curie)
        target_binding = NodeBinding(id=target.curie, query_id=target.query_curie)
        edge_map = {edge_element.edge_key: [edge_binding]}
        analysis = Analysis(resource_id=PROVENANCE_INFORES_KP_GENETICS, edge_bindings=edge_map, score=edge_element.score_translator, support_graphs=[], attributes=[])
        nodes_map = {source.node_key: [source_binding], target.node_key: [target_binding]}
        results.append(Result(node_bindings=nodes_map,  analyses=[analysis]))

    # build out the message
    message: Message = Message(results=results, query_graph=query_graph, knowledge_graph=knowledge_graph)
    results_response: Response = Response(message = message, schema_version=VERSION_TRAPI, biolink_version=VERSION_BIOLINK)

    # return
    return results_response

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
