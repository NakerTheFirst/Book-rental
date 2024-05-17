import sqlite3


class BookRental:
    def __init__(self):
        self.conn = sqlite3.connect('rental.db')
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.fetchall()

    # Functions needed in the long run
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


def main():

    drop_books_query = """DROP TABLE IF EXISTS Books;"""
    drop_people_query = """DROP TABLE IF EXISTS People;"""
    drop_rented_books_query = """DROP TABLE IF EXISTS RentedBooks;"""

    create_books_query = """
        CREATE TABLE IF NOT EXISTS Books(
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_title TEXT NOT NULL,
            book_author TEXT NOT NULL,
            book_genre TEXT NOT NULL);
    """

    create_people_query = """
        CREATE TABLE IF NOT EXISTS People(
            person_id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_fname TEXT NOT NULL,
            person_sname TEXT NOT NULL);
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
            FOREIGN KEY (person_id) REFERENCES People (person_id));
        """

    select_books_query = """SELECT * FROM Books;"""
    select_people_query = """SELECT * FROM People;"""

    # Initialise the database
    br = BookRental()

    # Drop tables
    br.execute_query(drop_books_query)
    br.execute_query(drop_people_query)
    br.execute_query(drop_rented_books_query)

    # Create tables
    br.execute_query(create_books_query)
    br.execute_query(create_people_query)
    br.execute_query(create_rented_books_query)

    # Add records
    br.add_book("George Orwell", "1984", "Dystopian")
    br.add_person("Kamil", "Nowak")

    print(br.execute_query(select_books_query))
    print(br.execute_query(select_people_query))
    br.delete_book(1)
    br.delete_person(1)
    print(br.execute_query(select_books_query))
    print(br.execute_query(select_people_query))

    # Close the database connection
    br.conn.close()

    return 0


if __name__ == '__main__':
    main()
