import configparser
import mysql.connector
from datetime import datetime
import math

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


def get_active_segs(connection, tel_num, mirror, measurment_type):
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
        SELECT *,
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
            AND measurement_type = '{measurment_type}'
    )
    SELECT *
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


def get_mirrorsamples(connection, mirror, tel_num, measurement_type):
    """
    Get all data from the table MirrorSamples and put into dictionary format.

    :param connection: connection to aniani db
    :type connection: object
    :returmn data: list of dicts for each row
    :type: list
    """

     # run the query
    cursor = connection.cursor()
    query = "USE aniani;"
    cursor.execute(query)

    query = f"select * from mirrorsamples where mirror='{mirror}' and telescope_num='{tel_num}' and measurement_type='{measurement_type}';"

    # returning all PM dirty samles
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def find_time_diff(data):
    """
    Find the time difference in between the install and measured date of the mirror samples.
    It also saves the value in the dictonaries themselves.

    :param data: list of dicts from MirrorSamples table
    :type data: list
    :return: list of the difference in dates
    :rtype: list
    """

    # list for all the delta dates from the dirty samples
    date_deltas = []

    # for each row in MirrorSamples table 
    for item in data:

        measured_date = item['measured_date']
        install_date = item['install_date']

        # if there are two dates, find the difference -> else just write error
        if measured_date is not None and install_date is not None:

            measured_date = int(measured_date.strftime("%y%m%d"))
            install_date = int(install_date.strftime("%y%m%d"))

            diff = measured_date - install_date

            item['date_delta'] = diff
            date_deltas.append(diff)

        else:
            item['date_delta'] = 'error'
            date_deltas.append('error')

    return data


def find_avg_rms(data, spectra, sample_status, attribute):
    """
    Finding the average and rms values for a specfiic spectrum, measurement type, sample on either telescope.
    Takes the average and rms of the reflectivity.

    :param data: list of dicts from the MirrorSamples table
    :type data: list
    :param spectra: all the wavelengths to be averaged
    :type spectra: list
    :param measurment_type: the type of measurment T, D, S
    :type measurment_type: str
    :param sample_status: what kind of sample? clean or dirty
    :type sample_status: str
    :param tel_num: Keck 1 or 2
    :type tel_num: int
    :return: dict of the form for each wavelenth with the given avg and rms values
    {
        wavelength:
            average:
            rms:
    }
    :rtype: dict
    """
    # dict to return
    results = {}
    
    # for each wavelength...
    for spectrum in spectra:

        # set starting values
        count = 0
        sum = 0
        sum_squared = 0

        for item in data:
            # find the correct data...
            if item['sample_status'] == sample_status and item['spectrum'] == spectrum:

                # if the reflectivity data exists -> add it to avg, count and rms
                value = item[attribute]

                if not value is None and value != 'error':

                    count += 1
                    sum += value
                    sum_squared += value ** 2
        

        # find the average sum / number of items
        average = sum / count

        # find rms -> square root (reflectivity^2 / count) 
        rms = math.sqrt(sum_squared / count)

        # add them into a dict to return
        results[spectrum] = {'average': average, 'rms': rms}
    
    return results


def find_degredation(data, clean_avg, measurment_type):

    for item in data:

        # grab the diry samples for the measurement type
        if item['sample_status'] == 'dirty' and item['measurement_type'] == measurment_type:

            # grab the row wavelength and reflectivity
            spectrum = item['spectrum']
            reflectivity = item['reflectivity']
            date_delta = item['date_delta']

            # grab the average ~clean~ reflectivity of the same wavelength 
            average = clean_avg[spectrum]['average']

            # if there is a sample reflectivity
            if not reflectivity is None:

                # calculate the difference between dirty current and the average clean reflectivity
                diff = reflectivity - average

                # calculate reflectivity degredation by the difference in change / change in date since measured and installed 
                degredation = diff / date_delta

                # adding item into dict for each row
                item['avg_delta'] = diff
                item['degredation'] = degredation

            else:
                item['avg_delta'] = 'error'
                item['degredation'] = 'error'


    return data

        
def find_current_reflectivity(tel_current, deg_avg, clean_avg):

    count = 0

    for item in tel_current:

        spectrum = item['spectrum']
        reflectivity = item['reflectivity']
        date_delta = item['date_delta']
        current_date = datetime.now()
        time_delta = (current_date.day - date_delta)

        if spectrum == '400-540' and reflectivity == None:
            count = 4

        if count == 0:
            item['predict_reflectivity'] = clean_avg[spectrum]['average'] + -(deg_avg[spectrum]['rms'] * time_delta)
        else:
            item['predict_reflectivity'] = reflectivity +  -(deg_avg[spectrum]['rms'] * time_delta)
            count -= 1

    return tel_current

        
def find_rate_per_year(deg_avg):

    for item in deg_avg:
        print(item)

        item['rate_of_deg'] = -1 * deg_avg['rms'] * 365

    return deg_avg
