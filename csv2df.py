from collections import OrderedDict

import pandas as pd


def get_book_content():
    df = pd.read_csv("test_example.csv", header=None).rename(
        columns={0: 'chapter', 1: 'sentence', 2: 'text'})

    book_dict = OrderedDict()

    for index, row in df.iterrows():
        ch_id = row['chapter']
        s_id = row['sentence']
        text = row['text']
        # print(ch_id, " -> ", s_id, " -> ", text)

        if ch_id not in book_dict:
            book_dict[ch_id] = []
        book_dict[ch_id].append(text)

    return book_dict


def get_book_metadata():

    dict_metadata = {
        "book_id": "abcdef",
        "title": "Bullshit",
        "lang": "en",
        "isTranslation": "true",
        "totalChapters": "2",
        "authors": [
            {
                "name": "Herr Riley",
                "translator": "true"
            },
            {
                "name": "Herr Singh"
            }
        ],
        "description": "Some Random Bullshit description",
        "source": "https://www.idontcare.com"
    }

    return dict_metadata
