
# imports
import pymysql as mdb
import requests 


# steps 
# 1 - delete old cache and upkeep cache status table 
# 1a - load curies into status table 
# 2 - query all curies
# 3 - for each 
# a - get synonyms (including current curie)
# b - get ancestors (do in batches of 30)
# 4 - save for each 30 batch and mark curies as done 

# constants 
DB_SCHEMA = "tran_test_202303"

# sql statements
SQL_DELETE_NODE = "delete from {}.comb_cache_ancestor_curie where genepro_node_id = {}"
SQL_INSERT_LINK = """
    insert into {}.comb_cache_ancestor_curie (genepro_node_id, genepro_node_id, parent_curie_id, parent_node_name)
    values({}, {}, {}, {})
    """
SQL_COUNT = "select count(id) from {}.comb_cache_ancestor_curie"


def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA)


def clear_cache_table(conn, log=False):
    '''
    clears the existing cache table 
    '''


def delete_rows_for_node_id(conn, node_id, log=False):
    '''
    deletes the entries for the given node_id
    '''
    # initialize
    cursor = conn.cursor()

    # run the sql 
    cursor.execute(SQL_DELETE_NODE.format(DB_SCHEMA, node_id))


def log_cache_entries(conn, log=False):
    '''
    logs the count of the cache table
    '''
    # intialize 
    count = 0

    # run the sql

    # print 
    print("the translator database: {} has cache row count of: {}".format(DB_SCHEMA, count))






if __name__ == "__main__":
    pass
