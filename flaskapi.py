from flask import Flask, jsonify, request
from os.path import isfile
import configparser

app = Flask(__name__)

#---------------------------------------
# ANIANI API Routes
#---------------------------------------

@app.route("/", methods=["GET"])
def home():
    """
    Display an error
    """

    return {"status":"ERROR", "message":"something went wrong"}



if __name__ == "__main__":
    api = "aniani"

     # Parse config file 
    config = configparser.ConfigParser()
    config.read('config.live.ini')

    # grab the information from the config file
    api_config = {
        'host': config.get('api', 'host'),
        'port': config.getint('api', 'port'),

    }

    host = api_config['host']
    port = api_config['port']

    app.run(host=host, port=port)