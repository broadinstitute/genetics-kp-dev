

# imports
import requests
import pymysql as mdb
from datetime import datetime
import os

# constants
url_query_aggregator = "https://bioindex-dev.hugeamp.org/api/bio/query/gene-associations-600trait?q=Mixed,{}"
# p_value_limit = 0.0025
p_value_limit = 0.05
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA = 'tran_upkeep'
DB_TABLE = "data_600k_gene_phenotype"
DB_TRANSLATOR_SCHEMA = "tran_test_202211"
debug = True

class GenePhenotypeAssociation:
    def __init__(self, gene, phenotype, phenotype_name, ancestry, mask, std_err, p_value, beta):
        self.gene = gene
        self.phenotype = phenotype
        self.phenotype_name = phenotype_name
        self.mask = mask
        self.std_err = std_err
        self.p_value = p_value
        self.beta = beta
        self.ancestry = ancestry

    def __str__(self):
        return "gene: {}, phenotype: {}, pValue: {}, beta: {}, mask: {}".format(self.gene, self.phenotype_name, self.p_value, self.beta, self.mask)    

    def to_array(self):
        return [self.gene, self.phenotype, self.phenotype_name, self.ancestry, self.mask, self.p_value, self.std_err, self.beta]

    def to_database(self):
        return (self.gene, self.phenotype, self.phenotype_name, self.ancestry, self.mask, self.p_value, self.std_err, self.beta)

def get_gene_list(conn):
    ''' 
    will return all the gene codes that are in the translator DB 
    '''
    result = []
    sql_string = "select node_code, ontology_id from {}.comb_node_ontology where node_type_id = 2".format(DB_TRANSLATOR_SCHEMA)

    # query the db
    cursor = conn.cursor()
    cursor.execute(sql_string)
    db_results = cursor.fetchall()

    # check
    if len(db_results) > 0:
        result = True

    # get the data
    if db_results:
        result = [[item[0], item[1]] for item in db_results]

    # return
    return result

def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA)

    # return
    return conn 

def query_web_service(url, gene, log=False):
    '''
    will query the web service and return the json
    '''
    # query the service
    response = requests.get(url.format(gene)).json()

    # return
    return response

def parse_json_response(json_input, gene, log=False):
    '''
    parses the web service response into a list of data
    '''
    # initialize
    list_associations = []
    data = json_input.get('data')

    # if there are results
    if data is not None:
        if log:
            print("for gene: {} for: {} phenotype results".format(gene, len(data)))

        # for each data list item, create and object
        for row in data:
            # for each sublist item, create and object
            for row_mask in row.get('masks'):
                object_association = GenePhenotypeAssociation(gene, row.get('phenotype'), row.get('phenotypeMeaning'), 
                    row.get('ancestry'), row_mask.get('mask'), row_mask.get('stdErr'), row_mask.get('pValue'), row_mask.get('beta'))

                # add to list
                list_associations.append(object_association)

                # log
                if False:
                    print(object_association)

    # log
    if log:
        print("for gene: {} for: {} phenotype mask results".format(gene, len(list_associations)))

    # return
    return list_associations

def delete_all_gene_associations(conn, log=False):
    ''' 
    delete all gene/phenotype associations from the database
    '''
    sql_delete = """
        delete from {}.{} 
        """.format(DB_SCHEMA, DB_TABLE)

    cur = conn.cursor()
    cur.execute(sql_delete)

    # commit
    conn.commit()


def insert_gene_associations(conn, list_gene_assoc, log=False):
    ''' 
    add gene/phenotype associations from the web service results
    '''
    sql_insert = """
        insert into {}.{} (gene_code, phenotype_code, phenotype, ancestry, mask, p_value, std_error, beta)
            values (%s, %s, %s, %s, %s, %s, %s, %s) 
        """.format(DB_SCHEMA, DB_TABLE)

    cur = conn.cursor()
    i = 0

    # loop through rows
    gene_association: GenePhenotypeAssociation
    for gene_association in list_gene_assoc:
        # log
        i += 1
        if log:
            if i % 200 == 0:
                print(gene_association)

        cur.execute(sql_insert, gene_association.to_database())

    # commit
    conn.commit()




if __name__ == "__main__":
    # initilize
    count = 0

    # get the db connection
    conn = get_connection()

    # delete the db
    delete_all_gene_associations(conn)
    if debug:
        print("deleted the old gene/phenotype associations")

    # get gene list
    list_gene = get_gene_list(conn)
    if debug:
        print("got {} genes".format(len(list_gene)))

    # debug list
    # list_gene = [['PPARG', 'stuff'] ['PCSK9', 'stuff'], ['DADA', stuff]]

    # for each gene, call the bioindex 
    for row_gene in list_gene:
        # iniatilize
        gene = row_gene[0]

        # increment the count
        count = count + 1

        # call the web service
        json_response = query_web_service(url_query_aggregator, gene)

        # get the relevant data from the response
        list_associations = parse_json_response(json_response, gene, log=True)

        # insert into the database 
        insert_gene_associations(conn, list_associations)

        # log
        if debug:
            print("{} - for gene: {} inserted row count: {}".format(count, gene, len(list_associations)))



    

