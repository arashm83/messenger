# src/gui/add_contact_dialog.py

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, 
                             QLabel, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal

class AddContactDialog(QDialog):
    contact_added = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
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

        # TODO: Connect to a service to find and add the contact
        # success, message = contact_service.add_contact(current_user, username, phone)
        success, message = True, f"User {username} added to contacts!" # Placeholder for testing
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.contact_added.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "Error", message)