from csv2df import get_book_content, get_book_metadata
import xml_parser.create_xml as create_xml
import xml_parser.read_xml as read_xml
import xml_parser.validate as validate


file_path = create_xml.create_xml_file(get_book_content(), get_book_metadata())

# print(file_path)

validate.validate_all_xml_files()

# book_dict = read_xml.parse_xml_file('/Users/pavanmandava/PythonWorkspace/bitext-aligner/xml_files/abcdef_en.xml')

