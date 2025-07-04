# src/gui/add_contact_dialog.py

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, 
                             QLabel, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal
from services.UserService import UserService

class AddContactDialog(QDialog):
    contact_added = pyqtSignal()
    user_service = UserService()

    def __init__(self, parent=None, current_user=None):
        super().__init__(parent)
        self.current_user = current_user
        self.setWindowTitle("Add Contact")
        self.setFixedSize(400, 250)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("Add New Contact")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
        layout.addWidget(self.username_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number")
        self.phone_input.setFixedHeight(40)
        layout.addWidget(self.phone_input)

        self.add_button = QPushButton("Add")
        self.add_button.setFixedHeight(40)
        self.add_button.clicked.connect(self.handle_add_contact)
        layout.addWidget(self.add_button)
        
    def handle_add_contact(self):
        username = self.username_input.text()
        phone = self.phone_input.text()

        if not username or not phone:
            QMessageBox.warning(self, "Input Error", "Username and Phone Number are required.")
            return

        contact = self.user_service.find_user(username)
        if not contact:
            QMessageBox.critical(self, "Error", 'User not found')
            return

        if contact.phone_number != phone:
            QMessageBox.critical(self, "Error", 'Phone number does not match user credentials')
            return
        success= self.user_service.add_contact(self.current_user, contact)

        if success:
            QMessageBox.information(self, "Success", 'Contact added successfully')
            self.contact_added.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "Error", 'Failed to add contact')