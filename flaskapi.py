from flask import Flask
from flask_mysqldb import MySQL
from os.path import isfile
import configparser

app = Flask(__name__)

#---------------------------------------
# ANIANI Class
#---------------------------------------
class aniani:

    def __init__():

        # read the config file
        config = configparser.ConfigParser()
        config.read('config.live.ini')

        # grab the information from the config file
        db_config = {
            'host': config.get('mysql', 'host'),
            'port': config.getint('mysql', 'port'),
            'admin_username': config.get('mysql', 'username'),
            'admin_password': config.get('mysql', 'password'),
            'database': config.get('mysql', 'database')
        }
            


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

    # read config
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