


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

SQL_INSERT_TISSUE = """
insert into agg_tissue (tissue_name, ontology_id) values(%s, %s)
"""

SQL_UPDATE_TISSUE = """
update agg_tissue set ontology_id = %s, tran_service_name = %s where tissue_name = %s
"""

# methods
def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA)

    # return
    return conn 


def db_get_phenotype_list(conn):
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


def db_get_distinct_tissue_list_from_staging_table(conn, log=True):
    ''' 
    will return all the tissues from the staging table
    '''
    list_result = []
    sql_string = "select distinct tissue from agg_tissue_phenotype"

    # query the db
    cursor = conn.cursor()
    cursor.execute(sql_string)
    db_results = cursor.fetchall()

    # get the data
    if db_results:
        list_result = [item[0] for item in db_results]

    # log
    if log:
        print("got unique tissue list of size: {}".format(len(list_result)))

    # return
    return list_result


def db_insert_tissues(conn, list_tissue, log=False):
    '''
    will determine if the items in the list are not in the db yet and insert if so
    '''
    list_result = []
    sql_string = "select tissue_name from agg_tissue where tissue_name = %s"

    # query the db
    cursor = conn.cursor()

    # loop
    for item in list_tissue:
        cursor.execute(sql_string, item)
        db_results = cursor.fetchall()

        # get the data
        if db_results and len(db_results) > 0:
            print("tissue: ({}) already in staging table, so skipping".format(item))
            continue
        else:
            print("tissue: ({}) not staging table, so inserting".format(item))
            cursor.execute(SQL_INSERT_TISSUE, (item, None))

    # commit()
    conn.commit()


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


def db_update_tissues(conn, log=True):
    '''
    will query the db for tissue that need ontologies and get them
    '''
    # initialize
    cursor = conn.cursor()
    sql_query = "select tissue_name from agg_tissue where ontology_id is null"

    # get the tissues
    cursor.execute(sql_query)
    db_results = cursor.fetchall()

    # log
    print("\nfound tissues to get ontologies of size: {}".format(len(db_results)))

    # loop
    for row in db_results:
        tissue_name = row[0]

        # log
        if log:
            print("searching for ontology for tissue: ({})".format(tissue_name))

        # get the ws data
        # ontology_id, service_name = ws_get_ontology_id(item=tissue_name, list_ontology=['UBERON', 'UMLS'])
        ontology_id, service_name = ws_get_ontology_id(item=tissue_name, list_ontology=['UBERON'])

        # update is appropriate
        if ontology_id and service_name:
            cursor.execute(SQL_UPDATE_TISSUE, (ontology_id, service_name, tissue_name))
            conn.commit()

            # log
            if log:
                print("db updated tissue: ({}) with ontology: {} and service name: ({})\n".format(tissue_name, ontology_id, service_name))
        else:
            # log
            if log:
                print("DID NOT db update tissue: ({}) with ontology: {} and service name: ({})\n".format(tissue_name, ontology_id, service_name))


def ws_bioindex_query_tissue_disease_assocations_service(input_phenotype, log=True):
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


def ws_get_ontology_id(item, list_ontology, log=True):
    '''
    will query the name lookup of translator to find the ontology_id that match prefixes given
    '''
    # initialize
    url_query = "https://name-resolution-sri.renci.org/lookup?limit=100&string={}".format(item)
    service_name = None
    ontology_id = None 

    # query
    response = requests.get(url_query).json()

    # loop
    for row in response:
        if row.get('curie') and row.get('curie').split(":")[0] in list_ontology:
            ontology_id = row.get('curie')
            service_name = row.get('label')
            break

    # log
    if log:
        print("for item: ({}) got ontology_id: {} with label: ({})".format(item, ontology_id, service_name))

    # return
    return ontology_id, service_name


if __name__ == "__main__":
    # get the db connection
    conn = get_connection()

    # get the inputs
    list_input = db_get_phenotype_list(conn)

    # log
    print("got input list of size {}".format(len(list_input)))
    
    # test the check_phenotype method
    assert (len(list_input) > 190) == True

    # test gene list
    # list_input = ['BMI']

    # loop
    # for item in list_input:
    #     # get the data from the service
    #     list_data = ws_bioindex_query_tissue_disease_assocations_service(input_phenotype=item)

    #     # insert the data into the DB
    #     db_load_tissue_phenotypes(conn=conn, list_data=list_data)


    # get the unique tissues in the data and load the staging tissue table with any new ones
    list_tissue = db_get_distinct_tissue_list_from_staging_table(conn=conn)
    db_insert_tissues(conn=conn, list_tissue=list_tissue)

    # get the ontologies for the tissues that don't have them
    db_update_tissues(conn=conn)

    # close the db connection
    conn.close()
