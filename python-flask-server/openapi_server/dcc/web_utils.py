
import connexion
import six
import pymysql
import copy
import os

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

from openapi_server.dcc.utils import translate_type, get_curie_synonyms, get_logger, build_pubmed_ids
from openapi_server.dcc.genetics_model import GeneticsModel, NodeOuput, EdgeOuput
import openapi_server.dcc.query_builder as qbuilder

# get logger
logger = get_logger(__name__)

# constants
list_ontology_prefix = ['UMLS', 'NCIT', 'MONDO', 'EFO', 'NCBIGene', 'GO', 'HP', 'MESH']
list_ontology_prefix_avoid = ['FMA', 'CHEMBL.TARGET', 'CHEMBL.COMPOUND', 'PUBCHEM.COMPOUND', 'UNII', 'CHEBI', 'DRUGBANK', 'CAS', 'DrugCentral', 'KEGG.COMPOUND', 'INCHIKEY', 'GTOPDB']

# infores
PROVENANCE_INFORES_KP_GENETICS='infores:genetics-data-provider'
PROVENANCE_INFORES_CLINVAR='infores:clinvar'
PROVENANCE_INFORES_CLINGEN='infores:clingen'
PROVENANCE_INFORES_GENCC='infores:gencc'
PROVENANCE_INFORES_GENEBASS='infores:genebass'

# provenance attributes
PROVENANCE_AGGREGATOR_KP_GENETICS = Attribute(value = PROVENANCE_INFORES_KP_GENETICS,
    attribute_type_id = 'biolink:aggregator_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://translator.broadinstitute.org/genetics_provider/trapi/v1.1',
    description = 'The Genetics Data Provider KP from NCATS Translator',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS)
PROVENANCE_AGGREGATOR_CLINVAR = Attribute(value = PROVENANCE_INFORES_CLINVAR,
    attribute_type_id = 'biolink:aggregator_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://www.ncbi.nlm.nih.gov/clinvar/',
    description = 'ClinVar is a freely accessible, public archive of reports of the relationships among human variations and phenotypes',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS)
PROVENANCE_AGGREGATOR_CLINGEN = Attribute(value = PROVENANCE_INFORES_CLINGEN,
    attribute_type_id = 'biolink:aggregator_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://clinicalgenome.org/',
    description = 'ClinGen is a NIH-funded resource dedicated to building a central resource that defines the clinical relevance of genes and variants for use in precision medicine and research',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS)
PROVENANCE_AGGREGATOR_GENCC = Attribute(value = PROVENANCE_INFORES_GENCC,
    attribute_type_id = 'biolink:aggregator_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://thegencc.org/',
    description = 'The GenCC DB provides information pertaining to the validity of gene-disease relationships, with a current focus on Mendelian diseases',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS)
PROVENANCE_AGGREGATOR_GENEBASS = Attribute(value = PROVENANCE_INFORES_GENEBASS,
    attribute_type_id = 'biolink:aggregator_knowledge_source',
    value_type_id = 'biolink:InformationResource',
    value_url = 'https://genebass.org/',
    description = 'Genebass is a resource of exome-based association statistics, made available to the public. The dataset encompasses 3,817 phenotypes with gene-based and single-variant testing across 281,852 individuals with exome sequence data from the UK Biobank.',
    attribute_source = PROVENANCE_INFORES_KP_GENETICS)

# build map for study types
MAP_PROVENANCE = {5: PROVENANCE_AGGREGATOR_CLINGEN, 6: PROVENANCE_AGGREGATOR_CLINVAR, 7: PROVENANCE_AGGREGATOR_GENCC, 17: PROVENANCE_AGGREGATOR_GENEBASS}

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

def queryOld(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: Dict[str, ]

    :rtype: Response
    """
    # cnx = mysql.connector.connect(database='Translator', user='mvon')
    # cnx = pymysql.connect(host='localhost', port=3306, database='Translator', user='mvon')
    cursor = cnx.cursor()

    if connexion.request.is_json:
        body = connexion.request.get_json()
        print("got {}".format(body))
        takenNodes = {}
        takenEdges = {}

        body['results'] = []
        body['knowledge_graph'] = {}
        body['knowledge_graph']['nodes'] = []
        body['knowledge_graph']['edges'] = []
 
        for edge in body['message']['query_graph']['edges']:
            if 'type' not in edge or edge['type'] != 'associated' or 'source_id' not in edge or 'target_id' not in edge:
                continue
            
            sourceNode = 0;
            for node in body['message']['query_graph']['nodes']:
                if 'id' in node and node['id'] == edge['source_id']:
                    sourceNode = node
                    break

            if sourceNode == 0 or 'type' not in sourceNode or 'curie' not in sourceNode:
                continue

            targetnode = 0;
            for node in body['message']['query_graph']['nodes']:
                if 'id' in node and node['id'] == edge['target_id']:
                    targetNode = node
                    break

            if targetNode == 0 or 'type' not in targetNode:
                continue
        
            qeID       = edge['id']
            sourceID   = sourceNode['curie']
            qn0ID      = sourceNode['id']
            qn1ID      = targetNode['id']
            sourceType = translate_type(sourceNode['type'])
            targetType = translate_type(targetNode['type'])

            # N = 0
            info    = []
            queries = []

            # log
            print("running query for source type: {} and source_id: {} and target type: {}".format(sourceType, sourceID, targetType))

            # queries
            if (sourceType == 'disease' or sourceType == 'phenotypic_feature') and targetType == 'gene':
                # N = 2
                info = [["MAGMA-pvalue", "smaller_is_better"],\
                        ["Richards-effector-genes", "higher_is_better"],\
                        ["ABC-genes", "not_displayed"],\
                        ["Genetics-quantile", "higher_is_better"]]
                queries = ["select GENE,ID,PVALUE from MAGMA_GENES where DISEASE='{}' and CATEGORY='{}' and PVALUE<2.5e-6 ORDER by PVALUE  ASC".format(sourceID,sourceType),\
                           "select gene, id, probability from richards_gene where phenotype='{}' and category='{}' ORDER by probability desc".format(sourceID,sourceType),\
                           "select gene_ncbi_id, edge_id, null from abc_gene_phenotype where phenotype_efo_id='{}' and category='{}' and gene_ncbi_id is not null order by edge_id".format(sourceID,sourceType),\
                           "select GENE,ID,SCORE  from SCORE_GENES where DISEASE='{}' and CATEGORY='{}' and SCORE >0.95   ORDER by SCORE  DESC".format(sourceID,sourceType)]

            elif (sourceType == 'disease' or sourceType == 'phenotypic_feature') and targetType == 'pathway':
                # N = 1
                info = [["MAGMA-pvalue", "smaller_is_better"]]
                queries = ["select PATHWAY,ID,PVALUE from MAGMA_PATHWAYS where DISEASE='{}' and CATEGORY='{}' and PVALUE<2.0e-6 ORDER by PVALUE ASC".format(sourceID,sourceType)]

            elif sourceType == 'gene' and (targetType == 'disease' or targetType == 'phenotypic_feature'):
                # N = 2
                info = [["MAGMA-pvalue", "smaller_is_better"],\
                        ["Richards-effector-genes", "higher_is_better"],\
                        ["ABC-genes", "not_displayed"],\
                        ["Genetics-quantile", "higher_is_better"]]
                queries = ["select DISEASE,ID,PVALUE from MAGMA_GENES where GENE='{}' and CATEGORY='{}' and PVALUE<0.05 ORDER by PVALUE ASC".format(sourceID,targetType),\
                           "select phenotype, id, probability from richards_gene where gene='{}' and category='{}' ORDER by probability desc".format(sourceID,targetType),\
                           "select phenotype_efo_id, edge_id, null from abc_gene_phenotype where gene_ncbi_id='{}' and category='{}' and phenotype_efo_id is not null order by edge_id".format(sourceID,targetType),\
                           "select DISEASE,ID,SCORE  from SCORE_GENES where GENE='{}' and CATEGORY='{}' and SCORE >0.80 ORDER by SCORE DESC".format(sourceID,targetType)]

            elif sourceType == 'pathway' and (targetType == 'disease' or targetType == 'phenotypic_feature'):
                # N = 1
                info = [["MAGMA-pvalue", "smaller_is_better"]]
                queries = ["select DISEASE,ID,PVALUE from MAGMA_PATHWAYS where PATHWAY='{}' and CATEGORY='{}' and PVALUE<0.05 ORDER by PVALUE ASC".format(sourceID,targetType)]

            if len(queries) > 0:
                for i in range(0, len(queries)):
                    print("running query: {}".format(queries[i]))
                    cursor.execute(queries[i])
                    results = cursor.fetchall()
                    print("result of type {} is {}".format(type(results), results))
                    if results:
                        for record in results:
                            targetID  = record[0]
                            edgeID    = record[1]
                            score     = record[2]

                            if sourceID not in takenNodes:
                                body['knowledge_graph']['nodes'].append({"id" : sourceID, "type" : sourceType})
                                takenNodes[sourceID] = 1

                            if targetID not in takenNodes:
                                body['knowledge_graph']['nodes'].append({"id" : targetID, "type" : targetType})
                                takenNodes[targetID] = 1

                            if edgeID not in takenEdges: 
                                if score is not None:
                                    body['knowledge_graph']['edges'].append({"id" : edgeID, "source_id": sourceID, "target_id" : targetID, "score_name" : info[i][0], "score" : score, "score_direction" : info[i][1], "type" : "associated"})
                                else:
                                    body['knowledge_graph']['edges'].append({"id" : edgeID, "source_id": sourceID, "target_id" : targetID, "score_name" : info[i][0], "type" : "associated"})
                                takenEdges[edgeID] = 1

                            body['results'].append({"edge_bindings": [ {"kg_id": edgeID, "qg_id": qeID} ], "node_bindings": [ { "kg_id": sourceID, "qg_id": qn0ID }, { "kg_id": targetID, 'qg_id': qn1ID } ] })

        body['query_graph'] = body['message']['query_graph']
        del body['message']
        return body

    cnx.close() 
    return({"status": 400, "title": "body content not JSON", "detail": "Required body content is not JSON", "type": "about:blank"}, 400)


def get_request_elements(body):
    """ translates the json into a neutral format """
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
        list_temp = []
        for item in list_source:
            if item.split(':')[0] not in list_ontology_prefix_avoid:
                list_temp.append(item)
            else:
                logger.info("skipping non serviced source: {}".format(item))
        list_source = list_temp
        list_temp = []
        for item in list_target:
            if item.split(':')[0] not in list_ontology_prefix_avoid:
                list_temp.append(item)
            else:
                logger.info("skipping non serviced target: {}".format(item))
        list_target = list_temp

        # TODO - get the normalized list
        # TODO - get the descendant list
        list_temp = []
        for item in list_source:
            # if curie already put in curie list, then no need to get synonyms/children
            if not item in list_temp:
                subject_curie_name, subject_curie_list = get_curie_synonyms(item, prefix_list=list_ontology_prefix, type_name='subject', log=True)
                list_temp += subject_curie_list

                # trim curie list to what is in genepro (pulled in at start)
                subject_curie_list = trim_disease_list_to_what_is_in_the_db(subject_curie_list, SET_CACHED_PHENOTYPES)
                for curie in subject_curie_list:
                    original_edge.add_source_normalized_id(curie, item)
            else:
                logger.info("skip source curie since already in list: {}".format(item))
        list_temp = []
        for item in list_target:
            if not item in list_temp:
                target_curie_name, target_curie_list = get_curie_synonyms(item, prefix_list=list_ontology_prefix, type_name='target', log=True)

                # trim curie list to what is in genepro (pulled in at start)
                target_curie_list = trim_disease_list_to_what_is_in_the_db(target_curie_list, SET_CACHED_PHENOTYPES)
                for curie in target_curie_list:
                    original_edge.add_target_normalized_id(curie, item)
            else:
                logger.info("skip target curie since already in list: {}".format(item))

        # TODO - trim the lists to unique values
        # should be done by map with key as sql input curies
        # TODO - trim the lists to what we have in cache

        # add new object to result list
        results.append(original_edge)

        # log
        logger.info("query with normalized source list: {}".format(original_edge.get_map_source_normalized_id().keys()))
        logger.info("query with normalized target list: {}".format(original_edge.get_map_target_normalized_id().keys()))
        logger.info("query with source count: {} and target count: {}".format(len(original_edge.get_map_source_normalized_id()), len(original_edge.get_map_target_normalized_id())))

        # split the source and target ids
        # list_source = original_edge.get_source_ids() if original_edge.get_source_ids() is not None and len(original_edge.get_source_ids()) > 0 else [None]
        # list_target = original_edge.get_target_ids() if original_edge.get_target_ids() is not None and len(original_edge.get_target_ids()) > 0 else [None]

        # # make sure each list has unique items
        # list_source = list(set(list_source))
        # list_target = list(set(list_target))

        # # for each combination, create a new request model object
        # for sitem in list_source:
        #     for titem in list_target:
        #         new_edge = GeneticsModel(edge, sourceNode, targetNode, source_id=sitem, target_id=titem)
                
        #         # add to the list
        #         results.append(new_edge)

    # return
    return results

def build_results(results_list, query_graph):
    """ build the trapi v1.0 response from the genetics model """
    # build the empty collections
    results = []
    knowledge_graph = KnowledgeGraph(nodes={}, edges={})
    nodes = {}
    edges = {}

    # loop through the results
    for edge_element in results_list:
        # get the nodes
        source = edge_element.source_node
        target = edge_element.target_node
        # print("edge element: {}".format(edge_element))

        # add the edge
        # build the provenance data
        attributes = [PROVENANCE_AGGREGATOR_KP_GENETICS]
        provenance_child = MAP_PROVENANCE.get(edge_element.study_type_id)
        if provenance_child:
            attributes.append(provenance_child)

        # add in the pvalue/probability if applicable
        attributes.append(Attribute(original_attribute_name='probability', value=edge_element.score_translator, attribute_type_id='biolink:probability'))
        if edge_element.score is not None:
            # OLD - pre score translator data
            # if edge_element.score_type == 'biolink:probability':
            #     attributes.append(Attribute(original_attribute_name='probability', value=edge_element.score, attribute_type_id=edge_element.score_type))

            # add p_value or classification if available
            if edge_element.score_type == 'biolink:classification':
                attributes.append(Attribute(original_attribute_name='classification', value=edge_element.score, attribute_type_id=edge_element.score_type))
            elif edge_element.score_type == 'biolink:p_value':
                attributes.append(Attribute(original_attribute_name='pValue', value=edge_element.score, attribute_type_id=edge_element.score_type))
            # print("added attributes: {}".format(attributes))

        if edge_element.publication_ids:
            list_publication = build_pubmed_ids(edge_element.publication_ids)
            if (list_publication):
                pub_source = None
                if MAP_PROVENANCE.get(edge_element.study_type_id):
                    pub_source = MAP_PROVENANCE.get(edge_element.study_type_id).value
                attributes.append(Attribute(original_attribute_name='publication', value=list_publication, 
                    attribute_type_id='biolink:has_supporting_publications', value_type_id='biolink:Publication', attribute_source=pub_source))

        # build the edge
        edge = Edge(predicate=translate_type(edge_element.predicate, False), subject=source.curie, object=target.curie, attributes=attributes)
        knowledge_graph.edges[edge_element.id] = edge
        edges[(source.node_key, target.node_key)] = edge

        # add the subject node
        node = Node(name=source.name, categories=[translate_type(source.category, False)], attributes=None)
        nodes[source.node_key] = node           
        knowledge_graph.nodes[source.curie] = node

        # add the target node
        node = Node(name=target.name, categories=[translate_type(target.category, False)], attributes=None)
        nodes[target.node_key] = node           
        knowledge_graph.nodes[target.curie] = node

        # build the bindings
        source_binding = NodeBinding(id=source.curie)
        edge_binding = EdgeBinding(id=edge_element.id)
        target_binding = NodeBinding(id=target.curie)
        edge_map = {edge_element.edge_key: [edge_binding]}
        nodes_map = {source.node_key: [source_binding], target.node_key: [target_binding]}
        results.append(Result(nodes_map, edge_map, score=edge_element.score_translator))

    # build out the message
    message = Message(results=results, query_graph=query_graph, knowledge_graph=knowledge_graph)
    results_response = Response(message = message)

    # return
    return results_response


def query(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: Dict[str, ]

    :rtype: Response
    """
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
        # cnx = mysql.connector.connect(database='Translator', user='mvon')
        # cnx = pymysql.connect(host='localhost', port=3306, database='Translator', user='mvon')
        # cnx = pymysql.connect(host='localhost', port=3306, database='tran_genepro', user='root', password='this is no password')
        # cnx = pymysql.connect(host='localhost', port=3306, database='tran_test_202108', user='root', password='yoyoma')
        cnx = pymysql.connect(host=DB_HOST, port=3306, database=DB_SCHEMA, user=DB_USER, password=DB_PASSWD)
        cursor = cnx.cursor()
        genetics_results = []
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



        # takenNodes = {}
        # takenEdges = {}

        # build the interim data structure
        request_input = get_request_elements(body)
        logger.info("got request input {}".format(request_input))

        # only allow small queries
        if len(request_input) > MAX_SIZE_ID_LIST:
            logger.error("too big request, asking for {} combinations".format(len(request_input)))
            return ({"status": 413, "title": "Query payload too large", "detail": "Query payload too large, exceeds the {} subject/object combination size".format(MAX_SIZE_ID_LIST), "type": "about:blank" }, 413)

 
        for web_request_object in request_input:
            # log
            # logger.info("running query for web query object: {}\n".format(web_request_object))

            # NOTE - now done in request oebject building
            # # get the normalized curies
            # # keep track of whether result came in for this curie; returns name from NN and synonym curie list
            # subject_curie_name, subject_curie_list = get_curie_synonyms(web_request_object.get_source_id(), prefix_list=list_ontology_prefix, type_name='subject', log=True)
            # target_curie_name, target_curie_list = get_curie_synonyms(web_request_object.get_target_id(), prefix_list=list_ontology_prefix, type_name='target', log=True)

            # # trim source/target lists to what we have in db
            # subject_curie_list = trim_disease_list_to_what_is_in_the_db(subject_curie_list, SET_CACHED_PHENOTYPES)
            # target_curie_list = trim_disease_list_to_what_is_in_the_db(target_curie_list, SET_CACHED_PHENOTYPES)

            # queries
            # NOTE - implemented batch subject/target input
            # for source_curie in subject_curie_list:
            #     for target_curie in target_curie_list:
            #         # only run next normalized curie in list if there were no other results, or else will get duplicate results

            # TODO - might have to implement uniqueness on the PK returned (use set); took out duplicate check
            # if not found_results_already:   # TODO - might not be needed anymore since ncats NN and each disease/phenotype entry should only have one curie in the DB
            # set the normalized curie for the call
            # web_request_object.set_source_normalized_id(source_curie)
            # web_request_object.set_target_normalized_id(target_curie)
            # make sure it is not an unbounded query (that we have matched with at leat one source/target)
            if len(web_request_object.get_list_source_id()) > 0 or len(web_request_object.get_list_target_id()) > 0:
                queries = qbuilder.get_queries(web_request_object)

                # if results
                if len(queries) > 0:
                    found_results_already = True
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
                                originalSourceID  = record[1]
                                originalTargetID  = record[2]

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

                                # build the result objects
                                source_node = NodeOuput(curie=originalSourceID, name=sourceName, category=sourceType, node_key=web_request_object.get_source_key())
                                target_node = NodeOuput(curie=originalTargetID, name=targetName, category=targetType, node_key=web_request_object.get_target_key())
                                output_edge = EdgeOuput(id=edgeID, source_node=source_node, target_node=target_node, predicate=edgeType, 
                                    score=score, score_type=scoreType, edge_key=web_request_object.get_edge_key(), study_type_id=studyTypeId, 
                                    publication_ids=publications, score_translator=score_translator)

                                # add to the results list
                                genetics_results.append(output_edge)
                    
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
        logger.info("web query with source count: {} and target count: {} return total edge count: {}".format(num_source, num_target, len(genetics_results)))

        # close the connection
        cnx.close()

        # build the response
        query_response = build_results(results_list=genetics_results, query_graph=query_graph)
        return query_response

    else :
        # return error
        return({"status": 400, "title": "body content not JSON", "detail": "Required body content is not JSON", "type": "about:blank"}, 400)

