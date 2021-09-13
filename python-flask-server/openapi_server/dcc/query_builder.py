
# import relative libraries
dir_code = "/home/javaprog/Code/"
from logging import debug
import sys
sys.path.insert(0, dir_code + 'TranslatorWorkspace/GeneticsPro/python-flask-server/')

# imports
import openapi_server.dcc.utils as dcc_utils
from openapi_server.dcc.genetics_model import GeneticsModel
import openapi_server.dcc.biolink_utils as bio_utils


class DbQueryObject():
    ''' class to contain sql string and parameter map for a query '''
    def __init__(self, sql_string, param_list):
        self.sql_string = sql_string
        self.param_list = param_list
    
    def __str__(self):
        return "query object with sql type: {}, sql: {}, parameters: {}".format(type(self.sql_string), self.sql_string, self.param_list)

    __repr__ = __str__

def expand_queries(web_query_object, debug=False):
    ''' will take a query object and expand it according to all possible queries supported '''
    # initialize
    object_list = []

    # get all the possible supported combinations
    query_list = bio_utils.get_overlap_queries_for_parts(web_query_object.get_source_types(), web_query_object.get_target_types(), web_query_object.get_edge_types(), debug)

    # loop
    for item in query_list:
        # split
        subject_type, predicate, object_type = item.split()

        # add new query
        # object_list.append(GeneticsModel(edge={"predicate": predicate},
        #         target={"category": object_type, "id": web_query_object.target.get('id')},
        #         source={"category": subject_type, "id": web_query_object.source.get('id')},
        #         source_normalized_id=web_query_object.get_source_normalized_id(),
        #         target_normalized_id=web_query_object.get_target_normalized_id()))

        # BUG? - not using split elements
        # object_list.append(GeneticsModel(edge=web_query_object.get_edge,
        #         source=web_query_object.get_source(),
        #         target=web_query_object.get_target(),
        #         source_id=web_query_object.get_source_id(),
        #         target_id=web_query_object.get_target_id(),
        #         edge_type=web_query_object.get_edge_type(),
        #         source_type=web_query_object.get_source_type(),
        #         target_type=web_query_object.get_target_type(),
        #         source_normalized_id=web_query_object.get_source_normalized_id(),
        #         target_normalized_id=web_query_object.get_target_normalized_id()))

        object_list.append(GeneticsModel(edge=web_query_object.get_edge,
                source=web_query_object.get_source(),
                target=web_query_object.get_target(),
                list_source_id=web_query_object.get_list_source_id(),
                list_target_id=web_query_object.get_list_target_id(),
                edge_type=predicate,
                source_type=subject_type,
                target_type=object_type,
                map_source_normalized_id=web_query_object.get_map_source_normalized_id(),
                map_target_normalized_id=web_query_object.get_map_target_normalized_id()))

    # return
    return object_list

def get_queries(web_query_object):
    ''' will return query/parameter objects based on the query provided '''
    # initialize
    sql_list = []
    sql_object = None

    # go through query calls and if get object returned, add to list
    # sql_object = get_magma_gene_phenotype_query(web_query_object)
    # if sql_object is not None:
    #     sql_list.append(sql_object)
    # sql_object = get_magma_phenotype_gene_query(web_query_object)
    # if sql_object is not None:
    #     sql_list.append(sql_object)

    # TODO - add in code to split one query into possible multiple ones
    # for more generalized queries
    query_list = expand_queries(web_query_object, True)

    # loop through the queries and get the sql to run
    for item in query_list:
        # get all the p_values, sorted best first
        sql_object = get_node_edge_score(item, score_type=dcc_utils.attribute_pvalue, return_ascending=True)
        if sql_object is not None:
            sql_list.append(sql_object)

        # get all the probabilities, sorted best first
        sql_object = get_node_edge_score(item, score_type=dcc_utils.attribute_probability, return_ascending=False)
        if sql_object is not None:
            sql_list.append(sql_object)

        # get all the clinvar/clingen data, sorted best first
        sql_object = get_node_edge_score(item, score_type=dcc_utils.attribute_classification, return_ascending=False)
        if sql_object is not None:
            sql_list.append(sql_object)

    # return the list
    return sql_list

def add_in_equals(sql, term, is_first=True):
    ''' add in and clause to the sql '''
    temp = str(sql)

    # add in where if necessary
    if is_first:
        temp = temp + " where " 
    else:
        temp = temp + " and "

    # add in the condition
    temp = temp + str(term) + " = %s "

    # return
    return temp

def add_in_in(sql, term, list_input, is_first=True):
    ''' add in and clause to the sql '''
    temp = str(sql)

    # add in where if necessary
    if is_first:
        temp = temp + " where " 
    else:
        temp = temp + " and "

    # build the in sql
    in_sql = ", ".join(list(map(lambda item: '%s', list_input)))

    # add in the condition
    temp = temp + str(term) + " in ({}) ".format(in_sql)

    # return
    return temp

def add_in_less_than(sql, term, is_first=True):
    ''' add in less than clause to the sql '''
    temp = str(sql)

    # add in where if necessary
    if is_first:
        temp = temp + " where " 
    else:
        temp = temp + " and "

    # add in the condition
    temp = temp + str(term) + " < %s "

    # return
    return temp

def add_in_more_than(sql, term, is_first=True):
    ''' add in less than clause to the sql '''
    temp = str(sql)

    # add in where if necessary
    if is_first:
        temp = temp + " where " 
    else:
        temp = temp + " and "

    # add in the condition
    temp = temp + str(term) + " > %s "

    # return
    return temp

def add_in_more_than_equals(sql, term, is_first=True):
    ''' add in less than clause to the sql '''
    temp = str(sql)

    # add in where if necessary
    if is_first:
        temp = temp + " where " 
    else:
        temp = temp + " and "

    # add in the condition
    temp = temp + str(term) + " >= %s "

    # return
    return temp

# def get_magma_gene_phenotype_query(web_query_object):
#     ''' takes in GeneticsModel and returns a DbQueryObject object if applicable, None otherwise '''
#     # initialize sql string
#     sql_string = None
#     param_list = []

#     # test the gene to disease tuple
#     if web_query_object.get_edge_type() == dcc_utils.edge_gene_disease and web_query_object.get_source_type() == dcc_utils.node_gene:
#         sql_string = "select concat('magma_gene_', mg.id) as id, mg.ncbi_id, mg.phenotype_ontology_id, mg.p_value, mg.gene, mg.phenotype, \
#             '" + dcc_utils.edge_gene_disease + "', '" + dcc_utils.node_gene + "', mg.biolink_category  \
#             from magma_gene_phenotype mg where mg.p_value < 0.025 "
#     else:
#         return None

#     # add in target type if given
#     if web_query_object.get_target_type() is not None:
#         sql_string = add_in_equals(sql_string, "mg.biolink_category", False)
#         param_list.append(web_query_object.get_target_type())

#     # add in source id if given
#     if web_query_object.get_source_id() is not None:
#         sql_string = add_in_equals(sql_string, "mg.ncbi_id", False)
#         param_list.append(web_query_object.get_source_id())

#     # add in target id if given
#     if web_query_object.get_target_id() is not None:
#         sql_string = add_in_equals(sql_string, "mg.phenotype_ontology_id", False)
#         param_list.append(web_query_object.get_target_id())

#     # add order by at end
#     sql_string = sql_string + " ORDER by mg.p_value ASC"

#     # build the query object and return
#     sql_object = DbQueryObject(sql_string, param_list)
#     return sql_object

# def get_magma_phenotype_gene_query(web_query_object):
#     ''' takes in GeneticsModel and returns a DbQueryObject object if applicable, None otherwise '''
#     # initialize sql string
#     sql_string = None
#     param_list = []

#     if web_query_object.get_edge_type() == dcc_utils.edge_disease_gene and web_query_object.get_target_type() == dcc_utils.node_gene:
#         sql_string = "select concat('magma_gene_', mg.id) as id, mg.phenotype_ontology_id, mg.ncbi_id, mg.p_value, mg.phenotype, mg.gene, \
#             '" + dcc_utils.edge_disease_gene + "', mg.biolink_category, '" + dcc_utils.node_gene + "'  \
#             from magma_gene_phenotype mg where mg.p_value < 0.025 "

#     else:
#         return None

#     # add in source type if given
#     if web_query_object.get_source_type() is not None:
#         sql_string = add_in_equals(sql_string, "mg.biolink_category", False)
#         param_list.append(web_query_object.get_source_type())

#     # add in target id if given
#     if web_query_object.get_target_id() is not None:
#         sql_string = add_in_equals(sql_string, "mg.ncbi_id", False)
#         param_list.append(web_query_object.get_target_id())

#     # add in source id if given
#     if web_query_object.get_source_id() is not None:
#         sql_string = add_in_equals(sql_string, "mg.phenotype_ontology_id", False)
#         param_list.append(web_query_object.get_source_id())
        
#     # add order by at end
#     sql_string = sql_string + " ORDER by mg.p_value ASC"

#     # build the query object and returnget_magma_gene_query


def get_node_edge_score(web_query_object, score_type=dcc_utils.attribute_pvalue, return_ascending=True, limit=1000):
    ''' takes in GeneticsModel and returns a DbQueryObject object if applicable, None otherwise '''
    # initialize sql string
    sql_string = None
    param_list = []

    # the data return order is:
    # edge_id
    # source ontology code
    # target ontology code
    # score
    # score_type
    # source name
    # target name
    # edge type
    # source type
    # target type
    # sql_string = "select concat(ed.edge_id, so.ontology_id, ta.ontology_id), so.ontology_id, ta.ontology_id, ed.score, sco_type.type_name, so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name \
    #     from comb_node_edge ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type \
    #     where ed.source_code = so.node_code and ed.target_code = ta.node_code and ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id \
    #     and ed.score_type_id = sco_type.type_id and ed.source_type_id = so.node_type_id and ed.target_type_id = ta.node_type_id "

    # # replace sql string if using classification
    # if score_type == dcc_utils.attribute_classification:
    #     sql_string = "select concat(ed.edge_id, so.ontology_id, ta.ontology_id), so.ontology_id, ta.ontology_id, ed.score_text, sco_type.type_name, so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name \
    #         from comb_node_edge ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type \
    #         where ed.source_code = so.node_code and ed.target_code = ta.node_code and ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id \
    #         and ed.score_type_id = sco_type.type_id and ed.source_type_id = so.node_type_id and ed.target_type_id = ta.node_type_id "

    sql_string = "select concat(ed.edge_id, so.ontology_id, ta.ontology_id), so.ontology_id, ta.ontology_id, ed.score, sco_type.type_name, \
            so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name, ed.study_id, ed.publication_ids, ed.score_translator \
        from comb_edge_node ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type \
        where ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id \
        and ed.score_type_id = sco_type.type_id and ed.source_node_id = so.id and ed.target_node_id = ta.id "

    # replace sql string if using classification; substitute ed.score_text for ed.score
    if score_type == dcc_utils.attribute_classification:
        sql_string = "select concat(ed.edge_id, so.ontology_id, ta.ontology_id), so.ontology_id, ta.ontology_id, ed.score_text, sco_type.type_name, \
                so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name, ed.study_id, ed.publication_ids, ed.score_translator \
            from comb_edge_node ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type \
            where ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id \
            and ed.score_type_id = sco_type.type_id and ed.source_node_id = so.id and ed.target_node_id = ta.id "

    # if web_query_object.get_edge_type() == dcc_utils.edge_disease_gene and web_query_object.get_target_type() == dcc_utils.node_gene:
    #     sql_string = "select concat('magma_gene_', mg.id) as id, mg.phenotype_ontology_id, mg.ncbi_id, mg.p_value, mg.phenotype, mg.gene, \
    #         '" + dcc_utils.edge_disease_gene + "', mg.biolink_category, '" + dcc_utils.node_gene + "'  \
    #         from magma_gene_phenotype mg where mg.p_value < 0.025 "

    # else:
    #     return None

    # make sure if edge predicate provided, that it is accepted one
    if web_query_object.get_edge_type() is not None:
        if web_query_object.get_edge_type() not in dcc_utils.accepted_edge_types:
            return None

    # add in edge type if given
    if web_query_object.get_edge_type() is not None:
        sql_string = add_in_equals(sql_string, "ted.type_name", False)
        param_list.append(web_query_object.get_edge_type())

    # add in source type if given
    if web_query_object.get_source_type() is not None:
        sql_string = add_in_equals(sql_string, "tso.type_name", False)
        param_list.append(web_query_object.get_source_type())

    # add in target type if given
    if web_query_object.get_target_type() is not None:
        sql_string = add_in_equals(sql_string, "tta.type_name", False)
        param_list.append(web_query_object.get_target_type())

    # add in score type if given
    if score_type is not None:
        sql_string = add_in_equals(sql_string, "sco_type.type_name", False)
        param_list.append(score_type)

    # add in score lower bound if score type is p_value 
    if score_type is not None:
        if score_type == dcc_utils.attribute_pvalue:
            sql_string = add_in_less_than(sql_string, "ed.score", False)
            param_list.append(0.0000025)
            # TODO - use for testing
            # param_list.append(0.0025)

    # add in score lower bound if score type is p_value 
    if score_type is not None:
        if score_type == dcc_utils.attribute_probability:
            sql_string = add_in_more_than_equals(sql_string, "ed.score", False)
            param_list.append(0.15)

    # add in source id if given
    # if web_query_object.get_source_id() is not None:
    #     sql_string = add_in_equals(sql_string, "so.ontology_id", False)
    #     param_list.append(web_query_object.get_source_id())
    # print("=====================================for normalized id {}".format(web_query_object.get_source_normalized_id()))
    # if web_query_object.get_source_normalized_id() is not None:
    #     sql_string = add_in_equals(sql_string, "so.ontology_id", False)
    #     param_list.append(web_query_object.get_source_normalized_id())
    if web_query_object.get_list_source_id():
        list_input = web_query_object.get_list_source_id()
        sql_string = add_in_in(sql=sql_string, term="so.ontology_id", list_input=list_input, is_first=False)
        param_list += list_input
        
    # add in target id if given
    # if web_query_object.get_target_id() is not None:
    #     sql_string = add_in_equals(sql_string, "ta.ontology_id", False)
    #     param_list.append(web_query_object.get_target_id())
    # if web_query_object.get_target_normalized_id() is not None:
    #     sql_string = add_in_equals(sql_string, "ta.ontology_id", False)
    #     param_list.append(web_query_object.get_target_normalized_id())
    if web_query_object.get_list_target_id():
        list_input = web_query_object.get_list_target_id()
        sql_string = add_in_in(sql=sql_string, term="ta.ontology_id", list_input=list_input, is_first=False)
        param_list += list_input

    # add order by at end
    if return_ascending:
        sql_string = sql_string + " order by ed.score"
    else:
        sql_string = sql_string + " order by ed.score"

    # add limit
    if limit:
        sql_string = sql_string + " limit " + str(limit)

    # build the query object and return
    sql_object = DbQueryObject(sql_string, param_list)
    return sql_object


if __name__ == "__main__":
    # build the test object
    web_test = GeneticsModel(edge={"predicate": dcc_utils.edge_gene_disease},
                source={"category": dcc_utils.node_gene, "id": "gene_dude"},
                target={"category": dcc_utils.node_disease,"id": "not_good"})

    # get the sql object
    sql_object = get_magma_phenotype_gene_query(web_test)
    print("got object: {}\n".format(sql_object))

    # build the test object
    web_test = GeneticsModel(edge={"predicate": dcc_utils.edge_gene_disease},
                source={"category": dcc_utils.node_gene},
                target={"category": dcc_utils.node_disease,"id": "not_good"})

    # get the sql object
    sql_object = get_magma_phenotype_gene_query(web_test)
    print("got object: {}\n".format(sql_object))

    # build the test object
    web_test = GeneticsModel(edge={"predicate": dcc_utils.edge_gene_disease},
                source={"category": dcc_utils.node_gene},
                target={"category": dcc_utils.node_disease})

    # get the sql object
    sql_object = get_magma_phenotype_gene_query(web_test)
    print("got object: {}\n".format(sql_object))

    # build the test object
    web_test = GeneticsModel(edge={"predicate": dcc_utils.edge_disease_gene},
                target={"category": dcc_utils.node_gene, "id": "gene_dude"},
                source={"category": dcc_utils.node_disease,"id": "not_good"})

    # get the sql object
    sql_object = get_magma_phenotype_gene_query(web_test)
    print("got object: {}\n".format(sql_object))

    # build the test object
    web_test = GeneticsModel(edge={"predicate": dcc_utils.edge_disease_gene},
                target={"category": dcc_utils.node_gene, "id": "gene_dude"},
                source={"category": dcc_utils.node_disease,"id": "not_good"})

    # get the sql object
    sql_object = get_queries(web_test)
    print("got object: {}\n".format(sql_object))

    # test biolink ancestry conversion
    print("testing biolink query expansion")
    web_test = GeneticsModel(edge={"predicate": "biolink:related_to"},
                target={"category": dcc_utils.node_gene, "id": "gene_dude"},
                source={"category": dcc_utils.node_disease,"id": "not_good"})
    query_list = expand_queries(web_test, True)
    print("for test query: {}".format(web_test))
    for item in query_list:
        print("got expanded query: {}".format(item))
    web_test = GeneticsModel(edge={"predicate": "biolink:related_to"},
                target={"id": "gene_dude"},
                source={"category": dcc_utils.node_disease,"id": "not_good"})
    query_list = expand_queries(web_test, True)
    print("for test query: {}".format(web_test))
    for item in query_list:
        print("got expanded query: {}".format(item))
    print()
