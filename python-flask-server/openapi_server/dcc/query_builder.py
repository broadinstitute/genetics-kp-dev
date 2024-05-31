
# import relative libraries
# dir_code = "/home/javaprog/Code/"
# from logging import debug
# import sys
# sys.path.insert(0, dir_code + 'TranslatorWorkspace/GeneticsPro/python-flask-server/')

# imports
import openapi_server.dcc.utils as dcc_utils
from openapi_server.dcc.genetics_model import GeneticsModel
import openapi_server.dcc.biolink_utils as bio_utils

from openapi_server.dcc.utils import translate_type, get_curie_synonyms, get_logger, build_pubmed_ids
import os

# get logger
logger = get_logger(__name__)

# constants
limit_db_results = 200
DB_RESULTS_LIMIT = os.environ.get('DB_RESULTS_LIMIT')
if DB_RESULTS_LIMIT:
    limit_db_results = DB_RESULTS_LIMIT
logger.info("using DB results limit of: {}".format(limit_db_results))


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
    ''' 
    will return query/parameter objects based on the query provided 
    '''
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
        # OLD - pre ordering by score_translator
        # get all the p_values, sorted best first
        # sql_object = get_node_edge_score(item, score_type=dcc_utils.attribute_pvalue, return_ascending=True)
        # if sql_object is not None:
        #     sql_list.append(sql_object)

        # # get all the probabilities, sorted best first
        # sql_object = get_node_edge_score(item, score_type=dcc_utils.attribute_probability, return_ascending=False)
        # if sql_object is not None:
        #     sql_list.append(sql_object)

        # # get all the clinvar/clingen data, sorted best first
        # sql_object = get_node_edge_score(item, score_type=dcc_utils.attribute_classification, return_ascending=False)
        # if sql_object is not None:
        #     sql_list.append(sql_object)

        sql_object = get_node_edge_score(item, score_type=dcc_utils.attribute_score_translator, return_ascending=True)
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

def build_qualifier_sql():
    '''
    returns the sql to get qualifers for an edge
    '''
    sql_select = """
    select qa.qualifier_type, qa.qualifier_value 
    from comb_qualifier qa, comb_edge_qualifier link 
    where qa.id = link.qualifier_id 
    and link.edge_id = %s
    order by qa.id;
    """

    # return
    return sql_select


def get_node_edge_score(web_query_object, score_type=dcc_utils.attribute_pvalue, return_ascending=True, limit=limit_db_results):
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

    # OLD - pre query ordered by score_translator
    # sql_string = "select concat(ed.edge_id, so.ontology_id, ta.ontology_id), so.ontology_id, ta.ontology_id, ed.score, sco_type.type_name, \
    #         so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name, ed.study_id, ed.publication_ids, ed.score_translator \
    #     from comb_edge_node ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type \
    #     where ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id \
    #     and ed.score_type_id = sco_type.type_id and ed.source_node_id = so.id and ed.target_node_id = ta.id "

    if score_type == dcc_utils.attribute_score_translator:
        sql_string = "select concat(ed.edge_id, so.ontology_id, ta.ontology_id), so.ontology_id, ta.ontology_id, ed.score, sco_type.type_name, \
                so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name, ed.study_id, ed.publication_ids, ed.score_translator, ed.id \
            from comb_edge_node ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta, comb_lookup_type sco_type \
            where ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id \
            and ed.score_type_id = sco_type.type_id and ed.source_node_id = so.id and ed.target_node_id = ta.id "

    # replace sql string if using classification; substitute ed.score_text for ed.score
    if score_type == dcc_utils.attribute_classification:
        sql_string = "select concat(ed.edge_id, so.ontology_id, ta.ontology_id), so.ontology_id, ta.ontology_id, ed.score_text, sco_type.type_name, \
                so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name, ed.study_id, ed.publication_ids, ed.score_translator, ed.id \
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

    # OLD - pre ordering by translator score
    # # add in score type if given
    # if score_type is not None:
    #     sql_string = add_in_equals(sql_string, "sco_type.type_name", False)
    #     param_list.append(score_type)

    # # add in score lower bound if score type is p_value 
    # if score_type is not None:
    #     if score_type == dcc_utils.attribute_pvalue:
    #         sql_string = add_in_less_than(sql_string, "ed.score", False)
    #         param_list.append(0.0000025)
    #         # TODO - use for testing
    #         # param_list.append(0.0025)

    # # add in score lower bound if score type is p_value 
    # if score_type is not None:
    #     if score_type == dcc_utils.attribute_probability:
    #         sql_string = add_in_more_than_equals(sql_string, "ed.score", False)
    #         param_list.append(0.15)

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

    # OLD - pre ordering by translator score
    # add order by at end
    # if return_ascending:
    #     sql_string = sql_string + " order by ed.score"
    # else:
    #     sql_string = sql_string + " order by ed.score"
    sql_string = sql_string + " order by ed.score_translator desc"

    # add limit
    if limit:
        sql_string = sql_string + " limit " + str(limit)

    # build the query object and return
    sql_object = DbQueryObject(sql_string, param_list)
    return sql_object


def build_creative_query(web_query_object, log=False):
    '''
    builds the creative drug-treats-disease query
    '''
    # initialize
    param_list = []
    # sql_string = '''
    #     select concat(path_disease.id, '_', gene_disease.id, '_', drug_gene.id, '_', pathway_gene.id) as result_id,
    #         pathway.ontology_id as pathway, pathway.node_name as pathway_name, 
    #         gene.ontology_id as gene, gene.node_name as gene_name,
    #         disease.ontology_id as disease, disease.node_name as disease_name,
    #         path_disease.score as pathway_score, gene_disease.score as gene_score, 
    #         drug_gene.drug_ontology_id as drug, drug_gene.drug_name, drug_gene.drug_category_biolink_id as drug_category,
    #         drug_gene.predicate_biolink_id as gene_drug_predicate,
    #         drug_gene.id as drug_gene_row_id, gene_disease.id as gene_disease_row_id, 
    #         pathway_gene.id as path_gene_row_id, path_disease.id as path_disease_row_id
    #     from comb_edge_node path_disease, comb_edge_node gene_disease, 
    #     comb_node_ontology pathway, comb_node_ontology gene,
    #     comb_node_ontology disease,
    #     comb_pathway_gene pathway_gene,
    #     infe_drug_gene drug_gene
    #     where path_disease.source_node_id = pathway.id and path_disease.target_node_id = disease.id 
    #     and gene_disease.source_node_id = gene.id and gene_disease.target_node_id = disease.id
    #     and pathway.node_type_id = 4 and gene.node_type_id = 2 and disease.node_type_id = 1
    #     and path_disease.score < 0.005 and gene_disease.score < 0.000006
    #     and pathway_gene.gene_node_id = gene.id and pathway_gene.pathway_node_id = pathway.id
    #     and gene.ontology_id = drug_gene.gene_ontology_id
    #     order by path_disease.score, gene_disease.score
    #     '''

    sql_string = '''
select concat(path_disease.id, '_', gene_disease.id, '_', drug_gene.id, '_', pathway_gene.id) as result_id,
    pathway.ontology_id as pathway, pathway.node_name as pathway_name, 
    gene.ontology_id as gene, gene.node_name as gene_name,
    disease.ontology_id as disease, disease.node_name as disease_name,
    path_disease.score as pathway_score, gene_disease.score as gene_score, 
    drug_gene.drug_ontology_id as drug, drug_gene.drug_name, drug_gene.drug_category_biolink_id as drug_category,
    drug_gene.predicate_biolink_id as gene_drug_predicate,
    drug_gene.id as drug_gene_row_id, gene_disease.id as gene_disease_row_id, 
    pathway_gene.id as path_gene_row_id, path_disease.id as path_disease_row_id
from comb_edge_node path_disease, comb_edge_node gene_disease, 
    comb_node_ontology pathway, comb_node_ontology gene,
    comb_node_ontology disease,
    comb_pathway_gene pathway_gene,
    infe_drug_gene drug_gene
where path_disease.source_node_id = pathway.id and path_disease.target_node_id = disease.id 
    and gene_disease.source_node_id = gene.id and gene_disease.target_node_id = disease.id
    and pathway.node_type_id = 4 and gene.node_type_id = 2 and disease.node_type_id = 1
    and path_disease.score < 0.0005 and (gene_disease.score < 0.000006 or gene_disease.score_translator > 0.7)
    and pathway_gene.gene_node_id = gene.id and pathway_gene.pathway_node_id = pathway.id
    and gene.ontology_id = drug_gene.gene_ontology_id
    '''
    # and path_disease.score < 0.0005 and gene_disease.score < 0.000006 and gene_disease.study_id = 1 
    # and path_disease.score < 0.005 and (gene_disease.score < 0.000006 or gene_disease.score_translator > 0.1)

    # ADDED BACK IN
    # and gene.ontology_id = drug_gene.gene_ontology_id
    # and path_disease.score < 0.0005 and (gene_disease.score < 0.000006 or gene_disease.score_translator > 0.7)
    # and pathway.node_type_id = 4 and gene.node_type_id = 2 and disease.node_type_id = 1

    # new trapi 1.4 query with new pvalue/beta direction of effect


    if web_query_object.get_list_source_id():
        list_input = web_query_object.get_list_source_id()
        sql_string = add_in_in(sql=sql_string, term="gene.ontology_id", list_input=list_input, is_first=False)
        param_list += list_input

    if web_query_object.get_list_target_id():
        list_input = web_query_object.get_list_target_id()
        sql_string = add_in_in(sql=sql_string, term="disease.ontology_id", list_input=list_input, is_first=False)
        param_list += list_input

    sql_string = sql_string + ' order by path_disease.score, gene_disease.score '

    sql_string = sql_string + " limit " + str(500)

    # log
    if log:
        logger.info("CREATIVE sql: {}".format(sql_string))
        logger.info("with params: {}".format(param_list))

    # return
    # build the query object and return
    sql_object = DbQueryObject(sql_string, param_list)
    return [sql_object]

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
