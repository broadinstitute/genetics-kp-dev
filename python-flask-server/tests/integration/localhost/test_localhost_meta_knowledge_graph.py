
# imports
import openapi_server.dcc.result_utils as rutils
import time 

# constants
url_trapi_service = "http://localhost:7003/genetics_provider/trapi/v1.5/{}"
time_elapsed_seconds = 1

# tests
def test_meta_knowledge_graph_api():
    ''' method to test the get MKG ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("meta_knowledge_graph")

    # call the query service and get the nodes
    time_start = time.time()
    list_edges = rutils.get_meta_knowlege_graph_list_edges(url, log=True)
    time_end = time.time()

    # test
    assert len(list_edges) > 0
    assert (time_end - time_start) < time_elapsed_seconds

