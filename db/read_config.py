from configparser import ConfigParser
import os


def read_db_config(filename, section):
    """ Read database configuration file and return a dictionary object
        :param filename: name of the configuration file
        :param section: section of database configuration
        :return: a dictionary of database parameters
    """

    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    try:
        db['password'] = os.environ[db['password']]
    except KeyError:
        print('Please set the Environment Variable ', db['password'])

    try:
        db['host'] = os.environ[db['host']]
    except KeyError:
        print('Please set the Environment Variable ', db['host'])

    return db
