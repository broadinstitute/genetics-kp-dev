

# imports
import sqlite3
import pymysql as mdb
from datetime import datetime
import os
import json

# constants
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA = 'tran_upkeep'
DIR_HOME = "/home/javaprog/Data/Broad/Translator/GeneticsPro"
FILE_DB = "{}/MultiCurie/Sqlite/mcq.db".format(DIR_HOME)

DB_STUDY_ID = 19
DB_TYPE_CELL_ID = 11
DB_ONTOLOGY_TYPE_CELL_ID = 9
DB_EDGE_TYPE_ID = 6



# sql
SQL_SQLITE_INSERT_NODE = """
insert into comb_node_ontology
(node_code, node_type_id, ontology_id, ontology_type_id, node_name, added_by_study_id)
values(:node_code, :node_type_id, :ontology_id, :ontology_type_id, :node_name, :added_by_study_id)
"""

SQL_SQLITE_INSERT_EDGE = """
insert into comb_edge_node
(edge_id, source_node_id, target_node_id, edge_type_id, study_id, score_translator, p_value, enrichment, annotation)
values(:edge_id, :source_node_id, :target_node_id, :edge_type_id, :study_id, :score_translator, :p_value, :enrichment, :annotation)
"""


# methods
def get_mysql_connection():
    ''' 
    get the mysql db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA)

    # return
    return conn 


def get_sqlite_connection():
    ''' 
    get the sqlite db connection 
    '''
    conn = sqlite3.connect(FILE_DB)

    # return
    return conn 


def db_mysql_get_tissue_data(conn, log=True):
    '''
    gets the data from the mysql tissue phenotype temp table
    '''
    # initialize
    list_nodes = []
    cursor = conn.cursor()
    # sql_query = "select phenotype_code, phenotype_id, tissue_code, tissue_id, pValue, annotation, enrichment from temp_load_tissue_phenotype limit 1"
    sql_query = "select phenotype_code, phenotype_id, tissue_code, tissue_id, pValue, annotation, enrichment from temp_load_tissue_phenotype where tissue_id is not null"

    # get the data
    cursor.execute(sql_query)
    db_results = cursor.fetchall()

    # loop
    for row in db_results:
        list_nodes.append({'phenotype_id': row[1], 'phenotype_code': row[0], 'tissue_code': row[2], 'tissue_id': row[3], 'p_value': row[4], 'annotation': row[5], 'enrichment': row[6]})

    if log:
        print("got stage node: {}".format(json.dumps(list_nodes, indent=2)))

    # return
    return list_nodes


def db_lite_find_node_by_ontology_id(conn, ontology_id, node_code, log=False):
    '''
    gets the node id from the ontology_id
    '''
    # initialize
    cursor = conn.cursor()
    sql_query = "select id, node_code, ontology_id from comb_node_ontology where ontology_id = ? and node_code = ?"
    row_id = None

    # search
    cursor.execute(sql_query, (ontology_id, node_code))
    db_results = cursor.fetchall()

    if db_results and len(db_results) > 0:
        row_id = db_results[0][0]

    # return
    return row_id


def db_lite_insert_node(conn, node, is_commit=False, log=False):
    '''
    insert a node into the sqlite db
    '''
    # initialize
    cursor = conn.cursor()
    columns, placeholders, values = db_sqlite_get_schema(data=node)
    sql = f'INSERT INTO comb_node_ontology ({columns}) VALUES ({placeholders})'

    # log
    if log:
        print("inserting: {}".format(node))

    # insert
    cursor.execute(sql, values)

    # commit
    if is_commit:
        conn.commit()


def db_lite_insert_edge(conn, edge, is_commit=False, log=False):
    '''
    insert a edge into the sqlite db
    '''
    # initialize
    cursor = conn.cursor()
    columns, placeholders, values = db_sqlite_get_schema(data=edge)
    sql = f'INSERT INTO comb_edge_node ({columns}) VALUES ({placeholders})'

    # log
    if log:
        print("inserting: {}".format(edge))

    # insert
    cursor.execute(sql, values)

    # commit
    if is_commit:
        conn.commit()


def db_lite_insert_tissue_edge(conn, list_tissue_phenotype, log=True):
    '''
    will insert the tissue/phenotype data
    '''
    # intialize
    cursor = conn.cursor()
    sql_delete_by_study_id = "delete from comb_edge_node where study_id = :study_id"

    # delete all the previous study data
    cursor.execute(sql_delete_by_study_id, ({'study_id': DB_STUDY_ID}))
    conn.commit()

    # loop
    for item in list_tissue_phenotype:
        # log
        if log:
            print("inserting edge data: {}".format(json.dumps(item, indent=2)))

        # find the phenotype_id
        phenotype_id = db_lite_find_node_by_ontology_id(conn=conn, ontology_id=item.get('phenotype_id'), node_code=item.get('phenotype_code'))

        if phenotype_id:
            # find or insert the tissue_id
            tissue_id = db_lite_find_node_by_ontology_id(conn=conn, ontology_id=item.get('tissue_id'), node_code=item.get('tissue_code'))
            if not tissue_id:
                tissue_node = {'node_code': item.get('tissue_code'),
                                'node_type_id': DB_TYPE_CELL_ID,
                                'ontology_id': item.get('tissue_id'),
                                'ontology_type_id': DB_ONTOLOGY_TYPE_CELL_ID,
                                'node_name': item.get('tissue_code'),
                                'added_by_study_id': DB_STUDY_ID}
                
                db_lite_insert_node(conn=conn, node=tissue_node)

            # now find tissue_id again
            tissue_id = db_lite_find_node_by_ontology_id(conn=conn, ontology_id=item.get('tissue_id'), node_code=item.get('tissue_code'))

            # make sure have tissue_id
            if tissue_id:
                # insert the subject edge
                tissue_subject_edge = {
                    'edge_id': item.get('tissue_id') + '-' + item.get('phenotype_id') + '-' + item.get('annotation'),
                    'source_node_id': tissue_id,
                    'target_node_id': phenotype_id,
                    'edge_type_id': DB_EDGE_TYPE_ID,
                    'score_translator': item.get('enrichment'),
                    'p_value': item.get('p_value'),
                    'enrichment': item.get('enrichment'),
                    'annotation': item.get('annotation'),
                    'study_id': DB_STUDY_ID
                }
                db_lite_insert_edge(conn=conn, edge=tissue_subject_edge)

                tissue_object_edge = {
                    'edge_id': item.get('phenotype_id') + '-' + item.get('tissue_id') + '-' + item.get('annotation'),
                    'source_node_id': phenotype_id,
                    'target_node_id': tissue_id,
                    'edge_type_id': DB_EDGE_TYPE_ID,
                    'score_translator': item.get('enrichment'),
                    'p_value': item.get('p_value'),
                    'enrichment': item.get('enrichment'),
                    'annotation': item.get('annotation'),
                    'study_id': DB_STUDY_ID
                }
                db_lite_insert_edge(conn=conn, edge=tissue_object_edge, is_commit=True)

                if log:
                    print("inserted subjects data: {}".format(json.dumps(tissue_subject_edge, indent=2)))

            else :
                print("ERROR: no tissue node found for {} - {}".format(item.get('phenotype_id'), item.get('phenotype_code')))

        else :
            print("ERROR: no phenotype node found for {} - {}".format(item.get('phenotype_id'), item.get('phenotype_code')))


def db_sqlite_get_schema(data, log=False):
    '''
    will return the schema data to insert into a sqlite table
    '''
    columns = ', '.join(data.keys())
    placeholders = ', '.join('?' for _ in data)
    values = tuple(data.values())

    return columns, placeholders, values

# def db_lite_insert_node(conn, node, is_commit=False, log=False):
#     '''
#     insert a node into the sqlite db
#     '''
#     # initialize
#     cursor = conn.cursor()
#     columns, placeholders, values = db_sqlite_get_schema(data=node)
#     sql = f'INSERT INTO comb_node_ontology ({columns}) VALUES ({placeholders})'

#     # log
#     if log:
#         print("inserting: {}".format(node))

#     # insert
#     cursor.execute(sql, values)

#     # commit
#     if is_commit:
#         conn.commit()


# main
if __name__ == "__main__":
    # get th4e connections
    conn_mysql = get_mysql_connection()
    conn_sqlite = get_sqlite_connection()

    # get the node data
    list_stage_tissue_phenotype = db_mysql_get_tissue_data(conn=conn_mysql)
    print("got list of tissue/phenotype of size: {}".format(len(list_stage_tissue_phenotype)))

    # insert into sqlite
    db_lite_insert_tissue_edge(conn=conn_sqlite, list_tissue_phenotype=list_stage_tissue_phenotype)

    # commit
    conn_sqlite.commit()