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

# methods
def db_insert_phenotype(conn, phenotype, log=False):
    ''' 
    inserts a phenotype into the table
    '''
    cursor = conn.cursor()

    # insert the row
    cursor.execute(SQL_INSERT_PHENOTYPE, {"phenotype": phenotype})
    conn.commit()

    # log
    print("inserted phenotype: {}".format(phenotype))


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
        db_insert_phenotype(conn=conn, phenotype=phenotype)

        # parse the file and insert the rows
        with open(item, 'r') as file_tsv:
            # Create a CSV DictReader object
            reader = csv.DictReader(file_tsv, delimiter='\t')
            
            # Get the fieldnames (column names)
            header = reader.fieldnames
            print("got file header: {}".format(header))
            
            # Iterate over the data rows
            for row in reader:
                # Process each row
                print("got data: {}, {}, {}".format(row['Gene'], row['combined_adj'], row['huge_score_gwas']))
        
            # Get the fieldnames (column names)
            header = reader.fieldnames
            print("got file header: {}".format(header))

        # with open(item) as f:
        #     tsv_reader = csv.reader(f)

        #     # get the header
        #     list_header = next(tsv_reader)


    # close the db connection
    conn.close()
