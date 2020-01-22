import mysql.connector
from mysql.connector import errorcode
import db.read_config as config
import utils.constants as const
import os


def get_new_mysql_connection(config_file_name):

    config_file_path = os.path.dirname(os.path.dirname(__file__))+'/'+config_file_name
    db_config = config.read_db_config(config_file_path, 'mysql')

    connection = None

    try:
        connection = mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(const.WARNING, 'Invalid Database User and Password', const.END)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(const.WARNING, 'Database doesn\'t exist ', const.END)
        else:
            print(err)

    if connection is not None:
        if connection.is_connected():
            connection.autocommit = False
            print(const.GREEN, 'MySQL Connection Successful => Connection ID :: ', connection.connection_id, const.END)
        else:
            connection = None

    return connection
