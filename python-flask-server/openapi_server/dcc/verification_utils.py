
# imports
from openapi_server.models.message import Message
from openapi_server.models.query import Query
from openapi_server.models.query_graph import QueryGraph




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


