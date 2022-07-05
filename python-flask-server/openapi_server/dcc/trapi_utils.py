

from logging import log
import six
import copy
import os
import time 

from openapi_server.models.message import Message
from openapi_server.models.knowledge_graph import KnowledgeGraph
from openapi_server.models.edge import Edge
from openapi_server.models.node import Node
from openapi_server.models.result import Result
from openapi_server.models.edge_binding import EdgeBinding
from openapi_server.models.node_binding import NodeBinding
from openapi_server.models.response import Response
from openapi_server.models.attribute import Attribute

from openapi_server import util
from openapi_server.dcc.creative_model import CreativeResult, CreativeEdge, CreativeNode

from openapi_server.dcc.utils import translate_type, get_curie_synonyms, get_logger, build_pubmed_ids, get_normalize_curies
from openapi_server.dcc.genetics_model import GeneticsModel, NodeOuput, EdgeOuput
import openapi_server.dcc.query_builder as qbuilder


# infores
PROVENANCE_INFORES_KP_GENETICS='infores:genetics-data-provider'
PROVENANCE_INFORES_CLINVAR='infores:clinvar'
PROVENANCE_INFORES_CLINGEN='infores:clingen'
PROVENANCE_INFORES_GENCC='infores:gencc'
PROVENANCE_INFORES_GENEBASS='infores:genebass'

# provenance attributes
PROVENANCE_AGGREGATOR_KP_GENETICS = Attribute(value = PROVENANCE_INFORES_KP_GENETICS,
    attribute_type_id = 'biolink:aggregator_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://translator.broadinstitute.org/genetics_provider/trapi/v1.2',
    description = 'The Genetics Data Provider KP from NCATS Translator',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS)
PROVENANCE_AGGREGATOR_CLINVAR = Attribute(value = PROVENANCE_INFORES_CLINVAR,
    attribute_type_id = 'biolink:aggregator_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://www.ncbi.nlm.nih.gov/clinvar/',
    description = 'ClinVar is a freely accessible, public archive of reports of the relationships among human variations and phenotypes',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS)
PROVENANCE_AGGREGATOR_CLINGEN = Attribute(value = PROVENANCE_INFORES_CLINGEN,
    attribute_type_id = 'biolink:aggregator_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://clinicalgenome.org/',
    description = 'ClinGen is a NIH-funded resource dedicated to building a central resource that defines the clinical relevance of genes and variants for use in precision medicine and research',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS)
PROVENANCE_AGGREGATOR_GENCC = Attribute(value = PROVENANCE_INFORES_GENCC,
    attribute_type_id = 'biolink:aggregator_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://thegencc.org/',
    description = 'The GenCC DB provides information pertaining to the validity of gene-disease relationships, with a current focus on Mendelian diseases',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS)
PROVENANCE_AGGREGATOR_GENEBASS = Attribute(value = PROVENANCE_INFORES_GENEBASS,
    attribute_type_id = 'biolink:aggregator_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://genebass.org/',
    description = 'Genebass is a resource of exome-based association statistics, made available to the public. The dataset encompasses 3,817 phenotypes with gene-based and single-variant testing across 281,852 individuals with exome sequence data from the UK Biobank.',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS)

# build map for study types
MAP_PROVENANCE = {5: PROVENANCE_AGGREGATOR_CLINGEN, 6: PROVENANCE_AGGREGATOR_CLINVAR, 7: PROVENANCE_AGGREGATOR_GENCC, 17: PROVENANCE_AGGREGATOR_GENEBASS}


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
            attributes = [PROVENANCE_AGGREGATOR_KP_GENETICS]

            # add in the pvalue/probability if applicable
            if edge_element.score:
                attributes.append(Attribute(original_attribute_name='pvalue', value=edge_element.score_translator, attribute_type_id='biolink:p_value'))

            # build the edge
            edge = Edge(predicate=edge_element.predicate, subject=edge_element.subject.id, object=edge_element.target.id, attributes=attributes)
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
            source_binding = NodeBinding(id=edge_element.subject.id)
            edge_binding = EdgeBinding(id=edge_element.edge_id)
            target_binding = NodeBinding(id=edge_element.target.id)
            edge_binding_map[edge_element.edge_key] = [edge_binding]
            node_binding_map[edge_element.subject.query_node_binding_key] = [source_binding]
            node_binding_map[edge_element.target.query_node_binding_key] = [target_binding]

        # add the bindings to the result
        results.append(Result(node_binding_map, edge_binding_map, score=None))

    # build out the message
    message = Message(results=results, query_graph=query_graph, knowledge_graph=knowledge_graph)
    results_response = Response(message = message)

    # return
    return results_response


def build_results(results_list, query_graph):
    """ build the trapi v1.0 response from the genetics model """
    # build the empty collections
    results = []
    knowledge_graph = KnowledgeGraph(nodes={}, edges={})
    nodes = {}
    edges = {}

    # loop through the results
    for edge_element in results_list:
        # get the nodes
        source = edge_element.source_node
        target = edge_element.target_node
        # print("edge element: {}".format(edge_element))

        # add the edge
        # build the provenance data
        attributes = [PROVENANCE_AGGREGATOR_KP_GENETICS]
        provenance_child = MAP_PROVENANCE.get(edge_element.study_type_id)
        if provenance_child:
            attributes.append(provenance_child)

        # add in the pvalue/probability if applicable
        if edge_element.score_translator:
            attributes.append(Attribute(original_attribute_name='probability', value=edge_element.score_translator, attribute_type_id='biolink:probability'))
        if edge_element.score is not None:
            # OLD - pre score translator data
            # if edge_element.score_type == 'biolink:probability':
            #     attributes.append(Attribute(original_attribute_name='probability', value=edge_element.score, attribute_type_id=edge_element.score_type))

            # add p_value or classification if available
            if edge_element.score_type == 'biolink:classification':
                attributes.append(Attribute(original_attribute_name='classification', value=edge_element.score, attribute_type_id=edge_element.score_type))
            elif edge_element.score_type == 'biolink:p_value':
                attributes.append(Attribute(original_attribute_name='pValue', value=edge_element.score, attribute_type_id=edge_element.score_type))
            # print("added attributes: {}".format(attributes))

        if edge_element.publication_ids:
            list_publication = build_pubmed_ids(edge_element.publication_ids)
            if (list_publication):
                pub_source = None
                if MAP_PROVENANCE.get(edge_element.study_type_id):
                    pub_source = MAP_PROVENANCE.get(edge_element.study_type_id).value
                attributes.append(Attribute(original_attribute_name='publication', value=list_publication, 
                    attribute_type_id='biolink:has_supporting_publications', value_type_id='biolink:Publication', attribute_source=pub_source))

        # build the edge
        edge = Edge(predicate=translate_type(edge_element.predicate, False), subject=source.curie, object=target.curie, attributes=attributes)
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
        source_binding = NodeBinding(id=source.curie)
        edge_binding = EdgeBinding(id=edge_element.id)
        target_binding = NodeBinding(id=target.curie)
        edge_map = {edge_element.edge_key: [edge_binding]}
        nodes_map = {source.node_key: [source_binding], target.node_key: [target_binding]}
        results.append(Result(nodes_map, edge_map, score=edge_element.score_translator))

    # build out the message
    message = Message(results=results, query_graph=query_graph, knowledge_graph=knowledge_graph)
    results_response = Response(message = message)

    # return
    return results_response
