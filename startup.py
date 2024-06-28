# .py file to create a connection to the database and run sql scripts
import configparser
import mysql.connector
from mysql.connector import Error
import pandas

def read_config(config_file):
    """
    Function to read the config file.

    :param config_file: path to the config file
    :type config_file: str
    :return: a dict with all extracted config attributes
    :rtype: dict
    """

    # read the config file
    config = configparser.ConfigParser()
    config.read(config_file)

    # grab the information from the config file
    db_config = {
        'host': config.get('mysql', 'host'),
        'port': config.getint('mysql', 'port'),
        'admin_username': config.get('mysql', 'username'),
        'admin_password': config.get('mysql', 'password'),
        'database': config.get('mysql', 'database')
    }

    # return the dict
    return db_config


def create_db_connection(db_config):
    """
    Function to create a mysql/python connection to access db

    :param db_config: dict with all the config attributes from read_config()
    :type db_config: dict
    :return: the connection between python and the database
    :rtype: connection object?
    """

    # create the connection to db 
    connection = mysql.connector.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['admin_username'],
        password=db_config['admin_password']
    )

    # returning the connection
    return connection


def run_sql_script(connection, script_path):
    """
    Function to run a specified sql script with the db connection to aniani.

    :param connection: connection to aniani db
    :type connection: mysql connection
    :param script_path: path to sql script wanted to run
    :type script_path: str
    """
    cursor = connection.cursor()

    try:
        with open(script_path, 'r') as file:
            sql_script = file.read()

        # each sql command is terminated with a ';'
        # strip the extra white space and execute each command before the next semicolon
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)

        print(f"sql scripts ran sucessfully!")
        cursor.close()
    
    # if something went wrong -> print out the error
    except Error as e:
        print(f"unable to run sql script: {e}")


def populate_db(db_config, connection, files):

    cursor = connection.cursor()

    # using the correct db from the config file
    # sql use -> so all further operations are on the correct db
    use_query = f"USE {db_config['database']};"
    cursor.execute(use_query)

    for file in files:

        # read csv using pandas into a 'dataframe'
        dataframe = pandas.read_csv(file)

        # grab the table name from the csv file name without the directory info
        table_name = file.replace('.csv', '').replace('csv/', '')
        print(table_name)

        # Show columns for the specified table
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = cursor.fetchall()

        # extract column names into a list
        # columns is a list of [0]'col name', [1]'type', [3]'is primary key' more properties...
        # csv does not have primary key -> don't need a col for it
        col_names = [col[0] for col in columns if col[3] != 'PRI']

        # join the colum names for the insert statement
        col_names = ', '.join(col_names)

        # grab the length of the col name list to find out how many cols per table
        # join together a list of '%s' with as many as the col names
        # so sql knows how many values it is expecting 
        col_cnt = ', '.join(['%s']*len(dataframe.columns))

        # query string 
        insert_query = f"INSERT INTO {table_name} ({col_names}) VALUES ({col_cnt})"

        # insert statement for each row of the csv at a time
        for row in dataframe.itertuples(index=False):
        
            # if there is not a value -> set it to null in the sql table
            row_values = [None if pandas.isna(value) else value for value in row]

            cursor.execute(insert_query, tuple(row_values))
        
        # commit changes to the db
        connection.commit()

    cursor.close()




if __name__ == "__main__":

    db_config = read_config('config.live.ini')

    connection = create_db_connection(db_config)

    create = True

    if create:
        # to create or delete the db and tables
        run_sql_script(connection, 'create-db.sql')

        # populate the db with already existing data
        # grab csv files with data in them 
        csv_insert_files = ['csv/CalibrationChecks.csv', 'csv/MirrorSamples.csv']

        populate_db(db_config, connection, csv_insert_files)

        connection.close()

    else:
        run_sql_script(connection, 'delete-db.sql')
        connection.close()



    







 

