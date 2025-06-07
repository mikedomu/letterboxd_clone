import sqlite3

class RatingManager:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def add_or_update_rating(self, user_id, movie_id, rating):
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
            print(f"Błąd bazy danych: {e}")
            return False

    def delete_rating(self, user_id, movie_id):
        try:
            self.cursor.execute("""
                DELETE FROM ratings 
                WHERE user_id = ? AND movie_id = ?
            """, (user_id, movie_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Błąd podczas usuwania oceny: {e}")

    def get_user_rated_movies(self, user_id):
        self.cursor.execute("""
            SELECT m.title, r.rating
            FROM ratings r
            JOIN movies m ON r.movie_id = m.id
            WHERE r.user_id = ?
            ORDER BY r.rating DESC
        """, (user_id,))
        return self.cursor.fetchall()

    def get_movie_id_by_title(self, title):
        self.cursor.execute("SELECT id FROM movies WHERE title = ?", (title,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_rating(self, user_id, movie_id):
        self.cursor.execute("""
            SELECT rating FROM ratings 
            WHERE user_id = ? AND movie_id = ?
        """, (user_id, movie_id))
        result = self.cursor.fetchone()
        return result[0] if result else 0