
# imports
import csv 
import pandas as pd 
import pymysql as mdb
import os
import requests 


# constants
debug = True
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA_UPKEEP = 'tran_upkeep'
DB_SCHEMA_TRANSLATOR = 'tran_test_202302'
DB_TABLE_UPKEEP = "data_600k_phenotype_ontology"
DB_TABLE_TRANSLATOR_EDGE = "comb_edge_node"
STUDY_ID = 18

def delete_from_translator_table(conn, study_id, log=False):
    '''
    will delete the table data 
    '''
    sql_delete = """
        delete from {}.{} where study_id = {}
        """.format(DB_SCHEMA_TRANSLATOR, DB_TABLE_TRANSLATOR_EDGE, study_id)

    cur = conn.cursor()
    cur.execute(sql_delete)

    # commit
    conn.commit()

def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA_TRANSLATOR)

    # return
    return conn 

def print_count_of_edges(conn, study_id, log=False):
    '''
    prints the number of edges from this study
    '''
    sql_count = """
        select count(id) from {}.{} where study_id = {}
        """.format(DB_SCHEMA_TRANSLATOR, DB_TABLE_TRANSLATOR_EDGE, study_id)

    cur = conn.cursor()
    cur.execute(sql_count)
    db_results = cur.fetchone()

    # check
    if len(db_results) > 0:
        result = True

    # get the data
    if db_results:
        print("for study: {} have row count:{}".format(study_id, db_results[0]))


def get_phenotype_node(conn, phenotype_id, log=False):
    '''
    gets the phenotype node id based on ontology_id
    '''
    # initialize
    node = None 
    sql_select = "select id, ontology_id, node_name from {}.comb_node_ontology where ontology_id = %s".format(DB_SCHEMA_TRANSLATOR)

    # get the node
    cur = conn.cursor()
    cur.execute(sql_select, (phenotype_id))
    db_results = cur.fetchone()

    if db_results:
        node = {'id': db_results[0], 'ontology_id': db_results[1],  'name': db_results[2]}

    # return
    return node

def get_gene_node(conn, gene_code, log=False):
    '''
    gets the gene db node from the gene name 
    '''
    node = None 
    sql_select = "select id, ontology_id, node_code from {}.comb_node_ontology where node_code = %s".format(DB_SCHEMA_TRANSLATOR)

    # get the node
    cur = conn.cursor()
    cur.execute(sql_select, (gene_code))
    db_results = cur.fetchone()

    if db_results:
        node = {'id': db_results[0], 'ontology_id': db_results[1],  'name': db_results[2]}
        
    # return
    return node


def add_edge(conn, gene, phenotype_id, phenotype_name, p_value, beta, log=False):
    '''
    inserts a edge into the translator DB (edge, node, qualifiers)
    '''
    # initialize
    node_phenotype = None
    node_gene = None 

    # get phenotype node id 
    node_phenotype = get_or_insert_phenotype(conn, phenotype_id, phenotype_name)

    # get gene node id 

    # insert the edge row

    # commit
    conn.commit()

    # log


    
def get_or_insert_phenotype(conn, ontology_id, phenotype_name, log=False):
    ''' 
    will insert phenotype into the translator node table 
    '''
    sql_insert = '''
    insert into {}.comb_node_ontology (node_code, node_type_id, ontology_id, ontology_type_id, node_name, added_by_study_id)
    values(%s, (select type_id from comb_lookup_type where type_name = 'biolink:Disease'), %s,
        (select ontology_id from comb_ontology_type where substring_index(%s, ':', 1) = prefix),
        %s, %s)
    '''.format(DB_SCHEMA_TRANSLATOR)

    # get the phenotype
    phenotype = get_phenotype_node(conn, ontology_id)

    # if no phenotype by that curie, insert 
    if not phenotype:
        cur = conn.cursor()
        cur.execute(sql_insert, (ontology_id, ontology_id, ontology_id, phenotype_name, STUDY_ID))

        # log
        if log:
            print("inserted phenotype: {} with curie: {}".format(ontology_id, phenotype_name))
            conn.commit()

    # get phenotype
    phenotype = get_phenotype_node(conn, ontology_id)

    # return 
    return phenotype


if __name__ == "__main__":
    # get the connection
    connection = get_connection()

    # count the current translator 600k data 
    print_count_of_edges(connection, STUDY_ID)

    # delete from the translator data the previous data
    delete_from_translator_table(connection, STUDY_ID)

    # count the current translator 600k data 
    print_count_of_edges(connection, STUDY_ID)

    # insert the new data

    # count the current translator 600k data 
    print_count_of_edges(connection, STUDY_ID)



    # test
    if debug:
        # get gene
        gene_code = 'PPARG'
        result = get_gene_node(connection, gene_code)
        print("for: {} got: {}".format(gene_code, result))

        # get gene
        gene_code = 'YOYO'
        result = get_gene_node(connection, gene_code)
        print("for: {} got: {}".format(gene_code, result))

        # get phenotype
        phenotype_id = 'MONDO:0005148'
        result = get_phenotype_node(connection, phenotype_id)
        print("for: {} got: {}".format(phenotype_id, result))

        # test insert of phenotype
        get_or_insert_phenotype(connection, 'MONDO:0015978', 'functional neutrophil defect', log=True)




# 20230209 - pre load 
# +------------+----------+------------------------+
# | edge_count | study_id | study_name             |
# +------------+----------+------------------------+
# |     899006 |        1 | Magma                  |
# |      72216 |        4 | Richards Effector Gene |
# |       2217 |        5 | ClinGen                |
# |       9160 |        6 | ClinVar                |
# |      12756 |        7 | genCC                  |
# |      34318 |       17 | GeneBass               |
# +------------+----------+------------------------+
# 6 rows in set (2.17 sec)

# 20230209 - post load 
