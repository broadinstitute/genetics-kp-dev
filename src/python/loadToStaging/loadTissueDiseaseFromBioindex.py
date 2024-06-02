


# imports
import requests
import pymysql as mdb
from datetime import datetime
import os

# constants
URL_QUERY_AGGREGATOR = "https://bioindex-dev.hugeamp.org/api/bio/query/partitioned-heritability?q={}"
p_value_limit = 0.0001
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA = 'tran_upkeep'
DB_TABLE = "agg_tissue_phenotype"

# sql
SQL_INSERT_TISSUE_PHENOTYPE = """
insert into agg_tissue_phenotype (phenotype, ancestry, annotation, tissue, expectedSNPs, SNPs, enrichment, pValue)
values(%s, %s, %s, %s, %s, %s, %s, %s)
"""


# methods
def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA)

    # return
    return conn 


def get_phenotype_list(conn):
    ''' 
    will return all the gene codes that are in the translator DB 
    '''
    list_result = []
    sql_string = "select phenotype_id from agg_aggregator_phenotype"

    # query the db
    cursor = conn.cursor()
    cursor.execute(sql_string)
    db_results = cursor.fetchall()

    # get the data
    if db_results:
        list_result = [item[0] for item in db_results]

    # return
    return list_result


def db_load_tissue_phenotypes(conn, list_data):
    ''' 
    add tissue/phenotype data to mysql table 
    '''
    sql = SQL_INSERT_TISSUE_PHENOTYPE
    cur = conn.cursor()
    i = 0

    # loop through rows
    for item in list_data:
        i += 1
        if i % 20 == 0:
            print("tissue: {}, phenotype: {}, enrichment: {}".format(item.get('tissue'), item.get('phenotype'), item.get('enrichment')))

        cur.execute(sql, (item.get('phenotype'), item.get('ancestry'), item.get('annotation'), item.get('tissue'), item.get('expectedSNPs'), item.get('SNPs'), 
                          item.get('enrichment'), item.get('pValue')))
        
    conn.commit()


def query_tissue_disease_assocations_service(input_phenotype, log=True):
    ''' 
    queries the bioindex service for tissuee/phenotype relationships 
    '''
    # intialize
    list_result = []

    # build the query
    url_query = URL_QUERY_AGGREGATOR.format(input_phenotype)

    # query the service
    response = requests.get(url_query).json()
    list_result = response.get('data')

    # log
    if log:
        print("for phenotype: {} got num results: {}".format(input_phenotype, len(list_result)))

    # return
    return list_result




if __name__ == "__main__":
    # get the db connection
    conn = get_connection()

    # get the inputs
    list_input = get_phenotype_list(conn)

    # log
    print("got input list of size {}".format(len(list_input)))
    
    # test the check_phenotype method
    assert (len(list_input) > 190) == True

    # test gene list
    phenotype_list = ['BMI']

    # loop
    for item in list_input:
        # get the data from the service
        list_data = query_tissue_disease_assocations_service(input_phenotype=item)

        # insert the data into the DB
        db_load_tissue_phenotypes(conn=conn, list_data=list_data)

    # close the db connection
    conn.close()
