
from logging import log
import six
import copy
import os
import time 
import yaml 

from openapi_server.models.message import Message
from openapi_server.models.knowledge_graph import KnowledgeGraph
from openapi_server.models.edge import Edge
from openapi_server.models.node import Node
from openapi_server.models.query import Query
from openapi_server.models.q_edge import QEdge
from openapi_server.models.q_node import QNode
from openapi_server.models.query_graph import QueryGraph
from openapi_server.models.qualifier import Qualifier
from openapi_server.models.result import Result
from openapi_server.models.edge_binding import EdgeBinding
from openapi_server.models.node_binding import NodeBinding
from openapi_server.models.response import Response
from openapi_server.models.attribute import Attribute
from openapi_server.models.analysis import Analysis
from openapi_server.models.retrieval_source import RetrievalSource
from openapi_server.models.resource_role_enum import ResourceRoleEnum
from openapi_server.models.auxiliary_graph import AuxiliaryGraph

from openapi_server import util
from openapi_server.dcc.creative_model import CreativeResult, CreativeEdge, CreativeNode
import openapi_server.dcc.trapi_constants as trapi_constants

from openapi_server.dcc.utils import translate_type, get_curie_synonyms, get_logger, build_pubmed_ids, get_normalize_curies
from openapi_server.dcc.genetics_model import GeneticsModel, NodeOuput, EdgeOuput
import openapi_server.dcc.query_builder as qbuilder

# set up the logger
logger = get_logger("trapi_extract")


# methods

#
# get the query graph subject data
def get_querygraph_key_node(trapi_query: Query, is_subject=True, log=False):
    '''
    will return the query graph subject key, curie and key
    '''
    # initialize
    key = None
    qnode: QNode = None
    qedge: QEdge = None 

    # get the query graph
    query_graph: QueryGraph = get_querygraph_from_query(trapi_query=trapi_query)

    # get the edge and find out what node key is the subject
    _, qedge = get_queryedge_key_edge(trapi_query=trapi_query)
    if qedge:
        if is_subject:
            key = qedge.subject
        else:
            key = qedge.object
        
    # get the corresponding node
    qnode: QNode = query_graph.nodes.get(key)

    # get the subject for the query
    return key, qnode

#
# get the query graph edge data
def get_queryedge_key_edge(trapi_query: Query, log=False):
    '''
    will return the query graph edge key and predicate
    '''
    key = None
    qedge: QEdge = None

    # get the query graph
    query_graph: QueryGraph = get_querygraph_from_query(trapi_query=trapi_query)

    # get the edge and find out what node key is the subject
    # assume one edge
    if query_graph.edges and len(query_graph.edges) == 1:
        key = next(iter(query_graph.edges))
        qedge = query_graph.edges[key]
        list_predicate = qedge.predicates

    # return
    return key, qedge
        

#
# get the query graph
def get_querygraph_from_query(trapi_query: Query, log=False):
    '''
    will extract the query message from the trapi query
    '''
    # initialize
    query_graph: QueryGraph = None

    # get the message
    if trapi_query:
        message: Message = trapi_query.message
        if message.query_graph:
            query_graph: QueryGraph = message.query_graph

    # return
    return query_graph




