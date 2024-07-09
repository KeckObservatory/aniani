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
        password=db_config['admin_password'],
        database=db_config['database']
    )

    # returning the connection
    return connection


def get_active_segs(connection, tel_num, mirror, measurment_type):
    """
    For a given mirror, telescope and measurement type (T,D,S), will return a dictionary
    of the active segment(s) and their values from the table MirrorSamples.

    Pulls from the most recent install date of 'clean' samples.

    For PM: returns a list of dictionaries of the info for each wavelength reflectivity measurment,
        so for 36 segments will return a total of 36*4 entries

    For SM/TM: returns a list of 4 dictionaries of the info for each wavelength reflectivity measurement.

    :param connection: connecton to the mysql db    
    :type connection: object
    :param tel_num: Keck telescope number (1 or 2)
    :type tel_num: int
    :param mirror: Keck telescope mirror ('primary','secondary','tertiary')
    :type mirror: str
    :param measurment_type: type of wavelength measurement ('T', 'D', 'S')
    :type measurment_type: str
    :return: a list of dictionaries of the rows from the MirrorSamples table from the most recent install date
    :rtype: list (of dicts)
    """    
    # connect to the db
    cursor = connection.cursor()

    # rank the data by the install date (to find the most recent)
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

    # run query and make sure the rows are stored as dictionaries 
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()

    # close the cursor
    cursor.close()

    return results  


def get_mirrorsamples(connection, mirror, tel_num, measurement_type):
    """
    Get all the data from the MirrorSamples table from the database, and create
    a list of dictionaries where each dictionary is a corresponding row in the db.

    :param connection: db connection
    :type connection: object
    :param mirror: Keck telescope mirror ('primary','secondary','tertiary')
    :type mirror: str
    :param tel_num: Keck telescope number (1 or 2)
    :type tel_num: int
    :param measurment_type: type of wavelength measurement ('T', 'D', 'S')
    :type measurment_type: str
    :return: a list of dictionaries of the rows from the MirrorSamples table 
    :rtype: list (of dicts)
    """    

    cursor = connection.cursor()

    # parameterized query to avoid sql injections
    # treats the parameters like strings (not executable code)
    query = """
        SELECT * FROM mirrorsamples
        WHERE mirror = %s AND telescope_num = %s AND measurement_type = %s;
    """

    params = (mirror, tel_num, measurement_type)

    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)
    data = cursor.fetchall()

    return data


def find_time_diff(data):
    """
    Finds the time difference between the measusred and install date from rows in the MirrorSamples table.
    For each dictionary it adds the value 'date_delta' as a key value pair. 

    :param data: data retunred from get_mirror_samples
    :type data: list of dicts
    :return: updated list of dicts
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
    For a given wavelength, sample status find the average and rms values of a given ~numerical~ attribute.

    The attribute can be any charactersitic of a dictionary with a number (not str) value.

    :param data: list of dictionaries from the MirrorSamples table
    :type data: list
    :param spectra: wavelenths to find average and rms of ['400-450', '',''...]
    :type spectra: list 
    :param sample_status: if it is a mirror or witness sample ('clean' or 'dirty')
    :type sample_status: str   
    :param attribute: key value of a numerical characterstic of the dictionaries
    :type attribute: str
    :return: dictionary of the form
    {
        '400-450':
            'average': #,
            'rms': #
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

                # if the data exists -> add it to avg, count and rms
                value = item[attribute]

                # if there is a value and NOT an error -> add to average and rms calculations
                if not value is None and value != 'error':

                    count += 1
                    sum += value
                    sum_squared += value ** 2
        

        # find the average sum / number of items
        average = sum / count

        # find rms -> square root(reflectivity^2 / count) 
        rms = math.sqrt(sum_squared / count)

        # add them into a dict to return
        results[spectrum] = {'average': average, 'rms': rms}
    
    return results


def find_degredation(data, clean_avg, measurment_type):
    """
    Find the degredation values for given data from the MirrorSamples table, the clean
    sample averages and the reflectivity measurement type.

    It updates the data list of dicts and adds two key value pairs 'avg_delta' and 'degredation'.

    avg_delta = the average difference for each entry of the measrured reflectivity and average sample
    degredation = the avg_delta divided by the date_delta (the difference in measrued and installed date)

    :param data: list of dictionaries from the MirrorSamples table
    :type data: list
    :param clean_avg: dict returned from find_avg_rms with 'clean' sample_status
    :type clean_avg: dict
    :param measurment_type: type of wavelength measurement ('T', 'D', 'S')
    :type measurment_type: str
    :return: updated version of 'data' with two new values for each entry 'avg_delta' and 'degredation' as key value pairs.
    :rtype: list of dicts
    """    

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

        
def find_predicted_reflectivity(tel_current, deg_avg, clean_avg):
    """
    Calculate the current predicted reflectivity using the degradations and clean average values.

    Each segment and wavelength pair entry now will have 'predict_reflectivity' calucluated using the average values.

    :param tel_current: list of dicts of the current active segment(s) returned from get_active_segs
    :type tel_current: list of dicts
    :param deg_avg: dictionary with the average and rms values of the degredation for each wavelength
    :type deg_avg: dict
    :param clean_avg: dictionary with the average and rms values of the reflectivity for each wavelength
    :type clean_avg: dict
    :return: updated version of the tel_current data passed in
    :rtype: list of dicts
    """    

    count = 0

    for item in tel_current:

        spectrum = item['spectrum']
        reflectivity = item['reflectivity']
        date_delta = item['date_delta']
        current_date = datetime.now()

        # find the current date of now
        time_delta = (current_date.day - date_delta)

        # if there is no blue light reflectivity data -> the next 4 entries will not use average values
        if spectrum == '400-540' and reflectivity == None:
            count = 4

        # there was blue light -> calculate the predicted reflectivity by adding the average reflectivity + -(degredation average by time passed)
        if count == 0:
            item['predict_reflectivity'] = clean_avg[spectrum]['average'] + -(deg_avg[spectrum]['rms'] * time_delta)

        # no blue light -> not enough samples -> use current reflectivity not average
        else:
            item['predict_reflectivity'] = reflectivity +  -(deg_avg[spectrum]['rms'] * time_delta)
            count -= 1

    return tel_current



def find_rate_per_year(deg_avg):
    """
    
    Find the rate of decay of reflectivity per year.

    And a new key value pair for each wavelenth called 'rate_of_decay'  = -1 * the rms degredation value * 365

    :param deg_avg: dictionary of average and rms values for each wavelength
    :type deg_avg: dict
    :return: updated deg_avg dictionary
    :rtype: dict
    """    

    for spectrum in deg_avg:

        deg_avg[spectrum]['rate_of_decay'] = -1 * deg_avg[spectrum]['rms'] * 365

    return deg_avg
