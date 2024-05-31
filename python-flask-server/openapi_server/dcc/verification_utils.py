
# imports
from openapi_server.models.message import Message
from openapi_server.models.query import Query
from openapi_server.models.q_node import QNode
from openapi_server.models.query_graph import QueryGraph

import openapi_server.dcc.trapi_constants as trapi_constants
import openapi_server.dcc.trapi_extract as textract


# methods
def is_query_acceptable_node_sets(query: Query, log=False):
    '''
    will evaluate the query nodes to make sure the set interpretation
    - only accept null or batch set_interpretation
    '''
    is_acceptable = True
    log_message = None

    # check all node set interpretation
    if query:
        message: Message = query.message
        Message.results = []
        if message.query_graph:
            query_graph: QueryGraph = message.query_graph
            if query_graph.nodes and len(query_graph.nodes) > 0:
                for node in query_graph.nodes.values():
                    set_interpretation = node.set_interpretation
                    if set_interpretation and set_interpretation not in [trapi_constants.SET_INTERPRETATION_BATCH, trapi_constants.SET_INTERPRETATION_MANY]:
                        is_acceptable = False
                        log_message = "The Genetics KP service only has BATCH and MANY node answers"

    # return
    return is_acceptable, log_message


# def is_query_multi_curie(query: Query, log=False):
#     '''
#     will determine if a query is many set interpretation
#     '''
#     # initialize
#     is_many = False

#     # find out if query is many
#     if query:
#         message: Message = query.message
#         Message.results = []
#         if message.query_graph:
#             query_graph: QueryGraph = message.query_graph
#             if query_graph.nodes and len(query_graph.nodes) > 0:
#                 for node in query_graph.nodes.values():
#                     set_interpretation = node.set_interpretation
#                     if set_interpretation and set_interpretation in [trapi_constants.SET_INTERPRETATION_MANY]:
#                         is_many = True

#     # return
#     return is_many


def is_query_creative(json_body, log=False):
    '''
    will determine if a query is creative based on the 'inferred' knowledge_type flag on the edge
    '''
    # initialize
    is_inferred = False
    str_inferred = 'inferred'

    # look at the edge knowledge type
    map_edges = json_body.get('message').get('query_graph').get('edges')
    if map_edges:
        for edge in map_edges.values():
            knowledge_type = edge.get('knowledge_type')
            if knowledge_type: 
                if isinstance(knowledge_type, str):
                    if knowledge_type == str_inferred:
                        is_inferred = True
                        break
                elif isinstance(knowledge_type, list):
                    if knowledge_type.contains(str_inferred):
                        is_inferred = True
                        break

    # return
    return is_inferred


def is_query_multi_curie(query: Query, log=False):
    ''' 
    will determine if the query is a muti curie query as opposed to a batch query
    '''
    is_mcq = False

    # test
    if query:
        message: Message = query.message
        Message.results = []
        if message.query_graph:
            query_graph: QueryGraph = message.query_graph
            if query_graph.nodes and len(query_graph.nodes) > 0:
                for node in query_graph.nodes.values():
                    set_interpretation = node.set_interpretation
                    if set_interpretation and set_interpretation in [trapi_constants.SET_INTERPRETATION_MANY]:
                        is_mcq = True

    # return
    return is_mcq



def is_query_tissue_related(query: Query, log=False):
    ''' 
    will determine if the query is a tissue related query
    '''
    is_tissue = False
    node: QNode = None

    # test for tissue type or UBERON curie
    if query:
        for is_subject in [True, False]:
            _, node = textract.get_querygraph_key_node(trapi_query=query, is_subject=is_subject)

            if node:
                if (node.categories and trapi_constants.BIOLINK_ENTITY_CELL in node.categories):
                    is_tissue = True
                if not is_tissue and node.ids:
                    for item in node.ids:
                        if trapi_constants.ONTOLOGY_PREFIX_UBERON in item:
                            is_tissue = True
                            break

    # return
    return is_tissue




