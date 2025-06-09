"""
Module managing movie ratings.
"""

import sqlite3

class RatingManager:
    """
    Class managing movie ratings in the database.

    :param cursor: SQLite database cursor.
    :type cursor: sqlite3.Cursor
    :param conn: SQLite database connection.
    :type conn: sqlite3.Connection
    """

    def __init__(self, cursor, conn):
        """
        Initializes the movie rating manager.

        :param cursor: SQLite database cursor.
        :type cursor: sqlite3.Cursor
        :param conn: SQLite database connection.
        :type conn: sqlite3.Connection
        """
        self.cursor = cursor
        self.conn = conn

    def add_or_update_rating(self, user_id, movie_id, rating):
        """
        Adds or updates a movie rating by user.

        :param user_id: User ID.
        :type user_id: int
        :param movie_id: Movie ID.
        :type movie_id: int
        :param rating: Movie rating (0.5-5.0).
        :type rating: float
        :return: True if operation succeeded, False otherwise.
        :rtype: bool
        :raises sqlite3.Error: In case of database error.
        """
        try:
            self.cursor.execute("""
                INSERT INTO ratings (user_id, movie_id, rating)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, movie_id)
                DO UPDATE SET rating = excluded.rating
            """, (user_id, movie_id, rating))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def delete_rating(self, user_id, movie_id):
        """
        Deletes a movie rating.

        :param user_id: User ID.
        :type user_id: int
        :param movie_id: Movie ID.
        :type movie_id: int
        :raises sqlite3.Error: In case of rating deletion error.
        """
        try:
            self.cursor.execute("""
                DELETE FROM ratings 
                WHERE user_id = ? AND movie_id = ?
            """, (user_id, movie_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting rating: {e}")

    def get_user_rated_movies(self, user_id):
        """
        Retrieves all movies rated by user.

        :param user_id: User ID.
        :type user_id: int
        :return: List of tuples (movie title, rating).
        :rtype: list[tuple]
        """
        self.cursor.execute("""
            SELECT m.title, r.rating
            FROM ratings r
            JOIN movies m ON r.movie_id = m.id
            WHERE r.user_id = ?
            ORDER BY r.rating DESC
        """, (user_id,))
        return self.cursor.fetchall()

    def get_movie_id_by_title(self, title):
        """
        Retrieves movie ID by its title.

        :param title: Movie title.
        :type title: str
        :return: Movie ID or None if not found.
        :rtype: int or None
        """
        self.cursor.execute("SELECT id FROM movies WHERE title = ?", (title,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_rating(self, user_id, movie_id):
        """
        Retrieves movie rating given by user.

        :param user_id: User ID.
        :type user_id: int
        :param movie_id: Movie ID.
        :type movie_id: int
        :return: Movie rating or 0 if not found.
        :rtype: float
        """
        self.cursor.execute("""
            SELECT rating FROM ratings 
            WHERE user_id = ? AND movie_id = ?
        """, (user_id, movie_id))
        result = self.cursor.fetchone()
        return result[0] if result else 0
