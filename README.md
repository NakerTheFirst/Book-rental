#  Book Rental System
A simple book rental system built with Python, SQLite, and PyQt6. The app allows users to manage books, people, and book rentals through a GUI.

<br>
<p align="center"><img width="802" src="https://github.com/NakerTheFirst/Book-rental/blob/main/gui_sreenshot.png" alt="Image of an interface of a the book rental app"></p>
<p align="center">Book Rental App's Graphical User Interface</p>

## Features
- **Books Management**:
  - Add new books with title, author, and genre.
  - Delete books by title.
  - View all books in the database.

- **People Management**:
  - Add new people with first name and surname.
  - Delete people by name.
  - View all people in the database.

- **Book Rentals**:
  - Borrow books by specifying the book title, author, and the renter's name.
  - Return books by specifying the book title, author, and the renter's name.
  - Prevent borrowing of already rented books.
  - View all currently rented books.

## Project Structure
```
├── rental.py               # Main entry point of the application
├── database_manager.py     # DatabaseManager class for database operations
├── gui.py                  # GUI class for the graphical user interface
├── requirements.txt        # Python dependencies
└── icon.png                # Icon for the application window
```

## Requirements
- Python 3.6+
- PyQt6

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/NakerTheFirst/Book-rental.git
    cd Book-rental
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```
3. Install the required dependencies:
    ```bash
   pip install -r requirements.txt
    ```

## Usage
1. Run the application:
    ```python rental.py```

2. Use the graphical interface to manage books, people, and rentals.
