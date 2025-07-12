from database.databasemanager import DatabaseManager
DatabaseManager().create_tables()
from services.UserService import UserService
from services.socketmanager import SocketManager
import threading

us = UserService()


name = 'arashm83'
password = 'Arash1383'
phone = '09123456789'

print(us.sign_up(name, password, phone))
print(us.sign_up('mamad', 'Mamamd1234', '09123456798'))
arash = us.find_user(name)
mamad = us.find_user('mamad')
print(us.update(arash, new_pic='assets/profiles/arashm83.png'))

def recive(sock: SocketManager):
    while sock.running:
        message = sock.receive_message()
        print(message)

    
if __name__== '__main__':
    sock_manager = SocketManager('127.0.0.1', 443)
    sock_manager.connect(mamad)
    print('you are mamad')
    receive_thread = threading.Thread(target=recive, args=(sock_manager,))
    receive_thread.daemon = True
    receive_thread.start()
    
    while sock_manager.running:
        content = input('> ')
        sock_manager.send(content, mamad, arash)

