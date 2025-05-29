"""
Configuration module for database connection and default JSON file paths.

This module defines:
- DB_SETTINGS: Dictionary with PostgreSQL database connection parameters.
- DEFAULT_ROOMS_JSON_FILE: Default path to the JSON file with rooms data.
- DEFAULT_STUDENTS_JSON_FILE: Default path to the JSON file with students data.
"""

# Database connection settings
DB_SETTINGS = {
    "host": "localhost",
    "port": "5433",
    "database": "mydatabase",
    "user": "postgres",
    "password": "secret"
}

# Default path to rooms JSON file
DEFAULT_ROOMS_JSON_FILE = 'data/rooms.json'

# Default path to students JSON file
DEFAULT_STUDENTS_JSON_FILE = 'data/students.json'
