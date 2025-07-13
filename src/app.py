import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
#from database.databasemanager import DatabaseManager

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    #db = DatabaseManager()
    #db.create_tables()
    main_win = MainWindow()
    main_win.show()
    
    sys.exit(app.exec())