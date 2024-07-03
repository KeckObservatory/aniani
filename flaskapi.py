from flask import Flask, request
from flask_mysqldb import MySQL
from os.path import isfile
import configparser
from aniani_functions import *

app = Flask(__name__)


#---------------------------------------
# ANIANI API Routes
#---------------------------------------

@app.route("/", methods=["GET"])
def home():
    """
    Display an error
    """

    return {"status":"sucess", "message":"home page for aniani applicaton"}


@app.route("/addData", methods=['POST'])
def add_data():
    '''
    data needed to add to db...
    {
        mirror = str,
        segment_id = int,
        mirror_type = enum ('1','2','3','4','5','6','A','B','C'),
        measured_date = str,
        install_date = str,
        telescope_status = enum ('before_installing','after_uninstalling')
        telescope_num = int
        .... 

        ever column but is_deleted
    }
    '''


@app.route("/deleteData", methods=['PATCH'])
def delete_data():
    '''
        data needed to update db..
    {

    }
    '''


@app.route("/getRecent", methods=['GET'])
def get_recent_data():
    pass 


@app.rote("/fancyMath", methods['GET'])
def fancy_math():
    pass


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