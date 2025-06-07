import sqlite3
import pandas as pd

class Database:
    def __init__(self, csv_path=None, db_path='movies.db'):
        self.csv_path = csv_path
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.df = None

    def create_connection(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.create_movies_table()
        self.create_users_table()
        self.create_ratings_table()
        self.create_metadata_table()

    def create_movies_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                genres TEXT,
                keywords TEXT,
                original_language TEXT,
                overview TEXT,
                production_companies TEXT,
                runtime INTEGER,
                "cast" TEXT,
                director TEXT
            )
        ''')
        self.conn.commit()

    def create_users_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create_ratings_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie_id INTEGER NOT NULL,
                rating REAL NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(movie_id) REFERENCES movies(id),
                UNIQUE(user_id, movie_id)
            )
        ''')
        self.conn.commit()

    def create_metadata_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                movies_loaded BOOLEAN DEFAULT 0
            )
        ''')
        self.cursor.execute("INSERT OR IGNORE INTO metadata (id, movies_loaded) VALUES (1, 0)")
        self.conn.commit()

    def load_data(self):
        if self.csv_path:
            self.df = pd.read_csv(self.csv_path)

    def insert_movies_data_if_needed(self):
        self.cursor.execute("SELECT movies_loaded FROM metadata WHERE id = 1")
        result = self.cursor.fetchone()

        if result and result[0] == 1:
            print("Filmy już załadowane — pomijam import.")
            return

        self.load_data()
        if self.df is None:
            print("Brak danych CSV.")
            return
        for i, (_, row) in enumerate(self.df.iterrows(), 1):
            try:
                self.cursor.execute('''
                    INSERT INTO movies (
                        title, genres, keywords, original_language, overview,
                        production_companies, runtime, "cast", director
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['title'],
                    row['genres'],
                    row['keywords'],
                    row['original_language'],
                    row['overview'],
                    row['production_companies'],
                    self.safe_int(row['runtime']),
                    row['cast'],
                    row['director']
                ))
            except sqlite3.IntegrityError:
                pass


        self.cursor.execute("UPDATE metadata SET movies_loaded = 1 WHERE id = 1")
        self.conn.commit()

    def safe_int(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    def get_movie_details(self, title):
        self.cursor.execute("""
            SELECT id, title, genres, keywords, original_language, overview,
                   production_companies, runtime, "cast", director
            FROM movies
            WHERE title = ?
        """, (title,))
        return self.cursor.fetchone()

    def search_movies(self, query):
        like_query = f"%{query}%"
        self.cursor.execute("""
            SELECT title FROM movies
            WHERE title LIKE ?
            LIMIT 20
        """, (like_query,))
        return [row[0] for row in self.cursor.fetchall()]

    def get_genres_by_movie_id(self, movie_id):
        self.cursor.execute("SELECT genres FROM movies WHERE id = ?", (movie_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None
