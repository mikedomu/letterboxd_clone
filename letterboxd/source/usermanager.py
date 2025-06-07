import sqlite3
from password_hasher import PasswordHasher

class UserManager:


    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def register_user(self, username, password):
        """Rejestruje nowego użytkownika z hashowaniem hasła."""
        hashed_password = PasswordHasher.hash(password)
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
            ''', (username, hashed_password))
            self.conn.commit()
            print(f"Użytkownik '{username}' został zarejestrowany.")
        except sqlite3.IntegrityError:
            print(f"Użytkownik '{username}' już istnieje!")

    def login_user(self, username, password):
        self.cursor.execute('SELECT id, password_hash FROM users WHERE username=?', (username,))
        result = self.cursor.fetchone()

        if result:
            user_id, stored_password_hash = result
            if PasswordHasher.verify(password, stored_password_hash):
                return True, user_id
        return False, None

