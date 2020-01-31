SELECT 
    dim_book_sentence.text AS Sentence,
    dim_book_chapter.c_num AS Chapter_Num,
    dim_book_info.title AS Book_Name,
    dim_book_info.lang AS Book_Language
FROM
    dim_book_sentence
        INNER JOIN
    dim_book_chapter ON dim_book_chapter.id = dim_book_sentence.chapter
        INNER JOIN
    dim_book_content ON dim_book_content.id = dim_book_chapter.book_content
        INNER JOIN
    dim_book ON dim_book.id = dim_book_content.book
        INNER JOIN
    dim_book_info ON dim_book_info.book = dim_book.id
WHERE
    dim_book_sentence.text LIKE '%spiteful%';