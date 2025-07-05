import socket
import threading
from models.user import User
from models.message import Message
from models.contact import Contact
from repositories.UserRepository import UserRepository
from repositories.messagerepository import MessageRepository
from datetime import datetime, timezone
from functions.singleton import singleton


@singleton
class SocketManager:
    def __init__(self, host= '127.0.0.1', port=443):
        self.socket = None
        self.host = host
        self.port = port
        self.running = False

    def connect(self, user: User):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            response = self.socket.recv(1024).decode().strip()
            if response == 'USER_NAME_REQUEST':
                self.socket.send(user.user_name.encode())
            else:
                print(f'Unexpected server response: {response}')
                self.socket.close()
                self.running = False
                return False
            self.running = True
            print(f'Connected as {user.user_name}')
            return True
        except Exception as e:
            print(f'Error happened during connect: {e}')
            if self.socket:
                try:
                    self.socket.close()
                except Exception:
                    pass
            self.running = False
            return False

    def receive_message(self):
        if not self.running:
            print("Not connected to server.")
            return None
        try:
            data = self.socket.recv(1024)
            if not data:
                print('Connection closed by server.')
                self.running = False
                return None
            mesg = Message.deserialize(data.decode())
            return mesg if mesg else data.decode()
        except Exception as e:
            print(f'Connection Lost')
            self.running = False
            try:
                self.socket.close()
            except Exception:
                pass
            return None

    def send(self, content: str, sender: User, receiver: User):
        if not self.running:
            print("Not connected to server.")
            return False
        time = datetime.now(timezone.utc)
        mesg = Message(content=content, sender_id=sender.id, receiver_id=receiver.id, timestamp=time)
        try:
            self.socket.send(mesg.serialize().encode())
            return True
        except Exception as e:
            print(f'Error sending message: {e}')
            self.running = False
            try:
                self.socket.close()
            except Exception:
                pass
            return False

    def close(self):
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass




