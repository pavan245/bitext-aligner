import xml.etree.ElementTree as ET


def parse_xml_file(full_path):

    book_dict = {}

    tree = ET.parse(full_path)
    book_root = tree.getroot()
    # print('Root Element :: ', book_root.tag, ' | Attributes :: ', book_root.attrib)
    book_dict['code'] = book_root.attrib['code']

    book_info_dict = {}
    book_content_dict = {}
    book_info_element = book_root.find('bookInfo')
    book_content_element = book_root.find('content')

    book_info_dict['authors'] = []
    for child in book_info_element:
        if 'author' == child.tag:
            author = {'name': child.text}
            if 'translator' in child.attrib:
                author['translator'] = child.attrib['translator']
            book_info_dict['authors'].append(author)
        else:
            book_info_dict[child.tag] = child.text

    book_dict['bookInfo'] = book_info_dict

    book_content_dict['chapters'] = []
    for chapter in book_content_element:
        chapter_dict = {'num': chapter.attrib['num']}
        if 'name' in chapter.attrib:
            chapter_dict['name'] = chapter.attrib['name']
        chapter_dict['sentences'] = {}
        for sentence in chapter.findall('sentence'):
            chapter_dict['sentences'][sentence.attrib['num']] = sentence.text
        book_content_dict['chapters'].append(chapter_dict)

    book_dict['content'] = book_content_dict

    return book_dict
