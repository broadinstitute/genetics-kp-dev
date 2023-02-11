

# imports
import csv 
import pandas as pd 
import pymysql as mdb
import os
import requests 

# constants 
file_phenotype_codes = "/home/javaprog/Data/Broad/Translator/DownloadedData/600kGeneDisease/finalModified600kPhenoCode20230202.tsv"
debug = True
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA = 'tran_upkeep'
DB_TABLE = "data_600k_phenotype_ontology"

def read_file(file, log=False):
    '''
    read the csv file into a list of dicts
    '''
    # initialize
    list_phenotypes = []

    # read the file
    with open(file) as f:
        # assuming the first row is "headers", let's skip it
        row_header = next(f)
        read = csv.reader(f, delimiter='\t')
        # map_row = dict(((first, last), float(grade)) for first, last, grade in read)
        for row in read:
            # keep pheno code, ontology id, phenotype name
            list_phenotypes.append({'code': row[0], 'name': row[1], 'ontology_id': row[4]})

        # (print("row: {}".format(row)) for row in read)
        # print(type(read))

    # return
    return list_phenotypes

def format_ontology_id(list_phenotypes, log=False):
    '''
    will make sure all rows returned are in xx:000 format and will discard the duplicates and rows with 2 ids
    '''
    # initialize
    map_phenotypes = {}
    map_curated = {}

    # loop through list
    for row in list_phenotypes:
        # keep only the first ontology_id
        ontology_id = row.get('ontology_id').split(',')[0].strip()
        ontology_id = ontology_id.split('/')[0].strip()

        # make sure the ontology is in XX:000 format (convert underscore)
        ontology_id = ontology_id.replace('_', ':')

        # skip any ontology with no colon
        if (ontology_id.find(':')):
            phenotype_name = row.get('name').replace('_', ' ')
            if map_phenotypes.get(ontology_id):
                map_phenotypes.get(ontology_id).append({'code': row.get('code'), 'name': phenotype_name, 'ontology_id': ontology_id})
            else:
                map_phenotypes[ontology_id] = [{'code': row.get('code'), 'name': phenotype_name, 'ontology_id': ontology_id}]

        # weed out phenotypes mapped to same ontology_id
        for key in map_phenotypes.keys():
            if len(map_phenotypes.get(key)) == 1:
                map_curated[key] = map_phenotypes.get(key)[0]

    # return
    return map_curated

def delete_table(conn, log=False):
    '''
    will delete the table data 
    '''
    sql_delete = """
        delete from {}.{} 
        """.format(DB_SCHEMA, DB_TABLE)

    cur = conn.cursor()
    cur.execute(sql_delete)

    # commit
    conn.commit()

def insert_phenotype_ontologies(conn, list_phenotypes, log=False):
    ''' 
    add phenotype ontologies from the csv file results
    '''
    sql_insert = """
        insert into {}.{} (phenotype_ontology_id, phenotype_code, phenotype_translator_name, phenotype_data_name, has_translator_name)
            values (%s, %s, %s, %s, %s) 
        """.format(DB_SCHEMA, DB_TABLE)

    cur = conn.cursor()
    i = 0

    # loop through rows
    for row in list_phenotypes:
        # log
        i += 1
        if log:
            if i % 50 == 0:
                print(row)

        cur.execute(sql_insert, (row.get('ontology_id'), row.get('code'), row.get('name_translator'), row.get('name'), row.get('has_translator_name')))

    # log
    print("inserted phenotypes row count: {}".format(len(list_phenotypes)))

    # commit
    conn.commit()

def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA)

    # return
    return conn 

def get_translator_name(ontology_id, name_backup, log=False):
    '''
    will use the translator node normalizer to get the official translator name
    '''
    # initialize 
    name_translator = name_backup
    has_translator_name = 'N'

    # log
    if log:
        print("looking for name for: {}".format(ontology_id))

    # query the service
    response = requests.get("https://nodenorm.transltr.io/1.3/get_normalized_nodes?curie={}".format(ontology_id)).json()

    # get the data
    if response.get(ontology_id):
        name_translator = response.get(ontology_id).get('id').get('label')
        has_translator_name = 'Y'

    else:
        print("found no name for: {}".format(ontology_id))

    # log
    if log:
        print("for: {} got name: {}".format(ontology_id, name_translator))

    # return
    return name_translator, has_translator_name


if __name__ == "__main__":
    # load the phenotype codes
    # df_phenotypes = pd.read_csv(file_phenotype_codes)
    list_phenotypes = read_file(file_phenotype_codes)

    # massage the data
    map_phenotypes = format_ontology_id(list_phenotypes)

    # log
    if debug:
        for key, value in map_phenotypes.items():
            print("{}: {}".format(key, value))
        print("got phenotype row count of: {}".format(len(map_phenotypes)))

    # get the official translator name 
    for key, value in map_phenotypes.items():
        name_translator, has_translator_name = get_translator_name(key, value.get('name'), log=False)
        value['name_translator'] = name_translator
        value['has_translator_name'] = has_translator_name

    # get the db connection
    connection = get_connection()

    # delete the table
    delete_table(connection)

    # insert the phenotypes
    insert_phenotype_ontologies(list_phenotypes=map_phenotypes.values(), conn=connection)




