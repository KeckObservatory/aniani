from flask import Flask, request, jsonify
from os.path import isfile
import configparser
from aniani_functions import *
from jsonschema import validate
from flask_swagger_ui import get_swaggerui_blueprint
import yaml
import db_conn

app = Flask(__name__)

reflectivity_input_schema = {
    "type": "object",
    "properties": {
        "mirror": {"type": "string", "enum": ["primary", "secondary", "tertiary"]},
        "tel_num": {"type": "integer", "enum": [1, 2]},
        "measurement_type": {"type": "string", "enum": ["T", "S", "D"]}
    },
    "required": ["mirror", "tel_num", "measurement_type"]
}

# --------------------
# with Keck db_conn.py db connector
#connection = db_conn.db_conn('config.live.ini', 'aniani')
# if connection.error():
#   connection.close()
# --------------------


#---------------------------------------
# ANIANI API Routes
#---------------------------------------

spectra = ['400-540', '480-600', '590-720', '900-1100']

@app.route("/", methods=["GET"])
def home():
    return {"status":"sucess", "message":"home page for aniani applicaton"}

@app.route("/aniani/swagger.json", methods=["GET"])
def swagger():
    api_path = './docs/openapi.yaml'
    with open(api_path, 'r') as f:
        return jsonify(yaml.safe_load(f))


@app.route("/addData", methods=['POST'])
def add_data():
    '''
    data needed to add to db... -> every col except is_deleted
    '''
    data_to_write = request.args.to_dict()


@app.route("/deleteData", methods=['PATCH'])
def delete_data():
    '''
        data needed to update db -> 
    '''
    pass


@app.route("/getCurrent", methods=['GET'])
def get_current_reflectivity():

    input = {
    "mirror": request.args['mirror'].lower(),
    "tel_num": int(request.args['tel_num']),
    "measurement_type": request.args['measurement_type'].upper()
    }       

    # validate input parameters
    validate(input, reflectivity_input_schema)
    
    mirror = input['mirror']
    tel_num = input['tel_num']
    measurement_type = input['measurement_type']

    # connect to mysql database with config file
    db_config = read_db_config('config.live.ini')
    connection = create_db_connection(db_config)

    # find current segments on the telescope and their information
    tel_current = get_active_segs(connection, tel_num, mirror, measurement_type)

    # creating a new dictionary to send to front end
    # will send 36 dicts, one for each current segment position
    pretty_print = {}

    for item in tel_current:
        seg_pos = item['segment_position']
        spectrum = item['spectrum']
        
        if seg_pos not in pretty_print:
            pretty_print[seg_pos] = {
                'install_date': item['install_date'],
                'measured_date': item['measured_date'],
                'measurement_type': item['measurement_type'],
                'mirror': item['mirror'],
                'mirror_type': item['mirror_type'],
                'seg_id': item['segment_id']
            }
        
        # for each spectrum -> add the reflectivity
        pretty_print[seg_pos][spectrum] = item['reflectivity']

    return jsonify(pretty_print)


@app.route("/getRecentFromDate", methods=['GET'])
def get_recent_data_from_date():
    pass


@app.route("/getPredicts", methods=['GET'])
def get_predicted_reflectivity():

    input = {
        "mirror": request.args['mirror'].lower(),
        "tel_num": int(request.args['tel_num']),
        "measurement_type": request.args['measurement_type'].upper()
        }       

    try :
        validate(input, reflectivity_input_schema)

    except:
        return jsonify({
            'error': 'Invalid Input!',
            'valid_data': reflectivity_input_schema['properties']
        })
    
    mirror = input['mirror']
    tel_num = input['tel_num']
    measurement_type = input['measurement_type']


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
    clean_avg = find_avg_rms(data, spectra, 'clean', 'reflectivity')

    # coating.PM.mirror.Spect_avg(1, 4)
    dirty_avg = find_avg_rms(data, spectra, 'dirty', 'reflectivity')

    # find the difference in the clean and dirty samples and calulate reflectivity degredation
    # coating.PM.mirror.Spectral_diff 
    # coating.PM.mirror.Spectrual_degrade
    data = find_degredation(data, clean_avg, measurement_type)

    # find the degredation values
    # coating.PM.mirror.Spectral_slope (1, 4) 
    deg_avg = find_avg_rms(data, spectra, 'dirty', 'degredation')

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
    r_avg = find_avg_rms(tel_current, spectra, 'clean', 'predict_reflectivity' )

    # lower left hand corner
    # -1 * coating.PM.mirror.Spectral_slope(4) * 365
    # -1*RMS dR/year
    deg_avg = find_rate_per_year(deg_avg)

    pretty_print = {}

    # making the dictionary to return
    # for dictionaries, one for each wavelength
    for spectrum in spectra:
        pretty_print[spectrum] = {
            'r_avg': r_avg[spectrum]['average'],
            'dR/year': deg_avg[spectrum]['rate_of_decay'],
            'segments': {}
        }

    # adding the current reflectivity data into the return dicts
    for item in tel_current:
        seg_pos = item['segment_position']
        spectrum = item['spectrum']

        if seg_pos not in pretty_print:
            pretty_print[spectrum]['segments'][seg_pos] = {
                'install_date': item['install_date'],
                'measured_date': item['measured_date'],
                'measurement_type': item['measurement_type'],
                'mirror': item['mirror'],
                'mirror_type': item['mirror_type'],
                'seg_id': item['segment_id']
            }
        
        # for each spectrum -> add the reflectivity
        pretty_print[seg_pos][spectrum] = item['reflectivity']

    
    return jsonify(pretty_print)



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

    SWAGGER_URL = '/aniani/swagger'
    API_URL = f'/aniani/swagger.json'

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "ani ani Application"
    })

    app.register_blueprint(swaggerui_blueprint)

    # run flask server with given config file
    app.run(host=host, port=port)