import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QMessageBox
)


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
        book_id = self.execute_query(book_query, (book_title, author_name))
        person_id = self.execute_query(person_query, (person_fname, person_sname))

        if book_id and person_id:
            borrow_query = """
            INSERT INTO RentedBooks (book_id, person_id)
            VALUES (?, ?);
            """
            self.execute_query(borrow_query, (book_id[0][0], person_id[0][0]))
            return True
        return False

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

    def select_rented_books(self):
        query = """
        SELECT RentedBooks.rental_id, Books.book_title, Books.book_author, People.person_fname, People.person_sname
        FROM RentedBooks
        JOIN Books ON RentedBooks.book_id = Books.book_id
        JOIN People ON RentedBooks.person_id = People.person_id;
        """
        return self.execute_query(query)


class BookRentalApp(QWidget):
    def __init__(self):
        super().__init__()
        self.books_text = None
        self.book_title_input = None
        self.book_author_input = None
        self.book_genre_input = None
        self.people_text = None
        self.person_fname_input = None
        self.person_sname_input = None
        self.rented_books_text = None
        self.rent_book_title_input = None
        self.rent_book_author_input = None
        self.rent_person_fname_input = None
        self.rent_person_sname_input = None
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Book Rental System')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Books Section
        books_layout = QVBoxLayout()
        books_label = QLabel('Books')
        self.books_text = QTextEdit()
        self.books_text.setReadOnly(True)
        books_layout.addWidget(books_label)
        books_layout.addWidget(self.books_text)

        self.book_title_input = QLineEdit(self)
        self.book_title_input.setPlaceholderText("Enter the title")
        self.book_author_input = QLineEdit(self)
        self.book_author_input.setPlaceholderText("Enter the author")
        self.book_genre_input = QLineEdit(self)
        self.book_genre_input.setPlaceholderText("Enter the genre")

        books_layout.addWidget(self.book_title_input)
        books_layout.addWidget(self.book_author_input)
        books_layout.addWidget(self.book_genre_input)

        add_book_button = QPushButton('Add Book')
        add_book_button.clicked.connect(self.add_book)
        delete_book_button = QPushButton('Delete Book')
        delete_book_button.clicked.connect(self.delete_book)

        books_layout.addWidget(add_book_button)
        books_layout.addWidget(delete_book_button)

        layout.addLayout(books_layout)

        # People Section
        people_layout = QVBoxLayout()
        people_label = QLabel('People')
        self.people_text = QTextEdit()
        self.people_text.setReadOnly(True)
        people_layout.addWidget(people_label)
        people_layout.addWidget(self.people_text)

        self.person_fname_input = QLineEdit(self)
        self.person_fname_input.setPlaceholderText("Enter first name")
        self.person_sname_input = QLineEdit(self)
        self.person_sname_input.setPlaceholderText("Enter surname")

        people_layout.addWidget(self.person_fname_input)
        people_layout.addWidget(self.person_sname_input)

        add_person_button = QPushButton('Add Person')
        add_person_button.clicked.connect(self.add_person)
        delete_person_button = QPushButton('Delete Person')
        delete_person_button.clicked.connect(self.delete_person)

        people_layout.addWidget(add_person_button)
        people_layout.addWidget(delete_person_button)

        layout.addLayout(people_layout)

        # Rented Books Section
        rented_books_layout = QVBoxLayout()
        rented_books_label = QLabel('Rented Books')
        self.rented_books_text = QTextEdit()
        self.rented_books_text.setReadOnly(True)
        rented_books_layout.addWidget(rented_books_label)
        rented_books_layout.addWidget(self.rented_books_text)

        layout.addLayout(rented_books_layout)

        # Actions Section
        actions_layout = QVBoxLayout()
        actions_label = QLabel('Actions')
        actions_layout.addWidget(actions_label)

        self.rent_book_title_input = QLineEdit(self)
        self.rent_book_title_input.setPlaceholderText("Enter book title")
        self.rent_book_author_input = QLineEdit(self)
        self.rent_book_author_input.setPlaceholderText("Enter book author")
        self.rent_person_fname_input = QLineEdit(self)
        self.rent_person_fname_input.setPlaceholderText("Enter renter's first name")
        self.rent_person_sname_input = QLineEdit(self)
        self.rent_person_sname_input.setPlaceholderText("Enter renter's surname")

        actions_layout.addWidget(self.rent_book_title_input)
        actions_layout.addWidget(self.rent_book_author_input)
        actions_layout.addWidget(self.rent_person_fname_input)
        actions_layout.addWidget(self.rent_person_sname_input)

        borrow_button = QPushButton('Borrow')
        borrow_button.clicked.connect(self.borrow_book)
        return_button = QPushButton('Return')
        return_button.clicked.connect(self.return_book)

        actions_layout.addWidget(borrow_button)
        actions_layout.addWidget(return_button)

        layout.addLayout(actions_layout)

        self.setLayout(layout)
        self.update_books()
        self.update_people()
        self.update_rented_books()

    def update_books(self):
        books = self.db_manager.select_books()
        self.books_text.clear()
        for book in books:
            self.books_text.append(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}")

    def update_people(self):
        people = self.db_manager.select_people()
        self.people_text.clear()
        for person in people:
            self.people_text.append(f"ID: {person[0]}, First Name: {person[1]}, Surname: {person[2]}")

    def update_rented_books(self):
        rented_books = self.db_manager.select_rented_books()
        self.rented_books_text.clear()
        for rented_book in rented_books:
            self.rented_books_text.append(f"Rental ID: {rented_book[0]}, Title: {rented_book[1]}, Author: {rented_book[2]}, "
                                          f"Renter: {rented_book[3]} {rented_book[4]}")

    def add_book(self):
        title = self.book_title_input.text()
        author = self.book_author_input.text()
        genre = self.book_genre_input.text()

        if title and author and genre:
            self.db_manager.add_book(title, author, genre)
            self.update_books()
        else:
            QMessageBox.warning(self, 'Input Error', 'All fields are required')

    def delete_book(self):
        title = self.book_title_input.text()

        if title:
            books = self.db_manager.select_books()
            for book in books:
                if book[1] == title:
                    self.db_manager.delete_book(book[0])
                    self.update_books()
                    return
            QMessageBox.warning(self, 'Not Found', 'Book not found')
        else:
            QMessageBox.warning(self, 'Input Error', 'Title is required to delete a book')

    def add_person(self):
        fname = self.person_fname_input.text()
        sname = self.person_sname_input.text()

        if fname and sname:
            self.db_manager.add_person(fname, sname)
            self.update_people()
        else:
            QMessageBox.warning(self, 'Input Error', 'Both fields are required')

    def delete_person(self):
        fname = self.person_fname_input.text()
        sname = self.person_sname_input.text()

        if fname and sname:
            people = self.db_manager.select_people()
            for person in people:
                if person[1] == fname and person[2] == sname:
                    self.db_manager.delete_person(person[0])
                    self.update_people()
                    return
            QMessageBox.warning(self, 'Not Found', 'Person not found')
        else:
            QMessageBox.warning(self, 'Input Error', 'Both fields are required to delete a person')

    def borrow_book(self):
        book_title = self.rent_book_title_input.text()
        author_name = self.rent_book_author_input.text()
        person_fname = self.rent_person_fname_input.text()
        person_sname = self.rent_person_sname_input.text()

        if book_title and author_name and person_fname and person_sname:
            success = self.db_manager.borrow_book(book_title, author_name, person_fname, person_sname)
            if success:
                self.update_rented_books()
            else:
                QMessageBox.warning(self, 'Not Found', 'Book or Person not found')
        else:
            QMessageBox.warning(self, 'Input Error', 'All fields are required')

    def return_book(self):
        book_title = self.rent_book_title_input.text()
        author_name = self.rent_book_author_input.text()
        person_fname = self.rent_person_fname_input.text()
        person_sname = self.rent_person_sname_input.text()

        if book_title and author_name and person_fname and person_sname:
            success = self.db_manager.return_book(book_title, author_name, person_fname, person_sname)
            if success:
                self.update_rented_books()
            else:
                QMessageBox.warning(self, 'Not Found', 'Rental record not found')
        else:
            QMessageBox.warning(self, 'Input Error', 'All fields are required')


def main():
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()

    db_manager.drop_tables()
    db_manager.create_tables()

    window = BookRentalApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
