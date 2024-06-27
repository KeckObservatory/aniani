# .py file to create a connection to the database and run sql scripts
import configparser
import mysql.connector
from mysql.connector import Error



def create_db_connection():
    """
    Function to create the database connection for the mysql maria db

    :return: connection to aniani db     
    :rtype: mysql connection
    """

    # read the config file
    config = configparser.ConfigParser()
    config.read('config.live.ini')

    # grab the information from the config file
    db_config = {
        'host': config.get('mysql', 'host'),
        'port': config.getint('mysql', 'port'),
        'admin_username': config.get('mysql', 'username'),
        'admin_password': config.get('mysql', 'password'),
        'database': config.get('mysql', 'database')
    }

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

    # need cursor object to run queries
    cursor = connection.cursor()

    try:
        with open(script_path, 'r') as file:
            sql_script = file.read()

        # each sql command is terminated with a ';'
        # strip the extra white space and execute each command before the next semicolon
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)

        print(f"sql script run sucessfully!")
    
    # if something went wrong -> print out the error
    except Error as e:
        print(f"unable to run sql script: {e}")




if __name__ == "__main__":

    connection = create_db_connection()

    # to create the db and tables
    run_sql_script(connection, 'create-db.sql')

    # to delete the db and tables 
    # run_sql_script(connection, 'delete-db.sql')





 

