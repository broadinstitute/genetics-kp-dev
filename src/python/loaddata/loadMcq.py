# imports
import sqlite3
import glob
import csv


# constants
DIR_HOME = "/home/javaprog/Data/Broad/Translator/GeneticsPro"
DIR_DATA = "{}/MultiCurie/Jason/".format(DIR_HOME)
FILE_DB = "{}/MultiCurie/Sqlite/mcq.db".format(DIR_HOME)

# sql constants
SQL_INSERT_PHENOTYPE = "insert into mcq_phenotype (name) values(:phenotype)"
SQL_DELETE_PHENOTYPE = "delete from mcq_phenotype where name = :phenotype"

SQL_INSERT_GENE_PHENOTYPE_DATA = "insert into mcq_gene_phenotype (gene, phenotype, probability) values(:gene, :phenotype, :probability)"
SQL_DELETE_GENE_PHENOTYPE_DATA = "delete from mcq_gene_phenotype where phenotype = :phenotype"



# methods
def db_insert_phenotype(conn, phenotype, do_delete=False, log=False):
    ''' 
    inserts a phenotype into the table
    '''
    cursor = conn.cursor()

    # delete of necessary
    if do_delete:
        cursor.execute(SQL_DELETE_PHENOTYPE, {"phenotype": phenotype})


    # insert the row
    cursor.execute(SQL_INSERT_PHENOTYPE, {"phenotype": phenotype})
    conn.commit()

    # log
    print("inserted phenotype: {}".format(phenotype))


def db_insert_gene_phenotype_data(conn, phenotype, reader_data, do_delete=False, log=False):
    ''' 
    inserts a phenotype into the table
    '''
    cursor = conn.cursor()
    count = 0

    # delete of necessary
    if do_delete:
        cursor.execute(SQL_DELETE_GENE_PHENOTYPE_DATA, {"phenotype": phenotype})

    # insert the rows
    for row in reader_data:
        # Process each row
        print("for phenotype: {}, got data: {}, {}, {}".format(phenotype, row['Gene'], row['combined_D'], row['huge_score_gwas']))
        cursor.execute(SQL_INSERT_GENE_PHENOTYPE_DATA, {"phenotype": phenotype, "gene": row['Gene'], "probability": row['combined_D']})
        count = count + 1
    conn.commit()

    # log
    print("inserted {} rows for phenotype: {}".format(count, phenotype))




# main
if __name__ == "__main__":
    # connect to db
    conn = sqlite3.connect(FILE_DB)

    # list the files in the directory
    list_files = glob.glob(DIR_DATA + "*.out")
    print("got file list: {}".format(list_files))

    # for each file
    for item in list_files:
        # get the phenotype from the file name
        phenotype = item.split("/")[-1].split(".")[0]
        print("parsing phenotype: {}".format(phenotype))

        # insert the phenotype
        db_insert_phenotype(conn=conn, phenotype=phenotype, do_delete=True)

        # parse the file and insert the rows
        with open(item, 'r') as file_tsv:
            # Create a CSV DictReader object
            reader = csv.DictReader(file_tsv, delimiter='\t')
            
            # Get the fieldnames (column names)
            header = reader.fieldnames
            print("got file header: {}".format(header))

            # insert the data
            db_insert_gene_phenotype_data(conn=conn, phenotype=phenotype, reader_data=reader)

            # # Iterate over the data rows
            # for row in reader:
            #     # Process each row
            #     print("got data: {}, {}, {}".format(row['Gene'], row['combined_D'], row['huge_score_gwas']))
        
            # Get the fieldnames (column names)
            header = reader.fieldnames
            print("got file header: {}".format(header))

        # with open(item) as f:
        #     tsv_reader = csv.reader(f)

        #     # get the header
        #     list_header = next(tsv_reader)


    # close the db connection
    conn.close()
