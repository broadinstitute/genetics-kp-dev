
# imports 
import requests 
import time
import os 
import sys
import logging
import pymysql as mdb
import json
import time

# dynamic lib
handler = logging.StreamHandler(sys.stdout)
logger = logging.getLogger(__name__)
dir_code = "/home/javaprog/Code/PythonWorkspace/"
dir_data = "/home/javaprog/Data/Broad/"
# sys.path.insert(0, dir_code + 'MachineLearningPython/DccKP/Translator/TranslatorLibraries')
# import translator_libs as tl

# constants 
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA = 'tran_upkeep'
FILE_JSON = "phenotypes_bioindex.json"

SQL_SELECT_WITH_ONTOLOGY = """
    select id, phenotype_name, phenotype_id, ontology_id from tran_upkeep.agg_aggregator_phenotype 
    order by phenotype_name
"""

# methods 
def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA)

    # return
    return conn 


def get_list_phenotypes(conn):
    '''
    get the list of upkeep db phenotypes that have an ontology
    returns list of tuples (name, id)
    '''
    # initialize
    sql_select = SQL_SELECT_WITH_ONTOLOGY

    # query the db
    cursor = conn.cursor()
    cursor.execute(sql_select)
    db_results = cursor.fetchall()
    
    # get the data
    if db_results:
        result = [{'id': item[0], 'name': item[1], 'bioindex_id': item[2], 'ontology_id': item[3]} for item in db_results]

    # return
    return result


def save_json_phentypes(map_phenotypes, file_name=FILE_JSON):
    '''
    saves the data to a json file
    '''
    with open(file_name, 'w') as f:
        json.dump(map_phenotypes, f, indent=2)    


if __name__ == "__main__":
    # get the db connection
    db_connection = get_connection()

    # get the phenotypes
    list_phenotypes = get_list_phenotypes(conn=db_connection)

    # create the map
    map_phenotypes = {}
    for phenotype in list_phenotypes:
        map_phenotypes[phenotype.get('bioindex_id')] = phenotype

    # save json file
    save_json_phentypes(map_phenotypes=map_phenotypes)
