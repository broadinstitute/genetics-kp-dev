
# imports
import openapi_server.dcc.result_utils as rutils

# constants
url_trapi_service = "https://translator.broadinstitute.org/genetics_provider/trapi/v1.2/{}"

# tests
def test_query_api():
    ''' method to test the post query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    map_nodes = rutils.get_nodes_one_hop(url, None, ["MONDO:0011936"], ["biolink:Gene"], ["biolink:DiseaseOrPhenotypicFeature"], None)

    # test
    assert len(map_nodes) > 0

def test_meta_knowledge_graph_api():
    ''' method to test the get MKG ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("meta_knowledge_graph")

    # call the query service and get the nodes
    map_nodes = rutils.get_nodes_one_hop(url, None, ["MONDO:0011936"], ["biolink:Gene"], ["biolink:DiseaseOrPhenotypicFeature"], None)

    # test
    assert len(map_nodes) > 0
