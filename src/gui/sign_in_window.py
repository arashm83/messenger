from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                             QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from services.UserService import UserService

class SignInWindow(QWidget):
    
    login_successful = pyqtSignal(str)  
    go_to_signup = pyqtSignal()
    user_service = UserService()

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Messenger - Sign In")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(15)
        
        title_label = QLabel("Sign In")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)

        self.signin_button = QPushButton("Sign In")
        self.signin_button.setFixedHeight(40)
        self.signin_button.clicked.connect(self.handle_signin)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        
        self.goto_signup_button = QPushButton("Go to Sign Up")
        self.goto_signup_button.setFixedHeight(40)
        self.goto_signup_button.clicked.connect(self.go_to_signup.emit)

        main_layout.addWidget(title_label)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.password_input)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.signin_button)
        main_layout.addWidget(line)
        main_layout.addWidget(self.goto_signup_button)
        
    def handle_signin(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password cannot be empty.")
            return

        user = self.user_service.sign_in(username, password)

        if user:
            self.login_successful.emit(username)
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password.")