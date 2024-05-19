import sqlite3


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('rental.db')
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def create_tables(self):
        create_books_query = """
            CREATE TABLE IF NOT EXISTS Books(
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_title TEXT NOT NULL,
                book_author TEXT NOT NULL,
                book_genre TEXT NOT NULL
            );
        """
        create_people_query = """
            CREATE TABLE IF NOT EXISTS People(
                person_id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_fname TEXT NOT NULL,
                person_sname TEXT NOT NULL
            );
        """
        create_rented_books_query = """
            CREATE TABLE IF NOT EXISTS RentedBooks(
                rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                person_id INTEGER NOT NULL,
                FOREIGN KEY (book_id) REFERENCES Books (book_id),
                FOREIGN KEY (person_id) REFERENCES People (person_id)
            );
        """
        self.execute_query(create_books_query)
        self.execute_query(create_people_query)
        self.execute_query(create_rented_books_query)

    def drop_tables(self):
        drop_books_query = """DROP TABLE IF EXISTS Books;"""
        drop_people_query = """DROP TABLE IF EXISTS People;"""
        drop_rented_books_query = """DROP TABLE IF EXISTS RentedBooks;"""
        self.execute_query(drop_books_query)
        self.execute_query(drop_people_query)
        self.execute_query(drop_rented_books_query)

    def add_book(self, book_title, book_author, book_genre):
        query = """
        INSERT INTO Books (book_title, book_author, book_genre)
        VALUES (?, ?, ?)
        """
        self.execute_query(query, (book_title, book_author, book_genre))

    def add_person(self, person_fname, person_sname):
        query = """
        INSERT INTO People (person_fname, person_sname)
        VALUES (?, ?)
        """
        self.execute_query(query, (person_fname, person_sname))

    def delete_book(self, book_id):
        query = """DELETE FROM Books WHERE book_id = ?;"""
        self.execute_query(query, (book_id,))

    def delete_person(self, person_id):
        query = """DELETE FROM People WHERE person_id = ?;"""
        self.execute_query(query, (person_id,))

    def select_books(self):
        query = """SELECT * FROM Books;"""
        return self.execute_query(query)

    def select_people(self):
        query = """SELECT * FROM People;"""
        return self.execute_query(query)

    def borrow_book(self, book_title, author_name, person_fname, person_sname):
        book_query = """SELECT book_id FROM Books WHERE book_title = ? AND book_author = ?;"""
        person_query = """SELECT person_id FROM People WHERE person_fname = ? AND person_sname = ?;"""
        book_ids = self.execute_query(book_query, (book_title, author_name))
        person_id = self.execute_query(person_query, (person_fname, person_sname))

        if book_ids and person_id:
            for book_id in book_ids:
                if not self.is_book_rented(book_id[0]):
                    borrow_query = """
                    INSERT INTO RentedBooks (book_id, person_id)
                    VALUES (?, ?);
                    """
                    self.execute_query(borrow_query, (book_id[0], person_id[0][0]))
                    return True, 'Book borrowed successfully'
            return False, 'All copies of this book are already rented'
        return False, 'Book or Person not found'

    def return_book(self, book_title, author_name, person_fname, person_sname):
        book_query = """SELECT book_id FROM Books WHERE book_title = ? AND book_author = ?;"""
        person_query = """SELECT person_id FROM People WHERE person_fname = ? AND person_sname = ?;"""
        book_id = self.execute_query(book_query, (book_title, author_name))
        person_id = self.execute_query(person_query, (person_fname, person_sname))

        if book_id and person_id:
            return_query = """DELETE FROM RentedBooks WHERE book_id = ? AND person_id = ?;"""
            self.execute_query(return_query, (book_id[0][0], person_id[0][0]))
            return True
        return False

    def is_book_rented(self, book_id):
        query = """SELECT COUNT(*) FROM RentedBooks WHERE book_id = ?;"""
        result = self.execute_query(query, (book_id,))
        return result[0][0] > 0

    def select_rented_books(self):
        query = """
        SELECT RentedBooks.rental_id, Books.book_title, Books.book_author, People.person_fname, People.person_sname
        FROM RentedBooks
        JOIN Books ON RentedBooks.book_id = Books.book_id
        JOIN People ON RentedBooks.person_id = People.person_id;
        """
        return self.execute_query(query)
