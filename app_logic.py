import sqlite3
import os


class AppLogic:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.create_db()

    def create_db(self):
        if not os.path.exists(self.db_name):
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE books (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    status TEXT
                )
            ''')
            conn.commit()
            conn.close()

    def add_book(self, title, author, status="want_to_read"):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, author, status) VALUES (?, ?, ?)',
                       (title, author, status))
        conn.commit()
        conn.close()

    def get_books(self, status=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        if status:
            cursor.execute('SELECT * FROM books WHERE status=?', (status,))
        else:
            cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        conn.close()
        return books
