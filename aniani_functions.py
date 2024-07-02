import configparser
import mysql.connector

# functions for the aniani application!

def read_db_config(config_file):
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