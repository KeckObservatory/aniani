from flask import Flask, request
from os.path import isfile
import configparser
from aniani_functions import *

app = Flask(__name__)


#---------------------------------------
# ANIANI API Routes
#---------------------------------------

@app.route("/", methods=["GET"])
def home():
    return {"status":"sucess", "message":"home page for aniani applicaton"}


@app.route("/addData", methods=['POST'])
def add_data():
    '''
    data needed to add to db... -> every col except is_deleted
    '''


@app.route("/deleteData", methods=['PATCH'])
def delete_data():
    '''
        data needed to update db -> 
    '''


@app.route("/getCurrent", methods=['GET'])
def get_current_reflectivity_status():
    '''
    get most recent reflectivity total ('T') data for segments in all positions (1-36) 
    and the ones for the secondary and tertiary mirrors
    '''

    db_config = read_db_config('config.live.ini')
    connection = create_db_connection(db_config)

    tel_num = 1
    mirror = 'primary'
    results = get_reflectivity_status(connection, tel_num, mirror)

    mirror = 'secondary'
    results += get_reflectivity_status(connection, tel_num, mirror)

    mirror = 'tertiary'
    results += get_reflectivity_status(connection, tel_num, mirror)
    
    connection.close()
    return results


@app.route("/getRecentFromDate", methods=['GET'])
def get_recent_data_from_date():

    pass


@app.route("/fancyMath", methods=['GET'])
def fancy_math():

    tel_num = 1
    measurment_type = 'S'
    mirror = 'primary'

    db_config = read_db_config('config.live.ini')
    connection = create_db_connection(db_config)

    # dict of all rows in the MirrorSamples table
    data = get_mirrorsamples(connection, mirror, tel_num)

    # find the time differences between measured and install date
    date_deltas = find_time_diff(data)

    # find the average spectural 'S' reflectivity for each wavelength for a telescope
    clean_avg = find_averages_and_rms(data, ['400-540', '480-600', '590-720', '900-1100'], 'S', 'clean', tel_num)
    dirty_avg = find_averages_and_rms(data, ['400-540', '480-600', '590-720', '900-1100'], 'S', 'dirty', tel_num)

    # find the difference in the clean and dirty samples
    # diff = dirty = clean average
    diff = find_diff_from_avg(data, clean_avg, tel_num, measurment_type)


    # find the degredation values


    return dirty_avg



if __name__ == "__main__":

    api = "aniani"

    # read config
    config = configparser.ConfigParser()
    config.read('config.live.ini')

    # grab the information from the config file
    api_config = {
        'host': config.get('api', 'host'),
        'port': config.getint('api', 'port'),
        'valid_segs': config.get('api', 'valid_segs')

    }

    host = api_config['host']
    port = api_config['port']
    # list of integers for all valid segment id numbers 
    valid_segs = api_config['valid_segs']

    # run flask server with given config file
    app.run(host=host, port=port)