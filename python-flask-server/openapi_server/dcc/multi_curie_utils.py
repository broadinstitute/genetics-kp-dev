
# imports
import sqlite3
import math
import json
import requests

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

URL_CHOD = "https://cohd-api.transltr.io/api/{}"
URI_TO_OMOP = "translator/biolink_to_omop"
URI_PREVALENCE = "frequencies/singleConceptFreq?dataset_id=1&q={}"
URI_PATIENT_COUNT = "metadata/patientCount?dataset_id=1"


# methods
def get_omop_for_list(list_curies, log=False):
    '''
    will query the cohd server for omop curies based on curies given
    '''
    # initialize
    map_results = {}
    url = URL_CHOD.format(URI_TO_OMOP)

    # log
    if log:
        logger.info("calling OMOP for curies: {}".format(list_curies))

    # call the service
    response = requests.post(url, json={'curies': list_curies})
    json_response = response.json()

    if log:
        logger.info("ompo response: \n{}".format(json.dumps(json_response, indent=2)))
        # print("ompo response: {}".format(json_response))

    # loop over results
    for key, value in json_response.items():
        if value:
            map_results[key] = value.get('omop_concept_id')
        # else:
        #     map_results[key] = value

    # log
    if log:
        logger.info("returning OMOP key map: {}".format(map_results))

    # return
    return map_results


def get_patient_count(log=False):
    '''
    will query the cohd server for the patient count
    '''
    # initialize
    result_count = 0
    url = URL_CHOD.format(URI_PATIENT_COUNT)

    # call the service
    response = requests.get(url)
    json_response = response.json()

    if log:
        print("count response: \n{}".format(json.dumps(json_response, indent=2)))
        # print("ompo response: {}".format(json_response))

    # loop over results
    if json_response.get('results'):
        if json_response.get('results').get('count'):
            result_count = json_response.get('results').get('count')

    # return
    return int(result_count)


def get_prevalence_for_list(list_curies, log=True):
    '''
    returns the prevalence for the given list of curies
    '''
    # initialize 
    map_results = {}

    # get omop curies
    map_phenotypes = get_omop_for_list(list_curies=list_curies, log=log)
    if log:
        logger.info("got OMOP mapping: {} for input phenotypes: {}".format(json.dumps(map_phenotypes, indent=2), list_curies))

    # flip the phenotype map
    map_temp = {}
    for key, value in map_phenotypes.items():
        map_temp[value] = key

    if log:
        print("got temp map: \n{}".format(json.dumps(map_temp, indent=2)))

    # call cohd service
    str_input = ",".join(str(num) for num in map_temp.keys())
    url = URL_CHOD.format(URI_PREVALENCE.format(str_input))
    if log:
        print("Using prevalence URL: {}".format(url))
    response = requests.get(url)
    json_response = response.json()

    # loop
    json_results = json_response.get('results')
    for item in json_results:
        omop_id = item.get('concept_id')
        map_results[map_temp.get(omop_id)] = {'prevalence': item.get('concept_frequency'), 'omop_id': omop_id}

    # return
    return map_results

def get_curie_name_map(list_curies, log=False):
    '''
    returns a map of key curies and values the name of the phenotype
    '''
    map_result = {}

    # for each phenotype, get the name
    for item in list_curies:
        map_result[item] = get_rest_name_for_curie(curie=item, log=log)

    # return
    return map_result

def get_rest_name_for_curie(curie, log=False):
    '''
    get the normalized name for the curie
    '''
    # initialize
    result_name = None
    URL = "https://nodenormalization-sri.renci.org/get_normalized_nodes?curie={}"

    # request
    url = URL.format(curie)

    if log:
        print("querying url: {}".format(url))

    response = requests.get(url)
    json_result = response.json()

    # get the name
    if json_result.get(curie):
        if json_result.get(curie).get('id'):
            if json_result.get(curie).get('id').get('label'):
                result_name = json_result.get(curie).get('id').get('label')

    # return
    return result_name


def get_rest_name_map_for_curie_list(list_curies, log=False):
    '''
    get the normalized name for the curie
    '''
    # initialize
    map_name = {}
    URL = "https://nodenormalization-sri.renci.org/get_normalized_nodes?{}"
    str_curie = "{}curie={}"

    # build the curie list
    str_input = ""
    for index, item in enumerate(list_curies):
        if index == 0:
            str_input = str_input + str_curie.format('', item)
        else:
            str_input = str_input + str_curie.format('&', item)

    # request
    url = URL.format(str_input)

    if log:
        print("querying url: {}".format(url))

    response = requests.get(url)
    json_result = response.json()

    # get the name
    for curie in list_curies:
        if json_result.get(curie):
            if json_result.get(curie).get('id'):
                if json_result.get(curie).get('id').get('label'):
                    map_name[curie] = json_result.get(curie).get('id').get('label')

    # return
    return map_name

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
    map_result = {}

    # TODO - get the prevalence
    # for row in list_phenotypes:
    #     map_prevalence[row] = 0.5
    map_prevalence = get_prevalence_for_list(list_curies=list_phenotypes)

    # log
    if log:
        logger.info("from COHD got prevalence map: {}".format(json.dumps(map_prevalence, indent=2)))

    # format into simple key/value map
    for key, value in map_prevalence.items():
        map_result[key] = value.get('prevalence')

    # return
    return map_result


def calculate_from_results(list_genes, num_results=10, log=True):
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
    if log:
        logger.info("got prevalence map: {}".format(json.dumps(map_prevalence, indent=2)))

    # for each result, build the gene probability
    for row in list_genes:
        # get data
        gene = row.get('gene_name')
        phenotype_id = row.get('phenotype_id')
        probability = row.get('probability')

        if map_prevalence.get(phenotype_id):
            # calulate the minus log of the prevalence times the probability
            score = -1.0 * math.log(map_prevalence.get(phenotype_id)) * probability

            if map_gene_results.get(gene):
                map_gene_results[gene] = map_gene_results.get(gene) + score
            else:
                map_gene_results[gene] = score

    # create a list from the gene map
    list_result = [{key: value} for key, value in map_gene_results.items()]
    # if log:
    #     logger.info("got final gene score list: {}".format(list_result))

    # sort list
    list_sorted_result = sorted(list_result, key=lambda item: list(item.values())[0], reverse=True)
    # if log:
    #     logger.info("got sorted list: {}".format(list_sorted_result))

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
if __name__ == "__main__":
    # data
    list_curies = [
        "HP:0002907",
        "HP:0012745",
        # "HP:0005110", 
        "HP:0000574",
        "HP:0002870",
        "HP:0034003"
    ]
    map_to_omop = {}

    # test the omop call
    map_to_omop = get_omop_for_list(list_curies=list_curies, log=False)
    print("got omop response: \n{}".format(json.dumps(map_to_omop, indent=2)))

    # test the prevalance call
    print()
    map_to_prevalence = get_prevalence_for_list(list_curies=list_curies, log=True)
    print("got prevalence response: \n{}".format(json.dumps(map_to_prevalence, indent=2)))

