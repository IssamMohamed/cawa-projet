import os
from lxml import etree

XML_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'students.xml')
XSD_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'students.xsd')


def load_students_xml():
    if not os.path.exists(XML_FILE_PATH):
        root = etree.Element("students")
        tree = etree.ElementTree(root)
        save_students_xml(tree)
    return etree.parse(XML_FILE_PATH)

def save_students_xml(tree):
    tree.write(XML_FILE_PATH, pretty_print=True, xml_declaration=True, encoding="UTF-8")

def validate_xml(xml_content):
    
    with open(XSD_FILE_PATH, 'rb') as xsd_file:
        schema_root = etree.XML(xsd_file.read())
        schema = etree.XMLSchema(schema_root)
    
    
    try:
        schema.assertValid(xml_content)
        return True
    except etree.DocumentInvalid as e:
        print(f"XML is invalid: {e}")
        return False

def append_student_to_xml(student_xml):
    
    student_element = etree.fromstring(student_xml)

    
    root_element = etree.Element("students")
    root_element.append(student_element)
    tree = etree.ElementTree(root_element)
    
    
    if not validate_xml(tree):
        return False  
    
    tree = load_students_xml()
    root = tree.getroot()
    root.append(student_element)
    save_students_xml(tree)
    
    return True

def delete_student_from_xml(student_id):
    tree = load_students_xml()
    
    
    xpath_query = f"//student[id='{student_id}']"
    students_to_remove = tree.xpath(xpath_query)
    
    if students_to_remove:
        for student in students_to_remove:
            student.getparent().remove(student)
        save_students_xml(tree)
        return True
    return False
