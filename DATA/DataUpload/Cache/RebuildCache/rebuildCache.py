
# imports
import pymysql as mdb
import requests 
import os

# steps 
# 1 - delete old cache and upkeep cache status table 
# 1a - load curies into status table 
# 2 - query all curies
# 3 - for each 
# a - get synonyms (including current curie)
# b - get ancestors (do in batches of 30)
# 4 - save for each 30 batch and mark curies as done 

# constants 
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA = "tran_test_202303"
DB_TABLE_CURIE_LIST = "comb_cache_curie_list"
DB_TABLE_CURIE_LINK = "comb_cache_curie_link"

# sql statements
SQL_DELETE_STATEMENT = "delete from {}.{}"

SQL_INSERT_CURIE = """
    insert into {}.{} (curie_id, curie_name, is_genepro)
    values(%s, %s, %s)
    """.format(DB_SCHEMA, DB_TABLE_CURIE_LIST)

SQL_INSERT_LINK = """
    insert into {}.{}} (genepro_list_id, synonym_list_id, is_synonym, is_ancestor)
    values(%s, %s, %s, %s)
    """.format(DB_SCHEMA, DB_TABLE_CURIE_LINK)

SQL_COUNT_STATEMENT = "select count(id) from {}.{}"


def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA)


def clear_cache_table(conn, log=False):
    '''
    clears the existing cache table 
    '''
    # get cursor
    cursor = conn.cursor()

    # clear link table
    cursor.execute(SQL_DELETE_STATEMENT.format(DB_SCHEMA, DB_TABLE_CURIE_LINK), ())

    # clear list table
    cursor.execute(SQL_DELETE_STATEMENT.format(DB_SCHEMA, DB_TABLE_CURIE_LIST), ())

    # commit
    conn.commit()


def log_cache_entries(conn, log=False):
    '''
    logs the count of the cache table
    '''
    # intialize 
    count = 0
    cursor = conn.cursor()

    # count the list 
    cursor.execute(SQL_COUNT_STATEMENT.format(DB_SCHEMA, DB_TABLE_CURIE_LIST))
    results = cursor.fetchall()
    print("have curie list of size: {}".format(results[0][0]))

    # count the link
    cursor.execute(SQL_COUNT_STATEMENT.format(DB_SCHEMA, DB_TABLE_CURIE_LINK))
    results = cursor.fetchall()
    print("have curie synonym link of size: {}".format(results[0][0]))






if __name__ == "__main__":
    pass
