# imports
import utils as dcc_utils
from genetics_model import GeneticsModel


class DbQueryObject():
    ''' class to contain sql string and parameter map for a query '''
    def __init__(self, sql_string, param_list):
        self.sql_string = sql_string
        self.param_list = param_list
    
    def __str__(self):
        return "query object with sql type: {}, sql: {}, paramaters: {}".format(type(self.sql_string), self.sql_string, self.param_list)

    __repr__ = __str__


def get_queries():
    ''' will return query/parameter objects based on the query provided '''
    pass

def add_in_equals(sql, term, is_first=True):
    ''' add in where clause to the sql '''
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

def get_magma_gene_query(web_query_object):
    ''' takes in GeneticsModel and returns a DbQueryObject object if applicable, None otherwise '''
    # initialize sql string
    sql_string = None
    param_list = []

    # test the gene to disease tuple
    if web_query_object.get_edge_type() == dcc_utils.edge_gene_disease and web_query_object.get_source_type() == dcc_utils.node_gene:
        sql_string = "select mg.phenotype_ontology_id, concat('magma_gene_', mg.id) as id, mg.p_value, mg.gene, mg.phenotype, \
            '" + dcc_utils.edge_gene_disease + "', '" + dcc_utils.node_gene + "', mg.biolink_category  \
            from magma_gene_phenotype mg where and mg.p_value < 0.0000025 "


    elif web_query_object.get_edge_type() == dcc_utils.edge_disease_gene and web_query_object.get_target_type() == dcc_utils.node_gene:
        sql_string = "select mg.ncbi_id, concat('magma_gene_', mg.id) as id, mg.p_value, mg.phenotype, mg.gene, \
            '" + dcc_utils.edge_disease_gene + "', mg.biolink_category, '" + dcc_utils.node_gene + "'  \
            from magma_gene_phenotype mg where and mg.p_value < 0.0000025 "

    else:
        return None

    # add in target type if given
    if web_query_object.get_target_type() is not None:
        sql_string = add_in_equals(sql_string, "mg.biolink_category", False)
        param_list.append(web_query_object.get_target_type())

    # add in source id if given
    if web_query_object.get_source_id() is not None:
        sql_string = add_in_equals(sql_string, "mg.ncbi_id", False)
        param_list.append(web_query_object.get_source_id())

    # add in target id if given
    if web_query_object.get_target_id() is not None:
        sql_string = add_in_equals(sql_string, "mg.phenotype_ontology_id", False)
        param_list.append(web_query_object.get_target_id())
    
    # add order by at end
    sql_string = sql_string + " ORDER by mg.p_value ASC"

    # build the query object and return
    sql_object = DbQueryObject(sql_string, param_list)
    return sql_object




if __name__ == "__main__":
    # build the test object
    web_test = GeneticsModel(edge={"predicate": dcc_utils.edge_gene_disease},
                source={"category": dcc_utils.node_gene, "id": "gene_dude"},
                target={"category": dcc_utils.node_disease,"id": "not_good"})

    # get the sql object
    sql_object = get_magma_gene_query(web_test)
    print("got object: {}\n".format(sql_object))

    # build the test object
    web_test = GeneticsModel(edge={"predicate": dcc_utils.edge_gene_disease},
                source={"category": dcc_utils.node_gene},
                target={"category": dcc_utils.node_disease,"id": "not_good"})

    # get the sql object
    sql_object = get_magma_gene_query(web_test)
    print("got object: {}\n".format(sql_object))

    # build the test object
    web_test = GeneticsModel(edge={"predicate": dcc_utils.edge_gene_disease},
                source={"category": dcc_utils.node_gene},
                target={"category": dcc_utils.node_disease})

    # get the sql object
    sql_object = get_magma_gene_query(web_test)
    print("got object: {}\n".format(sql_object))

    # build the test object
    web_test = GeneticsModel(edge={"predicate": dcc_utils.edge_disease_gene},
                target={"category": dcc_utils.node_gene, "id": "gene_dude"},
                source={"category": dcc_utils.node_disease,"id": "not_good"})

    # get the sql object
    sql_object = get_magma_gene_query(web_test)
    print("got object: {}\n".format(sql_object))

