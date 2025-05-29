"""
Module for managing PostgreSQL database interactions.

This module provides the DatabaseManager class, which handles establishing
connections to a PostgreSQL database, creating tables, inserting and updating
room and student data, executing queries, and adding indexes to optimize queries.

Typical usage involves:
- Creating an instance with database connection settings.
- Connecting to the database.
- Creating necessary tables.
- Inserting or updating data.
- Executing queries and retrieving results.
- Adding indexes to improve query performance.
- Disconnecting from the database when done.

Dependencies:
- psycopg2: PostgreSQL database adapter for Python.
"""

import psycopg2
from psycopg2 import Error


class DatabaseManager:
    """
    Manages PostgreSQL database connections, schema creation, data insertion, and query execution.

    Attributes:
        db_settings (dict): Dictionary with database connection settings.
        connection (psycopg2.connection): Connection object to the PostgreSQL database.
        cursor (psycopg2.cursor): Cursor object for executing SQL queries.
    """

    def __init__(self, db_settings):
        """
        Initializes the DatabaseManager with provided database settings.

        Args:
            db_settings (dict): A dictionary containing host, port, database, user, and password keys.
        """
        self.db_settings = db_settings
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Establishes a connection to the PostgreSQL database and initializes the cursor.

        Raises:
            ConnectionError: If the connection to the database fails.
        """
        try:
            self.connection = psycopg2.connect(
                host=self.db_settings['host'],
                port=self.db_settings['port'],
                database=self.db_settings['database'],
                user=self.db_settings['user'],
                password=self.db_settings['password']
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except Error as e:
            raise ConnectionError(f'Database connection error: {e}')

    def disconnect(self):
        """
        Closes the cursor and database connection if they exist.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        """
        Executes a given SQL query with optional parameters.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): Parameters to use with the SQL query.

        Raises:
            RuntimeError: If an error occurs during query execution.
        """
        try:
            self.cursor.execute(query, params)
        except Error as e:
            raise RuntimeError(f'Query mistake: {e}\n Query: {query}')

    def fetch_all(self):
        """
        Retrieves all rows from the last executed query.

        Returns:
            list: A list of tuples containing the query result rows.
        """
        return self.cursor.fetchall()

    def create_tables(self):
        """
        Creates the 'rooms' and 'students' tables in the database if they do not exist.
        """
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INT PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        );
        """)

        self.execute_query("""
        CREATE TABLE IF NOT EXISTS students (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            birthday DATE,
            room INT,
            sex CHAR(1),
            CONSTRAINT fk_rooms FOREIGN KEY(room) REFERENCES rooms(id)
        );
        """)

    def insert_rooms_data(self, rooms_data):
        """
        Inserts or updates room records in the database.

        Args:
            rooms_data (list): A list of dictionaries containing room data with 'id' and 'name' keys.
        """
        insert_sql = """
            INSERT INTO rooms (id, name)
            VALUES (%s, %s)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name;
        """
        for room in rooms_data:
            self.execute_query(insert_sql, (room['id'], room['name']))

    def insert_students_data(self, students_data):
        """
        Inserts or updates student records in the database.

        Args:
            students_data (list): A list of dictionaries containing student data with keys:
                                  'id', 'name', 'birthday', 'room', and 'sex'.
        """
        insert_sql = """
            INSERT INTO students (id, name, birthday, room, sex)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                birthday = EXCLUDED.birthday,
                room = EXCLUDED.room,
                sex = EXCLUDED.sex;
        """
        for student in students_data:
            birthday_date = student['birthday'].split('T')[0]
            self.execute_query(insert_sql, (
                student['id'],
                student['name'],
                birthday_date,
                student['room'],
                student['sex']
            ))

    def add_indexes(self):
        """
        Adds indexes to the 'students' table on the columns 'room', 'sex', and 'birthday'.

        Raises:
            RuntimeError: If an error occurs while creating the indexes.
        """
        try:
            self.execute_query("CREATE INDEX IF NOT EXISTS idx_students_room ON students (room);")
            self.execute_query("CREATE INDEX IF NOT EXISTS idx_students_sex ON students (sex);")
            self.execute_query("CREATE INDEX IF NOT EXISTS idx_students_birthday ON students (birthday);")
            self.connection.commit()
        except RuntimeError as e:
            print(f"Error adding indexes: {e}")
            raise
