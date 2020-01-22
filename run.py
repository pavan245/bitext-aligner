import xml_parser.read_xml as read_xml
import db.add_book as adb
import xml_parser.validate as validate
import utils.json_utils as json_utils
import utils.constants as const
import utils.env_utils as env


def validate_all_xml_files():
    validate.validate_all_xml_files()


def save_validated_files_to_db():
    json_data = json_utils.read_json_file(const.JSON_PATH)
    books_json = json_data['books']
    for book_code in books_json.keys():
        books_list = books_json[book_code]
        for book in books_list:
            if not book['is_validated']:
                print(const.WARNING, 'Book : ', book['xml_file'], ' is not validated against XSD', const.END)
                continue
            if not book['is_saved_to_db']:
                print(const.BLUE, 'Adding Book : ', book['xml_file'], ' to the DB', const.END)
                book_dict = read_xml.parse_xml_file(book['xml_file_path'])
                result = adb.add_book_to_db(book_code, book_dict)
                book['is_saved_to_db'] = result
                w_str = const.WARNING
                if result:
                    w_str = const.BLUE
                print(w_str, 'Result :: ', result, const.END, '\n')

    json_data['books'] = books_json
    json_utils.write_json_file(const.JSON_PATH, json_data)


if env.check_env_variables():
    validate_all_xml_files()
    save_validated_files_to_db()