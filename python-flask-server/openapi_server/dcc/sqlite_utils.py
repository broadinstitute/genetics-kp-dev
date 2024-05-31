

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
from openapi_server.models.response_message import ResponseMessage

import openapi_server.dcc.trapi_utils as tutils
import openapi_server.dcc.trapi_extract as textract
import openapi_server.dcc.trapi_constants as trapi_constants

from openapi_server.dcc.utils import get_logger

# logger
logger = get_logger('multi_curie_utils.py')

# constants
FILE_DB = "conf/mcq.db"

# methods
def get_connection(log=False):
    # get the db connection
    conn = sqlite3.connect(FILE_DB)

    # return
    return conn


def db_query_sqlite(sql_query, trapi_query: Query, log=False):
    '''
    will query the database for the data
    '''
    # initialize
    list_result = []

    # get the data

    # return
    return list_result


def build_trapi_response(list_result, trapi_query: Query, log=False):
    '''
    builds the trapi response from the given data list
    '''

def trapi_response(sql_query, trapi_query: Query, list_trapi_logs=[], log=False):
    '''
    builds the trapi response based on the sql query given
    '''
    # initialize
    list_result = []
    trapi_response_message: ResponseMessage = tutils.build_response_message(query_graph=trapi_query.message.query_graph)
    trapi_response: Response = Response(message=trapi_response_message, logs=list_trapi_logs, workflow=trapi_query.workflow, 
                            biolink_version=tutils.get_biolink_version(), schema_version=tutils.get_trapi_version())

    # get the data
    list_result = db_query_sqlite(sql_query=sql_query, trapi_query=trapi_query, log=log)

    # build the response
    list_trapi_logs.append("responding to tissue/gene query")

    # return
    return trapi_response



