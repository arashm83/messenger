# src/gui/settings_window.py

import os
from PyQt6.QtCore import pyqtSignal, Qt, QFile
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QMessageBox, QFileDialog, QFrame)

class SettingsWindow(QDialog):
    profile_updated = pyqtSignal()

    def __init__(self, current_user_data, parent=None):
        super().__init__(parent)
        self.current_user_data = current_user_data
        self.new_profile_pic_path = None
        
        self.setWindowTitle("Settings")
        self.setFixedSize(500, 600)
        self._setup_ui()
        self._load_user_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)
        
        self.profile_pic_label = QLabel()
        self.profile_pic_label.setFixedSize(128, 128)
        self.profile_pic_label.setStyleSheet("border: 1px solid #ccc; border-radius: 64px;")
        
        change_pic_button = QPushButton("Change Profile Picture")
        change_pic_button.clicked.connect(self.choose_image)
        
        layout.addWidget(self.profile_pic_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(change_pic_button)
        layout.addWidget(QFrame(frameShape=QFrame.Shape.HLine))

        self.username_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.new_password_input = QLineEdit()
        self.confirm_password_input = QLineEdit()

        for field in [self.username_input, self.phone_input, self.new_password_input, self.confirm_password_input]:
            field.setFixedHeight(40)

        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Phone Number:"))
        layout.addWidget(self.phone_input)
        layout.addWidget(QLabel("New Password (leave blank to keep current):"))
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_password_input)
        
        layout.addStretch()

        self.save_button = QPushButton("Save Changes")
        self.save_button.setFixedHeight(40)
        self.save_button.clicked.connect(self.handle_save_changes)
        layout.addWidget(self.save_button)

    def _load_user_data(self):
        self.username_input.setText(self.current_user_data.get("username", ""))
        self.phone_input.setText(self.current_user_data.get("phone", ""))
        
        profile_pic_path = self.current_user_data.get("picture", "assets/default_profile.png")
        if os.path.exists(profile_pic_path):
            pixmap = QPixmap(profile_pic_path)
            self.profile_pic_label.setPixmap(pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def choose_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.new_profile_pic_path = file_path
            pixmap = QPixmap(file_path)
            self.profile_pic_label.setPixmap(pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def handle_save_changes(self):
        new_username = self.username_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if new_password != confirm_password:
            QMessageBox.warning(self, "Password Error", "New passwords do not match.")
            return

        # TODO: Connect to UserService to save profile changes.
        success, message = True, "Profile updated successfully!"

        if success:
            if self.new_profile_pic_path:
                try:
                    dest_folder = "assets/profiles"
                    os.makedirs(dest_folder, exist_ok=True)
                    _, ext = os.path.splitext(self.new_profile_pic_path)
                    dest_path = os.path.join(dest_folder, f"{new_username}{ext}")
                    
                    source_file = QFile(self.new_profile_pic_path)
                    if not source_file.copy(dest_path):
                        # If copying fails, show the file error.
                        raise IOError(source_file.errorString())

                    # TODO: The new picture path (dest_path) must be saved in the database.
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Could not save new profile picture:\n{e}")
                    return

            QMessageBox.information(self, "Success", message)
            self.profile_updated.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "Error", message)