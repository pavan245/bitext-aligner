from xml.etree import ElementTree as ET
from xml.dom import minidom
import os
import json
from pathlib import Path


def create_xml_file(book_dict, book_metadata):
    book_root = ET.Element('book')
    book_root.set('code', book_metadata['book_id'])

    book_info = ET.SubElement(book_root, 'bookInfo')
    content = ET.SubElement(book_root, 'content')

    title = ET.SubElement(book_info, 'title')
    title.text = book_metadata['title']

    lang = ET.SubElement(book_info, 'lang')
    lang.text = book_metadata['lang']

    is_translation = ET.SubElement(book_info, 'isTranslation')
    is_translation.text = book_metadata['isTranslation']

    total_chapters = ET.SubElement(book_info, 'totalChapters')
    total_chapters.text = book_metadata['totalChapters']

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

    for key in book_dict.keys():
        chapter = ET.SubElement(content, 'chapter')
        chapter.set('num', str(key))
        for idx, val in enumerate(book_dict[key]):
            sentence = ET.SubElement(chapter, 'sentence')
            sentence.set('num', str(idx + 1))
            sentence.text = val

    # tree = ET.ElementTree(book_root)
    # tree.write(filename)
    root_dir = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(root_dir, "xml_files")
    filename = book_root.get('code') + "_" + lang.text + ".xml"
    file = open(output_dir + '/' + filename, 'w')
    file_path = file.name
    print('XML File Path :: ', file_path)
    file.write(prettify(book_root))
    file.close()
    json_obj = {}
    book_code = book_root.get('code')
    json_obj['xml_file'] = filename
    json_obj['lang'] = lang.text
    json_obj['xml_file_path'] = file_path
    json_obj['is_validated'] = False
    json_obj['is_saved_to_db'] = False
    add_xml_book_data_to_json(book_code, json_obj)


def add_xml_book_data_to_json(book_code, json_obj):
    json_file_path = Path('json/books.json')

    json_file = open(json_file_path, 'r')
    json_data = json.load(json_file)
    json_file.close()

    books = json_data['books']
    if book_code in books.keys():
        books[book_code].append(json_obj)
    else:
        books[book_code] = [json_obj]

    json_data['books'] = books

    json_file = open(json_file_path, 'w')
    json_file.write(json.dumps(json_data, indent=4))
    json_file.close()


def prettify(root):
    """ Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(root, 'utf-8')
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="\t")
