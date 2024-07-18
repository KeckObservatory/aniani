from flask import Flask, request, jsonify
from os.path import isfile
import configparser
from aniani_functions import *
import jsonschema
from jsonschema import validate, ValidationError, Draft202012Validator
from flask_swagger_ui import get_swaggerui_blueprint
import yaml
import db_conn
from schemas import reflectivity_input_schema, add_reflectivity_measurement_schema


app = Flask(__name__)


#---------------------------------------
# ANIANI API Routes
#---------------------------------------

spectra = ['400-540', '480-600', '590-720', '900-1100']

@app.route("/", methods=["GET"])
def home():
    return {"status":"success", "message":"home page for aniani applicaton"}


@app.route("/aniani/swagger.json", methods=["GET"])
def swagger():
    api_path = './docs/openapi.yaml'
    with open(api_path, 'r') as f:
        return jsonify(yaml.safe_load(f))

def validate_input(input, schema):
    validator = Draft202012Validator(schema)
    errors = []
    for error in validator.iter_errors(input):
        errors.append(f"{error.path.pop()}: {error.message}")
    if errors:
        return {
            'error':  errors,
        } 

@app.route("/getAllSamples", methods=["GET"])
# returns all data from the MirrorSamples table
def get_all_samples():

    # validate input parameters
    try:
        input = {
            "mirror": request.args['mirror'].lower(),
            "telescope_num": int(request.args['telescope_num']),
            "measurement_type": request.args['measurement_type'].upper()
        }       
        errOutput = validate_input(input, reflectivity_input_schema)
        if errOutput:
            return jsonify(errOutput), 400
        # validate(input, reflectivity_input_schema)
    except KeyError as err:
        return jsonify({
            'error': f'key error: {err} valid keys are: {", ".join([x for x in reflectivity_input_schema["properties"].keys()])}',
        }), 400
    
    mirror = input['mirror']
    telescope_num = input['telescope_num']
    measurement_type = input['measurement_type']

    connection = create_db_connection()

    # ask the database for all mirror samples
    samples = get_mirrorsamples(connection, mirror, telescope_num, measurement_type)

    return jsonify(samples)


@app.route("/addReflectivityMeasurement", methods=['POST'])
# add new rows of reflectivity information to the MirrorSamples table
def add_reflectivity_measurement():

    # grab data put into table rows! 
    to_write = request.json()

    # validate input parameters
    validate(to_write, add_reflectivity_measurement_schema)
    errOutput = validate_input(to_write, add_reflectivity_measurement_schema)
    if errOutput:
        return jsonify(errOutput), 400

    # create db connection 
    connection = create_db_connection()

    # for each dict in input 
    for row in to_write:

        # grab table cols and values to insert into table
        table_cols = ', '.join(to_write.keys())
        table_values = ', '.join(to_write.values())

        # for now, no default value -> manually set to 0 for not deleted 
        query = f"insert into MirrorSamples ({table_cols}, is_deleted) values ({table_values}, 0)"

        connection.query(query)


@app.route("/deleteData", methods=['PATCH'])
def delete_data():
    '''
        data needed to update db -> 
    '''
    pass


@app.route("/getCurrentReflectivity", methods=['GET'])
# get the lastest reflectivity data from the segments that are on telescope now
def get_current_reflectivity():

    input = {
        "mirror": request.args['mirror'].lower(),
        "telescope_num": int(request.args['telescope_num']),
        "measurement_type": request.args['measurement_type'].upper()
    }       

    # validate input parameters
    try:
        validate(input, reflectivity_input_schema)
    except jsonschema.exceptions.ValidationError as err:
        return jsonify({
            'error': err.cause,
            'valid_data': reflectivity_input_schema['properties']
        }), 400
    
    mirror = input['mirror']
    telescope_num = input['telescope_num']
    measurement_type = input['measurement_type']

    connection = create_db_connection()

    # find current segments on the telescope and their information
    tel_current = get_active_segs(connection, telescope_num, mirror, measurement_type)

    # creating a new dictionary to send to front end
    # will send  1 or 36 dicts, one for each current segment position
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


@app.route("/getPredictReflectivity", methods=['GET'])
def get_predicted_reflectivity():

    input = {
        "mirror": request.args['mirror'].lower(),
        "telescope_num": int(request.args['telescope_num']),
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
    telescope_num = input['telescope_num']
    measurement_type = input['measurement_type']

    connection = create_db_connection()

    # dict of all rows in the MirrorSamples table
    data = get_mirrorsamples(connection, mirror, telescope_num, measurement_type)

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
    tel_current = get_active_segs(connection, telescope_num, mirror, measurement_type)

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

        if seg_pos not in pretty_print[spectrum]['segments']:
            pretty_print[spectrum]['segments'][seg_pos] = {
                'install_date': item['install_date'],
                'measured_date': item['measured_date'],
                'measurement_type': item['measurement_type'],
                'mirror': item['mirror'],
                'mirror_type': item['mirror_type'],
                'seg_id': item['segment_id'],
                'predict_reflectivity': item['predict_reflectivity']
            }
    
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
