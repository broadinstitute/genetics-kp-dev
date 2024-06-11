

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

import openapi_server.dcc.trapi_utils as tutils
import openapi_server.dcc.trapi_extract as textract
import openapi_server.dcc.trapi_constants as tconstants
import openapi_server.dcc.web_utils as wutils

from openapi_server.dcc.utils import get_logger

# logger
logger = get_logger(__name__)

# constants
FILE_DB = "conf/mcq.db"

# methods
def get_connection(log=False):
    # get the db connection
    conn = sqlite3.connect(FILE_DB)

    # return
    return conn


def db_query_sqlite(sql_query, trapi_query: Query, list_params=[], log=False):
    '''
    will query the database for the data
    '''
    # initialize
    list_result = []
    conn = get_connection()
    cursor = conn.cursor()
    sql_logs = []

    # execute the query
    logger.info("running sql query: \n{}\n with params: \n{}".format(sql_query, list_params))
    cursor.execute(sql_query, list_params)

    # get the data
    rows = cursor.fetchall()
    str_message = "got DB result rows of count: {}".format(len(rows))
    logger.info(str_message)
    sql_logs.append(str_message)

    # get the data
    # list_result = [dict(row) for row in rows]
    for row in rows:
        list_result.append({tconstants.KEY_EDGE_ID: row[0], tconstants.KEY_SUBJECT_ID: row[1], tconstants.KEY_OBJECT_ID: row[2], tconstants.KEY_SCORE: row[3], 
                            tconstants.KEY_SUBJECT_NAME: row[4], tconstants.KEY_OBJECT_NAME: row[5], 
                            tconstants.KEY_EDGE_TYPE: row[6], tconstants.KEY_SUBJECT_TYPE: row[7], tconstants.KEY_OBJECT_TYPE: row[8],
                            tconstants.KEY_STUDY_ID: row[9], tconstants.KEY_PUBLICATIONS: row[10], tconstants.KEY_SCORE_TRANSLATOR: row[11], tconstants.KEY_ROW_ID: row[12],
                            tconstants.KEY_PVALUE: row[13], tconstants.KEY_BETA: row[14], tconstants.KEY_STD_ERROR: row[15], tconstants.KEY_PROB: row[16],
                            tconstants.KEY_PROB_BAYES: row[17], tconstants.KEY_ENRICHMENT: row[18], tconstants.KEY_ANNOTATION: row[19]})

    # log
    if log:
        logger.info("got results: \n{}".format(json.dumps(list_result, indent=2)))

    # return
    return list_result, sql_logs


def sub_query_sqlite(sql_query, trapi_query: Query, list_params=[], list_trapi_logs=[], log=False):
    '''
    builds the trapi response based on the results of the sql query given
    '''
    # initialize
    start = time.time()
    list_result = []
    trapi_response_message: ResponseMessage = tutils.build_response_message(query_graph=trapi_query.message.query_graph)
    trapi_response: Response = Response(message=trapi_response_message, logs=list_trapi_logs, workflow=trapi_query.workflow, 
                            biolink_version=tutils.get_biolink_version(), schema_version=tutils.get_trapi_version())
    map_nodes = {}
    map_edges = {}
    list_response_results = []
    num_subject = 0
    num_object = 0

    # get the data
    list_result, list_sql_logs = db_query_sqlite(sql_query=sql_query, trapi_query=trapi_query, list_params=list_params, log=log)

    # build the response
    # build object set node
    for item in list_result:
        # initialize
        list_attributes = []
        # create the edge nodes
        node_subject : Node = tutils.build_node_knowledge_graph(ontology_id=item.get(tconstants.KEY_SUBJECT_ID), name=item.get(tconstants.KEY_SUBJECT_NAME), list_categories=[item.get(tconstants.KEY_SUBJECT_TYPE)])
        node_object : Node = tutils.build_node_knowledge_graph(ontology_id=item.get(tconstants.KEY_OBJECT_ID), name=item.get(tconstants.KEY_OBJECT_NAME), list_categories=[item.get(tconstants.KEY_OBJECT_TYPE)])
        map_nodes[item.get(tconstants.KEY_SUBJECT_ID)] = node_subject
        map_nodes[item.get(tconstants.KEY_OBJECT_ID)] = node_object
        # # get the row data
        # name_gene = list(row.values())[0].get('gene_name')
        # score = list(row.values())[0].get('score')
        # id_gene = list(row.keys())[0]

        # build the score attribute and attributes list
        list_attributes.append(tutils.build_attribute(name_original=tconstants.NAME_AGENT_TYPE, value=tconstants.AGENT_PIPELINE, value_type=tconstants.BIOLINK_AGENT_TYPE, id_source=tconstants.DB_STUDY_ID_GENETICS))
        list_attributes.append(tutils.build_attribute(name_original=tconstants.NAME_KNOWLEDGE_LEVEL, value=tconstants.KNOWLEDGE_STATS, value_type=tconstants.BIOLINK_KNOWLEDGE_LEVEL, id_source=tconstants.DB_STUDY_ID_GENETICS))
        if item.get(tconstants.KEY_SCORE_TRANSLATOR):
            list_attributes.append(tutils.build_attribute(item.get(tconstants.KEY_SCORE_TRANSLATOR), tconstants.BIOLINK_SCORE, id_source=tconstants.DB_STUDY_ID_GENETICS))
        if item.get(tconstants.KEY_PVALUE):
            list_attributes.append(tutils.build_attribute(item.get(tconstants.KEY_PVALUE), tconstants.BIOLINK_PVALUE, id_source=tconstants.DB_STUDY_ID_GENETICS))
        if item.get(tconstants.KEY_ENRICHMENT):
            list_attributes.append(tutils.build_attribute(item.get(tconstants.KEY_ENRICHMENT), tconstants.BIOLINK_ENRICHMENT, id_source=tconstants.DB_STUDY_ID_GENETICS))
        if item.get(tconstants.KEY_ANNOTATION):
            list_attributes.append(tutils.build_attribute(value=item.get(tconstants.KEY_ANNOTATION), value_type=tconstants.BIOLINK_ANNOTATION, id_source=tconstants.DB_STUDY_ID_GENETICS))

        # build the source list
        list_sources = [tutils.SOURCE_PRIMARY_KP_GENETICS]

        # buid the edge
        key_edge, edge = tutils.build_edge_knowledge_graph(key_edge=item.get(tconstants.KEY_EDGE_ID), predicate=tconstants.BIOLINK_PREDICATE_GENETIC_ASSOCIATION, key_subject=item.get(tconstants.KEY_SUBJECT_ID), 
                                                           key_object=item.get(tconstants.KEY_OBJECT_ID), list_attributes=list_attributes, list_sources=list_sources)

        # add the nodes, edge to the map
        map_edges[key_edge] = edge

        # add the result
        list_response_results.append(tutils.build_response_result(query=trapi_query, edge_key=key_edge, subject_id=item.get(tconstants.KEY_SUBJECT_ID), object_id=item.get(tconstants.KEY_OBJECT_ID), 
                                                                  score=item.get(tconstants.KEY_SCORE_TRANSLATOR), scoring_method='probability'))
        
    # build the KG and add to response
    trapi_response_message.knowledge_graph = tutils.build_knowledge_graph(map_edges=map_edges, map_nodes=map_nodes, log=False)

    # build the results
    trapi_response_message.results = list_response_results

    # build the response
    # NOTE - not necessarily true as move all data to sqlite
    # list_trapi_logs.append("responding to tissue/gene query")
    list_trapi_logs.extend(list_sql_logs)

    # add data version to logs
    str_message = "Database version: {}".format(tutils.get_database_version())
    logger.info(str_message)
    list_trapi_logs.append(str_message)

    # add performance metrics
    _, node = textract.get_querygraph_key_node(trapi_query=trapi_query, is_subject=True)
    if node.ids:
        num_subject = len(node.ids)
    _, node = textract.get_querygraph_key_node(trapi_query=trapi_query, is_subject=False)
    if node.ids:
        num_object = len(node.ids)

    end = time.time()
    time_elapsed = end - start
    # str_message = "LOOKUP web query with source: {} and target: {} return total edge: {} in time: {}s".format(num_source, num_target, len(genetics_results), time_elapsed)
    str_message = "NEW LOOKUP web query with source: {} and target: {} return total edge: {} in time: {}s".format(num_subject, num_object, len(list_result), time_elapsed)
    logger.info(str_message)
    list_trapi_logs.append(str_message)

    # return
    return trapi_response









# def get_request_elements(body, is_creative=False):
#     """ 
#     translates the json into a neutral format 
#     input: trapi json
#     output: list of 1? element
#     """
#     # initialize
#     results = []
#     edge_map = body['message']['query_graph']['edges']
#     node_map = body['message']['query_graph']['nodes']

#     # build the 
#     for edge_key, edge in edge_map.items():

#         # if 'predicate' not in edge or translate_type(edge['predicate']) != 'associated' or 'subject' not in edge or 'object' not in edge:
#         if 'subject' not in edge or 'object' not in edge:
#             print("========== invalid edge format: {}".format(edge))
#             continue
#         else:
#             edge['edge_key'] = edge_key
        
#         sourceNode = node_map.get(edge.get('subject'))
#         # if sourceNode is None or 'category' not in sourceNode or 'id' not in sourceNode:
#         if sourceNode is None:
#             print("=========== invalid source node format: {}".format(sourceNode))
#             continue
#         else:
#             sourceNode['node_key'] = edge.get('subject')

#         targetNode = node_map.get(edge.get('object'))
#         # if targetNode is None or 'category' not in targetNode:
#         if targetNode is None:
#             print("============= invalid target node format: {}".format(targetNode))
#             continue
#         else:
#             targetNode['node_key'] = edge.get('object')

#         # create the edge/node object from the original query
#         original_edge = GeneticsModel(edge=edge, source=sourceNode, target=targetNode, map_source_normalized_id={}, map_target_normalized_id={})
#         logger.info(original_edge)

#         # get source and target lists with unique items
#         list_source = original_edge.get_original_source_ids() if original_edge.get_original_source_ids() is not None and len(original_edge.get_original_source_ids()) > 0 else []
#         list_target = original_edge.get_original_target_ids() if original_edge.get_original_target_ids() is not None and len(original_edge.get_original_target_ids()) > 0 else []
#         list_source = list(set(list_source))
#         list_target = list(set(list_target))
    
#         # filter out the ontologies we don't service
#         # BUG: https://github.com/broadinstitute/genetics-kp-dev/issues/26
#         # -- if source or target is only one id, don't bother filtering; if do end up filtering ID, will get unbounded incorrect query
#         # NOTE - CREATIVE - only filter subject if not creative query (not drug - treats - disease)

#         if not is_creative:
#             if len(list_source) > 1:
#                 list_temp = []
#                 for item in list_source:
#                     if item.split(':')[0] not in list_ontology_prefix_avoid:
#                         list_temp.append(item)
#                     else:
#                         logger.info("skipping non serviced source: {}".format(item))
#                 list_source = list_temp

#         # BUG: https://github.com/broadinstitute/genetics-kp-dev/issues/26
#         # -- if source or target is only one id, don't bother filtering
#         if len(list_target) > 1:
#             list_temp = []
#             for item in list_target:
#                 if item.split(':')[0] not in list_ontology_prefix_avoid:
#                     list_temp.append(item)
#                 else:
#                     logger.info("skipping non serviced target: {}".format(item))
#             list_target = list_temp


#         # test the new normalizing function
#         # logger.info("=====================================================")
#         # test_source = get_normalize_curies(list_source, log=True)
#         # logger.info("found new: {} for original: {}".format(len(test_source), len(list_source)))
#         # logger.info("=====================================================")

#         # get the normalized list
#         # get the descendant list
#         subject_curie_list = get_normalize_curies(list_source, log=False)
#         # trim curie list to what is in genepro (pulled in at start)
#         subject_curie_list = trim_disease_list_tuple_to_what_is_in_the_db(subject_curie_list, SET_CACHED_PHENOTYPES)
#         for curie in subject_curie_list:
#             original_edge.add_source_normalized_id(curie[1], curie[0])

#         target_curie_list = get_normalize_curies(list_target, log=False)
#         # trim curie list to what is in genepro (pulled in at start)
#         target_curie_list = trim_disease_list_tuple_to_what_is_in_the_db(target_curie_list, SET_CACHED_PHENOTYPES)
#         # logger.info("target: {}".format(target_curie_list))
#         for curie in target_curie_list:
#             original_edge.add_target_normalized_id(curie[1], curie[0])

#         # add new object to result list
#         results.append(original_edge)

#         # log
#         logger.info("query with normalized source list: {}".format(original_edge.get_map_source_normalized_id().keys()))
#         logger.info("query with normalized target list: {}".format(original_edge.get_map_target_normalized_id().keys()))
#         logger.info("query with source count: {} and target count: {}".format(len(original_edge.get_map_source_normalized_id()), len(original_edge.get_map_target_normalized_id())))

#     # return
#     return results



# def sub_query_lookup(trapi_query: Query, query_graph, request_body, list_trapi_logs=[], log=False):
#     '''
#     deal with a lookup query
#     '''
#     # initialize
#     genetics_results = []

#     # tag start time
#     start = time.time()

#     # build the interim data structure 
#     # NOTE - also expand the ID list based on ontology ancestry
#     request_input = get_request_elements(body)
#     logger.info("got request input {}".format(request_input))

#     # only allow small queries
#     if len(request_input) > MAX_SIZE_ID_LIST:
#         logger.error("too big request, asking for {} combinations".format(len(request_input)))
#         return ({"status": 413, "title": "Query payload too large", "detail": "Query payload too large, exceeds the {} subject/object combination size".format(MAX_SIZE_ID_LIST), "type": "about:blank" }, 413)

#     # log
#     logger.info("looping through queries for web query object list: {}\n".format(request_input))
#     for web_request_object in request_input:
#         # log
#         # logger.info("running query for web query object: {}\n".format(web_request_object))

#         # queries
#         # NOTE - implemented batch subject/target input - done in the batch sql structure

#         # TODO - might have to implement uniqueness on the PK returned (use set); took out duplicate check
#         # if not found_results_already:   # TODO - might not be needed anymore since ncats NN and each disease/phenotype entry should only have one curie in the DB

#         # make sure it is not an unbounded query (that we have matched with at leat one source/target)
#         if len(web_request_object.get_list_source_id()) > 0 or len(web_request_object.get_list_target_id()) > 0:
#             queries = qbuilder.get_queries(web_request_object)

#             # if results
#             if len(queries) > 0:
#                 found_results_already = True
#                 # only open web connection when have passed validation of request
#                 cnx = pymysql.connect(host=DB_HOST, port=3306, database=DB_SCHEMA, user=DB_USER, password=DB_PASSWD)
#                 cursor = cnx.cursor()

#                 for i in range(0, len(queries)):
#                     sql_object = queries[i]
#                     logger.info("running query: {}\n".format(sql_object))
#                     cursor.execute(sql_object.sql_string, tuple(sql_object.param_list))
#                     results = cursor.fetchall()
#                     # print("result of type {} is {}".format(type(results), results))
#                     logger.info("for DB query got result count of: {}".format(len(results)))
#                     if results:
#                         for record in results:
#                             edgeID    = record[0]
#                             sourceID  = record[1]
#                             targetID  = record[2]
#                             # trapi 1.3
#                             # originalSourceID  = record[1]
#                             # originalTargetID  = record[2]
#                             originalSourceID  = None
#                             originalTargetID  = None

#                             # find original source/target IDs
#                             if web_request_object.get_map_source_normalized_id().get(sourceID):
#                                 originalSourceID  = web_request_object.get_map_source_normalized_id().get(sourceID)

#                             if web_request_object.get_map_target_normalized_id().get(targetID):
#                                 originalTargetID  = web_request_object.get_map_target_normalized_id().get(targetID)
#                             # else:
#                             #     logger.info(web_request_object.get_map_target_normalized_id())
#                             # logger.info("original: {}, converted: {}".format(targetID, originalTargetID))

#                             score     = record[3]
#                             scoreType = record[4]
#                             sourceName = record[5]
#                             targetName = record[6]
#                             edgeType = record[7]
#                             sourceType = record[8]
#                             targetType = record[9]
#                             studyTypeId = record[10]
#                             publications = record[11]
#                             score_translator = record[12]
#                             id_db_edge = record[13]

#                             # TODO - add when direction of effect is ready to go
#                             # pValue = record[14]
#                             # beta = record[15]
#                             # standardError = record[16]
#                             # probability = record[17]
#                             # probability_bayes = record[18]

#                             # # replace probability with bayes probability if available
#                             # if probability_bayes:
#                             #     probability = probability_bayes
#                             # TODO - add when direction of effect is ready to go


#                             # 20230213 - add qualifiers is available
#                             list_qualifiers = []
#                             # deprecated since comb_edge_qualifier table deleted; qualifiers now dowe througb decorator class
#                             # if has_qualifiers == 'Y':
#                                 # query the db
#                                 # cursor.execute(qbuilder.build_qualifier_sql(), (id_db_edge))
#                                 # db_results_qualifiers = cursor.fetchall()

#                                 # # build the qualifiers as needed
#                                 # for row_qualifier in db_results_qualifiers:
#                                 #     list_qualifiers.append({'id':row_qualifier[0], 'value':row_qualifier[1]})

#                             # log
#                             # logger.info("got result: {}".format(record))

#                             # build the result objects
#                             # trapi 1.3
#                             # source_node = NodeOuput(curie=originalSourceID, name=sourceName, category=sourceType, node_key=web_request_object.get_source_key())
#                             # target_node = NodeOuput(curie=originalTargetID, name=targetName, category=targetType, node_key=web_request_object.get_target_key())
#                             source_node = NodeOuput(curie=sourceID, query_curie=originalSourceID, name=sourceName, category=sourceType, node_key=web_request_object.get_source_key())
#                             target_node = NodeOuput(curie=targetID, query_curie=originalTargetID, name=targetName, category=targetType, node_key=web_request_object.get_target_key())
#                             output_edge = EdgeOuput(id=edgeID, source_node=source_node, target_node=target_node, predicate=edgeType, 
#                                 score=score, score_type=scoreType, edge_key=web_request_object.get_edge_key(), study_type_id=studyTypeId, 
#                                 publication_ids=publications, score_translator=score_translator, list_qualifiers=list_qualifiers)

#                             # add to the results list
#                             genetics_results.append(output_edge)
                
#                 # close the connection
#                 cnx.close()

#         else:
#             logger.info("no source/target inputs that we have, so skip")

#         # log
#         logger.info("for query \n{}".format(request_body))
#         num_source = 0
#         if web_request_object.get_original_source_ids():
#             num_source = len(web_request_object.get_original_source_ids())
#         num_target = 0
#         if web_request_object.get_original_target_ids():
#             num_target = len(web_request_object.get_original_target_ids())
#         logger.info("LOOKUP web query with source count: {} and target count: {} return total edge count: {}".format(num_source, num_target, len(genetics_results)))


#     # build the response
#     query_response: Response = build_results(results_list=genetics_results, query_graph=query_graph)

#     # tag and print the time elapsed
#     end = time.time()
#     time_elapsed = end - start
#     str_message = "LOOKUP web query with source: {} and target: {} return total edge: {} in time: {}s".format(num_source, num_target, len(genetics_results), time_elapsed)
#     logger.info(str_message)
#     list_trapi_logs.append(str_message)

#     # add in the logs
#     query_response.logs = list_trapi_logs

#     # return
#     return query_response

