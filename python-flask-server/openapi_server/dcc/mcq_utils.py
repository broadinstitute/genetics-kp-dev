

# imports
import sqlite3

from openapi_server.models.message import Message
from openapi_server.models.query import Query
from openapi_server.models.query_graph import QueryGraph
from openapi_server.models.response import Response

from openapi_server.dcc.trapi_utils import get_biolink_version, get_trapi_version



# constants
FILE_DB = ""

DB_QUERY_GENE_PHENOTYPE = """
select gene_pheno.gene, pheno.name as phenotype, pheno.query_ontology_id as ontology_id, gene_pheno.probability
from mcq_phenotype pheno, mcq_gene_phenotype gene_pheno 
where gene_pheno.phenotype = pheno.name 
and pheno.query_ontology_id in ({})
order by gene_pheno.probability desc 
limit 20;
"""

# methods
def db_query_phenotype(conn, list_phenotypes, log=False):
    '''
    will query the sqlite db and return the data associated with the phenotypes given
    '''
    # initialize
    list_result = []
    cursor = conn.cursor()

    # Create a placeholder string for the number of values
    placeholders = ', '.join('?' for _ in list_phenotypes)

    # Construct the query
    query = DB_QUERY_GENE_PHENOTYPE.format(placeholders)

    # query
    cursor.execute(query, list_phenotypes)

    # Fetch all matching rows
    rows = cursor.fetchall()

    # get the data
    for row in rows:
        map_row = dict(row)
        list_result.append(map_row)

    # return
    return list_result


def sub_query_mcq(trapi_query: Query, log=False):
    ''' 
    respond to a trapi query
    '''
    # initialize 
    logs = ["query is lookup", "query is MANY muti curie"]
    trapi_respponse = Response(message=trapi_query.message, logs=logs, workflow=trapi_query.workflow, 
                            biolink_version=get_biolink_version(), schema_version=get_trapi_version())


    # get the inputs

    
    # get the data


    # build the response


    # return
    return trapi_respponse


# import sqlite3

# def query_database(db_path, table_name, column_name, values):
#     # Connect to the SQLite database
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Create a placeholder string for the number of values
#     placeholders = ', '.join('?' for _ in values)

#     # Construct the query
#     query = f"SELECT * FROM {table_name} WHERE {column_name} IN ({placeholders})"

#     # Execute the query with the provided values
#     cursor.execute(query, values)

#     # Fetch all matching rows
#     rows = cursor.fetchall()

#     # Close the connection
#     conn.close()

#     return rows

# # Example usage
# db_path = 'example.db'
# table_name = 'my_table'
# column_name = 'column_name'
# values = ['value1', 'value2', 'value3']

# matching_rows = query_database(db_path, table_name, column_name, values)

# for row in matching_rows:
#     print(row)



# main
if __name__ == "__main__":
    pass