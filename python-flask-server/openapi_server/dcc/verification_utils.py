
# imports
from openapi_server.models.message import Message
from openapi_server.models.query import Query
from openapi_server.models.query_graph import QueryGraph

import openapi_server.dcc.trapi_utils as trapi_utils


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
                    if set_interpretation and set_interpretation not in [trapi_utils.SET_INTERPRETATION_BATCH, trapi_utils.SET_INTERPRETATION_MANY]:
                        is_acceptable = False
                        log_message = "The Genetics KP service only has BATCH and MANY node answers"

    # return
    return is_acceptable, log_message


def is_query_multi_curie(query: Query, log=False):
    '''
    will determine if a query is many set interpretation
    '''
    # initialize
    is_many = False

    # find out if query is many
    if query:
        message: Message = query.message
        Message.results = []
        if message.query_graph:
            query_graph: QueryGraph = message.query_graph
            if query_graph.nodes and len(query_graph.nodes) > 0:
                for node in query_graph.nodes.values():
                    set_interpretation = node.set_interpretation
                    if set_interpretation and set_interpretation in [trapi_utils.SET_INTERPRETATION_MANY]:
                        is_many = True

    # return
    return is_many

