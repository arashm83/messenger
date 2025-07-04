# src/gui/profile_window.py

import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QWidget)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from models.user import User

class ProfileWindow(QDialog):
    def __init__(self, user: User, parent=None):
        super().__init__(parent)
        self.user = user

        self.setWindowTitle("User Profile")
        self.setFixedSize(350, 450)
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        # Profile Picture
        self.pic_label = QLabel()
        self.pic_label.setFixedSize(150, 150)
        self.pic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        profile_pic_path = self.user.profile_pic or 'assets/default_profile.png'
        if os.path.exists(profile_pic_path):
            pixmap = QPixmap(profile_pic_path)
            self.pic_label.setPixmap(
                pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            )

        # Username Label
        self.username_label = QLabel(f"Username: {self.user.user_name}")
        self.username_label.setFont(QFont("Arial", 12))
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Phone Number Label
        self.phone_label = QLabel(f"Phone: {self.user.phone_number}")
        self.phone_label.setFont(QFont("Arial", 12))
        self.phone_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Adding widgets to layout
        layout.addSpacing(20)
        layout.addWidget(self.pic_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.username_label)
        layout.addWidget(self.phone_label)
        layout.addStretch()

    def _apply_styles(self):
        # Apply styles similar to the PDF mockup
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
            }
            QLabel {
                color: white;
            }
        """)
        self.pic_label.setStyleSheet("border: 2px solid #1abc9c; border-radius: 75px;")