"""
Report Generator Script for Rooms and Students

This script performs the following operations:
1. Parses command-line arguments for student and room JSON input files.
2. Loads and inserts data into a database using custom classes.
3. Computes various analytical reports on the data.
4. Outputs reports to files in JSON or XML format based on user input.

Dependencies:
- db_config: Contains database connection settings and default paths.
- database_manager: Manages database connections, table creation, and data insertion.
- json_data_loader: Loads room and student data from JSON files.
- report_generator: Generates analytical reports from the database.

Run this script from the command line and follow the prompt to choose the output format.
"""

import argparse
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from decimal import Decimal
import os

from db_config import DB_SETTINGS, DEFAULT_ROOMS_JSON_FILE, DEFAULT_STUDENTS_JSON_FILE
from database_manager import DatabaseManager
from json_data_loader import JsonDataLoader
from report_generator import ReportGenerator


def generate_json_output(data, headers):
    """
    Convert query result data into a formatted JSON string.

    Each row in the input data is mapped to a dictionary using the headers,
    with special handling for Decimal values.

    Args:
        data (list[tuple]): List of tuples representing rows from a database query.
        headers (list[str]): List of column names corresponding to each element in the row.

    Returns:
        str: JSON-formatted string with pretty indentation and Unicode support.
    """
    results = []
    for row in data:
        row_dict = {}
        for i, header in enumerate(headers):
            value = row[i]
            if isinstance(value, Decimal):
                if header.endswith('_age') or header.endswith('_difference'):
                    value = int(value)
                else:
                    value = float(value)
            row_dict[header] = value
        results.append(row_dict)
    return json.dumps(results, indent=4, ensure_ascii=False)


def generate_xml_output(data, headers, root_name="report", item_name="item"):
    """
    Convert query result data into a formatted XML string.

    Constructs an XML tree where each row becomes a child element under a root element.
    Decimal values are converted to int or float depending on the field type.

    Args:
        data (list[tuple]): List of tuples representing rows from a database query.
        headers (list[str]): List of column names corresponding to each element in the row.
        root_name (str): Name of the root XML element. Defaults to "report".
        item_name (str): Name of each item element under the root. Defaults to "item".

    Returns:
        str: Pretty-formatted XML string with UTF-8 encoding.
    """
    root = ET.Element(root_name)
    for row in data:
        item = ET.SubElement(root, item_name)
        for i, header in enumerate(headers):
            sub_element = ET.SubElement(item, header)
            value = row[i]
            if isinstance(value, Decimal):
                if header.endswith('_age') or header.endswith('_difference'):
                    value = int(value)
                else:
                    value = float(value)
            sub_element.text = str(value)

    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding="utf-8").decode('utf-8')


def save_report_to_file(filename, content):
    """
    Save the given content to a file.

    Args:
        filename (str): Path to the file where the content should be saved.
        content (str): The content to be written to the file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    """
    Entry point for the report generation script.

    This function:
    - Parses command-line arguments for file paths and output directory.
    - Prompts the user to select an output format (JSON or XML).
    - Loads room and student data from JSON files.
    - Initializes and connects to the database.
    - Creates tables, inserts data, and builds indexes.
    - Generates various analytical reports and saves them in the selected format.

    Reports include:
    - Room student counts.
    - Rooms with minimum average student age.
    - Rooms with maximum age difference.
    - Rooms with mixed gender.

    Handles common runtime exceptions and ensures clean database disconnection.
    """
    parser = argparse.ArgumentParser(description="Generator of the results for students and rooms")
    parser.add_argument('--students', type=str, default=DEFAULT_STUDENTS_JSON_FILE,
                        help=f'Path to the students JSON file (default: {DEFAULT_STUDENTS_JSON_FILE})')
    parser.add_argument('--rooms', type=str, default=DEFAULT_ROOMS_JSON_FILE,
                        help=f'Path to the rooms JSON file (default: {DEFAULT_ROOMS_JSON_FILE})')
    parser.add_argument('--output_dir', type=str, default='reports',
                        help='Directory to save the reports (default: reports)')

    args = parser.parse_args()

    while True:
        choice = input("Choose output file type:\n1. JSON\n2. XML\nEnter 1 or 2: ")
        if choice == '1':
            output_format = 'json'
            break
        elif choice == '2':
            output_format = 'xml'
            break
        else:
            print("Incorrect choice. Choose 1 or 2.")

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    db_manager = None
    try:
        data_loader = JsonDataLoader(args.rooms, args.students)
        rooms_data = data_loader.load_rooms()
        students_data = data_loader.load_students()

        db_manager = DatabaseManager(DB_SETTINGS)
        db_manager.connect()

        db_manager.create_tables()
        db_manager.insert_rooms_data(rooms_data)
        db_manager.insert_students_data(students_data)

        db_manager.add_indexes()

        report_generator = ReportGenerator(db_manager)

        # Report 1: Room student counts
        rooms_students_count = report_generator.get_rooms_with_student_count()
        headers_count = ['room_id', 'room_name', 'student_count']
        output_content = generate_json_output(rooms_students_count, headers_count) if output_format == 'json' \
            else generate_xml_output(rooms_students_count, headers_count, "rooms_student_count", "room_stat")
        save_report_to_file(os.path.join(args.output_dir, f'rooms_student_count.{output_format}'), output_content)

        # Report 2: Rooms with minimum average age
        rooms_min_avg_age = report_generator.get_rooms_with_min_avg_age()
        headers_min_age = ['room_id', 'room_name', 'avg_age']
        output_content = generate_json_output(rooms_min_avg_age, headers_min_age) if output_format == 'json' \
            else generate_xml_output(rooms_min_avg_age, headers_min_age, "rooms_min_avg_age", "room_avg_age")
        save_report_to_file(os.path.join(args.output_dir, f'rooms_min_avg_age.{output_format}'), output_content)

        # Report 3: Rooms with maximum age difference
        rooms_max_age_diff = report_generator.get_rooms_with_max_age_difference()
        headers_max_diff = ['room_id', 'room_name', 'age_difference']
        output_content = generate_json_output(rooms_max_age_diff, headers_max_diff) if output_format == 'json' \
            else generate_xml_output(rooms_max_age_diff, headers_max_diff, "rooms_max_age_difference", "room_age_diff")
        save_report_to_file(os.path.join(args.output_dir, f'rooms_max_age_difference.{output_format}'), output_content)

        # Report 4: Rooms with mixed sex students
        rooms_mixed_sex = report_generator.get_rooms_with_mixed_sex_students()
        headers_mixed_sex = ['room_id', 'room_name']
        output_content = generate_json_output(rooms_mixed_sex, headers_mixed_sex) if output_format == 'json' \
            else generate_xml_output(rooms_mixed_sex, headers_mixed_sex, "rooms_mixed_sex", "room_mixed_sex")
        save_report_to_file(os.path.join(args.output_dir, f'rooms_mixed_sex.{output_format}'), output_content)

        print(f"\nAll your reports have been saved to the directory '{args.output_dir}'.")

    except (ConnectionError, FileNotFoundError, RuntimeError, ValueError) as e:
        print(f'Could not connect to the database. Error: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')
        import traceback
        traceback.print_exc()
    finally:
        if db_manager:
            db_manager.disconnect()


if __name__ == "__main__":
    main()
