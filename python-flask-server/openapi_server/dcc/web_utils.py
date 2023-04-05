
from logging import log
import connexion
import six
import pymysql
import copy
import os
import time 

from openapi_server.models.message import Message
from openapi_server.models.knowledge_graph import KnowledgeGraph
from openapi_server.models.edge import Edge
from openapi_server.models.node import Node
from openapi_server.models.result import Result
from openapi_server.models.edge_binding import EdgeBinding
from openapi_server.models.node_binding import NodeBinding
from openapi_server.models.response import Response
from openapi_server.models.attribute import Attribute

from openapi_server import util

from openapi_server.dcc.creative_model import CreativeResult, CreativeEdge, CreativeNode
from openapi_server.dcc.trapi_utils import build_results, build_results_creative
from openapi_server.dcc.utils import translate_type, get_curie_synonyms, get_logger, build_pubmed_ids, get_normalize_curies
from openapi_server.dcc.genetics_model import GeneticsModel, NodeOuput, EdgeOuput
import openapi_server.dcc.query_builder as qbuilder

# get logger
logger = get_logger(__name__)

# constants
list_ontology_prefix = ['UMLS', 'NCIT', 'MONDO', 'EFO', 'NCBIGene', 'GO', 'HP', 'MESH']
list_ontology_prefix_avoid = ['FMA', 'CHEMBL.TARGET', 'CHEMBL.COMPOUND', 'PUBCHEM.COMPOUND', 'UNII', 'CHEBI', 'DRUGBANK', 'CAS', 'DrugCentral', 'KEGG.COMPOUND', 'INCHIKEY', 'GTOPDB']

# # infores
# PROVENANCE_INFORES_KP_GENETICS='infores:genetics-data-provider'
# PROVENANCE_INFORES_CLINVAR='infores:clinvar'
# PROVENANCE_INFORES_CLINGEN='infores:clingen'
# PROVENANCE_INFORES_GENCC='infores:gencc'
# PROVENANCE_INFORES_GENEBASS='infores:genebass'

# provenance attributes
# PROVENANCE_AGGREGATOR_KP_GENETICS = Attribute(value = PROVENANCE_INFORES_KP_GENETICS,
#     attribute_type_id = 'biolink:aggregator_knowledge_source',
#     value_type_id = 'biolink:InformationResource',
#     value_url = 'https://translator.broadinstitute.org/genetics_provider/trapi/v1.2',
#     description = 'The Genetics Data Provider KP from NCATS Translator',
#     attribute_source = PROVENANCE_INFORES_KP_GENETICS)
# PROVENANCE_AGGREGATOR_CLINVAR = Attribute(value = PROVENANCE_INFORES_CLINVAR,
#     attribute_type_id = 'biolink:aggregator_knowledge_source',
#     value_type_id = 'biolink:InformationResource',
#     value_url = 'https://www.ncbi.nlm.nih.gov/clinvar/',
#     description = 'ClinVar is a freely accessible, public archive of reports of the relationships among human variations and phenotypes',
#     attribute_source = PROVENANCE_INFORES_KP_GENETICS)
# PROVENANCE_AGGREGATOR_CLINGEN = Attribute(value = PROVENANCE_INFORES_CLINGEN,
#     attribute_type_id = 'biolink:aggregator_knowledge_source',
#     value_type_id = 'biolink:InformationResource',
#     value_url = 'https://clinicalgenome.org/',
#     description = 'ClinGen is a NIH-funded resource dedicated to building a central resource that defines the clinical relevance of genes and variants for use in precision medicine and research',
#     attribute_source = PROVENANCE_INFORES_KP_GENETICS)
# PROVENANCE_AGGREGATOR_GENCC = Attribute(value = PROVENANCE_INFORES_GENCC,
#     attribute_type_id = 'biolink:aggregator_knowledge_source',
#     value_type_id = 'biolink:InformationResource',
#     value_url = 'https://thegencc.org/',
#     description = 'The GenCC DB provides information pertaining to the validity of gene-disease relationships, with a current focus on Mendelian diseases',
#     attribute_source = PROVENANCE_INFORES_KP_GENETICS)
# PROVENANCE_AGGREGATOR_GENEBASS = Attribute(value = PROVENANCE_INFORES_GENEBASS,
#     attribute_type_id = 'biolink:aggregator_knowledge_source',
#     value_type_id = 'biolink:InformationResource',
#     value_url = 'https://genebass.org/',
#     description = 'Genebass is a resource of exome-based association statistics, made available to the public. The dataset encompasses 3,817 phenotypes with gene-based and single-variant testing across 281,852 individuals with exome sequence data from the UK Biobank.',
#     attribute_source = PROVENANCE_INFORES_KP_GENETICS)

# # build map for study types
# MAP_PROVENANCE = {5: PROVENANCE_AGGREGATOR_CLINGEN, 6: PROVENANCE_AGGREGATOR_CLINVAR, 7: PROVENANCE_AGGREGATOR_GENCC, 17: PROVENANCE_AGGREGATOR_GENEBASS}

# PROVENANCE_AGGREGATOR_RICHARDS = Attribute(value = PROVENANCE_INFORES_CLINGEN,
#     attribute_type_id = 'biolink:aggregator_knowledge_source',
#     value_type_id = 'biolink:InformationResource',
#     value_url = 'https://clinicalgenome.org/',
#     description = 'ClinGen is a NIH-funded resource dedicated to building a central resource that defines the clinical relevance of genes and variants for use in precision medicine and research',
#     attribute_source = PROVENANCE_INFORES_KP_GENETICS)

# DB CONSTANTS
# TODO - when figure out how to get app_context working, get values from there
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA = os.environ.get('DB_SCHEMA')

# web constants
MAX_SIZE_ID_LIST = 500
max_query_size = int(os.environ.get('TRAN_MAX_QUERY_SIZE'))
if max_query_size:
    MAX_SIZE_ID_LIST = max_query_size
logger.info("Using max query size of: {}".format(MAX_SIZE_ID_LIST))

def build_cached_ontology_list(debug=True):
    ''' will build all the non gene ontology ids the KP services '''
    list_result = [None]

    # query db
    cnx = pymysql.connect(host=DB_HOST, port=3306, database=DB_SCHEMA, user=DB_USER, password=DB_PASSWD)
    cursor = cnx.cursor()
    cursor.execute("select ontology_id from comb_node_ontology where node_type_id in (1, 3)")
    results = cursor.fetchall()
    # print("result of type {} is {}".format(type(results), results))

    # build list
    if results:
        for record in results:
            list_result.append(record[0])

    # log
    if debug:
        logger.info("got {} disease/phenotype cached list\n".format(len(list_result)))

    # return unique set
    return set(list_result)

# build the cached disease/phenotype list
SET_CACHED_PHENOTYPES = build_cached_ontology_list()

def trim_disease_list_to_what_is_in_the_db(list_input, set_cache, debug=True):
    ''' will trim the list based on the list given; returns unique entries in the list '''
    list_result = []

    # trim the list
    list_result = [item for item in list_input if (item is None or 'Gene' in item or 'GO' in item or item in set_cache)]

    # log
    if debug:
        logger.info("for input list of {} - {} return cached in DB result {} - {}".format(len(list_input), list_input, len(list_result), list_result))

    # return
    return list_result

def trim_disease_list_tuple_to_what_is_in_the_db(list_input, set_cache, debug=True):
    ''' will trim the list based on the list given; returns unique entries in the list '''
    list_result = []

    if list_input and len(list_input) > 0:
        # trim the list
        list_result = [item for item in list_input if (item[1] is None or 'Gene' in item[1] or 'GO' in item[1] or item[1] in set_cache)]

        # BUG fix - if provide list but return none, mak sure to return at least one ro else will get unbounded query
        # https://github.com/NCATSTranslator/minihackathons/issues/305
        if len(list_result) < 1:
            list_result.append(list_input[0])

    # log
    if debug:
        logger.info("for input list of {} - {} return cached result {} - {}".format(len(list_input), list_input, len(list_result), list_result))

    # return
    return list_result

def query_post(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: Dict[str, ]

    :rtype: Response
    """
    return 'do some magic!'


def queryGenerated(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: dict | bytes

    :rtype: Message
    """
    return 'do some magic!'

def get_request_elements(body, is_creative=False):
    """ 
    translates the json into a neutral format 
    input: trapi json
    output: list of 1? element
    """
    # initialize
    results = []
    edge_map = body['message']['query_graph']['edges']
    node_map = body['message']['query_graph']['nodes']

    # build the 
    for edge_key, edge in edge_map.items():

        # if 'predicate' not in edge or translate_type(edge['predicate']) != 'associated' or 'subject' not in edge or 'object' not in edge:
        if 'subject' not in edge or 'object' not in edge:
            print("========== invalid edge format: {}".format(edge))
            continue
        else:
            edge['edge_key'] = edge_key
        
        sourceNode = node_map.get(edge.get('subject'))
        # if sourceNode is None or 'category' not in sourceNode or 'id' not in sourceNode:
        if sourceNode is None:
            print("=========== invalid source node format: {}".format(sourceNode))
            continue
        else:
            sourceNode['node_key'] = edge.get('subject')

        targetNode = node_map.get(edge.get('object'))
        # if targetNode is None or 'category' not in targetNode:
        if targetNode is None:
            print("============= invalid target node format: {}".format(targetNode))
            continue
        else:
            targetNode['node_key'] = edge.get('object')

        # create the edge/node object from the original query
        original_edge = GeneticsModel(edge=edge, source=sourceNode, target=targetNode, map_source_normalized_id={}, map_target_normalized_id={})
        logger.info(original_edge)

        # get source and target lists with unique items
        list_source = original_edge.get_original_source_ids() if original_edge.get_original_source_ids() is not None and len(original_edge.get_original_source_ids()) > 0 else []
        list_target = original_edge.get_original_target_ids() if original_edge.get_original_target_ids() is not None and len(original_edge.get_original_target_ids()) > 0 else []
        list_source = list(set(list_source))
        list_target = list(set(list_target))
    
        # filter out the ontologies we don't service
        # BUG: https://github.com/broadinstitute/genetics-kp-dev/issues/26
        # -- if source or target is only one id, don't bother filtering; if do end up filtering ID, will get unbounded incorrect query
        # NOTE - CREATIVE - only filter subject if not creative query (not drug - treats - disease)
        if not is_creative:
            if len(list_source) > 1:
                list_temp = []
                for item in list_source:
                    if item.split(':')[0] not in list_ontology_prefix_avoid:
                        list_temp.append(item)
                    else:
                        logger.info("skipping non serviced source: {}".format(item))
                list_source = list_temp

        # BUG: https://github.com/broadinstitute/genetics-kp-dev/issues/26
        # -- if source or target is only one id, don't bother filtering
        if len(list_target) > 1:
            list_temp = []
            for item in list_target:
                if item.split(':')[0] not in list_ontology_prefix_avoid:
                    list_temp.append(item)
                else:
                    logger.info("skipping non serviced target: {}".format(item))
            list_target = list_temp


        # test the new normalizing function
        # logger.info("=====================================================")
        # test_source = get_normalize_curies(list_source, log=True)
        # logger.info("found new: {} for original: {}".format(len(test_source), len(list_source)))
        # logger.info("=====================================================")

        # get the normalized list
        # get the descendant list
        subject_curie_list = get_normalize_curies(list_source, log=False)
        # trim curie list to what is in genepro (pulled in at start)
        subject_curie_list = trim_disease_list_tuple_to_what_is_in_the_db(subject_curie_list, SET_CACHED_PHENOTYPES)
        for curie in subject_curie_list:
            original_edge.add_source_normalized_id(curie[1], curie[0])

        target_curie_list = get_normalize_curies(list_target, log=False)
        # trim curie list to what is in genepro (pulled in at start)
        target_curie_list = trim_disease_list_tuple_to_what_is_in_the_db(target_curie_list, SET_CACHED_PHENOTYPES)
        # logger.info("target: {}".format(target_curie_list))
        for curie in target_curie_list:
            original_edge.add_target_normalized_id(curie[1], curie[0])

        # add new object to result list
        results.append(original_edge)

        # log
        logger.info("query with normalized source list: {}".format(original_edge.get_map_source_normalized_id().keys()))
        logger.info("query with normalized target list: {}".format(original_edge.get_map_target_normalized_id().keys()))
        logger.info("query with source count: {} and target count: {}".format(len(original_edge.get_map_source_normalized_id()), len(original_edge.get_map_target_normalized_id())))

    # return
    return results


def query(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: Dict[str, ]

    :rtype: Response
    """

    '''
    WORKFLOW:
    - query is verified for correctness and if can be serviced by KP
    - the subject/object IDs are then expanded
    - database connection started
    - in the query building, the predicates triples are expanded to what is serviced by the KP
    - the queries are run in sequence and the results appended to a list
    - the list is used to build the results in trapi result format
    '''
    # verify all operations asked for are supported
    if request_body.get("workflow") and len(request_body.get("workflow")) > 0:
        logger.info("got workflow: {}".format(request_body.get("workflow")))
        for item in request_body.get("workflow"):
            workflow_item = item.get('id')
            if workflow_item != 'lookup':
                return ({"status": 400, "title": "Workflow {} not implemented".format(workflow_item), "detail": "Workflow {} not implemented".format(workflow_item), "type": "about:blank" }, 400)
    else:
        logger.info("no workflow specified")

    if connexion.request.is_json:
        # initialize
        query_response = {}

        # verify the json
        body = connexion.request.get_json()
        logger.info("got {}".format(body))

        # copy the original query to return in the result
        query_graph = copy.deepcopy(body['message']['query_graph'])

        # check that not more than one hop query (edge list not more than one)
        if len(body.get('message').get('query_graph').get('edges')) > 1:
            logger.error("multi hop query requested, not supported")
            # switch to 400 error code for multi hop query
            # return ({"status": 501, "title": "Not Implemented", "detail": "Multi-edges queries not implemented", "type": "about:blank" }, 501)
            return ({"status": 503, "title": "Not Implemented", "detail": "Multi-edges queries not implemented", "type": "about:blank" }, 503)
        else:
            logger.info("single hop query requested, supported")

        # NOTE - split here based on get creative query; need to do this before expanding IDs based on ontology
        is_creative_query = is_query_creative(body)
        if is_creative_query:
            logger.info("query is CREATIVE")
            # build the response
            query_response = sub_query_creative(body, query_graph, request_body)

        else:
            logger.info("query is LOOKUP")
            # build the response
            query_response = sub_query_lookup(body, query_graph, request_body)

        # # build the response
        # query_response = sub_query_lookup(body, query_graph, request_body)


        # return
        return query_response

    else :
        # return error
        return({"status": 400, "title": "body content not JSON", "detail": "Required body content is not JSON", "type": "about:blank"}, 400)


def sub_query_lookup(body, query_graph, request_body, log=False):
    '''
    deal with a lookup query
    '''
    # initialize
    genetics_results = []

    # tag start time
    start = time.time()

    # build the interim data structure 
    # NOTE - also expand the ID list based on ontology ancestry
    request_input = get_request_elements(body)
    logger.info("got request input {}".format(request_input))

    # only allow small queries
    if len(request_input) > MAX_SIZE_ID_LIST:
        logger.error("too big request, asking for {} combinations".format(len(request_input)))
        return ({"status": 413, "title": "Query payload too large", "detail": "Query payload too large, exceeds the {} subject/object combination size".format(MAX_SIZE_ID_LIST), "type": "about:blank" }, 413)

    # log
    logger.info("looping through queries for web query object list: {}\n".format(request_input))
    for web_request_object in request_input:
        # log
        # logger.info("running query for web query object: {}\n".format(web_request_object))

        # queries
        # NOTE - implemented batch subject/target input - done in the batch sql structure

        # TODO - might have to implement uniqueness on the PK returned (use set); took out duplicate check
        # if not found_results_already:   # TODO - might not be needed anymore since ncats NN and each disease/phenotype entry should only have one curie in the DB

        # make sure it is not an unbounded query (that we have matched with at leat one source/target)
        if len(web_request_object.get_list_source_id()) > 0 or len(web_request_object.get_list_target_id()) > 0:
            queries = qbuilder.get_queries(web_request_object)

            # if results
            if len(queries) > 0:
                found_results_already = True
                # only open web connection when have passed validation of request
                cnx = pymysql.connect(host=DB_HOST, port=3306, database=DB_SCHEMA, user=DB_USER, password=DB_PASSWD)
                cursor = cnx.cursor()

                for i in range(0, len(queries)):
                    sql_object = queries[i]
                    logger.info("running query: {}\n".format(sql_object))
                    cursor.execute(sql_object.sql_string, tuple(sql_object.param_list))
                    results = cursor.fetchall()
                    # print("result of type {} is {}".format(type(results), results))
                    logger.info("for DB query got result count of: {}".format(len(results)))
                    if results:
                        for record in results:
                            edgeID    = record[0]
                            sourceID  = record[1]
                            targetID  = record[2]
                            # trapi 1.3
                            # originalSourceID  = record[1]
                            # originalTargetID  = record[2]
                            originalSourceID  = None
                            originalTargetID  = None

                            # find original source/target IDs
                            if web_request_object.get_map_source_normalized_id().get(sourceID):
                                originalSourceID  = web_request_object.get_map_source_normalized_id().get(sourceID)

                            if web_request_object.get_map_target_normalized_id().get(targetID):
                                originalTargetID  = web_request_object.get_map_target_normalized_id().get(targetID)
                            # else:
                            #     logger.info(web_request_object.get_map_target_normalized_id())
                            # logger.info("original: {}, converted: {}".format(targetID, originalTargetID))

                            score     = record[3]
                            scoreType = record[4]
                            sourceName = record[5]
                            targetName = record[6]
                            edgeType = record[7]
                            sourceType = record[8]
                            targetType = record[9]
                            studyTypeId = record[10]
                            publications = record[11]
                            score_translator = record[12]
                            id_db_edge = record[13]
                            probability = None
                            pValue = None 
                            beta = None 


                            # 20230213 - add qualifiers is available
                            list_qualifiers = []
                            # deprecated since comb_edge_qualifier table deleted; qualifiers now dowe througb decorator class
                            # if has_qualifiers == 'Y':
                                # query the db
                                # cursor.execute(qbuilder.build_qualifier_sql(), (id_db_edge))
                                # db_results_qualifiers = cursor.fetchall()

                                # # build the qualifiers as needed
                                # for row_qualifier in db_results_qualifiers:
                                #     list_qualifiers.append({'id':row_qualifier[0], 'value':row_qualifier[1]})

                            # log
                            # logger.info("got result: {}".format(record))

                            # build the result objects
                            # trapi 1.3
                            # source_node = NodeOuput(curie=originalSourceID, name=sourceName, category=sourceType, node_key=web_request_object.get_source_key())
                            # target_node = NodeOuput(curie=originalTargetID, name=targetName, category=targetType, node_key=web_request_object.get_target_key())
                            source_node = NodeOuput(curie=sourceID, query_curie=originalSourceID, name=sourceName, category=sourceType, node_key=web_request_object.get_source_key())
                            target_node = NodeOuput(curie=targetID, query_curie=originalTargetID, name=targetName, category=targetType, node_key=web_request_object.get_target_key())
                            output_edge = EdgeOuput(id=edgeID, source_node=source_node, target_node=target_node, predicate=edgeType, 
                                score=score, score_type=scoreType, edge_key=web_request_object.get_edge_key(), study_type_id=studyTypeId, 
                                publication_ids=publications, score_translator=score_translator, list_qualifiers=list_qualifiers)

                            # add to the results list
                            genetics_results.append(output_edge)
                
                # close the connection
                cnx.close()

        else:
            logger.info("no source/target inputs that we have, so skip")

        # log
        logger.info("for query \n{}".format(request_body))
        num_source = 0
        if web_request_object.get_original_source_ids():
            num_source = len(web_request_object.get_original_source_ids())
        num_target = 0
        if web_request_object.get_original_target_ids():
            num_target = len(web_request_object.get_original_target_ids())
        logger.info("LOOKUP web query with source count: {} and target count: {} return total edge count: {}".format(num_source, num_target, len(genetics_results)))


    # build the response
    query_response = build_results(results_list=genetics_results, query_graph=query_graph)

    # tag and print the time elapsed
    end = time.time()
    time_elapsed = end - start
    logger.info("LOOKUP web query with source: {} and target: {} return total edge: {} in time: {}s".format(num_source, num_target, len(genetics_results), time_elapsed))

    # return
    return query_response

def sub_query_creative(body, query_graph, request_body, log=False):
    '''
    deal with a creative query
    '''
    # initialize
    genetics_results = []

    # tag start time
    start = time.time()

    # build the interim data structure 
    # NOTE - also expand the ID list based on ontology ancestry
    request_input = get_request_elements(body, is_creative=True)
    logger.info("got request input {}".format(request_input))

    # only allow small queries
    if len(request_input) > MAX_SIZE_ID_LIST:
        logger.error("too big request, asking for {} combinations".format(len(request_input)))
        return ({"status": 413, "title": "Query payload too large", "detail": "Query payload too large, exceeds the {} subject/object combination size".format(MAX_SIZE_ID_LIST), "type": "about:blank" }, 413)

    # log
    logger.info("looping through queries for CREATIVE web query object list: {}\n".format(request_input))
    for web_request_object in request_input:
        # log
        # logger.info("running query for web query object: {}\n".format(web_request_object))

        # make sure it is not an unbounded query (that we have matched with at leat one source/target)
        if len(web_request_object.get_list_source_id()) > 0 or len(web_request_object.get_list_target_id()) > 0:
            queries = qbuilder.build_creative_query(web_request_object, log=True)

            # if results
            if len(queries) > 0:
                found_results_already = True
                # only open web connection when have passed validation of request
                cnx = pymysql.connect(host=DB_HOST, port=3306, database=DB_SCHEMA, user=DB_USER, password=DB_PASSWD, cursorclass=pymysql.cursors.DictCursor)
                cursor = cnx.cursor()

                for i in range(0, len(queries)):
                    sql_object = queries[i]
                    logger.info("running query: {}\n".format(sql_object))
                    cursor.execute(sql_object.sql_string, tuple(sql_object.param_list))
                    list_db_results = cursor.fetchall()
                    # print("result of type {} is {}".format(type(results), results))
                    logger.info("for DB query got result count of: {}".format(len(list_db_results)))


# select concat(path_disease.id, '_', gene_disease.id, '_', drug_gene.id, '_', pathway_gene.id) as result_id,
#     pathway.ontology_id as pathway, pathway.node_name as pathway_name, 
#     gene.ontology_id as gene, gene.node_name as gene_name,
#     disease.ontology_id as disease, disease.node_name as disease_name,
#     path_disease.score as pathway_score, gene_disease.score as gene_score, 
#     drug_gene.drug_ontology_id as drug, drug_gene.drug_name, drug_gene.drug_category_biolink_id as drug_category,
#     drug_gene.predicate_biolink_id as gene_drug_predicate,
#     drug_gene.id as drug_gene_row_id, gene_disease.id as gene_disease_row_id, 
#     pathway_gene.id as path_gene_row_id, path_disease.id as path_disease_row_id
                    if list_db_results:
                        for db_record in list_db_results:
                            # logger.info("record: {}".format(db_record))
                            pathway = CreativeNode(db_record['pathway'], db_record['pathway_name'], 'biolink:Pathway', 'pathway', 'path')
                            gene = CreativeNode(db_record['gene'], db_record['gene_name'], 'biolink:Gene', 'gene', 'gene')
                            disease = CreativeNode(db_record['disease'], db_record['disease_name'], 'biolink:Disease', 'disease', 'dise')
                            drug = CreativeNode(db_record['drug'], db_record['drug_name'], db_record['drug_category'], 'drug', 'drug')
                            drug_gene = CreativeEdge(db_record['drug_gene_row_id'], drug, gene, db_record['gene_drug_predicate'], None)
                            gene_disease = CreativeEdge(db_record['gene_disease_row_id'], gene, disease, 'biolink:genetic_association', db_record['gene_score'])
                            pathway_gene = CreativeEdge(db_record['path_gene_row_id'], pathway, gene, 'biolink:has_part', None)
                            pathway_disease = CreativeEdge(db_record['path_disease_row_id'], pathway, disease, 'biolink:genetic_association', db_record['pathway_score'])
                            creative_result = CreativeResult(db_record['result_id'], gene, pathway, disease, drug, pathway_gene, gene_disease, pathway_disease, drug_gene)

    # def __int__(self, row_id, gene, pathway, disease, drug, pathway_gene, gene_disease, pathway_disease, drug_gene):

                            # edgeID    = record[0]
                            # sourceID  = record[1]
                            # targetID  = record[2]
                            # originalSourceID  = record[1]
                            # originalTargetID  = record[2]

                            # # find original source/target IDs
                            # if web_request_object.get_map_source_normalized_id().get(sourceID):
                            #     originalSourceID  = web_request_object.get_map_source_normalized_id().get(sourceID)

                            # if web_request_object.get_map_target_normalized_id().get(targetID):
                            #     originalTargetID  = web_request_object.get_map_target_normalized_id().get(targetID)
                            # # else:
                            # #     logger.info(web_request_object.get_map_target_normalized_id())
                            # # logger.info("original: {}, converted: {}".format(targetID, originalTargetID))

                            # score     = record[3]
                            # scoreType = record[4]
                            # sourceName = record[5]
                            # targetName = record[6]
                            # edgeType = record[7]
                            # sourceType = record[8]
                            # targetType = record[9]
                            # studyTypeId = record[10]
                            # publications = record[11]
                            # score_translator = record[12]

                            # # build the result objects
                            # source_node = NodeOuput(curie=originalSourceID, name=sourceName, category=sourceType, node_key=web_request_object.get_source_key())
                            # target_node = NodeOuput(curie=originalTargetID, name=targetName, category=targetType, node_key=web_request_object.get_target_key())
                            # output_edge = EdgeOuput(id=edgeID, source_node=source_node, target_node=target_node, predicate=edgeType, 
                            #     score=score, score_type=scoreType, edge_key=web_request_object.get_edge_key(), study_type_id=studyTypeId, 
                            #     publication_ids=publications, score_translator=score_translator)

                            # add to the results list
                            genetics_results.append(creative_result)
                
                # close the connection
                cnx.close()

        else:
            logger.info("no source/target inputs that we have, so skip")

        # log
        logger.info("for query \n{}".format(request_body))
        num_source = 0
        if web_request_object.get_original_source_ids():
            num_source = len(web_request_object.get_original_source_ids())
        num_target = 0
        if web_request_object.get_original_target_ids():
            num_target = len(web_request_object.get_original_target_ids())
        logger.info("CREATIVE web query with source count: {} and target count: {} return total result count: {}".format(num_source, num_target, len(genetics_results)))


    # build the response
    query_response = build_results_creative(results_list=genetics_results, query_graph=query_graph)

    # tag and print the time elapsed
    end = time.time()
    time_elapsed = end - start
    logger.info("CREATIVE web query with source: {} and target: {} return total edge: {} in time: {}s".format(num_source, num_target, len(genetics_results), time_elapsed))

    # return
    # query_response = {"dude": "creative query"}
    return query_response


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
