

# imports
import csv 
import pandas as pd 
import pymysql as mdb
import os
import requests 
import math
import numpy as np

# constants
debug = True
DB_PASSWD = os.environ.get('DB_PASSWD')
DB_SCHEMA_UPKEEP = 'tran_upkeep'
DB_TABLE_UPKEEP = "data_600k_gene_phenotype"


# methods
def calculate_abf(standard_error, effect_size, variance=0.396):
    ''' calculates the approximate bayes factor '''
    V = standard_error ** 2

    # calculate result
    left_side = math.sqrt(V / (V + variance))
    # exp_num = (variance * effect_size ** 2) / 2 * V * (V + variance)
    # print("got exp: {}".format(exp_num))
    right_side = np.exp((variance * effect_size ** 2) / 2 * V * (V + variance))
    result = left_side * right_side

    # return
    return result

def convert_abf_to_probability(abf):
    ''' converts the approximate bayes factor to a probability '''
    PO = (0.05 / 0.95) * abf
    probability = PO / (1 + PO)

    # return
    return probability


def calc_probabilty(list_association, log=False):
    '''
    inserts the calculated probability in the db row
    '''
    for row in list_association:
        # print("got row: {}".format(row))
        abf = calculate_abf(standard_error=row['se'], effect_size=row['beta'])
        probability = convert_abf_to_probability(abf)
        row['prob'] = probability

def get_connection():
    ''' 
    get the db connection 
    '''
    conn = mdb.connect(host='localhost', user='root', password=DB_PASSWD, charset='utf8', db=DB_SCHEMA_UPKEEP)

    # return
    return conn 

def get_data(conn, num_batch, log=False):
    '''
    get the rows
    '''
    list_data = []

    # get the data
    sql_select = """
    select id, std_error, beta from data_600k_gene_phenotype 
    where std_error is not null and beta is not null
    and mask = 'LoF_HC'
    limit {}
    """.format(num_batch)

    cursor = conn.cursor()
    cursor.execute(sql_select)
    db_results = cursor.fetchall()

    # loop
    for row in db_results:
        list_data.append({'id': row[0], 'se': row[1], 'beta': row[2]})

    # return
    return list_data

def save_data(conn, list_row, log=False):
    '''
    save the data
    '''
    sql_update = "update data_600k_gene_phenotype set probability_calculated = %s where id = %s"

    # loop
    cursor = conn.cursor()
    for row in list_row:
        # cursor.execute(sql_update, (row['prob'], row['id']))
        try:
            cursor.execute(sql_update, (str(row['prob'].item()).encode('utf-8','ignore'), row['id']))
        except mdb.err.DataError:
            pass

    # commit
    conn.commit()

if __name__ == "__main__":
    num_batch = 1000

    # get the connection
    connection = get_connection()

    for i in range
    # get the data
    list_association = get_data(connection, num_batch)

    # calculate the probability
    calc_probabilty(list_association)

    # save the calculated data
    save_data(connection, list_association)

