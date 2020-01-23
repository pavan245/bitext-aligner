import txt_parser.csv_utils as read_csv
import utils.constants as const

books_list = read_csv.read_books_csv_file(const.CSV_FILE)

for book in books_list:
    print(book)
    print(type(book))

read_csv.write_books_data_to_csv(const.CSV_FILE, books_list)