import psycopg2
from psycopg2.extras import RealDictCursor


class AppLogic:
    def __init__(self):
        # Подключение к базе данных
        self.connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="",
            host="localhost",
            port="5432"
        )
        self.connection.autocommit = True

    # Получение всех книг или фильтрация по статусу
    def get_books(self, status_code=None):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            if status_code:
                cursor.execute("""
                    SELECT b.id, b.title, b.author, b.description, s.name AS status
                    FROM books b
                    JOIN statuses s ON b.status_id = s.id
                    WHERE s.code = %s
                    ORDER BY b.created_at DESC
                """, (status_code,))
            else:
                cursor.execute("""
                    SELECT b.id, b.title, b.author, b.description, s.name AS status
                    FROM books b
                    JOIN statuses s ON b.status_id = s.id
                    ORDER BY b.created_at DESC
                """)
            return cursor.fetchall()

    # Добавление новой книги
    def add_book(self, title, author=None, description=None, status_code="want_to_read"):
        """Добавление новой книги"""
        with self.connection.cursor() as cursor:
            # Получаем ID статуса
            cursor.execute("SELECT id FROM statuses WHERE code = %s", (status_code,))
            status_id = cursor.fetchone()
            if not status_id:
                raise ValueError("Неверный статус книги")

            # Добавляем запись в таблицу books
            cursor.execute("""
                INSERT INTO books (title, author, description, status_id)
                VALUES (%s, %s, %s, %s)
            """, (title, author, description, status_id[0]))

    # Обновление статуса книги
    def update_status(self, book_id, new_status_code):
        """Обновление статуса книги"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id FROM statuses WHERE code = %s", (new_status_code,))
            status_id = cursor.fetchone()
            if not status_id:
                raise ValueError("Неверный статус книги")

            cursor.execute("""
                UPDATE books
                SET status_id = %s
                WHERE id = %s
            """, (status_id[0], book_id))

    # Удаление книги
    def delete_book(self, book_id):
        """Удаление книги"""
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
