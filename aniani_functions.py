import configparser
import mysql.connector
import datetime

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


def get_reflectivity_status(connection, tel_num, mirror):
    """
    Function to return the latest reflectivity data for the primary mirror.
    Just plain data (no math done to it yet), simply the most recent values
    for each wavelength for each position on the primary mirror.        

    :param connection: mysql db connection
    :type connection: object
    :return: dictionary of the form with #s 0-151 (for all mirrors)
        {
            #: {
                install_date
                measurement_type
                mirror
                mirror_type
                reflectivity
                segment_id
                segment_position
                spectrum
            }
        }
    :rtype: dict
    """    

    # run the query
    cursor = connection.cursor()
    query = "USE aniani;"
    cursor.execute(query)

    query = f"""
        WITH ranked_data AS (
            SELECT
                mirror,
                mirror_type,
                segment_position,
                spectrum,
                segment_id,
                reflectivity,
                install_date,
                measurement_type,
                ROW_NUMBER() OVER (
                    PARTITION BY segment_position, spectrum, measurement_type
                    ORDER BY install_date DESC
                ) AS rn
            FROM
                MirrorSamples
            WHERE
                mirror = '{mirror}'
                AND sample_status = 'clean'
                AND telescope_num = {tel_num}
                AND measurement_type = 'T'
        )
        SELECT
            mirror,
            mirror_type,
            segment_position,
            segment_id,
            spectrum,
            measurement_type,
            reflectivity,
            install_date
        FROM
            ranked_data
        WHERE
            rn = 1;
        """

    # run sql query
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()

    # close the cursor
    cursor.close()

    return results


def mathy(connection, tel_num):

     # run the query
    cursor = connection.cursor()
    query = "USE aniani;"
    cursor.execute(query)

    query = "select * from mirrorsamples;"

    # returning all PM dirty samles
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()

    # FIND TIME DIFFERENCE FOR DIRTY SAMPLES

    # list for all the delta dates from the dirty samples
    date_deltas = []

    # for each row in MirrorSamples table 
    for item in data:
        # grab the PM and dirty samples
        if item['mirror']=='primary' and item['sample_status']=='dirty' and item['telescope_num'] == 1:

            measured_date = item['measured_date']
            install_date = item['install_date']

            # if there are two dates, find the difference -> else just write error
            if measured_date is not None and install_date is not None:
                measured_date = int(measured_date.strftime("%y%m%d"))
                install_date = int(install_date.strftime("%y%m%d"))

                date_deltas.append(measured_date - install_date)
            else:
                date_deltas.append('error')

    # FIND MEAN AND RMS OF WITNESS SAMPLE DATA

    
    return data







