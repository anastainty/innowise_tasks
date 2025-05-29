"""
Module for generating analytical reports on student and room data.

This module defines the ReportGenerator class, which uses a DatabaseManager
instance to execute SQL queries and produce various analytical reports
related to student demographics and room assignments stored in a PostgreSQL database.

Features include:
- Counting students per room.
- Identifying rooms with minimum average student age.
- Finding rooms with maximum age differences among students.
- Listing rooms with mixed-sex student populations.
- Utility method to calculate age from birthday strings.

Intended usage:
- Instantiate ReportGenerator with an active DatabaseManager.
- Call report methods to retrieve analysis results.
"""

from datetime import date
from decimal import Decimal

class ReportGenerator:
    """
    Generates analytical reports from student and room data stored in a PostgreSQL database.

    Attributes:
        db_manager (DatabaseManager): Instance responsible for database operations.
    """

    def __init__(self, db_manager):
        """
        Initializes the ReportGenerator with a given DatabaseManager instance.

        Args:
            db_manager (DatabaseManager): An instance for executing queries and fetching results.
        """
        self.db_manager = db_manager

    def get_rooms_with_student_count(self):
        """
        Retrieves a list of all rooms along with the number of students assigned to each room.

        Returns:
            list: A list of tuples containing room ID, room name, and student count.
        """
        self.db_manager.execute_query("""
            SELECT
                r.id AS room_id,
                r.name AS room_name,
                COUNT(s.id) AS student_count
            FROM
                rooms r
            LEFT JOIN
                students s ON r.id = s.room
            GROUP BY
                r.id, r.name
            ORDER BY
                r.id;
        """)
        return self.db_manager.fetch_all()

    def get_rooms_with_min_avg_age(self):
        """
        Retrieves the top 5 rooms with the lowest average student age.

        Returns:
            list: A list of tuples containing room ID, room name, and average age.
        """
        self.db_manager.execute_query("""
            SELECT
                r.id AS room_id,
                r.name AS room_name,
                AVG(EXTRACT(YEAR FROM AGE(NOW(), s.birthday)))::numeric(5,2) AS avg_age
            FROM
                rooms r
            JOIN
                students s ON r.id = s.room
            GROUP BY
                r.id, r.name
            HAVING
                COUNT(s.id) > 0 
            ORDER BY
                avg_age ASC
            LIMIT 5;
        """)
        return self.db_manager.fetch_all()

    def get_rooms_with_max_age_difference(self):
        """
        Retrieves the top 5 rooms with the largest age difference among students.

        Returns:
            list: A list of tuples containing room ID, room name, and age difference.
        """
        self.db_manager.execute_query("""
            SELECT
                r.id AS room_id,
                r.name AS room_name,
                (MAX(EXTRACT(YEAR FROM AGE(NOW(), s.birthday))) - MIN(EXTRACT(YEAR FROM AGE(NOW(), s.birthday))))::numeric(5,2) AS age_difference
            FROM
                rooms r
            JOIN
                students s ON r.id = s.room
            GROUP BY
                r.id, r.name
            HAVING
                COUNT(s.id) > 1
            ORDER BY
                age_difference DESC
            LIMIT 5;
        """)
        return self.db_manager.fetch_all()

    def get_rooms_with_mixed_sex_students(self):
        """
        Retrieves a list of rooms that contain students of both sexes.

        Returns:
            list: A list of tuples containing room ID and room name.
        """
        self.db_manager.execute_query("""
            SELECT
                r.id AS room_id,
                r.name AS room_name
            FROM
                rooms r
            JOIN
                students s ON r.id = s.room
            GROUP BY
                r.id, r.name
            HAVING
                COUNT(DISTINCT s.sex) > 1 
            ORDER BY
                r.id;
        """)
        return self.db_manager.fetch_all()

    @staticmethod
    def calculate_age_from_birthday(birthday_str):
        """
        Calculates age from an ISO-formatted birthday string.

        Args:
            birthday_str (str): Birthday string in ISO format (e.g., "2000-01-01T00:00:00").

        Returns:
            int: Age in full years based on today's date.
        """
        birth_date = date.fromisoformat(birthday_str.split('T')[0])
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
