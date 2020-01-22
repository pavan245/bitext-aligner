import json
import os


def read_json_file(file_path):
    json_file_path = os.path.dirname(os.path.dirname(__file__))+'/'+file_path

    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        json_file.close()
        return json_data


def write_json_file(file_path, json_data):
    json_file_path = os.path.dirname(os.path.dirname(__file__))+'/'+file_path

    with open(json_file_path, 'w') as updated_json:
        updated_json.write(json.dumps(json_data, indent=4))
        updated_json.close()