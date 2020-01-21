DB_CONFIG_FILE = 'db_config.ini'

BOOK_INSERT_QUERY = "INSERT INTO dim_book (code, added_at) " \
                    "VALUES (%(code)s, %(added_at)s)"

AUTHOR_INSERT_QUERY = "INSERT INTO dim_author (name, total_books) " \
                      "VALUES (%(name)s, %(total_books)s)"

BOOK_INFO_INSERT_QUERY = "INSERT INTO dim_book_info (title, description, lang, source, is_translation, " \
                         "total_chapters, isbn, book) " \
                         "VALUES (%(title)s, %(description)s, %(lang)s, %(source)s, %(is_translation)s, " \
                         "%(total_chapters)s, %(isbn)s, %(book)s) "

BOOK_AUTHOR_INSERT_QUERY = "INSERT INTO map_book_author (author, book, translator) " \
                           "VALUES (%(author)s, %(book)s, %(translator)s)"

CONTENT_INSERT_QUERY = "INSERT INTO dim_book_content (book) VALUES(%(book)s)"

CHAPTER_INSERT_QUERY = "INSERT INTO dim_book_chapter (c_num, name, book_content) " \
                       "VALUES (%(c_num)s, %(name)s, %(book_content)s)"

SENTENCE_INSERT_QUERY = "INSERT INTO dim_book_sentence (s_num, text, chapter) VALUES (%(s_num)s, %(text)s, %(chapter)s)"

AUTHOR_SEARCH_QUERY = "SELECT * FROM dim_author WHERE dim_author.name = %(name)s"

AUTHOR_UPDATE_QUERY = "UPDATE dim_author SET dim_author.total_books = %(total_books)s WHERE id = %(id)s"