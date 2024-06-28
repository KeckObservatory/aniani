# .py file to create a connection to the database and run sql scripts
import configparser
import mysql.connector
from mysql.connector import Error
import pandas

def read_config(config_file):

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

    return db_config


def create_db_connection(db_config):

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

    use_query = f"USE {db_config['database']};"
    cursor.execute(use_query)

    for file in files:

        # read csv using pandas into a 'dataframe'
        dataframe = pandas.read_csv(file)

        # grap the col names for insert statement
        dataframe.columns.tolist()
        col_names = ', '.join(dataframe.columns)
        col_cnt = ', '.join(['%s']*len(dataframe.columns))
        table_name = file.replace('.csv', '').replace('csv/', '')


        insert_query = f"INSERT INTO {table_name} ({col_names}) VALUES ({col_cnt})"

        # Insert rows into the database
        for row in dataframe.itertuples(index=False):
            # Convert 'null' strings to None (which will be NULL in MySQL/MariaDB)
            #row_values = [None if value == 'null' else value for value in row]
            row_values = [None if pandas.isna(value) else value for value in row]
            cursor.execute(insert_query, tuple(row_values))
        
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
        csv_insert_files = ['csv/CommentLog.csv', 'csv/CalibrationCertifiedReference.csv']

        populate_db(db_config, connection, csv_insert_files)

        connection.close()

    else:
        run_sql_script(connection, 'delete-db.sql')
        connection.close()



    







 

