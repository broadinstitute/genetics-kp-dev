
# process:
# load all phenotypes from upkeep DB
# load phenotypes from file (usually updated with ontology ids)
# save phenotyps with new ontology ids

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
file_rare_disease = '/home/javaprog/Data/Broad/Translator/RareDisease/DCC_GARD_RareDiseases.csv'
file_test_rare_disease = '/home/javaprog/Data/Broad/Translator/RareDisease/Test_DCC_GARD_RareDiseases.csv'
# url_name_search = 'https://name-resolution-sri.renci.org/lookup?string={}'
url_name_search = 'https://name-lookup.transltr.io/lookup?limit=100&string={}'
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA = 'tran_upkeep'
LIST_ONTOLOGY = ['MONDO', 'EFO', 'UMLS', 'NCIT', 'HP']
URL_NAME_RESOLVER ="https://name-lookup.transltr.io/lookup?limit={}&string={}"
FILE_JSON = "phenotypes_bioindex.json"

SQL_SELECT_WITH_ONTOLOGY = """
    select id, phenotype_name, phenotype_id, ontology_id from tran_upkeep.agg_aggregator_phenotype 
    where ontology_id is not null 
    order by phenotype_name
"""

SQL_SELECT_WITHOUT_ONTOLOGY = """
    select id, phenotype_name, phenotype_id from tran_upkeep.agg_aggregator_phenotype 
    where ontology_id is null 
    order by len(phenotype_name)
"""

SQL_SELECT_ALL_PHENOTYPES = """
    select id, phenotype_name, phenotype_id, ontology_id from tran_upkeep.agg_aggregator_phenotype 
"""

# keys
KEY_ONTOLOGY_ID = "ontology_id"
KEY_BIOINDEX_ID = "bioindex_id"

# methods 
def load_phenotypes_map_from_file(file_name=FILE_JSON):
    '''
    load all phenotypes from the file where ontology ids have been added
    '''
    map_phenotypes = {}

    # load the file
    with open(file_name, "r") as f:
        json_data = f.read()  # read the file contents into a string
        map_data = json.loads(json_data)

    # return
    return map_data


# def get_curies(entity_name, list_ontologies, limit=20, log=False):
#     '''
#     gets the ontology ids for an input
#     '''
#     list_result = []
#     url = URL_NAME_RESOLVER.format(limit, entity_name)

#     # do the call
#     try:
#         response = requests.post(url, json={}, timeout=10)
#         response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

#         map_json = response.json()

#         if log:
#             print("got json result: {}".format(json.dumps(map_json, indent=2)))

#         list_result = [s.get('curie', "") for s in map_json if any(sub in s.get('curie', "") for sub in list_ontologies)]

#         # return response.json()       # Returns the parsed JSON content

#     except requests.exceptions.HTTPError as http_err:
#         print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
#     except requests.exceptions.ConnectionError as conn_err:
#         print(f"Connection error occurred: {conn_err}")
#     except requests.exceptions.Timeout as timeout_err:
#         print(f"Timeout error occurred: {timeout_err}")
#     except requests.exceptions.RequestException as req_err:
#         print(f"An unexpected error occurred: {req_err}")

#     # log
#     if log:
#         print("return curie list: {}".format(list_result))

#     # return
#     return list_result


def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA)

    # return
    return conn 


def get_db_phenotypes_map(conn):
    '''
    get the map of upkeep db phenotypes
    returns map by bioindex id as key
    '''
    # initialize
    sql_select = SQL_SELECT_ALL_PHENOTYPES
    map_phenotype = {}

    # query the db
    cursor = conn.cursor()
    cursor.execute(sql_select)
    db_results = cursor.fetchall()
    
    # get the data
    if db_results:
        for item in db_results:
            map_phenotype[item[2].strip()] = {'id': item[0], 'name': item[1], KEY_BIOINDEX_ID: item[2], KEY_ONTOLOGY_ID: item[3]}

    # return
    return map_phenotype


# def get_list_phenotype_with_ontology(conn):
#     '''
#     get the list of upkeep db phenotypes that have an ontology
#     returns list of tuples (name, id)
#     '''
#     # initialize
#     sql_select = SQL_SELECT_WITH_ONTOLOGY

#     # query the db
#     cursor = conn.cursor()
#     cursor.execute(sql_select)
#     db_results = cursor.fetchall()
    
#     # get the data
#     if db_results:
#         result = [{'id': item[0], 'name': item[1], 'bioindex_id': item[2], 'ontology_id': item[3]} for item in db_results]

#     # return
#     return result


# def get_map_phenotypes_with_ontology(conn):
#     '''
#     get the map of existing phenotypes by curie as key
#     '''
#     # initialize
#     map_pheno = {}

#     # get the db results
#     db_result = get_list_phenotype_with_ontology(conn=conn)
        
#     # populate the map
#     for phenotype in db_result:
#         map_pheno[phenotype.get('ontology_id')] = phenotype

#     # return
#     return map_pheno


# def get_list_phenotype_without_ontology(conn):
#     '''
#     get the list of upkeep db phenotypes that do not have an ontology
#     returns list of tuples (name, id)
#     '''
#     # initialize
#     sql_select = SQL_SELECT_WITH_ONTOLOGY

#     # query the db
#     cursor = conn.cursor()
#     cursor.execute(sql_select)
#     db_results = cursor.fetchall()
    
#     # get the data
#     if db_results:
#         result = [{'id': item[0], 'name': item[1], 'bioindex_id': item[2]} for item in db_results]

#     # return
#     return result


def add_db_phenotype_ontology_id(conn, row_id, ontology_id):
    '''
    add in found ontology_id for the given phenotype
    '''
    # initialize
    sql_update = "update tran_upkeep.agg_aggregator_phenotype set ontology_id = %s where id = %s"

    # query the db
    cursor = conn.cursor()
    cursor.execute(sql_update, (ontology_id, row_id))
    conn.commit()


if __name__ == "__main__":
    # initialize
    list_phenotypes = []
    count = 0

    # get the connection
    db_connection = get_connection()

    # load the phenotypes in the db
    map_db_phenotype = get_db_phenotypes_map(conn=db_connection)
    print(json.dumps(map_db_phenotype, indent=2))

    # load the phenotypes from the updated file
    map_file_phenotype = load_phenotypes_map_from_file()

    # print(json.dumps(list(map_file_phenotype.keys()), indent=2))

    # loop through the db phenotypes and see if any have ontology ids to update
    for db_key, db_value in map_db_phenotype.items():
        file_phenotype = map_file_phenotype.get(db_key.strip())
        # print(db_key)
        # print(db_value)
        # print(file_phenotype)
        if file_phenotype is not None:
            if file_phenotype.get(KEY_ONTOLOGY_ID) is not None:
                if not db_value.get(KEY_ONTOLOGY_ID) or (db_value.get(KEY_ONTOLOGY_ID) != file_phenotype.get(KEY_ONTOLOGY_ID)):
                    # replace phenotype ontology id
                    # add_db_phenotype_ontology_id(conn=db_connection, row_id=db_value.get('id'), ontology_id=file_phenotype.get(KEY_ONTOLOGY_ID))

                    # log
                    print("replaced ontology: {} with: {} for phenotype: {}".format(db_value.get(KEY_ONTOLOGY_ID), file_phenotype.get(KEY_ONTOLOGY_ID), db_value))


















    # # search for ontology id for those phenotypes
    # for phenotype in list_phenotypes:
    #     # get the onlogy_id for the phenotype
    #     list_curies = get_curies(entity_name=phenotype.get('name'), list_ontologies=LIST_ONTOLOGY, limit=5)

    #     # if there is an ontology id
    #     if len(list_curies) > 0 and list_curies[0]:
    #         # sleep for API
    #         time.sleep(5)

    #         # get the curies
    #         potential_curie_id = list_curies[0]
            
    #         # skip if phenotype in map
    #         if not map_phenotype.get(potential_curie_id):
    #             # if not, insert ontology for phenotype
    #             # add_db_phenotype_ontology_id(conn=db_connection, row_id=phenotype.get('id'), ontology_id=potential_curie_id)

    #             # add to map
    #             map_phenotype[potential_curie_id] = phenotype

    #             # log
    #             print("DB added curie: {} for phentype: {}".format(potential_curie_id, phenotype))







    # # get the list of phenotypes that are not in the 
    # list_phenotypes = get_new_phenotype_list(db_connection)
    # num_total = len(list_phenotypes)
    # print("got {} new phenotypes to add to translator".format(num_total))

    # # loop
    # for (row_id, name, phenotype_id) in list_phenotypes:
    #     count = count + 1
    #     if count > 5000:
    #         break
    
    #     # pause for rest service
    #     time.sleep(0.5)
        
    #     # search for an ontology id
    #     ontology_id = tl.find_ontology(name, list_ontology)
    #     print("{} - {} found for {} - '{}'".format(count, ontology_id, phenotype_id, name))

    #     # add in to table if not null
    #     if ontology_id:
    #         add_phenotype_ontology_id(db_connection, row_id, ontology_id)
    #         print("row {}/{} - {} added for {} - {}".format(row_id, num_total, ontology_id, phenotype_id, name))

    # # commit
    # db_connection.commit()

# # get the phenotypes from 
# # read the file
# df_rare_disease = pd.read_csv(file_rare_disease, sep=',', header=0)
# print("after reading: \n{}".format(df_rare_disease.info()))

# # loop through rows and look for match for disease name 
# count = 0
# for index, row in df_rare_disease.iterrows():
#     ontology = row['ontology']
#     ontology_check = row['ontology_check']
#     if pd.isnull(ontology) and pd.isnull(ontology_check):
#         # log
#         print("no previous ontology for: {}".format(row['d.name']))
#         count += 1

#         # find ontology
#         result = find_ontology(row['d.name'])

#         # if found, log and set
#         if result is not None:
#             print("found ontology for: {} - {}\n".format(row['d.name'], result))
#             df_rare_disease.loc[df_rare_disease['d.name'] == row['d.name'], ['ontology']] = result
        
#         # log that checked
#         df_rare_disease.loc[df_rare_disease['d.name'] == row['d.name'], ['ontology_check']] = "yes"

#         # break if count reached
#         if count%10 == 0:
#             print("{} - data saved to file".format(count))
#             df_rare_disease.to_csv(file_rare_disease, sep=',', index=False)
#             # break

#         # sleep for throttling avoidance
#         # time.sleep(10)
    
# # log
# print("\nafter updating: \n{}".format(df_rare_disease.info()))

# # write out results 
# # df_rare_disease.to_csv(file_test_rare_disease, sep=',')
# df_rare_disease.to_csv(file_rare_disease, sep=',', index=False)
