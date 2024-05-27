

# imports
import sqlite3
import pymysql as mdb
from datetime import datetime
import os
import json

# constants
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA = 'tran_test_202303'
DIR_HOME = "/home/javaprog/Data/Broad/Translator/GeneticsPro"
FILE_DB = "{}/MultiCurie/Sqlite/mcq.db".format(DIR_HOME)

# sql
SQL_MYSQL_QUERY_NODE = """
select node_code, node_type_id, ontology_id, ontology_type_id, node_name, added_by_study_id 
from comb_node_ontology
order by node_type_id, node_code
"""

SQL_SQLITE_INSERT_NODE = """
insert into comb_node_ontology
(node_code, node_type_id, ontology_id, ontology_type_id, node_name, added_by_study_id)
values(:node_code, :node_type_id, :ontology_id, :ontology_type_id, :node_name, :added_by_study_id)
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


def db_mysql_get_nodes(conn, log=False):
    '''
    gets the data from the mysql node table
    '''
    # initialize
    list_nodes = []
    cursor = conn.cursor()

    # get the data
    cursor.execute(SQL_MYSQL_QUERY_NODE)
    db_results = cursor.fetchall()

    # loop
    for row in db_results:
        list_nodes.append({'node_code': row[0], 'node_type_id': row[1], 'ontology_id': row[2], 'node_name': row[4], 'ontology_type_id': row[3], 'added_by_study_id': row[5]})
        if log:
            print("got type: {} of node: {} with curie: {}".format(row[1], row[0], row[2]))

    # return
    return list_nodes


def db_sqlite_get_schema(data, log=False):
    '''
    will return the schema data to insert into a sqlite table
    '''
    columns = ', '.join(data.keys())
    placeholders = ', '.join('?' for _ in data)
    values = tuple(data.values())

    return columns, placeholders, values

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

# main
if __name__ == "__main__":
    # get th4e connections
    conn_mysql = get_mysql_connection()
    conn_sqlite = get_sqlite_connection()

    # get the node data
    list_nodes = db_mysql_get_nodes(conn=conn_mysql, log=True)

    # print list
    print(json.dumps(list_nodes, indent=2))

    # loop and insert
    for row in list_nodes:
        db_lite_insert_node(conn=conn_sqlite, node=row, log=True)

    # commit
    conn_sqlite.commit()