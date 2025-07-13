# src/gui/chat_window.py

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QListWidget, 
                             QTextEdit, QLineEdit, QPushButton, QLabel, QListWidgetItem, QFrame)
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt, QSize

from .settings_window import SettingsWindow
from .add_contact_dialog import AddContactDialog
from .profile_window import ProfileWindow
from services.UserService import UserService
from services.socketmanager import SocketManager
from repositories.messagerepository import MessageRepository
from models.message import Message
from threading import Thread
from datetime import datetime, timezone

class ChatWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.user_service = UserService()
        self.socket_manager = SocketManager()
        self.message_repository = MessageRepository()
        self.current_user = self.user_service.find_user(username)
        self.current_chat_partner = None
        self._setup_ui()
        self._load_initial_data()
        self.socket_manager.connect(self.current_user)

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
        #left_panel.setStyleSheet("background-color: #2c3e50;")
        left_panel_layout = QVBoxLayout(left_panel)
        left_panel_layout.setContentsMargins(0,0,0,0)
        left_panel_layout.setSpacing(0)

        top_bar = QWidget()
        #top_bar.setStyleSheet("background-color: #34495e;")
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0,0,0,0)
        top_bar_layout.setSpacing(0)
        
        self.profile_button = QPushButton("")
        self.settings_button = QPushButton(QIcon("assets/settings_icon.png"), "")
        self.add_contact_button = QPushButton(QIcon("assets/add_contact_icon.png"), "")
        
        buttons = [self.profile_button, self.settings_button, self.add_contact_button]

        for button in buttons:
            button.setIconSize(QSize(48, 48)) 
            #button.setStyleSheet("border: none; background-color: transparent;")
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
        #right_panel.setStyleSheet("background-color: #ecf0f1;")
        right_panel_layout = QVBoxLayout(right_panel)
        right_panel_layout.setContentsMargins(0,0,0,0)
        right_panel_layout.setSpacing(0)
        
        chat_header = QWidget()
        #chat_header.setStyleSheet("background-color: #bdc3c7; padding: 10px;")
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

        self.message_input.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.message_input.setFixedHeight(40)
        self.send_button = QPushButton("Send")
        self.send_button.setFixedHeight(40)
        self.message_input.returnPressed.connect(self.send_button.click) 
        self.send_button.clicked.connect(self.send_message)

        message_input_layout.addWidget(self.message_input)
        message_input_layout.addWidget(self.send_button)
        
        right_panel_layout.addWidget(chat_header)
        right_panel_layout.addWidget(self.chat_display, 1)
        right_panel_layout.addLayout(message_input_layout)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)

    def _load_initial_data(self):
        profile_icon = self._create_circular_icon(self.current_user.profile_pic)
        self.profile_button.setIcon(profile_icon)
        
        self.refresh_contact_list()

    def contact_selected(self, current_item):
        if not current_item:
            return

        self.current_chat_partner = self.user_service.find_user(current_item.text())
        self.chat_partner_label.setText(f"Chat with {self.current_chat_partner.user_name}")
        self.chat_display.clear()
        self.load_messages()
        receive_thread = Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()

    def receive_messages(self):
        while self.socket_manager.running:
            message = self.socket_manager.receive_message()
            if message and self.current_chat_partner.id == message.sender_id:
                self.show_message(message)

    def open_profile_window(self):
        dialog = ProfileWindow(self.current_user, self)
        dialog.exec()

    def open_settings(self):
        dialog = SettingsWindow(self.current_user, self)
        dialog.profile_updated.connect(self.refresh_user_data)
        dialog.exec()

    def open_add_contact(self):
        dialog = AddContactDialog(self, self.current_user)
        dialog.contact_added.connect(self.refresh_contact_list)
        dialog.exec()
        
    def refresh_user_data(self):
        self._load_initial_data()
        
    def refresh_contact_list(self):
        self.contacts_list.clear()
        contacts = self.user_service.get_contact(self.current_user)
        for contact in contacts:
            item = QListWidgetItem(contact.user_name)
            item.setIcon(QIcon(contact.profile_pic or 'assets/default_profile.png'))
            item.setSizeHint(QSize(item.sizeHint().width(), 60))
            self.contacts_list.addItem(item)

    def show_message(self, message: Message):
        sender = self.user_service.find_user_by_id(message.sender_id)
        time = f'{message.timestamp.hour}:{message.timestamp.minute}'
        sender_name = 'You' if sender.id == self.current_user.id else sender.user_name
        if sender:
            msg_text = f'{time} - {sender_name}: {message.content}'
            if sender.id == self.current_user.id:
                self.chat_display.append(f'<span style="color: #1abc9c;">{msg_text}</span>')
            else:
                self.chat_display.append(msg_text)

    def send_message(self):
        message = self.message_input.text()
        if message and self.current_chat_partner:
            self.socket_manager.send(message, self.current_user, self.current_chat_partner)
            self.show_message(Message(content=message, sender_id=self.current_user.id, receiver_id=self.current_chat_partner.id, timestamp=datetime.now(timezone.utc)))
            self.message_input.clear()

    def load_messages(self):
        if self.current_chat_partner:
            messages = self.message_repository.get_messages(self.current_user.id, self.current_chat_partner.id)
            for message in messages:
                self.show_message(message)