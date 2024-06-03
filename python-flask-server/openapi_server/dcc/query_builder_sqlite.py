
# imports
from openapi_server.models.query import Query
from openapi_server.models.q_node import QNode

import openapi_server.dcc.db_utils as dutils
import openapi_server.dcc.trapi_extract as textract

# constants



# methods
def get_basic_sqlite_query(log=False):
    '''
    will return the basic no param sql query
    '''
    # initialize
    sql_string = "select ed.id || ed.edge_id || so.ontology_id || ta.ontology_id, so.ontology_id, ta.ontology_id, ed.score, \
            so.node_name, ta.node_name, ted.type_name, tso.type_name, tta.type_name, ed.study_id, ed.publication_ids, ed.score_translator, ed.id, \
            ed.p_value, ed.beta, ed.standard_error, ed.probability, ed.probability_app_bayes_factor, ed.enrichment, ed.annotation\
        from comb_edge_node ed, comb_node_ontology so, comb_node_ontology ta, comb_lookup_type ted, comb_lookup_type tso, comb_lookup_type tta \
        where ed.edge_type_id = ted.type_id and so.node_type_id = tso.type_id and ta.node_type_id = tta.type_id \
        and ed.source_node_id = so.id and ed.target_node_id = ta.id "

    # return
    return sql_string


def get_sqlite_query(trapi_query: Query, log=True):
    '''
    returns the sql query and parameters to use
    '''
    sql_string = get_basic_sqlite_query()
    node_subject: QNode = None
    node_object: QNode = None 
    list_params = []

    # if there are subject ids
    _, node_subject = textract.get_querygraph_key_node(trapi_query=trapi_query, is_subject=True)
    if node_subject and node_subject.ids and len(node_subject.ids) > 0:
        sql_string = add_in(sql=sql_string, term="so.ontology_id", list_input=node_subject.ids, is_first=False)
        list_params.extend(node_subject.ids)

    # if there are subject category ids
    if node_subject and node_subject.categories and len(node_subject.categories) > 0:
        sql_string = add_in(sql=sql_string, term="tso.type_name", list_input=node_subject.categories, is_first=False)
        list_params.extend(node_subject.categories)

    # if there are object ids
    _, node_object = textract.get_querygraph_key_node(trapi_query=trapi_query, is_subject=False)
    if node_object and node_object.ids and len(node_object.ids) > 0:
        sql_string = add_in(sql=sql_string, term="ta.ontology_id", list_input=node_object.ids, is_first=False)
        list_params.extend(node_object.ids)

    # if there are object category ids
    if node_object and node_object.categories and len(node_object.categories) > 0:
        sql_string = add_in(sql=sql_string, term="tta.type_name", list_input=node_object.categories, is_first=False)
        list_params.extend(node_object.categories)




    # add in the limit
    sql_string = sql_string + " limit 5000"

    # log
    if log:
        print("got query: \n{} \n with params: \n{}".format(sql_string, list_params))

    # return
    return sql_string, list_params





def add_equals(sql, term, is_first=True):
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

def add_in(sql, term, list_input, is_first=True):
    ''' add in and clause to the sql '''
    temp = str(sql)

    # add in where if necessary
    if is_first:
        temp = temp + " where " 
    else:
        temp = temp + " and "

    # build the in sql
    in_sql = ", ".join(list(map(lambda item: '?', list_input)))

    # add in the condition
    temp = temp + str(term) + " in ({}) ".format(in_sql)

    # return
    return temp

def add_less_than(sql, term, is_first=True):
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

def add_more_than(sql, term, is_first=True):
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

def add_more_than_equals(sql, term, is_first=True):
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
