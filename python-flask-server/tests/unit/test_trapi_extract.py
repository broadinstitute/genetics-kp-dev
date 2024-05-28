
# imports
import pytest 
import json 

import openapi_server.dcc.trapi_extract as textract
from openapi_server.models.q_edge import QEdge
from openapi_server.models.q_node import QNode
from openapi_server.models.query import Query

# constants
text_data = '''
  {
    "workflow": [
        {
            "id": "lookup"
        }
    ],
    "message": {
      "query_graph": {
        "edges": {
          "e00": {
            "subject": "subj",
            "object": "obj"
          }
        },
        "nodes": {
          "obj": {
            "categories": ["biolink:Gene"]
          },
          "subj": {
            "ids": ["MONDO:0011936"],
            "categories": ["biolink:DiseaseOrPhenotypicFeature"],
            "set_interpretation": "BATCH"
          }
        }
      }
    }
  }
'''
json_data = json.loads(text_data)

def test_get_queryedge_key_edge():
    '''
    test the qedge retrieval
    '''
    # initialize
    query: Query = Query.from_dict(json_data)
    key = None 
    qedge: QEdge = None

    # get the data
    key, qedge = textract.get_queryedge_key_edge(trapi_query=query)

    # test
    assert key == "e00"
    assert qedge.subject == "subj"
    assert qedge.object == "obj"


def test_get_querygraph_key_node():
    '''
    test the qnode retrieval
    '''
    # initialize
    query: Query = Query.from_dict(json_data)
    key = None 
    qnode: QNode = None

    # get the data
    key, qnode = textract.get_querygraph_key_node(trapi_query=query)

    # test
    assert key == "subj"
    assert qnode.ids == ["MONDO:0011936"]
    assert qnode.set_interpretation == "BATCH"

    # get the data
    key, qnode = textract.get_querygraph_key_node(trapi_query=query, is_subject=False)

    # test
    assert key == "obj"
    assert qnode.ids is None
    assert qnode.set_interpretation is None
