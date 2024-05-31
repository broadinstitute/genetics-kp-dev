
# imports
import pytest 
import json 

import openapi_server.dcc.trapi_extract as textract
import openapi_server.dcc.verification_utils as vutils
import openapi_server.dcc.trapi_constants as tconstants


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
            "set_interpretation": "BATCH"
          }
        }
      }
    }
  }
'''
json_data = json.loads(text_data)

def test_is_query_tissue_related():
    '''
    test recognizing a issue query
    '''
    # initialize
    node: QNode = None
    query: Query = Query.from_dict(json_data)
    _, node = textract.get_querygraph_key_node(trapi_query=query, is_subject=True)

    # set the data
    node.categories = [tconstants.BIOLINK_ENTITY_CELL]

    # get data
    is_tissue = vutils.is_query_tissue_related(query=query)

    # test
    assert is_tissue

    # set the data
    query: Query = Query.from_dict(json_data)
    _, node = textract.get_querygraph_key_node(trapi_query=query, is_subject=False)
    node.ids = ["UBERON:11223344"]

    # get data
    is_tissue = vutils.is_query_tissue_related(query=query)

    # test
    assert is_tissue

