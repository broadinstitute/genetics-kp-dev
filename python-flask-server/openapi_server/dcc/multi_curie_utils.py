
# imports
from openapi_server.models.message import Message
from openapi_server.models.query import Query
from openapi_server.models.query_graph import QueryGraph
from openapi_server.models.response import Response

from openapi_server.dcc.trapi_utils import build_results, build_results_creative14, get_biolink_version, get_trapi_version
import openapi_server.dcc.trapi_constants as trapi_constants

# constants



# methods
def query_multi_curie(query: Query, log=False):
    ''' 
    will process a multi curie query 
    '''
    # initialize
    logs = []
    list_mcq_nodes = []
    input_set_interpretation = None

    # process
    # get the set interpretation and the nodes set
    if query:
        message: Message = query.message
        Message.results = []
        if message.query_graph:
            query_graph: QueryGraph = message.query_graph
            if query_graph.nodes and len(query_graph.nodes) > 0:
                for node in query_graph.nodes.values():
                    set_interpretation = node.set_interpretation
                    if set_interpretation in [trapi_constants.SET_INTERPRETATION_ALL, trapi_constants.SET_INTERPRETATION_MANY]:
                        input_set_interpretation = set_interpretation
                        if node.ids:
                            # make sure at least 1 element
                            list_mcq_nodes = node.ids
                            if len(list_mcq_nodes) < 1:
                                logs.append("Error: no curies provided for set interpretation: {}".format(input_set_interpretation))
                            else:
                                # add acceptance log message
                                logs.append("processing mcq query with set interpretation {} for nodes: {}".format(input_set_interpretation, list_mcq_nodes))
                                
                                # process MCQ

                        else:
                            logs.append("Error: no curies provided for set interpretation: {}".format(input_set_interpretation))


    # return
    return Response(message=query.message, logs=logs, workflow=query.workflow, 
                biolink_version=get_biolink_version(), schema_version=get_trapi_version())


# main

