from collections import OrderedDict
import os
import pandas as pd


def get_book_content():
    csv_path = os.path.dirname(os.path.realpath(__file__)) + '/test_example.csv'
    print('Test CSV File :: ', csv_path)
    df = pd.read_csv(csv_path, header=None).rename(
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
        "book_id": "fdcap_book",
        "title": "Crime and Punishment",
        "lang": "en",
        "isTranslation": "true",
        "totalChapters": "2",
        "authors": [
            {
                "name": "Herr Isaac Riley",
                "translator": "true"
            },
            {
                "name": "Fyodor Dostoevsky"
            }
        ],
        "description": "Crime and Punishment (Russian: Преступление и наказание) is a novel written by Russian author "
                       "Fyodor Dostoevsky.First published in a journal named The Russian Messenger, it appeared in "
                       "twelve monthly installments in 1866, and was later published as a novel",
        "source": "https://en.wikisource.org/wiki/Crime_and_Punishment"
    }

    return dict_metadata
