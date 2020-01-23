import xml_parser.read_xml as read_xml
import db.add_book as adb
import xml_parser.validate as validate
import utils.json_utils as json_utils
import utils.constants as const
import utils.env_utils as env
import xml_parser.create_xml as create_xml
import txt_parser.csv_utils as csv_utils
from csv2df import get_book_content, get_book_metadata


def validate_all_xml_files():
    validate.validate_all_xml_files()


def save_validated_files_to_db():
    json_data = json_utils.read_json_file(const.JSON_PATH)
    books_json = json_data['books']
    for book_code in books_json.keys():
        books_list = books_json[book_code]
        for book in books_list:
            if not book['is_validated']:
                print(const.WARNING, 'XML File :: ', book['xml_file'], ' is not validated against XSD', const.END)
                continue
            if not book['is_saved_to_db']:
                print(const.BLUE, 'Adding Book Data : ', book['xml_file'], ' to the DB', const.END)
                book_dict = read_xml.parse_xml_file(book['xml_file_path'])
                result = adb.add_book_to_db(book_code, book_dict)
                book['is_saved_to_db'] = result
                w_str = const.WARNING
                if result:
                    w_str = const.BLUE
                print(w_str, 'Result :: ', result, const.END, '\n')

    json_data['books'] = books_json
    json_utils.write_json_file(const.JSON_PATH, json_data)


def read_data_files_and_align_sentences(book_code):
    books_list = csv_utils.read_books_csv_file(const.CSV_FILE)
    books_dict = {}
    for book in books_list:
        if book[1] not in books_dict:
            books_dict[book[1]] = []
        books_dict[book[1]].append(book)

    if book_code in books_dict:
        book_code_list = books_dict[book_code]

        for book in book_code_list:
            book_lines = csv_utils.read_data_file(book[3].strip())
            # TODO (for Jassi) :: Take this 'book_lines' and return dictionary after parsing chapters
            # TODO :: Please Follow the below Dictionary Structure, ==
            # Later Isaac will use this dict structure to align sentences
            # book_dict = {
            #     'meta_data': {
            #         "book_id": "",
            #         "title": "",
            #         "lang": "",
            #         "isTranslation": "",
            #         "totalChapters": "",
            #         "authors": [
            #             {
            #                 "name": "",
            #                 "translator": ""
            #             },
            #             {
            #                 "name": ""
            #             }
            #         ],
            #         "description": "", # Optional
            #         "source": ""
            #     },
            #     'content' : [
            #         {
            #             'chapter_num': '',
            #             'chapter_name': '',
            #             'text_content': ''
            #         },
            #         {
            #             'chapter_num': '',
            #             'chapter_name': '',
            #             'text_content': ''
            #         }
            #     ]
            # }


def create_xml_file(book_content_dict, book_metadata_dict):
    create_xml.create_xml_file(book_content_dict, book_metadata_dict)


if env.check_env_variables():
    read_data_files_and_align_sentences('dost_cap')
    # validate_all_xml_files()
    # save_validated_files_to_db()
