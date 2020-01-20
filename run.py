import json
from pathlib import Path
import xml_parser.read_xml as read_xml
import db.add_book as adb

json_file_path = Path('json/books.json')

with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)
    json_file.close()

    books_json = json_data['books']
    for book_code in books_json.keys():
        books_list = books_json[book_code]
        for book in books_list:
            # TODO :: Add not for the below check later (after doing XSD)
            if book['is_validated']:
                print('Book : ', book['xml_file'], ' is not validated against XSD')
                continue
            if not book['is_saved_to_db']:
                print('Saving Book : ', book['xml_file'], ' in the DB')
                book_dict = read_xml.parse_xml_file(book['xml_file_path'])
                result = adb.add_book_to_db(book_code, book_dict)
                book['is_saved_to_db'] = result

    json_data['books'] = books_json

    with open(json_file_path, 'w') as updated_json:
        updated_json.write(json.dumps(json_data, indent=4))
        updated_json.close()

