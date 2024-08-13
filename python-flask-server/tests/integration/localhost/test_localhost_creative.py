
# imports
import openapi_server.dcc.result_utils as rutils

# constants
url_trapi_service = "http://localhost:7003/genetics_provider/trapi/v1.5/{}"

# tests

def test_creative_query_api():
    ''' method to test the post creative query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    map_nodes = rutils.post_query_nodes_one_hop(url, None, ["MONDO:0004975"], ["biolink:ChemicalEntity"], ["biolink:Disease"], ["biolink:treats"], knowledge_type="inferred", log=False)

    # test
    assert len(map_nodes) > 0

