
import requests
import logging 
import sys 

# constants
logging.basicConfig(level=logging.INFO, format=f'[%(asctime)s] - %(levelname)s - %(name)s : %(message)s')
handler = logging.StreamHandler(sys.stdout)
logger = logging.getLogger(__name__)


def post_query_nodes_one_hop(url, list_source, list_target, list_source_categories, list_target_categories, list_predicates, knowledge_type=None, log=False):
    ''' 
    method to query a trapi url and get the resulting node list back 
    '''
    list_result = []

    # query
    json_response = query_one_hop(url, list_source, list_target, list_source_categories, list_target_categories, list_predicates, knowledge_type=knowledge_type, log=log)

    # loop and build the list
    list_nodes = json_response.get("message").get("knowledge_graph").get("nodes")
    if list_nodes and len(list_nodes) > 1:
        for key, value in list_nodes.items():
            list_result.append((key, value.get("name")))

    # log
    if log:
        logger.info("got {} resulting nodes: {}".format(len(list_result), list_result))

    # return
    return list_result

def post_query_nodes_one_hop(url, list_source, list_target, list_source_categories, list_target_categories, list_predicates, knowledge_type=None, log=False):
    ''' 
    method to query a trapi url and get the resulting node list back 
    '''
    list_result = []

    # query
    json_response = query_one_hop(url, list_source, list_target, list_source_categories, list_target_categories, list_predicates, knowledge_type=knowledge_type, log=log)

    # loop and build the list
    list_nodes = json_response.get("message").get("knowledge_graph").get("nodes")
    if list_nodes and len(list_nodes) > 1:
        for key, value in list_nodes.items():
            list_result.append((key, value.get("name")))

    # log
    if log:
        logger.info("got {} resulting nodes: {}".format(len(list_result), list_result))

    # return
    return list_result

def post_query_edges_one_hop(url, list_source, list_target, list_source_categories, list_target_categories, list_predicates, knowledge_type=None, log=False):
    ''' 
    method to query a trapi url and get the resulting node list back 
    '''
    list_result = []

    # query
    json_response = query_one_hop(url, list_source, list_target, list_source_categories, list_target_categories, list_predicates, knowledge_type=knowledge_type, log=log)

    # loop and build the list
    map_edges = json_response.get("message").get("knowledge_graph").get("edges")
    if map_edges and len(map_edges) > 1:
        for key, value in map_edges.items():
            list_result.append((key, value))

    # log
    if log:
        logger.info("got {} resulting nodes: {}".format(len(list_result), list_result))

    # return
    return list_result

def get_meta_knowlege_graph_list_edges(url, log=False):
    ''' 
    method to query a trapi url and get the resulting node list back 
    '''
    list_edges = []

    # call the url
    logger.info("GET query: {}".format(url))
    response = requests.get(url)
    json_response = response.json()
    logger.info("got results from: {}".format(url))

    # get the edges
    list_edges = json_response.get("edges")

    # log
    if log:
        logger.info("got {} resulting nodes: {}".format(len(list_edges), list_edges))

    # return
    return list_edges

def query_one_hop(url, list_source, list_target, list_source_categories, list_target_categories, list_predicates, knowledge_type=None, log=False):
    ''' 
    method to call a trapi url 
    '''
    response = None

    # build the payload
    payload = build_one_hop_payload(list_source, list_target, list_source_categories, list_target_categories, list_predicates, knowledge_type=knowledge_type, log=log)

    # call the url
    logger.info("POST query: {}".format(url))
    response = requests.post(url, json=payload)
    output_json = response.json()
    logger.info("got results from: {}".format(url))

    # log
    # if log:
    #     logger.info("got response: {}".format(output_json))

    # return the json
    return output_json

def build_one_hop_payload(list_source, list_target, list_source_categories, list_target_categories, list_predicates, knowledge_type=None, log=False):
    ''' 
    method to build a one hop json payload for a trapi query 
    '''
    payload = {}

    # build the payload
    nodes = {"n00": build_trapi_query_node(list_source, list_source_categories, log=True), "n01": build_trapi_query_node(list_target, list_target_categories, log=True)}
    edge = {"subject": "n00", "object": "n01"}
    if list_predicates and len(list_predicates) > 0:
        edge["predicates"]= list_predicates
    if knowledge_type:
        edge["knowledge_type"] = knowledge_type
    edges = {"e00": edge}
    payload["message"] = {"query_graph": {"edges": edges, "nodes": nodes}}

    # log
    if log:
        logger.info("build trapi payload: \n{}".format(json.dumps(payload, indent=4)))

    # return
    return payload

def build_trapi_query_node(list_source, list_source_categories, log=False):
    ''' 
    method to build a trapi query node 
    '''
    node = {}

    # log
    # if log:
    #     logger.info("got id: {} and categories: {}".format(list_source, list_source_categories))

    # build the node
    if list_source and len(list_source) > 0:
        node['ids'] = list_source
    if list_source_categories and len(list_source_categories) > 0:
        node['categories'] = list_source_categories

    # return
    return node