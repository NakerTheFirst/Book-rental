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
                author TEXT NOT NULL,
                rentee_fname TEXT NOT NULL,
                rentee_sname TEXT NOT NULL,
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
        query = """
        DELETE FROM Books WHERE book_id = ?;
        """
        self.execute_query(query, (book_id,))

    def delete_person(self, person_id):
        query = """
        DELETE FROM People WHERE person_id = ?;
        """
        self.execute_query(query, (person_id,))

    def select_books(self):
        query = """SELECT * FROM Books;"""
        return self.execute_query(query)

    def select_people(self):
        query = """SELECT * FROM People;"""
        return self.execute_query(query)


def main():

    # Initialise the database
    br = DatabaseManager()

    # Drop tables
    br.drop_tables()

    # Create tables
    br.create_tables()

    # Add records
    br.add_book("1984", "George Orwell", "Dystopian")
    br.add_person("Kamil", "Nowak")

    # Test if stuff works
    print(br.select_books())
    print(br.select_people())
    br.delete_book(1)
    br.delete_person(1)
    print(br.select_books())
    print(br.select_people())

    # Close the database & cursor connection
    br.close_connection()
    return 0


if __name__ == '__main__':
    main()
