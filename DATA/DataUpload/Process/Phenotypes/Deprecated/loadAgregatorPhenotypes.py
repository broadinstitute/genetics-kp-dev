
# imports
import requests
import pymysql as mdb

# constants
url_aggregator = "https://bioindex-dev.hugeamp.org/api/portal/phenotypes"
db_schema = 'tran_test_202303'


def query_service_phenotypes(url):
    ''' queries the service for all phenotypes '''
    # query the service
    response = requests.get(url).json()

    # return
    return response

def get_phenotype_values(input_json):
    ''' will parse the graphql output and generate phenotype information tuples list '''
    data = input_json.get('data')
    result = []

    # loop
    if data is not None:
        result = [(item.get('name'), item.get('description'), item.get('group')) for item in data]

    # rerurn
    return result

def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password='yoyoma', charset='utf8', db='tran_test_202108')

    # return
    return conn 

def load_phenotypes_reference(conn, phenotype_list):
    ''' 
    add phenotypes to mysql phenotype table 
    '''
    sql_insert = """insert ignore into tran_upkeep.agg_aggregator_phenotype (phenotype_id, phenotype_name, group_name)
            values (%s, %s, %s) 
        """
    sql_delete = """delete from tran_upkeep.agg_aggregator_phenotype 
        """
    cur = conn.cursor()

    # delete the data in the table
    cur.execute(sql_delete)

    # insert the new data
    i = 0
    # loop through rows
    for phenotype_id, phenotype_name, group_name in phenotype_list:
        i += 1
        if i % 20 == 0:
            print("{} - disease {}".format(i, phenotype_id))

        cur.execute(sql_insert, (phenotype_id, phenotype_name, group_name))
    conn.commit()

# def load_phenotypes_to_translator(conn, phenotype_list):
#     ''' 
#     add phenotypes to the translator mysql phenotype table 
#     '''
    
#     # initialize
#     sql = """insert into comb_node_ontology (node_code, node_type_id, node_name)
#             values (%s, 12, %s) 
#         """
#     cur = conn.cursor()

#     i = 0
#     # loop through rows
#     for phenotype_id, phenotype_name, group_name in phenotype_list:
#         i += 1
#         if i % 20 == 0:
#             print("disease {}".format(phenotype_id))

#         # check if phenotype not loaded yet
#         if not check_phenotype(conn, phenotype_id):
#             cur.execute(sql,(phenotype_id, phenotype_name))
#             print("loading phenotype/disease {} - {}".format(phenotype_id, phenotype_name))

#     conn.commit()

def check_phenotype(conn, phenotype_id):
    ''' 
    method to query DB and see if the phenoptype is already loaded 
    '''
    
    # initialize
    sql = """
    select * from comb_node_ontology where node_code = %s and node_type_id in (1, 3, 12)
    """
    result = False
    cursor = conn.cursor()

    # call the query
    cursor.execute(sql, phenotype_id)
    db_results = cursor.fetchall()

    # check
    if len(db_results) > 0:
        result = True

    # return
    return result

def print_num_translator_phenotypes_in_db(conn):
    ''' 
    will query and print the count of phenotypes in the translator nodes table 
    '''
    
    # initialize
    sql = """
    select count(*) from comb_node_ontology where node_type_id in (1, 3, 12)
    """
    cursor = conn.cursor()
    count = 0

    # call the query
    cursor.execute(sql)
    db_results = cursor.fetchall()

    # get the data
    if db_results:
        count = db_results[0][0]

    # print
    print("the are {} phenotypes/diseases in the translator db".format(count))

def print_num_upkeep_phenotypes_in_db(conn):
    ''' 
    will query and print the count of phenotypes in the upkeep table 
    '''
    
    # initialize
    sql = """
    select count(*), in_translator from tran_upkeep.agg_aggregator_phenotype group by in_translator
    """
    cursor = conn.cursor()

    # call the query
    cursor.execute(sql)
    db_results = cursor.fetchall()

    # get the data
    for row in db_results:
        print("the are {} phenotypes/diseases in the upkeep db with in_translator status: {}".format(row[0], row[1]))

def mark_phenotypes_in_translator(conn, log=False):
    '''
    method will mark phenotypes in the upkeep table that are already in the translator production schema
    '''
    sql_update = '''
    update tran_upkeep.agg_aggregator_phenotype set in_translator = 'true'
        where phenotype_id COLLATE utf8mb4_general_ci in (
        select node_code from {}.comb_node_ontology where node_type_id in (1, 3)
        );
    '''.format(db_schema)

    # query the db
    cursor = conn.cursor()
    cursor.execute(sql_update)
    conn.commit()



if __name__ == "__main__":
    resp = query_service_phenotypes(url_aggregator)

    # get the phenotype data
    data_aggregator_phenotypes = get_phenotype_values(resp)
    print(f'got aggregator phenotype data from REST serviec of size: {len(data_aggregator_phenotypes)}')

    # get the db connection
    conn = get_connection()

    # log
    print_num_translator_phenotypes_in_db(conn)
    print_num_upkeep_phenotypes_in_db(conn)
    
    # # load the data
    # load_phenotypes_to_translator(conn, data)

    # load the data to the translator upkeep schema
    load_phenotypes_reference(conn, data_aggregator_phenotypes)

    # test the check_phenotype method
    assert check_phenotype(conn, 'BMI') == True
    assert check_phenotype(conn, 'testasif') == False

    # log
    print_num_translator_phenotypes_in_db(conn)
    print_num_upkeep_phenotypes_in_db(conn)
    
    # mark the phenotypes previously loaded in translator
    mark_phenotypes_in_translator(conn)

    # log
    print_num_translator_phenotypes_in_db(conn)
    print_num_upkeep_phenotypes_in_db(conn)

    