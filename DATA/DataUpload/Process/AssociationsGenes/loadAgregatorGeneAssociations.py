
# imports
import requests
import pymysql as mdb
from datetime import datetime
import os

# constants
url_query_aggregator = "https://bioindex-dev.hugeamp.org/api/bio/query"
# p_value_limit = 0.0025
p_value_limit = 0.05
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA = 'tran_upkeep'
DB_TRANSLATOR_SCHEMA = "tran_test_202211"

def get_gene_list(conn):
    ''' 
    will return all the gene codes that are in the translator DB 
    '''
    result = []
    sql_string = "select node_code, ontology_id from {}.comb_node_ontology where node_type_id = 2".format(DB_TRANSLATOR_SCHEMA)

    # query the db
    cursor = conn.cursor()
    cursor.execute(sql_string)
    db_results = cursor.fetchall()

    # check
    if len(db_results) > 0:
        result = True

    # get the data
    if db_results:
        result = [[item[0], item[1]] for item in db_results]

    # return
    return result

def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA)

    # return
    return conn 

def print_num_phenotypes_in_db(conn):
    ''' 
    will query and print the count of phenotypes in the db 
    '''
    # initialize
    sql = """
    select count(*) from comb_node_ontology where node_type_id in (1, 3, 12)
    """
    cursor = conn.cursor()
    count = 0

    # call the query
    cursor.execute(sql)
    db_results = cursor.fetchall()

    # get the data
    if db_results:
        count = db_results[0][0]

    # print
    print("the are {} phenotypes/diseases in the translator db".format(count))


def print_num_phenotypes_for_gene_in_db(conn, gene, gene_id):
    ''' 
    will query and print the count of phenotypes for the gene in the translator db 
    '''
    # initialize
    sql = """
    select count(id) from {}.comb_edge_node where source_node_id = %s and study_id = 1
    """.format(DB_TRANSLATOR_SCHEMA)
    cursor = conn.cursor()
    count = 0

    # call the query
    cursor.execute(sql, (gene_id))
    db_results = cursor.fetchall()

    # get the data
    if db_results:
        count = db_results[0][0]

    # print
    print("for gene {} the are {} phenotypes/diseases in the translator db".format(gene, count))


def query_gene_assocations_service(input_gene, url):
    ''' 
    queries the service for disease/chem relationships 
    '''
    # build the query
    query_string = """
    query {
        GeneAssociations(gene: "%s") {
            phenotype, gene, pValue, zStat, type
        }
    }
    """ % (input_gene)

    # query the service
    response = requests.post(url, data=query_string).json()

    # return
    return response


def get_phenotype_values(input_json):
    ''' 
    will parse the graphql output and generate phenotype/pValue tupes list 
    '''
    query_key = 'GeneAssociations'
    data = input_json.get('data').get(query_key)
    result = []

    # loop
    if data is not None:
        # result = [(item.get('gene'), item.get('phenotype'), item.get('pValue')) for item in data]
        # result = [{'gene'; item.get('gene'), 'phenotype': item.get('phenotype'), 'pValue': item.get('pValue')} for item in data if item.get('pValue') <  p_value_limit]
        result = data

    # rerurn
    return result


def delete_gene_associations(conn):
    ''' 
    delete the gene/phenotype associations from the agregator load table
    '''
    sql_delete = """delete from {}.agg_gene_phenotype 
        """.format(DB_SCHEMA)

    # delete the data
    cur = conn.cursor()
    cur.execute(sql_delete)

    # commit
    conn.commit()


def insert_gene_associations(conn, list_gene_assoc, log=False):
    ''' 
    add gene/phenotype associations from the agregator results
    '''
    sql_insert = """
        insert into {}.agg_gene_phenotype (gene_code, phenotype_code, gene_type, z_stat, p_value)
            values (%s, %s, %s, %s, %s) 
        """.format(DB_SCHEMA)

    cur = conn.cursor()

    i = 0
    # loop through rows
    for gene_association in list_gene_assoc:
        phenotype = gene_association.get('phenotype')
        gene = gene_association.get('gene')
        pValue = gene_association.get('pValue')
        zStat = gene_association.get('zStat')
        geneType = gene_association.get('type')

        # log
        i += 1
        if log:
            if i % 200 == 0:
                print("gene: {}, phenotype: {}, pValue: {}".format(gene, phenotype, pValue))

        cur.execute(sql_insert, (gene, phenotype, geneType, zStat, pValue))

    # commit
    conn.commit()


# def insert_all_gene_aggregator_data(conn, map_phenotype,  log=False):
#     ''' 
#     will query the aggregator for all disease/phentype gene magma association data for all genes in the translator DB 
#     '''

#     # initialize
#     cursor = conn.cursor()

#     # sql to get all the genes in the translator DB
#     sql_select = "select id, node_code from comb_node_ontology where node_type_id = 2 order by node_code"
#     count = 0

#     # get the list of genes
#     cursor.execute(sql_select)
#     db_results = cursor.fetchall()

#     # loop for each gene
#     for item in db_results:
#         gene_id = item[0]
#         gene = item[1]
#         count += 1

#         # get the aggregator data
#         result_json = query_gene_assocations_service(gene, url_query_aggregator)
#         phenotype_list = get_phenotype_values(result_json, p_value_limit)

#         # log
#         if log:
#             print("\n{} - {}".format(count, len(db_results)))
#             print_num_phenotypes_for_gene_in_db(conn, gene, gene_id)
#             print("for {} got new gene associations of size {}".format(gene, len(phenotype_list)))

#         # insert into the db
#         # insert_or_update_gene_data(conn, phenotype_list, gene, gene_id, map_phenotype, log=True)
#         insert_or_update_gene_data(conn, phenotype_list, gene, gene_id, map_phenotype, log=True)

#         # log
#         if log:
#             print_num_phenotypes_for_gene_in_db(conn, gene, gene_id)

# def build_phenotype_map(conn, log=False):
#     ''' will query the aggregator for all disease/phentype gene magma association data for all genes in the translator DB '''
#     cursor = conn.cursor()
#     sql_select = "select id, node_code from comb_node_ontology where node_type_id in (1, 3, 12) order by node_code"
#     map_phenotype = {}

#     # get the list of genes
#     cursor.execute(sql_select)
#     db_results = cursor.fetchall()

#     # loop for each gene
#     for item in db_results:
#         map_phenotype[item[1]] = item[0]

#     # log
#     if log:
#         print("got phenotype map size of {}".format(len(map_phenotype)))

#     # return
#     return map_phenotype

def log_gene_associations_data_counts(conn):
    '''
    method to print out the number of gene/phenotype associations
    '''
    sql_count = "select count(id) from {}.{}"

    # log the number
    cursor = conn.cursor()
    sql_to_run = sql_count.format(DB_SCHEMA, "agg_gene_phenotype")
    cursor.execute(sql_to_run)
    results = cursor.fetchall()

    for row in results:
        print("for: {} got row count: {}".format("gene/phenotype", row[0]))
    # print("for: {} got row count: {}".format(key, results))


if __name__ == "__main__":
    # get the db connection
    conn = get_connection()
    count_gene = 0

    # log
    log_gene_associations_data_counts(conn)

    # delete the existing data
    print("deleting table tran_upkeep.agg_gene_phenotype")
    delete_gene_associations(conn)

    # get the genes
    list_gene = get_gene_list(conn)

    # log
    print("got gene list of size {}".format(len(list_gene)))
    
    # test the check_phenotype method
    assert (len(list_gene) > 19000) == True

    # test gene list
    # list_gene = [['PPARG'], [12618]]

    # log
    print_num_phenotypes_for_gene_in_db(conn, list_gene[0][0], list_gene[1][0])

    # get the phenotypes pvalues for the gene from the bioindex
    for gene in list_gene:
        count_gene = count_gene + 1
        result_json = query_gene_assocations_service(gene[0], url_query_aggregator)
        phenotype_list = get_phenotype_values(result_json)
        print("for {} - {} got new gene associations of size {}".format(count_gene, gene[0], len(phenotype_list)))
    
        # insert the data
        insert_gene_associations(conn, phenotype_list)

    # log
    log_gene_associations_data_counts(conn)


