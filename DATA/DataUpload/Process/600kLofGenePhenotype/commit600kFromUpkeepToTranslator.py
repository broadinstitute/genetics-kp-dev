
# imports
import csv 
import pandas as pd 
import pymysql as mdb
import os
import requests 


# constants
debug = True
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA_UPKEEP = 'tran_upkeep'
DB_SCHEMA_TRANSLATOR = 'tran_test_202302'
DB_TABLE_UPKEEP = "data_600k_phenotype_ontology"
DB_TABLE_TRANSLATOR_EDGE = "comb_edge_node"
DB_TABLE_TRANSLATOR_QUALIFIER = "comb_edge_qualifier"
STUDY_ID = 18

def delete_from_translator_table(conn, study_id, log=False):
    '''
    will delete the table data 
    '''
    sql_delete = """
        delete from {}.{} where study_id = %s
        """
    sql_delete_edge = sql_delete.format(DB_SCHEMA_TRANSLATOR, DB_TABLE_TRANSLATOR_EDGE)
    sql_delete_qualifier = sql_delete.format(DB_SCHEMA_TRANSLATOR, DB_TABLE_TRANSLATOR_QUALIFIER)

    cur = conn.cursor()
    cur.execute(sql_delete_edge, (STUDY_ID))
    cur.execute(sql_delete_qualifier, (STUDY_ID))

    # commit
    conn.commit()

def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA_TRANSLATOR)

    # return
    return conn 

def print_count_of_edges(conn, study_id, log=False):
    '''
    prints the number of edges from this study
    '''
    sql_count = """
        select count(id) from {}.{} where study_id = {}
        """.format(DB_SCHEMA_TRANSLATOR, DB_TABLE_TRANSLATOR_EDGE, study_id)

    cur = conn.cursor()
    cur.execute(sql_count)
    db_results = cur.fetchone()

    # check
    if len(db_results) > 0:
        result = True

    # get the data
    if db_results:
        print("for study: {} have edge row count:{}".format(study_id, db_results[0]))


def get_phenotype_node(conn, phenotype_id, log=False):
    '''
    gets the phenotype node id based on ontology_id
    '''
    # initialize
    node = None 
    sql_select = "select id, ontology_id, node_name from {}.comb_node_ontology where ontology_id = %s".format(DB_SCHEMA_TRANSLATOR)

    # get the node
    cur = conn.cursor()
    cur.execute(sql_select, (phenotype_id))
    db_results = cur.fetchone()

    if db_results:
        node = {'id': db_results[0], 'ontology_id': db_results[1],  'name': db_results[2]}

    # return
    return node

def get_gene_node(conn, gene_code, log=False):
    '''
    gets the gene db node from the gene name 
    '''
    node = None 
    sql_select = "select id, ontology_id, node_code from {}.comb_node_ontology where node_code = %s".format(DB_SCHEMA_TRANSLATOR)

    # get the node
    cur = conn.cursor()
    cur.execute(sql_select, (gene_code))
    db_results = cur.fetchone()

    if db_results:
        node = {'id': db_results[0], 'ontology_id': db_results[1],  'name': db_results[2]}
        
    # return
    return node


def add_edge(conn, gene, phenotype_ontology_id, phenotype_type, phenotype_code, phenotype_name, p_value, beta, log=False):
    '''
    inserts a edge into the translator DB (edge, node, qualifiers)
    '''
    # initialize
    node_phenotype = None
    node_gene = None 
    id_gene_condition_edge = 5
    id_condition_gene_edge = 10
    id_new_edge = None
    sql_edge_insert = """
    insert into {}.comb_edge_node (edge_id, source_node_id, target_node_id, edge_type_id, score, score_type_id, study_id, has_qualifiers)
    values(concat('600k_', %s, '_', %s), %s, %s, %s, %s, 8, %s, 'Y')
    """.format(DB_SCHEMA_TRANSLATOR)
    sql_select_edge = """
    select id from {}.comb_edge_node where source_node_id = %s and target_node_id = %s and edge_type_id = %s and study_id = %s
    """.format(DB_SCHEMA_TRANSLATOR)
    sql_qualifier_insert = """
    insert into comb_edge_qualifier (edge_id, qualifier_id, study_id) values (%s, %s, %s)
    """

    # get phenotype node id 
    node_phenotype = get_or_insert_phenotype(conn, phenotype_ontology_id, phenotype_type, phenotype_code, phenotype_name)

    # get gene node id 
    node_gene = get_gene_node(conn, gene)

    # insert the edge row
    # insert the gene to condition row
    cur = conn.cursor()
    cur.execute(sql_edge_insert, (node_gene.get('id'), node_phenotype.get('id'), node_gene.get('id'), node_phenotype.get('id'), id_gene_condition_edge, p_value, STUDY_ID))

    # find the id of the recntly inserted row
    cur.execute(sql_select_edge, (node_gene.get('id'), node_phenotype.get('id'), id_gene_condition_edge, STUDY_ID))
    db_results = cur.fetchone()
    id_new_edge = db_results[0]

    # insert the qualifiers
    # subject activity decreased, object severity decreased/increased, predicate causes
    cur.execute(sql_qualifier_insert, (id_new_edge, 'subject_aspect_activity', STUDY_ID))
    cur.execute(sql_qualifier_insert, (id_new_edge, 'subject_direction_decreased', STUDY_ID))
    cur.execute(sql_qualifier_insert, (id_new_edge, 'object_aspect_severity', STUDY_ID))
    if beta < 0:
        # opposite direction of subject
        cur.execute(sql_qualifier_insert, (id_new_edge, 'object_direction_increased', STUDY_ID))
    else:
        # same direction of subject
        cur.execute(sql_qualifier_insert, (id_new_edge, 'object_direction_decreased', STUDY_ID))
    cur.execute(sql_qualifier_insert, (id_new_edge, 'qualified_predicate_causes', STUDY_ID))

    # log
    if log:
        print("inserted edges: {} and gene: {} at edge: {}".format(node_gene, node_phenotype, id_new_edge))


    # insert the condition to gene row 
    cur = conn.cursor()
    cur.execute(sql_edge_insert, (node_phenotype.get('id'), node_gene.get('id'), node_phenotype.get('id'), node_gene.get('id'), id_condition_gene_edge, p_value, STUDY_ID))

    # find the id of the recntly inserted row
    cur.execute(sql_select_edge, (node_phenotype.get('id'), node_gene.get('id'), id_condition_gene_edge, STUDY_ID))
    db_results = cur.fetchone()
    id_new_edge = db_results[0]

    # insert the qualifiers
    # subject activity decreased, object severity decreased/increased, predicate causes
    cur.execute(sql_qualifier_insert, (id_new_edge, 'object_aspect_activity', STUDY_ID))
    cur.execute(sql_qualifier_insert, (id_new_edge, 'object_direction_decreased', STUDY_ID))
    cur.execute(sql_qualifier_insert, (id_new_edge, 'subject_aspect_severity', STUDY_ID))
    if beta < 0:
        # opposite direction of subject
        cur.execute(sql_qualifier_insert, (id_new_edge, 'subject_direction_increased', STUDY_ID))
    else:
        # same direction of subject
        cur.execute(sql_qualifier_insert, (id_new_edge, 'subject_direction_decreased', STUDY_ID))
    cur.execute(sql_qualifier_insert, (id_new_edge, 'qualified_predicate_caused_by', STUDY_ID))

    # commit
    conn.commit()

    # log
    if log:
        print("inserted edges: {} and gene: {} at edge: {}".format(node_phenotype, node_gene, id_new_edge))

    
def get_or_insert_phenotype(conn, ontology_id, node_type, phenotype_code, phenotype_name, log=True):
    ''' 
    will insert phenotype into the translator node table 
    '''
    sql_insert = '''
    insert into {}.comb_node_ontology (node_code, node_type_id, ontology_id, ontology_type_id, node_name, added_by_study_id)
    values(%s, 
        (select type_id from comb_lookup_type where type_name = %s), 
        %s,
        (select ontology_id from comb_ontology_type where substring_index(%s, ':', 1) = prefix),
        %s, 
        %s)
    '''.format(DB_SCHEMA_TRANSLATOR)

    # get the phenotype
    phenotype = get_phenotype_node(conn, ontology_id)

    # if no phenotype by that curie, insert 
    if not phenotype:
        cur = conn.cursor()
        cur.execute(sql_insert, (phenotype_code, node_type, ontology_id, ontology_id, phenotype_name, STUDY_ID))

        # log
        if log:
            print("inserted phenotype: {} with curie: {} and name: {}".format(ontology_id, phenotype_name, phenotype_name))
            conn.commit()

    # get phenotype
    phenotype = get_phenotype_node(conn, ontology_id)

    # return 
    return phenotype


if __name__ == "__main__":
    # get the connection
    connection = get_connection()

    # count the current translator 600k data 
    print_count_of_edges(connection, STUDY_ID)

    # delete from the translator data the previous data
    delete_from_translator_table(connection, STUDY_ID)

    # count the current translator 600k data 
    print_count_of_edges(connection, STUDY_ID)

    # insert the new data

    # count the current translator 600k data 
    print_count_of_edges(connection, STUDY_ID)

    count = 0
    sql_edges = """
    select link.id, link.gene_code, phenotype.phenotype_code, phenotype.phenotype_ontology_id, 
    phenotype.node_type, phenotype.phenotype_translator_name,
    link.ancestry, link.mask, link.p_value, link.beta
    from tran_upkeep.data_600k_gene_phenotype link, tran_upkeep.data_600k_phenotype_ontology phenotype 
    where link.phenotype_code = phenotype.phenotype_code
    and link.p_value < 0.0025 and link.mask = 'LoF_HC'
    order by link.phenotype_code
    """
    cursor = connection.cursor()
    cursor.execute(sql_edges)
    db_results = cursor.fetchall()
    for row in db_results:
        count = count + 1
        print("\n{} - {}".format(count, len(db_results)))
        map_input = {'conn':connection, 'gene':row[1], 'phenotype_ontology_id':row[3], 'phenotype_type':row[4], 'phenotype_code':row[2], 
            'phenotype_name':row[5], 'p_value':row[8], 'beta':row[9], 'log':True}
        # print("test input: {}".format(map_input))
        add_edge(**map_input)


    # test
    if False:
        # get gene
        # gene_code = 'PPARG'
        # result = get_gene_node(connection, gene_code)
        # print("for: {} got: {}".format(gene_code, result))

        # # get gene
        # gene_code = 'YOYO'
        # result = get_gene_node(connection, gene_code)
        # print("for: {} got: {}".format(gene_code, result))

        # # get phenotype
        # phenotype_id = 'MONDO:0005148'
        # result = get_phenotype_node(connection, phenotype_id)
        # print("for: {} got: {}".format(phenotype_id, result))

        # # test insert of phenotype
        # # get_or_insert_phenotype(connection, p 'MONDO:0015978', 'functional neutrophil defect', log=True)
        # get_or_insert_phenotype(conn=connection, node_type='biolink:Disease', ontology_id='MONDO:015978', phenotype_code='test015978', phenotype_name='functional neutrophil defect', log=True)

        # test insert of one pair of edges
        sql_test = """
        select link.id, link.gene_code, phenotype.phenotype_code, phenotype.phenotype_ontology_id, 
        phenotype.node_type, phenotype.phenotype_translator_name,
        link.ancestry, link.mask, link.p_value, link.beta
        from tran_upkeep.data_600k_gene_phenotype link, tran_upkeep.data_600k_phenotype_ontology phenotype 
        where link.phenotype_code = phenotype.phenotype_code
        and link.id = 21331947
        order by link.p_value;
        """
        cursor = connection.cursor()
        cursor.execute(sql_test)
        row = cursor.fetchone()
        map_input = {'conn':connection, 'gene':row[1], 'phenotype_ontology_id':row[3], 'phenotype_type':row[4], 'phenotype_code':row[2], 
            'phenotype_name':row[5], 'p_value':row[8], 'beta':row[9], 'log':True}
        print("test input: {}".format(map_input))
        add_edge(**map_input)

# def add_edge(conn, gene, phenotype_ontology_id, phenotype_type, phenotype_code, phenotype_name, p_value, beta, log=False):


# 20230209 - pre load 
# +------------+----------+------------------------+
# | edge_count | study_id | study_name             |
# +------------+----------+------------------------+
# |     899006 |        1 | Magma                  |
# |      72216 |        4 | Richards Effector Gene |
# |       2217 |        5 | ClinGen                |
# |       9160 |        6 | ClinVar                |
# |      12756 |        7 | genCC                  |
# |      34318 |       17 | GeneBass               |
# +------------+----------+------------------------+
# 6 rows in set (2.17 sec)

# 20230209 - post load 
