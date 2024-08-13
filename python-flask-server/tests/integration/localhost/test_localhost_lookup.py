
# imports
import openapi_server.dcc.result_utils as rutils

# constants
url_trapi_service = "http://localhost:7003/genetics_provider/trapi/v1.5/{}"

# tests
def test_query_api():
    ''' method to test the post query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    map_nodes = rutils.post_query_nodes_one_hop(url, None, ["MONDO:0011936"], ["biolink:Gene"], ["biolink:DiseaseOrPhenotypicFeature"], None)

    # test
    assert len(map_nodes) > 0

# def test_creative_query_api():
#     ''' method to test the post creative query ncats itrb cloud deployment of the genetics kp '''

#     # get the url
#     url = url_trapi_service.format("query")

#     # call the query service and get the nodes
#     map_nodes = rutils.post_query_nodes_one_hop(url, None, ["MONDO:0004975"], ["biolink:ChemicalEntity"], ["biolink:Disease"], ["biolink:treats"], knowledge_type="inferred", log=False)

#     # test
#     assert len(map_nodes) > 0

def test_meta_knowledge_graph_api():
    ''' method to test the get MKG ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("meta_knowledge_graph")

    # call the query service and get the nodes
    list_edges = rutils.get_meta_knowlege_graph_list_edges(url, log=True)

    # test
    assert len(list_edges) > 0

def test_primary_knowledge_sources_for_edge():
    ''' method to test the get MKG ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    list_edges = rutils.post_query_edges_one_hop(url, None, ["MONDO:0011936"], ["biolink:Gene"], ["biolink:DiseaseOrPhenotypicFeature"], None)

    # test
    for (name, edge) in list_edges:
        # get the attributes amd make sure one is a primary KS
        list_attributes = edge.get('sources')
        has_primary = False
        for attribute in list_attributes:
            if attribute.get('resource_role') == 'primary_knowledge_source':
                has_primary = True
                break
        assert has_primary
