import csv
import os
import utils.constants as const


csv_header_row = ['Index', 'BookCode', 'Language', 'BookName', 'Status']


def read_books_csv_file(csv_file_name):
    csv_file_path = os.path.dirname(os.path.dirname(__file__))+'/'+csv_file_name
    with open(csv_file_path, 'r') as file:
        books_data = csv.reader(file, delimiter=';')
        books_list = []
        is_header = True
        for book in books_data:
            if is_header:
                is_header = False
                continue
            books_list.append(book)
        return books_list


def write_books_data_to_csv(csv_file_name, books_list):
    csv_file_path = os.path.dirname(os.path.dirname(__file__))+'/'+csv_file_name
    with open(csv_file_path, 'w') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(csv_header_row)
        for book in books_list:
            writer.writerow(book)


def read_data_file(file_name):
    txt_file_path = os.path.dirname(os.path.dirname(__file__)) + const.DATA_FOLDER + file_name
    with open(txt_file_path, 'r') as file:
        lines = file.readline()
        file.close()
        return lines