"""
Module managing application users.
"""

import sqlite3
from password_hasher import PasswordHasher

class UserManager:
    """
    Class managing application users.

    :param cursor: SQLite database cursor.
    :type cursor: sqlite3.Cursor
    :param conn: SQLite database connection.
    :type conn: sqlite3.Connection
    """

    def __init__(self, cursor, conn):
        """
        Initializes the user manager.

        :param cursor: SQLite database cursor.
        :type cursor: sqlite3.Cursor
        :param conn: SQLite database connection.
        :type conn: sqlite3.Connection
        """
        self.cursor = cursor
        self.conn = conn

    def register_user(self, username, password):
        """
        Registers a new user in the system.

        :param username: Username.
        :type username: str
        :param password: User's password.
        :type password: str
        :raises sqlite3.IntegrityError: If user with given username already exists.
        """
        hashed_password = PasswordHasher.hash(password)
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
            ''', (username, hashed_password))
            self.conn.commit()
            print(f"User '{username}' has been registered.")
        except sqlite3.IntegrityError:
            print(f"User '{username}' already exists!")

    def login_user(self, username, password):
        """
        Verifies user login credentials.

        :param username: Username.
        :type username: str
        :param password: User's password.
        :type password: str
        :return: Tuple (bool, int) - (login success, user_id).
        :rtype: tuple
        """
        self.cursor.execute('SELECT id, password_hash FROM users WHERE username=?', (username,))
        result = self.cursor.fetchone()

        if result:
            user_id, stored_password_hash = result
            if PasswordHasher.verify(password, stored_password_hash):
                return True, user_id
        return False, None
