import xml_parser.read_xml as read_xml
import db.add_book as adb
import xml_parser.validate as validate
import utils.json_utils as json_utils
import utils.constants as const
import utils.env_utils as env
import xml_parser.create_xml as create_xml
import txt_parser.csv_utils as csv_utils
import fb2_parser.read_fb2 as read_fb2
import aligner.bitext_align as aligner
import time


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
        full_book_dict = {}
        book_lang_list = []
        for book in book_code_list:
            book_dict = read_fb2.read_fb2_file(book[3].strip(), book_code, book[4], book[5])
            full_book_dict[book[2]] = book_dict
            book_lang_list.append(book[2])

        book1 = full_book_dict[book_lang_list[0]]
        book2 = full_book_dict[book_lang_list[1]]

        book1_lang = book1['metadata']['lang']
        book1_chapters = book1['content']
        book2_lang = book2['metadata']['lang']
        book2_chapters = book2['content']

        print(const.BLUE, 'Total Chapters :: ', book1['metadata']['totalChapters'])
        for idx, book1_chapter in enumerate(book1_chapters):
            book2_chapter = book2_chapters[idx]
            if book1_chapter['chapter_num'] == book2_chapter['chapter_num']:
                book1_sen, book2_sen = aligner.master_align(book1_chapter['text_content'], book2_chapter['text_content'], book1_lang, book2_lang)
                print(const.GREEN, 'Chapter :', book1_chapter['chapter_num'], '-> Sentence Alignment Done', const.END)
                book1_chapter.pop('text_content')
                book2_chapter.pop('text_content')
                book1_chapter.update({'sentences': book1_sen})
                book2_chapter.update({'sentences': book2_sen})
                book1_chapters[idx] = book1_chapter
                book2_chapters[idx] = book2_chapter
                time.sleep(60)
            if idx == 1:
                break

        print(const.BLUE, 'Book Sentence Alignment Done', const.END)

        create_xml_file(book1_chapters, book1['metadata'])
        create_xml_file(book2_chapters, book2['metadata'])


def create_xml_file(book_content, book_metadata_dict):
    create_xml.create_xml_file(book_content, book_metadata_dict)


if env.check_env_variables():
    read_data_files_and_align_sentences('dost_cap_ende')
    validate_all_xml_files()
    save_validated_files_to_db()
