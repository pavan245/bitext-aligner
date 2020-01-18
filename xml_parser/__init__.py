from pathlib import Path
import json

json_file_path = Path('json/books.json')

json_data = {'books': {}}
if not json_file_path.is_file():
    json_file = open(json_file_path, 'w')
    json_file.write(json.dumps(json_data, indent=4))
    json_file.close()
    print('JSON File Created :: '+json_file.name)

