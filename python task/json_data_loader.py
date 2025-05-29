"""
Module for loading JSON data for rooms and students.

This module provides the JsonDataLoader class, which handles reading and parsing
JSON files containing information about rooms and students. It ensures file existence
and handles potential parsing errors.
"""

import json
import os

class JsonDataLoader:
    """
    A class for loading JSON data from specified files containing rooms and students information.

    Attributes:
        rooms_data_path (str): Path to the JSON file containing room data.
        students_data_path (str): Path to the JSON file containing student data.
    """

    def __init__(self, rooms_data_path, students_data_path):
        """
        Initializes JsonDataLoader with paths to the rooms and students JSON files.

        Args:
            rooms_data_path (str): Path to the rooms JSON file.
            students_data_path (str): Path to the students JSON file.

        Raises:
            FileNotFoundError: If either of the provided file paths does not exist.
        """
        if not os.path.exists(students_data_path):
            raise FileNotFoundError(f'{students_data_path} does not exist')
        if not os.path.exists(rooms_data_path):
            raise FileNotFoundError(f'{rooms_data_path} does not exist')
        self.rooms_data_path = rooms_data_path
        self.students_data_path = students_data_path

    def load_rooms(self):
        """
        Loads and returns room data from the JSON file.

        Returns:
            list or dict: Parsed JSON data from the rooms file.

        Raises:
            ValueError: If the JSON file cannot be parsed.
            RuntimeError: For other errors encountered during file loading.
        """
        try:
            with open(self.rooms_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.decoder.JSONDecodeError:
            raise ValueError('Parsing of rooms data failed')
        except Exception as e:
            raise RuntimeError(f'Failed to load rooms data: {e}')

    def load_students(self):
        """
        Loads and returns student data from the JSON file.

        Returns:
            list or dict: Parsed JSON data from the students file.

        Raises:
            ValueError: If the JSON file cannot be parsed.
            RuntimeError: For other errors encountered during file loading.
        """
        try:
            with open(self.students_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.decoder.JSONDecodeError:
            raise ValueError('Parsing of students data failed')
        except Exception as e:
            raise RuntimeError(f'Failed to load students data: {e}')
