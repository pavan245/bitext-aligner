from xml.etree import ElementTree as ET
from xml.dom import minidom
import os
import json
import utils.json_utils as json_utils
import utils.constants as const


def create_xml_file(book_content, book_metadata):
    book_root = ET.Element('book')
    book_root.set('code', book_metadata['book_code'])

    book_info = ET.SubElement(book_root, 'bookInfo')
    content = ET.SubElement(book_root, 'content')

    title = ET.SubElement(book_info, 'title')
    title.text = book_metadata['title']

    lang = ET.SubElement(book_info, 'lang')
    lang.text = book_metadata['lang']

    is_translation = ET.SubElement(book_info, 'isTranslation')
    is_translation.text = book_metadata['isTranslation']

    total_chapters = ET.SubElement(book_info, 'totalChapters')
    total_chapters.text = str(book_metadata['totalChapters'])

    source = ET.SubElement(book_info, 'source')
    source.text = book_metadata['source']

    if 'description' in book_metadata:
        description = ET.SubElement(book_info, 'description')
        description.text = book_metadata['description']

    if 'isbn' in book_metadata:
        isbn = ET.SubElement(book_info, 'isbn')
        isbn.text = book_metadata['isbn']

    authors_list = book_metadata['authors']
    for auth in authors_list:
        author = ET.SubElement(book_info, 'author')
        author.text = auth['name']
        if 'translator' in auth:
            author.set('translator', auth['translator'])

    for chapter in book_content:
        if 'sentences' not in chapter:
            continue
        chapter_element = ET.SubElement(content, 'chapter')
        chapter_element.set('num', str(chapter['chapter_num']))
        chapter_element.set('name', chapter['chapter_name'])
        sentences_dict = chapter['sentences']
        for key in sentences_dict.keys():
            sentence = ET.SubElement(chapter_element, 'sentence')
            sentence.set('num', str(key + 1))
            sentence.text = sentences_dict[key]

    # tree = ET.ElementTree(book_root)
    # tree.write(filename)
    root_dir = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(root_dir, "xml_files")
    filename = book_root.get('code') + "_" + lang.text + ".xml"
    file = open(output_dir + '/' + filename, 'w')
    file_path = file.name
    file.write(prettify(book_root))
    file.close()
    print(const.BLUE, 'Saved XML File Path :: ', file_path, const.END)
    json_obj = {}
    book_code = book_root.get('code')
    json_obj['xml_file'] = filename
    json_obj['lang'] = lang.text
    json_obj['xml_file_path'] = file_path
    json_obj['is_validated'] = False
    json_obj['is_saved_to_db'] = False
    add_xml_book_data_to_json(book_code, json_obj)

    return file_path


def add_xml_book_data_to_json(book_code, json_obj):

    json_data = json_utils.read_json_file(const.JSON_PATH)

    books = json_data['books']
    if book_code in books.keys():
        books[book_code].append(json_obj)
    else:
        books[book_code] = [json_obj]

    json_data['books'] = books

    json_utils.write_json_file(const.JSON_PATH, json_data)
    print(const.BLUE, 'Added XML Book Entry to JSON', const.END)


def prettify(root):
    """ Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(root, 'utf-8')
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="\t")
