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
    db_config = read_db_config('config.live.ini')
    connection = create_db_connection(db_config)

    new_data = mathy(connection, tel_num)

    return new_data



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