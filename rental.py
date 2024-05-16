import sqlite3


class BookRental:
    def __init__(self):
        self.conn = sqlite3.connect('rental.db')
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()

    # Functions needed in the long run
    def add_book(self, title, author, category):
        pass

    def delete_book(self, book_id):
        pass


def main():

    create_books_query = (
        "CREATE TABLE IF NOT EXISTS Books("
        "book_id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "book_title TEXT NOT NULL,"
        "book_author TEXT NOT NULL,"
        "book_category TEXT NOT NULL);"
    )

    create_people_query = (
        "CREATE TABLE IF NOT EXISTS People("
        "person_id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "person_fname TEXT NOT NULL,"
        "person_sname TEXT NOT NULL);"
    )

    select_query = (
        "SELECT * FROM Books;"
    )

    # Initialise the database
    br = BookRental()

    # Create tables
    br.execute_query(create_books_query)
    br.execute_query(create_people_query)

    print(br.execute_query(select_query))

    # Close the database connection
    br.conn.close()

    return 0


if __name__ == '__main__':
    main()
