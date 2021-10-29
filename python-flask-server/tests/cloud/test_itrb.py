
# imports
import openapi_server.dcc.result_utils as rutils

# tests
def test_genetics_api():
    ''' method to test the ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url_genetics_kp = "https://genetics-kp.ci.transltr.io/genetics_provider/trapi/v1.2/{}".format("query")

    # call the query service and get the nodes
    map_nodes = rutils.get_nodes_one_hop(url_genetics_kp, None, ["MONDO:0011936"], ["biolink:Gene"], ["biolink:DiseaseOrPhenotypicFeature"], None)

    # test
    assert len(map_nodes) > 0
