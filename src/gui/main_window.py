# src/main_window.py

from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon
from gui.sign_in_window import SignInWindow
from gui.sign_up_window import SignUpWindow
from gui.chat_window import ChatWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Messenger")
        self.setWindowIcon(QIcon("assets/logo_icon.png"))
        
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self._create_windows()
        self.show_signin()

    def _create_windows(self):
        self.signin_window = SignInWindow()
        self.signup_window = SignUpWindow()
        
        self.central_widget.addWidget(self.signin_window)
        self.central_widget.addWidget(self.signup_window)
        
        self.signin_window.go_to_signup.connect(self.show_signup)
        self.signin_window.login_successful.connect(self.show_chat)
        
        self.signup_window.go_to_signin.connect(self.show_signin)
        self.signup_window.signup_successful.connect(self.show_signin)

    def show_signin(self):
        self.setFixedSize(500, 600)
        self.central_widget.setCurrentWidget(self.signin_window)
        self.center()
        
    def show_signup(self):
        self.setFixedSize(500, 600)
        self.central_widget.setCurrentWidget(self.signup_window)
        self.center()
        
    def show_chat(self, username):
        self.chat_window = ChatWindow(username)
        self.central_widget.addWidget(self.chat_window)
        self.central_widget.setCurrentWidget(self.chat_window)
        self.setFixedSize(1000, 700)
        self.center()

    def center(self):
        screen_geometry = self.screen().geometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)