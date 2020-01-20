import time
import db.mysql_connection as mysql
import db.constants as const


def add_book_to_db(book_code, book_dict):
    # print('Adding Book Code :: ', book_code, ' Dict  :: ', book_dict)

    conn = mysql.get_new_mysql_connection('db_config.ini')
    if conn is None:
        return False

    db_cursor = conn.cursor(buffered=True)

    # add book data to the Table First
    book_row = {
        'code': book_code,
        'added_at': int(time.time())
    }

    # returns the last row id, if row added to the table successfully
    last_rowid = add_book_row_to_table(db_cursor, const.BOOK_INSERT_QUERY, book_row)
    book_id = last_rowid
    print('Book Row Id :: ', last_rowid)

    book_info_dict = book_dict['bookInfo']
    if last_rowid > 0:
        book_info_row = {
            'title': book_info_dict['title'],
            'description': book_info_dict['description'] if 'description' in book_info_dict else None,
            'lang': book_info_dict['lang'],
            'source': book_info_dict['source'],
            'is_translation': 'true' == book_info_dict['isTranslation'].lower(),
            'total_chapters': book_info_dict['totalChapters'],
            'isbn': book_info_dict['isbn'] if 'isbn' in book_info_dict else None,
            'book': book_id
        }

        # returns the last row id, if row added to the table successfully
        last_rowid = add_book_info_row_to_table(db_cursor, const.BOOK_INFO_INSERT_QUERY, book_info_row)
        print('Book Info Row Id :: ', last_rowid)

    if last_rowid > 0:
        book_info_id = last_rowid
        authors_list = book_info_dict['authors']
        for author in authors_list:
            author_row = {
                'id': -1,
                'name': author['name'].strip().lower(),
                'total_books': 1
            }
            author_row = search_author(db_cursor, const.AUTHOR_SEARCH_QUERY, author_row)
            print('Author Search Result :: ', author_row)
            if author_row['id'] > 0:
                author_row['total_books'] = author_row['total_books'] + 1
                last_rowid = update_author_book_count(db_cursor, const.AUTHOR_UPDATE_QUERY, author_row)
                print('Author Update Row count :: ', last_rowid)
                if last_rowid <= 0:
                    break
            else:
                author_row['name'] = author['name']
                author_row['total_books'] = 1
                last_rowid = add_author_to_table(db_cursor, const.AUTHOR_INSERT_QUERY, author_row)
                print('Add Author Row Id :: ', last_rowid)
                if last_rowid > 0:
                    author_row['id'] = last_rowid

            if author_row['id'] > 0:
                author_is_translator = False
                if 'translator' in author:
                    author_is_translator = 'true' == author['translator'].lower()
                map_author_book = {
                    'author': author_row['id'],
                    'book': book_info_id,
                    'translator': author_is_translator
                }

                last_rowid = add_author_book_mapping(db_cursor, const.BOOK_AUTHOR_INSERT_QUERY, map_author_book)
                print('Author Book Mapping Row ID :: ', last_rowid)
                if last_rowid < 0:
                    break

    if last_rowid > 0:
        book_content_row = {
            'book': book_id
        }

        # returns the last row id, if row added to the table successfully
        last_rowid = add_book_content_row_to_table(db_cursor, const.CONTENT_INSERT_QUERY, book_content_row)
        print('Book Content Row Id :: ', last_rowid)

    if last_rowid > 0:
        content_id = last_rowid
        book_chapters_list = book_dict['content']['chapters']
        for chapter in book_chapters_list:
            book_chapter_row = {
                'c_num': chapter['num'],
                'name': chapter['name'] if 'name' in chapter else None,
                'book_content': content_id
            }
            chapter_id = add_book_chapter_to_table(db_cursor, const.CHAPTER_INSERT_QUERY, book_chapter_row)
            print('Book Chapter Row Id :: ', chapter_id)
            if chapter_id > 0:
                sentences_dict = chapter['sentences']
                for s_num in sentences_dict.keys():
                    sentence_row = {
                        's_num': s_num,
                        'text': sentences_dict[s_num],
                        'chapter': chapter_id
                    }
                    sen_id = add_book_sentence_to_table(db_cursor, const.SENTENCE_INSERT_QUERY, sentence_row)
                    print('Book Sentence Id :: ', sen_id)
                    if sen_id <= 0:
                        break
                    else:
                        last_rowid = sen_id
            else:
                break

    db_cursor.close()

    is_success = False
    if last_rowid > 0:
        conn.commit()
        is_success = True
    else:
        conn.rollback()
        is_success = False

    conn.close()

    return is_success


def add_book_row_to_table(db_cursor, book_insert_query, book_row):
    try:
        # Insert this Book row to Table
        db_cursor.execute(book_insert_query, book_row)
        book_id = db_cursor.lastrowid
        if book_id is not None:
            return book_id
        else:
            return -1

    except Exception as e:
        print(str(e))
        return -1


def add_book_info_row_to_table(db_cursor, book_info_insert_query, book_info_row):
    try:
        # Insert this BookInfo row
        db_cursor.execute(book_info_insert_query, book_info_row)
        book_info_id = db_cursor.lastrowid
        if book_info_id is not None:
            return book_info_id
        else:
            return -1

    except Exception as e:
        print(str(e))
        return -1


def add_book_content_row_to_table(db_cursor, book_content_insert_query, book_content_row):
    try:
        # Insert Book Content row
        db_cursor.execute(book_content_insert_query, book_content_row)
        book_content_id = db_cursor.lastrowid
        if book_content_id is not None:
            return book_content_id
        else:
            return -1

    except Exception as e:
        print(str(e))
        return -1


def add_book_chapter_to_table(db_cursor, book_chapter_insert_query, book_chapter_row):
    try:
        # Insert Book chapter row
        db_cursor.execute(book_chapter_insert_query, book_chapter_row)
        book_chapter_id = db_cursor.lastrowid
        if book_chapter_id is not None:
            return book_chapter_id
        else:
            return -1

    except Exception as e:
        print(str(e))
        return -1


def add_book_sentence_to_table(db_cursor, book_sentence_insert_query, book_sentence):
    try:
        # Insert sentence
        db_cursor.execute(book_sentence_insert_query, book_sentence)
        book_sen_id = db_cursor.lastrowid
        if book_sen_id is not None:
            return book_sen_id
        else:
            return -1

    except Exception as e:
        print(str(e))
        return -1


def add_author_to_table(db_cursor, author_insert_query, author_data):
    try:
        # Insert Author
        db_cursor.execute(author_insert_query, author_data)
        author_id = db_cursor.lastrowid
        if author_id is not None:
            return author_id
        else:
            return -1

    except Exception as e:
        print(str(e))
        return -1


def add_author_book_mapping(db_cursor, book_author_insert_query, book_author_data):
    try:
        # Insert Book Author Mapping
        db_cursor.execute(book_author_insert_query, book_author_data)
        map_id = db_cursor.rowcount
        if map_id > 0:
            return map_id
        else:
            return -1

    except Exception as e:
        print(str(e))
        return -1


def search_author(db_cursor, author_search_query, author_data):
    try:
        # Search Author
        db_cursor.execute(author_search_query, author_data)
        row = db_cursor.fetchone()
        if row is not None:
            author_data['id'] = int(row[0])
            author_data['total_books'] = int(row[2])
            return author_data
        else:
            author_data['id'] = -1
            return author_data

    except Exception as e:
        print(str(e))
        author_data['id'] = -1
        return author_data


def update_author_book_count(db_cursor, author_update_query, author_data):
    try:
        # Update Author Book Count
        db_cursor.execute(author_update_query, author_data)
        row_cnt = db_cursor.rowcount
        if row_cnt > 0:
            return row_cnt
        else:
            return -1

    except Exception as e:
        print(str(e))
        return -1
