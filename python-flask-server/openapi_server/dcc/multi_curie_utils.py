
# imports
import sqlite3
import math
import json
import requests
import time

from openapi_server.models.message import Message
from openapi_server.models.query import Query
from openapi_server.models.query_graph import QueryGraph
from openapi_server.models.response import Response
from openapi_server.models.edge import Edge
from openapi_server.models.node import Node
from openapi_server.models.response_message import ResponseMessage
from openapi_server.models.log_level import LogLevel

import openapi_server.dcc.trapi_utils as tutils
import openapi_server.dcc.trapi_extract as textract
import openapi_server.dcc.trapi_constants as trapi_constants

from openapi_server.dcc.utils import get_logger

# logger
logger = get_logger('multi_curie_utils.py')

# constants
FILE_DB = "conf/mcq.db"
# TODO - get this dynamically
CHOD_PATIENT_COUNT = 1790431

DB_QUERY_GENE_PHENOTYPE = """
select gene.ontology_id, gene_pheno.gene, pheno.name, pheno.query_ontology_id, gene_pheno.probability
from mcq_phenotype pheno, mcq_gene_phenotype gene_pheno, comb_node_ontology gene
where gene_pheno.phenotype = pheno.name 
and gene.node_code = gene_pheno.gene
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
        logger.info("calling OMOP url: {} for curies: {}".format(url, list_curies))

    # call the service
    response = requests.post(url, json={'curies': list_curies})
    json_response = response.json()

    if log:
        logger.info("ompo response: \n{}".format(json.dumps(json_response, indent=2)))
        # print("ompo response: {}".format(json_response))

    # loop over results
    for key, value in json_response.items():
        if value:
            map_results[key] = {'omop_id': value.get('omop_concept_id'), 'omop_name': value.get('omop_concept_name')}
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
        map_temp[value.get('omop_id')] = key

    if log:
        logger.info("got OMOP to curie_id temp map: \n{}".format(json.dumps(map_temp, indent=2)))

    # call cohd service
    # make sure at least one phenotype has an OMOP result match
    if len(map_temp) > 0:
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
            # omop_name = 
            map_results[map_temp.get(omop_id)] = {'prevalence': item.get('concept_frequency'), 'omop_id': omop_id, 'omop_name': map_phenotypes.get(map_temp.get(omop_id)).get('omop_name')}

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
        list_result.append({'gene_id': row[0], 'gene_name': row[1], 'phenotype_name': row[2], 'phenotype_id': row[3], 'probability': row[4]})
    if log: 
        logger.info("got DB results: {}".format(list_result))

    # return
    return list_result


def sub_query_mcq(trapi_query: Query, log=True):
    ''' 
    respond to a trapi query
    '''
    # initialize 
    start = time.time()
    str_message = "query is lookup"
    logger.info(str_message)
    list_logs = [tutils.build_log_entry(message=str_message)]
    str_message = "query is MANY muti curie"
    logger.info(str_message)
    list_logs.append(tutils.build_log_entry(message=str_message))
    # list_logs = [tutils.build_log_entry(message="query is lookup"), tutils.build_log_entry(message="query is MANY muti curie")]
    logger.info(list_logs)
    trapi_response_message: ResponseMessage = tutils.build_response_message(query_graph=trapi_query.message.query_graph)
    trapi_response = Response(message=trapi_response_message, logs=tutils.build_log_entry_list(list_logs=list_logs),
                              workflow=trapi_query.workflow, 
                            biolink_version=tutils.get_biolink_version(), schema_version=tutils.get_trapi_version())
    list_mcq_nodes = []
    map_nodes = {}
    map_edges = {}
    list_response_results = []
    set_name = 'trapi:set01'
    
    # get the inputs
    _, subject_node = textract.get_querygraph_key_node(trapi_query=trapi_query, is_subject=True)
    _, object_node = textract.get_querygraph_key_node(trapi_query=trapi_query, is_subject=False)

    # TODO - only respond to PhenotypicFeature to Gene
    if not subject_node.categories or (subject_node.categories and trapi_constants.BIOLINK_ENTITY_PHENOTYPE in subject_node.categories):
        if not object_node.categories or (object_node.categories and trapi_constants.BIOLINK_ENTITY_GENE in object_node.categories):
            if subject_node.set_interpretation in [trapi_constants.SET_INTERPRETATION_MANY]:
                # ids are now the set name
                if subject_node.ids and len(subject_node.ids) > 0:
                    set_name = subject_node.ids[0]

                    # inputs are now in the member_ids field
                    # make sure at least 1 element
                    if subject_node.member_ids:
                        list_mcq_nodes = subject_node.member_ids
                        if len(list_mcq_nodes) < 1:
                            log_msg = "Error: no curies provided for set interpretation: {}".format(subject_node.set_interpretation)
                            logger.error(log_msg)
                            list_logs.append(tutils.build_log_entry(message=log_msg, level=LogLevel.ERROR, code=LogLevel.ERROR))
                        else:
                            # add acceptance log message
                            log_msg = "processing mcq query with set interpretation {} for nodes: {}".format(subject_node.set_interpretation, list_mcq_nodes)
                            list_logs.append(tutils.build_log_entry(message=log_msg))
                        
                else:
                    log_msg = "Error: no curies provided for set interpretation: {}".format(subject_node.set_interpretation)
                    logger.error(log_msg)
                    list_logs.append(tutils.build_log_entry(message=log_msg, level=LogLevel.ERROR, code=LogLevel.ERROR))


    # get the inputs
    # if trapi_query:
    #     message: Message = trapi_query.message
    #     Message.results = []
    #     if message.query_graph:
    #         query_graph: QueryGraph = message.query_graph
    #         if query_graph.nodes and len(query_graph.nodes) > 0:
    #             for node in query_graph.nodes.values():
    #                 set_interpretation = node.set_interpretation
    #                 # if set_interpretation in [trapi_constants.SET_INTERPRETATION_ALL, trapi_constants.SET_INTERPRETATION_MANY]:
    #                 if set_interpretation in [trapi_constants.SET_INTERPRETATION_MANY]:
    #                     input_set_interpretation = set_interpretation

    #                     # ids are now the set name
    #                     if node.ids and len(node.ids) > 0:
    #                         set_name = node.ids[0]

    #                         # inputs are now in the member_ids field
    #                         # make sure at least 1 element
    #                         list_mcq_nodes = node.ids
    #                         if len(list_mcq_nodes) < 1:
    #                             log_msg = "Error: no curies provided for set interpretation: {}".format(input_set_interpretation)
    #                             list_logs.append(log_msg)
    #                         else:
    #                             # add acceptance log message
    #                             log_msg = "processing mcq query with set interpretation {} for nodes: {}".format(input_set_interpretation, list_mcq_nodes)
    #                             list_logs.append(log_msg)
                                
    #                     else:
    #                         log_msg = "Error: no curies provided for set interpretation: {}".format(input_set_interpretation)
    #                         list_logs.append(log_msg)


    # only process if inputs
    if list_mcq_nodes and len(list_mcq_nodes) > 0:
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
        node_subject : Node = tutils.build_node_knowledge_graph(ontology_id=set_name, name=set_name, list_categories=[trapi_constants.BIOLINK_ENTITY_PHENOTYPE])
        map_nodes[node_subject.name] = node_subject
        for row in list_result:
            # get the row data
            name_gene = list(row.values())[0].get('gene_name')
            score = list(row.values())[0].get('score')
            id_gene = list(row.keys())[0]

            # build the score attribute and attributes list
            list_attributes = [tutils.build_attribute(value=score, value_type=trapi_constants.BIOLINK_SCORE, id_source=trapi_constants.DB_STUDY_ID_GENETICS)]
            list_attributes.append(tutils.build_attribute(name_original=trapi_constants.NAME_AGENT_TYPE, value=trapi_constants.AGENT_PIPELINE, value_type=trapi_constants.BIOLINK_AGENT_TYPE, id_source=trapi_constants.DB_STUDY_ID_GENETICS))
            list_attributes.append(tutils.build_attribute(name_original=trapi_constants.NAME_KNOWLEDGE_LEVEL, value=trapi_constants.KNOWLEDGE_STATS, value_type=trapi_constants.BIOLINK_KNOWLEDGE_LEVEL, id_source=trapi_constants.DB_STUDY_ID_GENETICS))

            # build the source list
            list_sources = [tutils.SOURCE_PRIMARY_KP_GENETICS]

            # build subject gene node
            node_object: Node = tutils.build_node_knowledge_graph(ontology_id=id_gene, name=name_gene, list_categories=[trapi_constants.BIOLINK_ENTITY_GENE])

            # buid the edge
            key_edge, edge = tutils.build_edge_knowledge_graph(predicate=trapi_constants.BIOLINK_PREDICATE_GENETIC_ASSOCIATION, key_subject=set_name, key_object=id_gene, 
                                                            list_attributes=list_attributes, list_sources=list_sources)

            # add the nodes, edge to the map
            map_nodes[id_gene] = node_object
            map_edges[key_edge] = edge

            # add the result
            list_response_results.append(tutils.build_response_result(query=trapi_query, edge_key=key_edge, subject_id=set_name, object_id=id_gene, score=score, scoring_method='probability'))
            
        # build the KG and add to response
        trapi_response_message.knowledge_graph = tutils.build_knowledge_graph(map_edges=map_edges, map_nodes=map_nodes, log=False)

        # build the results
        trapi_response_message.results = list_response_results

    # add performance metrics
    end = time.time()
    time_elapsed = end - start
    str_message = "NEW LOOKUP MCQ web query with source: {} and target: {} return total edge: {} in time: {}s".format(1, 0, len(list_response_results), time_elapsed)
    logger.info(str_message)
    list_logs.append(tutils.build_log_entry(message=str_message))

    # return
    trapi_response.logs = tutils.build_log_entry_list(list_logs=list_logs)
    return trapi_response


def get_map_phenotype_prevalence(list_phenotypes, log=True):
    '''
    returns a map of the prevalence of the phenotypes given 
    '''
    # initialize
    map_prevalence = {}
    map_result = {}

    # get the prevalence
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


def calculate_from_results(list_genes, num_results=50, log=True):
    '''
    will do the algorithmic calculation of the results 
    '''
    # initialize
    map_prevalence = {}
    # test data
    list_result = [{'NCBIGene:99008': {'gene_name': 'PPARG', 'score':75}}, {'NCBIGene:23008': {'gene_name': 'SLC30A8', 'score':68}}, {'NCBIGene:56006': {'gene_name': 'PCSK9', 'score':50}}]
    map_gene_results = {}
    
    # get only the unique phenotypes
    for row in list_genes:
        map_prevalence[row.get('phenotype_id')] = 0
    list_phenotypes = list(map_prevalence.keys())
    if log:
        logger.info("got list of phenotypes for prevalence: {}".format(list_phenotypes))

    # build the phenotype weight
    map_prevalence = get_map_phenotype_prevalence(list_phenotypes=list_phenotypes)

    # for any phenotype that doesn't have a prevalence, set to n/n+1
    for phenotype in list_phenotypes:
        if not map_prevalence.get(phenotype):
            map_prevalence[phenotype] = CHOD_PATIENT_COUNT / (CHOD_PATIENT_COUNT + 1)

    # log prevalence map
    if log:
        logger.info("got prevalence map: {}".format(json.dumps(map_prevalence, indent=2)))

    # for each result, build the gene probability
    for row in list_genes:
        # get data
        gene_id = row.get('gene_id')
        gene_name = row.get('gene_name')
        phenotype_id = row.get('phenotype_id')
        probability = row.get('probability')

        if map_prevalence.get(phenotype_id):
            # calulate the minus log of the prevalence times the probability
            score = -1.0 * math.log(map_prevalence.get(phenotype_id)) * probability

            if map_gene_results.get(gene_id):
                map_gene_results[gene_id]['score'] = map_gene_results.get(gene_id).get('score') + score
            else:
                map_gene_results[gene_id] = {}
                map_gene_results[gene_id]['score'] = score
                map_gene_results[gene_id]['gene_name'] = gene_name

    # create a list from the gene map
    list_result = [{key: value} for key, value in map_gene_results.items()]
    # if log:
    #     logger.info("got final gene score list: {}".format(list_result))

    # sort list
    list_sorted_result = sorted(list_result, key=lambda item: list(item.values())[0].get('score'), reverse=True)
    # if log:
    #     logger.info("got sorted list: {}".format(list_sorted_result))

    # return
    return list_sorted_result[:num_results]

# def query_multi_curie(query: Query, log=False):
#     ''' 
#     will process a multi curie query 
#     '''
#     # initialize
#     logs = []
#     list_subject_mcq_nodes = []
#     list_object_mcq_nodes = []
#     set_subject = None
#     set_object = None

#     # just do MANY set interpretation for now
    
#     # process
#     # get the set interpretation and the nodes set
#     if query:
#         message: Message = query.message
#         Message.results = []
#         if message.query_graph:
#             query_graph: QueryGraph = message.query_graph
#             if query_graph.nodes and len(query_graph.nodes) > 0:
#                 for node in query_graph.nodes.values():
#                     set_interpretation = node.set_interpretation
#                     if set_interpretation in [trapi_constants.SET_INTERPRETATION_ALL, trapi_constants.SET_INTERPRETATION_MANY]:
#                         input_set_interpretation = set_interpretation
#                         if node.ids:
#                             # make sure at least 1 element
#                             list_mcq_nodes = node.ids
#                             if len(list_mcq_nodes) < 1:
#                                 logs.append("Error: no curies provided for set interpretation: {}".format(input_set_interpretation))
#                             else:
#                                 # add acceptance log message
#                                 logs.append("processing mcq query with set interpretation {} for nodes: {}".format(input_set_interpretation, list_mcq_nodes))
                                
#                                 # process MCQ

#                         else:
#                             logs.append("Error: no curies provided for set interpretation: {}".format(input_set_interpretation))


#     # return
#     return Response(message=query.message, logs=logs, workflow=query.workflow, 
#                 biolink_version=tutils.get_biolink_version(), schema_version=tuple.get_trapi_version())


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

