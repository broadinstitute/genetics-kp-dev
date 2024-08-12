
# imports
import requests
import pymysql as mdb
from datetime import datetime
import os
import time 

# constants
url_query_aggregator = "https://bioindex-dev.hugeamp.org/api/bio/query/pigean-gene?q={},2,small"
# p_value_limit = 0.0025
p_value_limit = 0.05
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA = 'tran_upkeep'
TIME_SLEEP = 1

# metthods
def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA)

    # return
    return conn 


def get_gene_list(conn, is_incremental=False, log=False):
    ''' 
    will return all the gene codes that are in the translator DB 
    '''
    result = []
    sql_string = "select node_code, ontology_id from {}.agg_gene".format(DB_SCHEMA)

    if is_incremental:
        sql_string = """
        select gene.node_code, gene.ontology_id from {}.agg_gene gene where not exists (select id from {}.agg_gene_phenotype_pigean magma where magma.gene_code = gene.node_code collate utf8mb4_unicode_ci)
        """.format(DB_SCHEMA, DB_SCHEMA)

    # query the db
    cursor = conn.cursor()
    cursor.execute(sql_string)
    db_results = cursor.fetchall()

    # check
    if len(db_results) > 0:
        result = True

    # get the data
    if db_results:
        result = [{'gene': item[0], 'ontology_id': item[1]} for item in db_results]

    # return
    return result


def delete_gene_associations_pigean(conn):
    ''' 
    delete the gene/phenotype associations from the agregator load table
    '''
    sql_delete = """
    delete from {}.agg_gene_phenotype_pigean 
    """.format(DB_SCHEMA)

    # delete the data
    cur = conn.cursor()
    cur.execute(sql_delete)

    # commit
    conn.commit()


def insert_gene_associations(conn, list_gene_assoc, log=False):
    ''' 
    add gene/phenotype associations from the agregator results
    '''
    sql_insert = """
        insert into {}.agg_gene_phenotype_pigean (gene_code, phenotype_code, score_huge, prob_combined) values(%s, %s, %s, %s) 
        """.format(DB_SCHEMA)

    cur = conn.cursor()

    i = 0
    # loop through rows
    for gene_association in list_gene_assoc:
        # initialize

        # get the lookup date
        phenotype = gene_association.get('phenotype')
        gene = gene_association.get('gene')
        probability = gene_association.get('prob_combined')
        hugeScore = gene_association.get('score_huge')

        # log
        i += 1
        if log:
            if i % 300 == 0:
                print("inserted gene: {}, phenotype: {}, probability: {}".format(gene, phenotype, probability))

        cur.execute(sql_insert, (gene, phenotype, hugeScore, probability))

    # commit
    conn.commit()


def log_gene_associations_data_counts(conn):
    '''
    method to print out the number of gene/phenotype associations
    '''
    sql_count = "select count(id) from {}.{}"

    # log the number
    cursor = conn.cursor()
    sql_to_run = sql_count.format(DB_SCHEMA, "agg_gene_phenotype_pigean")
    cursor.execute(sql_to_run)
    results = cursor.fetchall()

    for row in results:
        print("for: {} got row count: {}".format("gene/phenotype", row[0]))
    # print("for: {} got row count: {}".format(key, results))


def rest_get_gene_associations(map_gene, log=True):
    '''
    will query the bioindex rest service for te gene/phenotype association data
    '''
    # initialize
    list_result = []
    list_data = []
    gene = map_gene.get('gene')

    # query the service
    response = requests.get(url_query_aggregator.format(gene)).json()
    list_data = response.get('data')

    # loop and build list
    for row in list_data:
        list_result.append({'gene': row.get('gene'), 'phenotype': row.get('phenotype'), 'score_huge': row.get('huge_score'), 
                            'prob_combined': row.get('combined')})

    # log
    if log:
        print("for gene: {} got results of count: {}".format(gene, len(list_data)))
              
    # return
    return list_result


# main
if __name__ == "__main__":
    # count for testing 
    num_count = -1
    is_incremental = True

    # get the db connection
    conn = get_connection()
    count_gene = 0

    # log
    log_gene_associations_data_counts(conn)

    # delete the existing data
    if not is_incremental:
        print("deleting table tran_upkeep.agg_gene_phenotype_pigean")
        delete_gene_associations_pigean(conn)

    # get the genes
    list_gene = get_gene_list(conn, is_incremental=is_incremental)

    # test gene list
    # list_gene = [{'gene': 'PPARG', 'ontology_id': 'dude'}, {'gene': 'PCSK9', 'ontology_id': 'dude'}]
    # list_gene = [['SEP15'], [12618]]
    
    # log
    print("got gene list of size {}".format(len(list_gene)))
    
    # test the check_phenotype method
    num_genes = len(list_gene)
    # assert (num_genes > 19000) == True

    # log
    # print_num_phenotypes_for_gene_in_db(conn, list_gene[0][0], list_gene[1][0])

    # get the phenotypes pvalues for the gene from the bioindex
    for gene in list_gene:
        if num_count < 0 or count_gene < num_count:
            count_gene = count_gene + 1

            # get the gene data
            list_data = rest_get_gene_associations(map_gene=gene)

            # insert the data in the upkeep db
            insert_gene_associations(conn=conn, list_gene_assoc=list_data)

            # json_association = query_gene_assocations_service(gene[0], url_query_aggregator)
            # map_phenotype = get_phenotype_values(json_association)
            # json_bayes = query_gene_bayes_service(gene[0], url_query_aggregator)
            # map_phenotype = add_bayes_values(json_bayes, map_phenotype)
            print("for {}/{} - {} got new gene/phenotype associations of size {}\n".format(count_gene, num_genes, gene.get('gene'), len(list_data)))

            # sleep
            time.sleep(TIME_SLEEP)

    # log
    log_gene_associations_data_counts(conn)






# def insert_all_gene_aggregator_data(conn, map_phenotype,  log=False):
#     ''' 
#     will query the aggregator for all disease/phentype gene magma association data for all genes in the translator DB 
#     '''

#     # initialize
#     cursor = conn.cursor()

#     # sql to get all the genes in the translator DB
#     sql_select = "select id, node_code from comb_node_ontology where node_type_id = 2 order by node_code"
#     count = 0

#     # get the list of genes
#     cursor.execute(sql_select)print
#     db_results = cursor.fetchall()

#     # loop for each gene
#     for item in db_results:
#         gene_id = item[0]
#         gene = item[1]
#         count += 1

#         # get the aggregator data
#         result_json = query_gene_assocations_service(gene, url_query_aggregator)
#         phenotype_list = get_phenotype_values(result_json, p_value_limit)

#         # log
#         if log:
#             print("\n{} - {}".format(count, len(db_results)))
#             print_num_phenotypes_for_gene_in_db(conn, gene, gene_id)
#             print("for {} got new gene associations of size {}".format(gene, len(phenotype_list)))

#         # insert into the db
#         # insert_or_update_gene_data(conn, phenotype_list, gene, gene_id, map_phenotype, log=True)
#         insert_or_update_gene_data(conn, phenotype_list, gene, gene_id, map_phenotype, log=True)

#         # log
#         if log:
#             print_num_phenotypes_for_gene_in_db(conn, gene, gene_id)

# def build_phenotype_map(conn, log=False):
#     ''' will query the aggregator for all disease/phentype gene magma association data for all genes in the translator DB '''
#     cursor = conn.cursor()
#     sql_select = "select id, node_code from comb_node_ontology where node_type_id in (1, 3, 12) order by node_code"
#     map_phenotype = {}

#     # get the list of genes
#     cursor.execute(sql_select)
#     db_results = cursor.fetchall()

#     # loop for each gene
#     for item in db_results:
#         map_phenotype[item[1]] = item[0]

#     # log
#     if log:
#         print("got phenotype map size of {}".format(len(map_phenotype)))

#     # return
#     return map_phenotype


# def calc_prob_from_bayes(bayes_factor, log=False):
#     '''
#     calculate the probabilty from the bayes factor using a prior of 0.05
#     '''
#     prior = 0.05
#     probability = 0

#     if bayes_factor:
#         # calculate the prior odds
#         odds = (bayes_factor * prior) / (1.0 - prior)

#         # calculate the probability
#         probability = odds / (1 + odds)

#     # log
#     if log:
#         print("bayes: {}, odds: {}, probability: {}".format(bayes_factor, odds, probability))

#     # return 
#     return probability 

# def add_bayes_values(json_bayes, map_association, log=False):
#     '''
#     will take the bayes json and add the data to the association map
#     '''
#     list_data = json_bayes.get('data').get('Huge')

#     if list_data:
#         for row in list_data:
#             # for the row, get the phenotype update the map after verifying the gene 
#             map_pheno = map_association.get(row.get('phenotype'))
#             if map_pheno:
#                 if map_pheno.get('gene') == row.get('gene'):
#                     map_pheno.update(row)

#     # return 
#     return map_association


# def get_phenotype_values(input_json):
#     ''' 
#     will parse the graphql output and generate phenotype/pValue tupes list 
#     '''
#     query_key = 'GeneAssociations'
#     data = input_json.get('data').get(query_key)
#     result = {}

#     # loop
#     if data is not None:
#         # result = [(item.get('gene'), item.get('phenotype'), item.get('pValue')) for item in data]
#         # result = [{'gene'; item.get('gene'), 'phenotype': item.get('phenotype'), 'pValue': item.get('pValue')} for item in data if item.get('pValue') <  p_value_limit]
#         for row in data:
#             result[row.get('phenotype')] = row

#     # rerurn
#     return result


# def print_num_phenotypes_in_db(conn):
#     ''' 
#     will query and print the count of phenotypes in the db 
#     '''
#     # initialize
#     sql = """
#     select count(*) from comb_node_ontology where node_type_id in (1, 3, 12)
#     """
#     cursor = conn.cursor()
#     count = 0

#     # call the query
#     cursor.execute(sql)
#     db_results = cursor.fetchall()

#     # get the data
#     if db_results:
#         count = db_results[0][0]

#     # print
#     print("the are {} phenotypes/diseases in the translator db".format(count))


# def print_num_phenotypes_for_gene_in_db(conn, gene, gene_id):
#     ''' 
#     will query and print the count of phenotypes for the gene in the translator db 
#     '''
#     # initialize
#     sql = """
#     select count(id) from {}.comb_edge_node where source_node_id = %s and study_id = 1
#     """.format(DB_TRANSLATOR_SCHEMA)
#     cursor = conn.cursor()
#     count = 0

#     # call the query
#     cursor.execute(sql, (gene_id))
#     db_results = cursor.fetchall()

#     # get the data
#     if db_results:
#         count = db_results[0][0]

#     # print
#     print("for gene {} the are {} phenotypes/diseases in the translator db".format(gene, count))



# def query_gene_assocations_service(input_gene, url):
#     ''' 
#     queries the service for disease/chem relationships 
#     '''
#     # build the query
#     query_string = """
#     query {
#         GeneAssociations(gene: "%s") {
#             phenotype, gene, pValue, zStat, type
#         }
#     }
#     """ % (input_gene)

#     # query the service
#     response = requests.post(url, data=query_string).json()

#     # return
#     return response

# def query_gene_bayes_service(input_gene, url):
#     ''' 
#     queries the service for disease/chem relationships 
#     '''
#     # build the query
#     query_string = """
#     query {
#         Huge(gene: "%s") {
#             gene, phenotype, bf_rare, huge, bf_common
#         }
#     }
#     """ % (input_gene)

#     # query the service
#     response = requests.post(url, data=query_string).json()

#     # return
#     return response


# def insert_gene_associations(conn, map_gene_assoc, log=False):
#     ''' 
#     add gene/phenotype associations from the agregator results
#     '''
#     sql_insert = """
#         insert into {}.agg_gene_phenotype (gene_code, phenotype_code, gene_type, z_stat, p_value,
#             values (%s, %s, %s, %s, %s) 
#         """.format(DB_SCHEMA)

#     cur = conn.cursor()

#     i = 0
#     # loop through rows
#     for gene_association in map_gene_assoc.values():
#         # initialize

#         # get the lookup date
#         phenotype = gene_association.get('phenotype')
#         gene = gene_association.get('gene')
#         pValue = gene_association.get('pValue')
#         zStat = gene_association.get('zStat')
#         geneType = gene_association.get('type')

#         # # calculate
#         # if gene_association.get('bf_common'):
#         #     abf_common = float(gene_association.get('bf_common'))
#         #     prob_common = calc_prob_from_bayes(abf_common)

#         # if gene_association.get('bf_rare'):
#         #     abf_rare = float(gene_association.get('bf_rare'))
#         #     prob_rare = calc_prob_from_bayes(abf_rare)

#         # if gene_association.get('huge'):
#         #     abf_combined = float(gene_association.get('huge'))
#         #     prob_combined = calc_prob_from_bayes(abf_combined, log=False)

#         # log
#         i += 1
#         if log:
#             if i % 300 == 0:
#                 print("inserted gene: {}, phenotype: {}, pValue: {}".format(gene, phenotype, pValue))

#         cur.execute(sql_insert, (gene, phenotype, geneType, zStat, pValue))

#     # commit
#     conn.commit()



