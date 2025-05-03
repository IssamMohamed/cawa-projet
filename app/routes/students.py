from flask import Blueprint, jsonify, request
from app.services.db import get_connection
from app.services.xml_file_sync import load_students_xml, append_student_to_xml, delete_student_from_xml
from app.services.xml_utils import transform_xml
import os
import xml.etree.ElementTree as ET

students_bp = Blueprint('students', __name__)
XSLT_PATH = os.path.join(os.path.dirname(__file__), '..', 'xslt', 'student_transform.xslt')

def get_students_file_name():
    try:
        conn = get_connection()
        if conn is None:
            print("Connection failed!")
            return None
        
        # Debugging: Check connection
        print("Successfully connected to the database.")

        cur = conn.cursor()

        # Test query to check the connection
        cur.execute("SELECT 1;")
        test_result = cur.fetchone()
        print(f"Test query result: {test_result}")  # Should return [(1,)]

        # Now query for the filename
        cur.execute("SELECT filename FROM students LIMIT 1;")
        row = cur.fetchone()

        # Debugging: Output the fetched row
        print(f"Query result: {row}")  # Should return something like ('filename_value',)

        if row:
            print(row)
            return row[0]  # This should be the filename, returned from the first column
        else:
            print("No filename found in the database.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if conn:
            cur.close()
            conn.close()





# GET /students
@students_bp.route('/', methods=['GET'])
def get_students():
    file_name = get_students_file_name()
    if not file_name:
        return jsonify({"error": "No students file name found in database."}), 404

    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', file_name)

    if not os.path.exists(file_path):
        return jsonify({"error": "Students XML file does not exist."}), 404

    tree = ET.parse(file_path)
    root = tree.getroot()

    students = []
    for student_element in root.findall('student'):
        xml_string = ET.tostring(student_element, encoding='unicode')
        student_json = transform_xml(xml_string, XSLT_PATH)
        if student_json:
            students.append(student_json)

    return jsonify(students)

# POST /students
@students_bp.route('/', methods=['POST'])
def add_student():
    student_data = request.json
    
    full_name = student_data.get('full_name')
    birth_date = student_data.get('birth_date')
    faculty = student_data.get('faculty')
    specialty = student_data.get('specialty')
    matricule_id = student_data.get('matricule_id')
    year_of_study = student_data.get('year_of_study')
    college = student_data.get('college')

    # Generate a new student id
    tree = load_students_xml()
    root = tree.getroot()
    existing_ids = [int(student.find('id').text) for student in root.findall('student')]
    new_id = max(existing_ids, default=0) + 1

    # Create new student XML string
    student_xml = f"""
    <student>
        <id>{new_id}</id>
        <full_name>{full_name}</full_name>
        <birth_date>{birth_date}</birth_date>
        <faculty>{faculty}</faculty>
        <specialty>{specialty}</specialty>
        <matricule_id>{matricule_id}</matricule_id>
        <year_of_study>{year_of_study}</year_of_study>
        <college>{college}</college>
    </student>
    """

    success = append_student_to_xml(student_xml)
    if not success:
        return jsonify({"error": "Invalid student data."}), 400

    return jsonify({"id": new_id, "message": "Student added successfully"}), 201

# DELETE /students/<id>
@students_bp.route('/<int:id>', methods=['DELETE'])
def delete_student(id):
    success = delete_student_from_xml(id)
    if not success:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": f"Student with ID {id} deleted successfully"}), 200
