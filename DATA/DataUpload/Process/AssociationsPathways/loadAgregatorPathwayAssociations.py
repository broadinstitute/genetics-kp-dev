
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

def get_phenotype_list(conn):
    ''' 
    will return all the gene codes that are in the translator DB 
    '''
    result = []
    sql_string = """
    select phenotype_id, phenotype_name from {}.agg_aggregator_phenotype order by phenotype_id
    """.format(DB_SCHEMA)

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

def query_pathway_assocations_service(input_gene, url):
    ''' 
    queries the service for disease/chem relationships 
    '''
    # build the query
    query_string = """
    query {
        PathwayAssociations(phenotype: "%s") {
            pathwayName, phenotype, pValue, stdErr, beta, ancestry
        }
    }
    """ % (input_gene)

    # query the service
    response = requests.post(url, data=query_string).json()

    # return
    return response


def get_pathway_values(input_json):
    ''' 
    will parse the graphql output and generate phenotype/pValue tuples list 
    '''
    query_key = 'PathwayAssociations'
    data = input_json.get('data').get(query_key)
    result = []

    # loop
    if data is not None:
        result = data

    # rerurn
    return result


def delete_pathway_associations(conn):
    ''' 
    delete the pathway/phenotype associations from the agregator load table
    '''
    # sql_delete = """delete from {}.agg_pathway_phenotype 
    #     """.format(DB_SCHEMA)
    sql_delete = """truncate table {}.agg_pathway_phenotype2 
        """.format(DB_SCHEMA)

    # delete the data
    cur = conn.cursor()
    cur.execute(sql_delete)

    # commit
    conn.commit()


def insert_pathway_associations(conn, list_pathway_assoc, log=False):
    ''' 
    add pathway/phenotype associations from the agregator results
    '''
    sql_insert = """
        insert into {}.agg_pathway_phenotype2 (pathway_code, phenotype_code, beta, standard_error, p_value)
            values (%s, %s, %s, %s, %s) 
        """.format(DB_SCHEMA)
    # print(sql_insert)

    cur = conn.cursor()

    i = 0
    # loop through rows
    for pathway_association in list_pathway_assoc:
        if pathway_association.get('ancestry') == 'Mixed':
            phenotype = pathway_association.get('phenotype')
            pathway = pathway_association.get('pathwayName')
            pValue = pathway_association.get('pValue')
            stdErr = pathway_association.get('stdErr')
            beta = pathway_association.get('beta')
        else:
            print("ancestry no MIXED")

        # log
        i += 1
        if log:
            if i % 2000 == 0:
                print("pathway: {}, phenotype: {}, pValue: {}".format([pathway], phenotype, pValue))
                conn.commit()

        cur.execute(sql_insert, (pathway, phenotype, beta, stdErr, pValue))

    # commit
    conn.commit()


def log_pathway_associations_data_counts(conn):
    '''
    method to print out the number of gene/phenotype associations
    '''
    sql_count = "select count(id) from {}.{}"

    # log the number
    cursor = conn.cursor()
    sql_to_run = sql_count.format(DB_SCHEMA, "agg_pathway_phenotype2")
    cursor.execute(sql_to_run)
    results = cursor.fetchall()

    for row in results:
        print("for upkeep: {} got row count: {}".format("pathway/phenotype", row[0]))
    # print("for: {} got row count: {}".format(key, results))


# MAIN ###############################
if __name__ == "__main__":
    # get the db connection
    conn = get_connection()
    count_phenotype = 0
    COUNT_BREAK = -1

    # log
    log_pathway_associations_data_counts(conn)

    # delete the existing data
    print("deleting table tran_upkeep.agg_pathway_phenotype")
    delete_pathway_associations(conn)

    # log
    log_pathway_associations_data_counts(conn)

    # get the genes
    list_phenotype = get_phenotype_list(conn)

    # log
    num_phenotypes = len(list_phenotype)
    print("got upkeep phenotype list of size {}".format(num_phenotypes))
    
    # test the check_phenotype method
    assert (num_phenotypes > 190) == True

    # get the phenotypes pvalues for the gene from the bioindex
    for phenotype in list_phenotype:
        count_phenotype = count_phenotype + 1

        # see if need to break
        if COUNT_BREAK > 0 and count_phenotype > COUNT_BREAK:
            break

        # get and insert the data
        result_json = query_pathway_assocations_service(phenotype[0], url_query_aggregator)
        pathway_list = get_pathway_values(result_json)
        print("for {}/{} - {} got new pathway associations of size {}".format(count_phenotype, num_phenotypes, phenotype[0], len(pathway_list)))
    
        # insert the data
        insert_pathway_associations(conn, pathway_list)

    # log
    log_pathway_associations_data_counts(conn)


