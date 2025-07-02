# src/gui/chat_window.py

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QListWidget, 
                             QTextEdit, QLineEdit, QPushButton, QLabel, QListWidgetItem, QFrame)
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt, QSize

from .settings_window import SettingsWindow
from .add_contact_dialog import AddContactDialog
from .profile_window import ProfileWindow

class ChatWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.current_user = username
        self.current_user_data = {}
        self.current_chat_partner = None
        self._setup_ui()
        self._load_initial_data()

    def _create_circular_icon(self, image_path, size=48):
        source_pixmap = QPixmap(image_path)
        if source_pixmap.isNull():
            source_pixmap = QPixmap("assets/default_profile.png")

        scaled_pixmap = source_pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        
        circular_pixmap = QPixmap(size, size)
        circular_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()
        
        return QIcon(circular_pixmap)

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        left_panel = QWidget()
        left_panel.setFixedWidth(300)
        left_panel.setStyleSheet("background-color: #2c3e50;")
        left_panel_layout = QVBoxLayout(left_panel)
        left_panel_layout.setContentsMargins(0,0,0,0)
        left_panel_layout.setSpacing(0)

        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: #34495e;")
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0,0,0,0)
        top_bar_layout.setSpacing(0)
        
        self.profile_button = QPushButton("")
        self.settings_button = QPushButton(QIcon("assets/settings_icon.png"), "")
        self.add_contact_button = QPushButton(QIcon("assets/add_contact_icon.png"), "")
        
        buttons = [self.profile_button, self.settings_button, self.add_contact_button]

        for button in buttons:
            button.setIconSize(QSize(48, 48)) 
            button.setStyleSheet("border: none; background-color: transparent;")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            top_bar_layout.addWidget(button, 1)
        
        self.profile_button.clicked.connect(self.open_profile_window)
        self.settings_button.clicked.connect(self.open_settings)
        self.add_contact_button.clicked.connect(self.open_add_contact)

        self.contacts_list = QListWidget()
        self.contacts_list.setStyleSheet("""
            QListWidget { border: none; background-color: #2c3e50; color: white; }
            QListWidget::item { padding: 10px; }
            QListWidget::item:selected { background-color: #1abc9c; }
        """)
        self.contacts_list.currentItemChanged.connect(self.contact_selected)

        left_panel_layout.addWidget(top_bar)
        left_panel_layout.addWidget(self.contacts_list)

        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: #ecf0f1;")
        right_panel_layout = QVBoxLayout(right_panel)
        right_panel_layout.setContentsMargins(0,0,0,0)
        right_panel_layout.setSpacing(0)
        
        chat_header = QWidget()
        chat_header.setStyleSheet("background-color: #bdc3c7; padding: 10px;")
        chat_header_layout = QHBoxLayout(chat_header)
        self.chat_partner_label = QLabel("Select a contact to start chatting")
        self.chat_partner_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        chat_header_layout.addWidget(self.chat_partner_label)
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Arial", 11))
        
        message_input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.setFixedHeight(40)
        self.send_button = QPushButton("Send")
        self.send_button.setFixedHeight(40)
        
        message_input_layout.addWidget(self.message_input)
        message_input_layout.addWidget(self.send_button)
        
        right_panel_layout.addWidget(chat_header)
        right_panel_layout.addWidget(self.chat_display, 1)
        right_panel_layout.addLayout(message_input_layout)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)

    def _load_initial_data(self):
        self.current_user_data = {
            "username": self.current_user,
            "phone": "09123456789",
            "picture": "assets/default_profile.png"
        }
        
        profile_icon = self._create_circular_icon(self.current_user_data["picture"])
        self.profile_button.setIcon(profile_icon)
        
        self.refresh_contact_list()

    def contact_selected(self, current_item, previous_item):
        if not current_item:
            return

        self.current_chat_partner = current_item.text()
        self.chat_partner_label.setText(f"Chat with {self.current_chat_partner}")
        self.chat_display.clear()
        self.chat_display.append(f"--- Chat history with {self.current_chat_partner} ---")
        
    def open_profile_window(self):
        dialog = ProfileWindow(self.current_user_data, self)
        dialog.exec()

    def open_settings(self):
        dialog = SettingsWindow(self.current_user_data, self)
        dialog.profile_updated.connect(self.refresh_user_data)
        dialog.exec()

    def open_add_contact(self):
        dialog = AddContactDialog(self)
        dialog.contact_added.connect(self.refresh_contact_list)
        dialog.exec()
        
    def refresh_user_data(self):
        self._load_initial_data()
        
    def refresh_contact_list(self):
        self.contacts_list.clear()
        contacts = ["Parsa", "Arian", "Arman"] 
        for contact in contacts:
            item = QListWidgetItem(contact)
            item.setIcon(QIcon("assets/default_profile.png"))
            item.setSizeHint(QSize(item.sizeHint().width(), 60))
            self.contacts_list.addItem(item)