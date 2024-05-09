
# imports
from openapi_server.models.message import Message
from openapi_server.models.query import Query
from openapi_server.models.query_graph import QueryGraph

import openapi_server.dcc.trapi_constants as trapi_constants


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
                    if set_interpretation and set_interpretation != 'BATCH':
                        is_acceptable = False
                        log_message = "The Genetics KP service only has BATCH node answers"

    # return
    return is_acceptable, log_message


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
                    if set_interpretation and set_interpretation in [trapi_constants.SET_INTERPRETATION_ALL, trapi_constants.SET_INTERPRETATION_MANY]:
                        is_mcq = True

    # return
    return is_mcq