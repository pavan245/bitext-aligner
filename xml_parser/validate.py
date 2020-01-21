import xmlschema
import json
from pathlib import Path
import utils.json_utils as json_utils
import utils.constants as const


def is_valid(book_schema, xml_path):
    return book_schema.is_valid(xml_path)


def get_book_schema(book_xsd_path):
    xsd_path = Path(book_xsd_path)
    book_schema = xmlschema.XMLSchema(str(xsd_path.absolute()))
    return book_schema


def validate_all_xml_files():

    json_data = json_utils.read_json_file(const.JSON_PATH)

    book_schema = get_book_schema(const.XSD_PATH)

    books_json = json_data['books']
    for book_code in books_json.keys():
        books_list = books_json[book_code]
        for book in books_list:
            if book['is_validated']:
                print(const.BLUE, 'Book : ', book['xml_file'], ' is valid', const.END)
                continue
            else:
                if 'xml_file_path' in book:
                    result = book_schema.is_valid(book['xml_file_path'])
                    print('Validating Book : ', book['xml_file'], ' -> ', result)
                    book['is_validated'] = result

    json_data['books'] = books_json
    json_utils.write_json_file(const.JSON_PATH, json_data)
