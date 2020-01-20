import mysql.connector
from mysql.connector import errorcode

import db.read_config as config


def get_new_mysql_connection(config_file_path):

    db_config = config.read_db_config(config_file_path, 'mysql')

    connection = None

    try:
        connection = mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Invalid Database User and Password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database doesn\'t exist ')
        else:
            print(err)

    if connection is not None:
        if connection.is_connected():
            connection.autocommit = False
        else:
            connection = None

    return connection
