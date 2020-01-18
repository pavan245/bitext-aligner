from csv2df import get_book_content, get_book_metadata
import xml_parser.create_xml as create_xml
import xml_parser.read_xml as read_xml

create_xml.create_xml_file(get_book_content(), get_book_metadata())


book_dict = read_xml.parse_xml_file('/Users/pavanmandava/PythonWorkspace/bitext-aligner/xml_files/abcdef_en.xml')

print(book_dict)

