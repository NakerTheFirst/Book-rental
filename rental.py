import sys
from PyQt6.QtWidgets import QApplication

from gui import GUI
from database_manager import DatabaseManager


def main():
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()

    db_manager.drop_tables()
    db_manager.create_tables()

    window = GUI()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
