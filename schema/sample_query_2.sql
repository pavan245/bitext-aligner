SELECT 
    b1.sen, b2.sen
FROM
    (SELECT 
        text AS sen, s_num AS s_num
    FROM dim_book_sentence
    INNER JOIN dim_book_chapter ON dim_book_chapter.id = dim_book_sentence.chapter
    INNER JOIN dim_book_content ON dim_book_content.id = dim_book_chapter.book_content
    INNER JOIN dim_book ON dim_book.id = dim_book_content.book
    INNER JOIN dim_book_info ON dim_book_info.book = dim_book.id
    WHERE
        dim_book.code = 'dost_under_ende'
            AND dim_book_info.lang = 'en'
            AND dim_book_chapter.c_num = '1') AS b1
        INNER JOIN
    (SELECT 
        text AS sen, s_num AS s_num
    FROM dim_book_sentence
    INNER JOIN dim_book_chapter ON dim_book_chapter.id = dim_book_sentence.chapter
    INNER JOIN dim_book_content ON dim_book_content.id = dim_book_chapter.book_content
    INNER JOIN dim_book ON dim_book.id = dim_book_content.book
    INNER JOIN dim_book_info ON dim_book_info.book = dim_book.id
    WHERE
        dim_book.code = 'dost_under_ende'
            AND dim_book_info.lang = 'de'
            AND dim_book_chapter.c_num = '1') AS b2 ON b1.s_num = b2.s_num;