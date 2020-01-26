from lxml import etree
import os
import utils.constants as const
import unicodedata as unicode


namespaces = {'xmlns': "http://www.gribuser.ru/xml/fictionbook/2.0"}


def read_fb2_file(file_name, book_code, source, encoding):
    full_file_path = os.path.dirname(os.path.dirname(__file__))+'/data/'+file_name
    print(const.BLUE, 'Reading :: ', full_file_path, const.END)

    book_dict = {}
    tree = etree.parse(full_file_path)
    root = tree.getroot()

    book_info_dict = create_book_info_dict(root, book_code, source)

    # Add Book Metadata to Book Dictionary
    book_dict['metadata'] = book_info_dict

    book_content = create_book_content(root, book_info_dict['lang'])

    # Add Chapter count to Book Metadata
    book_dict['metadata']['totalChapters'] = len(book_content)

    # Add Book Content/Chapters List to book_dict
    book_dict['content'] = book_content

    # print('Book Metadata :: ', file_name, ' -> ', book_dict['metadata'])
    # print('Book Content :: ', file_name, ' -> ', book_dict['content'][0:2])

    return book_dict


def create_book_content(root, lang):
    book_content_list = []

    body_element = root.find('xmlns:body', namespaces)
    if body_element is None:
        return book_content_list

    section_list = body_element.findall('xmlns:section', namespaces)
    # print('Length of Sections :: ', len(section_list))
    chapter_num = 1
    for section in section_list:
        sub_section_list = section.findall('xmlns:section', namespaces)
        # print('Length of Subsections :: ', len(sub_section_list))
        paragraph_list = section.findall('xmlns:p', namespaces)
        # print('Length of Paragraphs :: ', len(paragraph_list))

        # Check if this section is first Header Section without Content
        if len(sub_section_list) == 0 and len(paragraph_list) == 0:
            continue

        if len(sub_section_list) > 0:
            section_title = get_section_title(section, lang, False).strip()
            # get subsection title and subsection paragraphs
            for sub_section in sub_section_list:
                sub_section_title = get_section_title(sub_section, lang, True)
                if sub_section_title is None or len(sub_section_title) <= 0:
                    continue

                chapter_content = get_chapter_content_from_section(sub_section)
                if chapter_content is None or len(chapter_content) <= 0:
                    continue

                book_content_list.append({
                    'chapter_num': chapter_num,
                    'chapter_name': section_title+' - '+sub_section_title.strip(),
                    'text_content': chapter_content
                })
                chapter_num += 1

        elif len(paragraph_list) > 0:
            section_title = get_section_title(section, lang, True)
            if section_title is None or len(section_title) <= 0:
                continue

            chapter_content = get_chapter_content_from_section(section)
            if chapter_content is None or len(chapter_content) <= 0:
                continue

            book_content_list.append({
                'chapter_num': chapter_num,
                'chapter_name': section_title.strip(),
                'text_content': chapter_content
            })
            chapter_num += 1

    return book_content_list


def get_chapter_content_from_section(section):
    paragraphs = section.findall('xmlns:p', namespaces)
    chapter_content = ''
    if len(paragraphs) > 0:
        for paragraph in paragraphs:
            paragraph_text = paragraph.text
            if paragraph_text is None:
                continue

            chapter_content = chapter_content+' '+paragraph_text.strip()

        normalized_content = unicode.normalize("NFKD", chapter_content)
        return normalized_content
    else:
        return None


def get_section_title(section, lang, is_chapter):
    section_title_name = ''
    title_p_list = section.findall('xmlns:title/xmlns:p', namespaces)
    if len(title_p_list) > 0:
        for title_p in title_p_list:
            p_text = title_p.text
            if p_text is None:
                continue
            section_title_name = section_title_name+' '+p_text.strip()

        if is_chapter and len(section_title_name) <= 5:
            section_title_name = const.CHAPTER_NAMES[lang]+' '+section_title_name
        return section_title_name


def create_book_info_dict(root, book_code, book_source):
    book_info_dict = {}
    title_info = root.find('xmlns:description/xmlns:title-info', namespaces)
    if title_info is None:
        return book_info_dict

    book_info_dict['book_code'] = book_code

    book_title = title_info.find('xmlns:book-title', namespaces)
    if book_title is not None:
        book_info_dict['title'] = book_title.text

    book_info_dict['lang'] = title_info.find('xmlns:lang', namespaces).text

    src_lang = title_info.find('xmlns:src-lang', namespaces)
    if src_lang is not None:
        book_src_lang = src_lang.text
        if book_src_lang != book_info_dict['lang']:
            book_info_dict['isTranslation'] = 'true'
        else:
            book_info_dict['isTranslation'] = 'false'
    else:
        book_info_dict['isTranslation'] = 'false'

    book_info_dict['totalChapters'] = 0
    book_info_dict['source'] = book_source

    book_info_dict[ 'authors'] = []
    author = title_info.find('xmlns:author', namespaces)
    author_name = get_author_name(author)
    if len(author_name) > 0:
        book_info_dict['authors'].append({'name': author_name})

    translators = title_info.findall('xmlns:translator', namespaces)
    for translator in translators:
        translator_name = get_author_name(translator)
        if len(translator_name) > 0:
            book_info_dict['authors'].append({'name': translator_name, 'translator':'true'})

    return book_info_dict


def get_author_name(author_root):
    first_name = author_root.find('xmlns:first-name', namespaces)
    middle_name = author_root.find('xmlns:middle-name', namespaces)
    last_name = author_root.find('xmlns:last-name', namespaces)
    name = ''
    if first_name is not None:
        first_name_text = first_name.text
        if first_name_text is not None and len(first_name_text) > 0:
            name = first_name_text.strip()
    if middle_name is not None:
        middle_name_text = middle_name.text
        if middle_name_text is not None and len(middle_name_text) > 0:
            name = name+' '+middle_name_text.strip()
    if last_name is not None:
        last_name_text = last_name.text
        if last_name_text is not None and len(last_name_text) > 0:
            name = name+' '+last_name_text.strip()

    return name