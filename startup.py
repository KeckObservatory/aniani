# .py file to create a connection to the database and run sql scripts
import configparser
import pandas
import db_conn
import pdb

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
#    cursor = connection.cursor()

    try:
        with open(script_path, 'r') as file:
            sql_script = file.read()

        # each sql command is terminated with a ';'
        # strip the extra white space and execute each command before the next semicolon
        for statement in sql_script.split(';'):
            if statement.strip():
                connection.query(statement)

        print(f"sql scripts ran sucessfully!")
    
    # if something went wrong -> print out the error
    except Error as e:
        print(f"unable to run sql script: {e}")


def populate_db(my_db_conn, files):
	 
    for file in files:

        # read csv using pandas into a 'dataframe'
        dataframe = pandas.read_csv(file)

        # grap the col names for insert statement
        dataframe.columns.tolist()
        # pdb.set_trace()

        table_name = file.replace('.csv', '').replace('csv/', '')
        # Show columns for the specified table
        my_conn = my_db_conn.conn.cursor()
        my_conn.execute(f'select * from {table_name} limit 0;')
        col_names = [desc[0] for desc in my_conn.description]
        col_names = col_names[1:]
        num_cols = len(col_names)
        col_cnt = ', '.join(['%s']*len(col_names))
        col_names = ', '.join(col_names)


        # Insert rows into the database
        pdb.set_trace()
        for row in dataframe.itertuples(index=False):
            # Convert 'null' strings to None (which will be NULL in MySQL/MariaDB)   
            # pdb.set_trace()
            #row_values = [None if value == 'null' else value for value in row]
            row_values = [None if pandas.isna(value) else value for value in row]

            try:
                assert len(row_values) == num_cols
            except:
                pdb.set_trace()
                print()
            insert_query = f"INSERT INTO {table_name} ({col_names}) VALUES ({col_cnt})"
            my_db_conn.query(insert_query, tuple(row_values))
        





if __name__ == "__main__":


    pdb.set_trace()
    connection = db_conn.db_conn('config.live.ini','acs')
    assert connection.errors == None, 'Error connecting to database'

 
    csv_insert_files = ['csv/MirrorSamples.csv', 'csv/CalibrationChecks.csv']
    #csv_insert_files = [ 'csv/CalibrationChecks.csv']
    populate_db(connection,csv_insert_files)


   #  if create:
        # to create or delete the db and tables
        # run_sql_script(connection, 'create-db.sql')

        # populate the db with already existing data
        # grab csv files with data in them 

        #populate_db(db_config, connection, csv_insert_files)

       #  connection.close()


    







 

