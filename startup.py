# .py file to create a connection to the database
import configparser


if __name__ == "__main__":

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

 

