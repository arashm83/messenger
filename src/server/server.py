import socket
import threading
from models.user import User
from models.message import Message
from models.contact import Contact
from repositories.UserRepository import UserRepository
from repositories.messagerepository import MessageRepository

HOST = '0.0.0.0'
PORT = 443

class Server:

    def __init__(self, host = HOST, port = PORT):
        
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.Lock()
        self.running = False
        self.user_repo = UserRepository()
        self.message_repo = MessageRepository()
        self.clients: dict[str, socket.socket] = {}

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.running = True
        print(f'server listening on {self.host}:{self.port}')
        
        accept_thread = threading.Thread(target=self.accept_connection)
        accept_thread.daemon = True
        accept_thread.start()

        self.handle_server_commands()

    def accept_connection(self):
        while self.running:
            try:
                client_sock, client_addr = self.socket.accept()
                client_sock.send('USER_NAME_REQUEST'.encode("utf-8"))
                client_sock.settimeout(10)
                user_name = client_sock.recv(1024).decode().strip() 
                if not user_name:
                    raise ValueError('empty username')
                client_sock.settimeout(None)
                print('connection accepted')

                user = self.user_repo.get_user(user_name)
                if not user:
                    print(f'User not found: {user_name}')
                    client_sock.close()
                    continue

                with self.lock:
                    self.clients[user.user_name] = client_sock
                    print('user accepted')

                client_handle = threading.Thread(target=self.handle_client, args=(client_sock, user))
                client_handle.daemon = True
                client_handle.start()

            except Exception as e:
                print(f'An error occurred in accept_connection: {e}')
                try:
                    client_sock.close()
                except Exception:
                    pass
                continue
            except OSError:
                break

    def handle_client(self, conn: socket.socket, user: User):
        user_name = user.user_name
        try:
            while self.running:
                try:
                    mesg = conn.recv(1024).decode()
                    if not mesg:
                        print(f'Connection closed by {user_name}')
                        raise ConnectionResetError
                        
                    
                    formated_mesg = Message.deserialize(mesg)
                    self.send(formated_mesg)
                    self.message_repo.save_message(formated_mesg)
                except Exception as e:
                    print(f'Error handling message from {user_name}: {e}')
                    break
                except (ConnectionResetError, ConnectionAbortedError):
                    self.delete_client(user_name)
        except Exception as e:
            print(f'Unexpected error in handle_client for {user_name}: {e}')
        finally:
            self.delete_client(user_name)

    def send(self, mesg: Message):
        receiver_user = self.user_repo.get_user_by_id(mesg.receiver_id)
        if not receiver_user:
            print(f'Receiver user with id {mesg.receiver_id} not found.')
            return
        receiver_name = receiver_user.user_name
        with self.lock:
            client_sock = self.clients.get(receiver_name)
            if client_sock:
                try:
                    client_sock.send(mesg.serialize().encode())
                except Exception as e:
                    print(f'Error sending message to {receiver_name}: {e}')
                    try:
                        client_sock.close()
                    except Exception:
                        pass
                    del self.clients[receiver_name]
            else:
                print(f'Client socket for {receiver_name} not found.')

    def delete_client(self, user_name):
        with self.lock:
            if user_name in self.clients.keys():
                try:
                    self.clients[user_name].close()
                    del self.clients[user_name]
                    print(f'client {user_name} disconnected')
                except:
                    pass
                    

    def handle_server_commands(self):
        while True:
            com = input()
            if com == 'SHUTDOWN':
                for client_socket in self.clients.values():
                    try:
                        client_socket.send("shutting down the server")
                        client_socket.close()
                    except:
                        pass

if __name__== '__main__':
    server = Server()
    server.start()
    
