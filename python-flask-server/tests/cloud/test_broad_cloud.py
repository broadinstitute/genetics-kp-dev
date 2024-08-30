
# imports
import openapi_server.dcc.result_utils as rutils
import time

# constants
url_trapi_service = "https://translator.broadinstitute.org/genetics_provider/trapi/v1.5/{}"
time_elapsed_seconds = 5

# tests
def test_query_api_gene_disease():
    ''' method to test the post query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=None, list_target=["MONDO:0011936"], 
                                                list_source_categories=["biolink:Gene"], list_target_categories=["biolink:DiseaseOrPhenotypicFeature"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds

    # as disease
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=None, list_target=["MONDO:0011936"], 
                                                list_source_categories=["biolink:Gene"], list_target_categories=["biolink:Disease"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds


def test_query_api_disease_gene():
    ''' method to test the post query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=["MONDO:0011936"], list_target=None, 
                                                list_source_categories=["biolink:DiseaseOrPhenotypicFeature"], list_target_categories=["biolink:Gene"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds

    # as disease
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=["MONDO:0011936"], list_target=None, 
                                                list_source_categories=["biolink:Disease"], list_target_categories=["biolink:Gene"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds


def test_query_api_gene_phenotype():
    ''' method to test the post query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=["NCBIGene:652"], list_target=None, 
                                                list_source_categories=["biolink:Gene"], list_target_categories=["biolink:DiseaseOrPhenotypicFeature"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds

    # as disease
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=["NCBIGene:652"], list_target=None, 
                                                list_source_categories=["biolink:Gene"], list_target_categories=["biolink:PhenotypicFeature"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds


def test_query_api_phenotype_gene():
    ''' method to test the post query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=None, list_target=["NCBIGene:652"], 
                                                list_source_categories=["biolink:DiseaseOrPhenotypicFeature"], list_target_categories=["biolink:Gene"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds

    # as disease
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=None, list_target=["NCBIGene:652"], 
                                                list_source_categories=["biolink:PhenotypicFeature"], list_target_categories=["biolink:Gene"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds


def test_query_api_phenotype_pathway():
    ''' method to test the post query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=None, list_target=["GO:0045444"], 
                                                list_source_categories=["biolink:PhenotypicFeature"], list_target_categories=["biolink:Pathway"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds

    # as disease
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=None, list_target=["GO:0045444"], 
                                                list_source_categories=["biolink:DiseaseOrPhenotypicFeature"], list_target_categories=["biolink:Pathway"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds


def test_query_api_pathway_phenotype():
    ''' method to test the post query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=["GO:0045444"], list_target=None, 
                                                list_source_categories=["biolink:Pathway"], list_target_categories=["biolink:PhenotypicFeature"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds

    # as disease
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=["GO:0045444"], list_target=None, 
                                                list_source_categories=["biolink:Pathway"], list_target_categories=["biolink:DiseaseOrPhenotypicFeature"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds


def test_query_api_disease_pathway():
    ''' method to test the post query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=None, list_target=["GO:0045444"], 
                                                list_source_categories=["biolink:Disease"], list_target_categories=["biolink:Pathway"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds

    # as disease
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=None, list_target=["GO:0045444"], 
                                                list_source_categories=["biolink:DiseaseOrPhenotypicFeature"], list_target_categories=["biolink:Pathway"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds


def test_query_api_pathway_disease():
    ''' method to test the post query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=["GO:0045444"], list_target=None, 
                                                list_source_categories=["biolink:Pathway"], list_target_categories=["biolink:Disease"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds

    # as disease
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=["GO:0045444"], list_target=None, 
                                                list_source_categories=["biolink:Pathway"], list_target_categories=["biolink:DiseaseOrPhenotypicFeature"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds


def test_query_api_disease_cell():
    ''' method to test the post query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=None, list_target=None, 
                                                list_source_categories=["biolink:Disease"], list_target_categories=["biolink:Cell"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds

    # TODO - error
    # # as disease
    # time_start = time.time()
    # map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=None, list_target=["NCBIGene:652"], 
    #                                             list_source_categories=["biolink:DiseaseOrPhenotypicFeature"], list_target_categories=["biolink:Cell"],
    #                                             list_predicates=None, knowledge_type=None, log=False)
    # time_end = time.time()
    # time_elapsed = (time_end - time_start)
    # # test
    # assert len(map_nodes) > 0
    # assert time_elapsed < time_elapsed_seconds


def test_query_api_phenotype_cell():
    ''' method to test the post query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=None, list_target=None, 
                                                list_source_categories=["biolink:PhenotypicFeature"], list_target_categories=["biolink:Cell"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert len(map_nodes) > 0
    assert (time_end - time_start) < time_elapsed_seconds

    # TODO - error
    # # as disease
    # time_start = time.time()
    # map_nodes = rutils.post_query_nodes_one_hop(url=url, list_source=None, list_target=["NCBIGene:652"], 
    #                                             list_source_categories=["biolink:DiseaseOrPhenotypicFeature"], list_target_categories=["biolink:Cell"],
    #                                             list_predicates=None, knowledge_type=None, log=False)
    # time_end = time.time()
    # time_elapsed = (time_end - time_start)
    # # test
    # assert len(map_nodes) > 0
    # assert time_elapsed < time_elapsed_seconds


def test_creative_query_api():
    ''' method to test the post creative query ncats itrb cloud deployment of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    map_nodes = rutils.post_query_nodes_one_hop(url, None, ["MONDO:0004975"], ["biolink:ChemicalEntity"], ["biolink:Disease"], ["biolink:affects"], knowledge_type="inferred", log=False)

    # test
    assert len(map_nodes) > 0


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


def test_query_logs():
    ''' method to test the post query logs result of the genetics kp '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    list_logs = rutils.post_query_logs_one_hop(url=url, list_source=None, list_target=["GO:0045444"], 
                                                list_source_categories=["biolink:Disease"], list_target_categories=["biolink:Pathway"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert list_logs is not None
    assert len(list_logs) > 0
    assert (time_end - time_start) < time_elapsed_seconds
    for row_log in list_logs:
        assert type(row_log) == dict
        assert row_log.get('code') is not None
        assert row_log.get('level') is not None
        assert row_log.get('message') is not None
        assert row_log.get('timestamp') is not None


def test_query_edge_bindings_mapping_old():
    ''' 
    method to test the post query edge binding map to make sure value is a list of edge bindings
    '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    list_results = rutils.post_query_results_one_hop(url=url, list_source=None, list_target=["GO:0045444"], 
                                                list_source_categories=["biolink:Disease"], list_target_categories=["biolink:Pathway"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert list_results is not None
    assert len(list_results) > 0
    assert (time_end - time_start) < time_elapsed_seconds
    for row_result in list_results:
        list_analyses = row_result.get("analyses")
        assert list_analyses is not None
        assert len(list_analyses) > 0
        for row_analysis in list_analyses:
            map_edge_bindings = row_analysis.get('edge_bindings')
            assert map_edge_bindings is not None
            assert len(map_edge_bindings) > 0
            for key, value in map_edge_bindings.items():
                assert type(value) == list


def test_query_edge_bindings_mapping_new():
    ''' 
    method to test the post query edge binding map to make sure value is a list of edge bindings
    '''

    # get the url
    url = url_trapi_service.format("query")

    # call the query service and get the nodes
    time_start = time.time()
    # list_results = rutils.post_query_results_one_hop(url=url, list_source=None, list_target=["GO:0045444"], 
    #                                             list_source_categories=["biolink:Disease"], list_target_categories=["biolink:Pathway"],
    #                                             list_predicates=None, knowledge_type=None, log=False)
    list_results = rutils.post_query_results_one_hop(url=url, list_source=None, list_target=None, 
                                                list_source_categories=["biolink:PhenotypicFeature"], list_target_categories=["biolink:Cell"],
                                                list_predicates=None, knowledge_type=None, log=False)
    time_end = time.time()

    # test
    assert list_results is not None
    assert len(list_results) > 0
    assert (time_end - time_start) < time_elapsed_seconds
    for row_result in list_results:
        list_analyses = row_result.get("analyses")
        assert list_analyses is not None
        assert len(list_analyses) > 0
        for row_analysis in list_analyses:
            map_edge_bindings = row_analysis.get('edge_bindings')
            assert map_edge_bindings is not None
            assert len(map_edge_bindings) > 0
            for key, value in map_edge_bindings.items():
                assert type(value) == list

