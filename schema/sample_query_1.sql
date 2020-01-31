SELECT 
    title, lang, is_translation
FROM
    dim_book_info
        INNER JOIN
    map_book_author ON map_book_author.book = dim_book_info.id
        INNER JOIN
    dim_author ON dim_author.id = map_book_author.author
WHERE
    dim_author.name LIKE '%Fjodor%';