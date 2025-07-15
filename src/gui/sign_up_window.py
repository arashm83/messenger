# src/gui/sign_up_window.py

from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from services.UserService import UserService

class SignUpWindow(QWidget):
    signup_successful = pyqtSignal()
    go_to_signin = pyqtSignal()
    user_service = UserService()

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(15)

        title_label = QLabel("Sign Up")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number")
        self.phone_input.setFixedHeight(40)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setFixedHeight(40)

        self.signup_button = QPushButton("Sign Up")
        self.signup_button.setFixedHeight(40)
        self.signup_button.clicked.connect(self.handle_signup)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)

        self.goto_signin_button = QPushButton("Go to Sign In")
        self.goto_signin_button.setFixedHeight(40)
        self.goto_signin_button.clicked.connect(self.go_to_signin.emit)

        main_layout.addWidget(title_label)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.phone_input)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(self.confirm_password_input)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.signup_button)
        main_layout.addWidget(line)
        main_layout.addWidget(self.goto_signin_button)

    def handle_signup(self):
        username = self.username_input.text()
        phone = self.phone_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not all([username, phone, password, confirm_password]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Password Error", "Passwords do not match.")
            return
            
        
        success, message = self.user_service.sign_up(username, password, phone)

        if success:
            QMessageBox.information(self, "Success", message)
            self.signup_successful.emit()
        else:
            QMessageBox.critical(self, "Registration Failed", message)