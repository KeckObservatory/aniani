from flask import Flask, request, jsonify
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
    pass


@app.route("/deleteData", methods=['PATCH'])
def delete_data():
    '''
        data needed to update db -> 
    '''
    pass


@app.route("/getCurrent", methods=['GET'])
def get_current_reflectivity():

    mirror = request.args.get('mirror')
    if mirror is None:
        mirror = 'primary'

    tel_num = request.args.get('tel_num')
    if tel_num is None:
        tel_num = 1

    measurement_type = request.args.get('measurement_type')
    if measurement_type is None:
        measurement_type = 'S'

    # connect to mysql database with config file
    db_config = read_db_config('config.live.ini')
    connection = create_db_connection(db_config)

    # find current segments on the telescope and their information
    tel_current = get_active_segs(connection, tel_num, mirror, measurement_type)

    return jsonify(tel_current), 200



@app.route("/getRecentFromDate", methods=['GET'])
def get_recent_data_from_date():
    pass


@app.route("/primaryPredicts", methods=['GET'])
def get_predicted_reflectivity():

    mirror = request.args.get('mirror')
    if mirror is None:
        mirror = 'primary'

    tel_num = request.args.get('tel_num')
    if tel_num is None:
        tel_num = 1

    measurement_type = request.args.get('measurement_type')
    if measurement_type is None:
        measurement_type = 'S'

    # connect to mysql database with config file
    db_config = read_db_config('config.live.ini')
    connection = create_db_connection(db_config)

    # dict of all rows in the MirrorSamples table
    data = get_mirrorsamples(connection, mirror, tel_num, measurement_type)

    # find the time differences between measured and install date
    # coating.PM.time_delta
    data = find_time_diff(data)

    # find the average spectural 'S' reflectivity for each wavelength for a telescope
    # coating.PM.witness.Spect_avg(1, 4)
    clean_avg = find_avg_rms(data, ['400-540', '480-600', '590-720', '900-1100'], 'clean', 'reflectivity')

    # coating.PM.mirror.Spect_avg(1, 4)
    dirty_avg = find_avg_rms(data, ['400-540', '480-600', '590-720', '900-1100'], 'dirty', 'reflectivity')

    # find the difference in the clean and dirty samples and calulate reflectivity degredation
    # coating.PM.mirror.Spectral_diff 
    # coating.PM.mirror.Spectrual_degrade
    data = find_degredation(data, clean_avg, measurement_type)

    # find the degredation values
    # coating.PM.mirror.Spectral_slope (1, 4) 
    deg_avg = find_avg_rms(data, ['400-540', '480-600', '590-720', '900-1100'], 'dirty', 'degredation')

    # find current segments on the telescope
    # coating.tel_current from coating.PM.witness.Spectrual (most recent clean samples)
    tel_current = get_active_segs(connection, tel_num, mirror, measurement_type)

    # find time difference between meansred and install date for clean samples
    # coating.tel_current(4)
    tel_current = find_time_diff(tel_current)

    # calculate the predicted current reflectivity
    # coating.tel_current(5, ,6, 7, 8)
    tel_current = find_predicted_reflectivity(tel_current, deg_avg, clean_avg)

    # upper left hand corner
    # mean(coating.tell_current(5, 6, 7, 8)
    # Ravg
    r_avg = find_avg_rms(tel_current, ['400-540', '480-600', '590-720', '900-1100'], 'clean', 'predict_reflectivity' )

    # lower left hand corner
    # -1 * coating.PM.mirror.Spectral_slope(4) * 365
    # -1*RMS dR/year
    deg_avg = find_rate_per_year(deg_avg)

    # consolidation of all data to be plotted
    to_plot = {}

    return jsonify(deg_avg), 200



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