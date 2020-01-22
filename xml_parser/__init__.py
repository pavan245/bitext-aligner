from pathlib import Path
import json
import utils.constants as const
import os


json_path = os.path.dirname(os.path.dirname(__file__))+'/'+const.JSON_PATH
json_file_path = Path(json_path)

json_data = {'books': {}}
if not json_file_path.is_file():
    json_file = open(json_file_path, 'w')
    json_file.write(json.dumps(json_data, indent=4))
    json_file.close()
    print(const.BLUE, 'JSON File Created :: '+json_file.name, const.END)

