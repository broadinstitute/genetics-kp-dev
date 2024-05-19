
# imports
from openapi_server.models.message import Message
from openapi_server.models.query import Query
from openapi_server.models.query_graph import QueryGraph
from openapi_server.models.response import Response

from openapi_server.dcc.trapi_utils import build_results, build_results_creative14, get_biolink_version, get_trapi_version
import openapi_server.dcc.trapi_constants as trapi_constants

# constants
FILE_DB = ""

DB_QUERY_GENE_PHENOTYPE = """
select gene_pheno.gene, pheno.name as phenotype, pheno.query_ontology_id as ontology_id, gene_pheno.probability
from mcq_phenotype pheno, mcq_gene_phenotype gene_pheno 
where gene_pheno.phenotype = pheno.name 
and pheno.query_ontology_id in ({})
order by gene_pheno.probability desc 
limit 20;
"""


# methods
def db_query_phenotype(conn, list_phenotypes, log=False):
    '''
    will query the sqlite db and return the data associated with the phenotypes given
    '''
    # initialize
    list_result = []
    cursor = conn.cursor()

    # Create a placeholder string for the number of values
    placeholders = ', '.join('?' for _ in list_phenotypes)

    # Construct the query
    query = DB_QUERY_GENE_PHENOTYPE.format(placeholders)

    # query
    cursor.execute(query, list_phenotypes)

    # Fetch all matching rows
    rows = cursor.fetchall()

    # get the data
    for row in rows:
        map_row = dict(row)
        list_result.append(map_row)

    # return
    return list_result


def sub_query_mcq(trapi_query: Query, log=False):
    ''' 
    respond to a trapi query
    '''
    # initialize 
    logs = ["query is lookup", "query is MANY muti curie"]
    trapi_respponse = Response(message=trapi_query.message, logs=logs, workflow=trapi_query.workflow, 
                            biolink_version=get_biolink_version(), schema_version=get_trapi_version())


    # get the inputs

    
    # get the data


    # build the response


    # return
    return trapi_respponse


def query_multi_curie(query: Query, log=False):
    ''' 
    will process a multi curie query 
    '''
    # initialize
    logs = []
    list_subject_mcq_nodes = []
    list_object_mcq_nodes = []
    set_subject = None
    set_object = None

    # just do MANY set interpretation for now
    
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

