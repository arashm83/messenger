import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # TODO: Initialize services (UserService, etc.) and repositories here.
    # Pass them to the MainWindow if needed.
    
    main_win = MainWindow()
    main_win.show()
    
    sys.exit(app.exec())