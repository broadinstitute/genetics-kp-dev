
# imports
import sqlite3
import math
import json

from openapi_server.models.message import Message
from openapi_server.models.query import Query
from openapi_server.models.query_graph import QueryGraph
from openapi_server.models.response import Response
from openapi_server.models.edge import Edge
from openapi_server.models.node import Node

import openapi_server.dcc.trapi_utils as tutils
import openapi_server.dcc.trapi_constants as trapi_constants

from openapi_server.dcc.utils import get_logger

# logger
logger = get_logger('multi_curie_utils.py')

# constants
FILE_DB = "conf/mcq.db"

DB_QUERY_GENE_PHENOTYPE = """
select gene_pheno.gene, pheno.name as phenotype, pheno.query_ontology_id as ontology_id, gene_pheno.probability
from mcq_phenotype pheno, mcq_gene_phenotype gene_pheno 
where gene_pheno.phenotype = pheno.name 
and pheno.query_ontology_id in ({})
order by gene_pheno.probability desc 
"""


# methods
def db_query_phenotype(conn, list_phenotypes, log=False):
    '''
    will query the sqlite db and return the data associated with the phenotypes given
    '''
    # initialize
    list_result = []
    cursor = conn.cursor()

    # build the placeholders
    placeholders = ', '.join('?' for _ in list_phenotypes)

    # Construct the query
    query = DB_QUERY_GENE_PHENOTYPE.format(placeholders)

    # Execute the query with the provided values
    logger.info("running query: {} for inputs: {}".format(query, list_phenotypes))

    # query
    cursor.execute(query, list_phenotypes)

    # Fetch all matching rows
    rows = cursor.fetchall()
    logger.info("got result rows of count: {}".format(len(rows)))

    # get the data
    # list_result = [dict(row) for row in rows]
    for row in rows:
        list_result.append({'gene_name': row[0], 'phenotype_name': row[1], 'phenotype_id': row[2], 'probability': row[3]})
    if log: 
        logger.info("got DB results: {}".format(list_result))

    # return
    return list_result


def sub_query_mcq(trapi_query: Query, log=False):
    ''' 
    respond to a trapi query
    '''
    # initialize 
    list_logs = ["query is lookup", "query is MANY muti curie"]
    trapi_respponse = Response(message=trapi_query.message, logs=list_logs, workflow=trapi_query.workflow, 
                            biolink_version=tutils.get_biolink_version(), schema_version=tutils.get_trapi_version())
    list_mcq_nodes = []
    map_nodes = {}
    map_edges = {}

    # get the inputs
    if trapi_query:
        message: Message = trapi_query.message
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
                                log_msg = "Error: no curies provided for set interpretation: {}".format(input_set_interpretation)
                                list_logs.append(log_msg)
                            else:
                                # add acceptance log message
                                log_msg = "processing mcq query with set interpretation {} for nodes: {}".format(input_set_interpretation, list_mcq_nodes)
                                list_logs.append(log_msg)
                                
                        else:
                            log_msg = "Error: no curies provided for set interpretation: {}".format(input_set_interpretation)
                            list_logs.append(log_msg)

    
    # get the db connection
    conn = sqlite3.connect(FILE_DB)

    # get the data
    list_genes = db_query_phenotype(conn=conn, list_phenotypes=list_mcq_nodes)

    # calculate the data
    # will get a gene -> score map
    list_result = calculate_from_results(list_genes=list_genes)
    logger.info("got final sorted results: {}".format(json.dumps(list_result, indent=2)))

    # build the response
    # build object set node
    node_object : Node = tutils.build_node_knowledge_graph(ontology_id='trapi:set01', name='trapi:set01', list_categories=[trapi_constants.BIOLINK_ENTITY_PHENOTYPE])
    map_nodes[node_object.name] = node_object
    for row in list_result:
        # build the score attribute
        list_attributes = [tutils.build_attribute(list(row.values())[0], trapi_constants.BIOLINK_SCORE, id_source=trapi_constants.PROVENANCE_INFORES_KP_GENETICS)]

        # build subject gene node
        name_gene = list(row.keys())[0]
        node_subject: Node = tutils.build_node_knowledge_graph(ontology_id=name_gene, name=name_gene, list_categories=[trapi_constants.BIOLINK_ENTITY_GENE])

        # buid the edge
        key_edge, edge = tutils.build_edge_knowledge_graph(predicate=trapi_constants.BIOLINK_PREDICATE_GENETIC_ASSOCIATION, key_subject=node_subject.name, key_object=node_object.name, list_attributes=list_attributes)

        # add the nodes, edge to the map
        map_nodes[name_gene] = node_subject
        map_edges[key_edge] = edge
        
    # build the KG and add to response
    trapi_query.message.knowledge_graph = tutils.build_knowledge_graph(map_edges=map_edges, map_nodes=map_nodes, log=False)

    # return
    trapi_respponse.logs = list_logs
    return trapi_respponse


def get_map_phenotype_prevalence(list_phenotypes, log=True):
    '''
    returns a map of the prevalence of the phenotypes given 
    '''
    # initialize
    map_prevalence = {}

    # TODO - get the prevalence
    for row in list_phenotypes:
        map_prevalence[row] = 0.5

    # log
    if log:
        logger.info("using prevalence map: {}".format(map_prevalence))

    # return
    return map_prevalence


def calculate_from_results(list_genes, num_results=10, log=False):
    '''
    will do the algorithmic calculation of the results 
    '''
    # initialize
    map_prevalence = {}
    # test data
    list_result = [{'PPARG': 75}, {'SLC30A8': 90}, {'PCSK9': 58}]
    map_gene_results = {}
    
    # get only the unique phenotypes
    for row in list_genes:
        map_prevalence[row.get('phenotype_id')] = 0
    list_phenotypes = list(map_prevalence.keys())
    if log:
        logger.info("got list pf phenotypes for prevalence: {}".format(list_phenotypes))

    # build the phenotype weight
    map_prevalence = get_map_phenotype_prevalence(list_phenotypes=list_phenotypes)

    # for each result, build the gene probability
    for row in list_genes:
        # get data
        gene = row.get('gene_name')
        phenotype_id = row.get('phenotype_id')
        probability = row.get('probability')

        # calulate the minus log of the prevalence times the probability
        score = -1.0 * math.log(map_prevalence.get(phenotype_id)) * probability

        if map_gene_results.get(gene):
            map_gene_results[gene] = map_gene_results.get(gene) + score
        else:
            map_gene_results[gene] = score

    # create a list from the gene map
    list_result = [{key: value} for key, value in map_gene_results.items()]
    if log:
        logger.info("got final gene score list: {}".format(list_result))

    # sort list
    list_sorted_result = sorted(list_result, key=lambda item: list(item.values())[0], reverse=True)
    if log:
        logger.info("got sorted list: {}".format(list_sorted_result))

    # return
    return list_sorted_result[:num_results]

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
                biolink_version=tutils.get_biolink_version(), schema_version=tuple.get_trapi_version())


# main

