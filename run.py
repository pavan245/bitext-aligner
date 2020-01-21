import json
import xml_parser.read_xml as read_xml
import db.add_book as adb
import xml_parser.validate as validate
import utils.json_utils as json_utils
import utils.constants as const


def save_validated_files_to_db():
    json_data = json_utils.read_json_file(const.JSON_PATH)
    books_json = json_data['books']
    for book_code in books_json.keys():
        books_list = books_json[book_code]
        for book in books_list:
            if not book['is_validated']:
                print('Book : ', book['xml_file'], ' is not validated against XSD')
                continue
            if not book['is_saved_to_db']:
                print('Saving Book : ', book['xml_file'], ' in the DB')
                book_dict = read_xml.parse_xml_file(book['xml_file_path'])
                result = adb.add_book_to_db(book_code, book_dict)
                book['is_saved_to_db'] = result

    json_data['books'] = books_json
    json_utils.write_json_file(const.JSON_PATH, json_data)


def validate_all_xml_files():
    validate.validate_all_xml_files()


validate_all_xml_files()