from xml.etree import ElementTree as ET
from xml.dom import minidom


def create_xml_file(book_dict, book_metadata):
    book_root = ET.Element('book')
    book_root.set('id', book_metadata['book_id'])

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

    if 'description' in book_metadata:
        description = ET.SubElement(book_info, 'description')
        description.text = book_metadata['description']

    if 'source' in book_metadata:
        source = ET.SubElement(book_info, 'source')
        source.text = book_metadata['source']

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
        chapter.set('id', str(key))
        for idx, val in enumerate(book_dict[key]):
            sentence = ET.SubElement(chapter, 'sentence')
            sentence.set('id', str(idx + 1))
            sentence.text = val

    # tree = ET.ElementTree(book_root)
    # tree.write(filename)
    filename = book_root.get('id') + "_" + lang.text + ".xml"
    file = open(filename, 'w')
    file.write(prettify(book_root))


def prettify(element):
    """ Return a pretty-printed XML string for the Element.
        """
    rough_string = ET.tostring(element, 'utf-8')
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="    ")
