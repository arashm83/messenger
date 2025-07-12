from database.databasemanager import DatabaseManager
DatabaseManager().create_tables()
from services.UserService import UserService
from services.socketmanager import SocketManager
import threading

us = UserService()


name = 'arashm83'
password = 'Arash1383'
phone = '09123456789'

#print(us.sign_up(name, password, phone))
#print(us.sign_up('mamad', 'Mamamd1234', '09123456798'))
arash = us.find_user(name)
mamad = us.find_user('mamad')

def recive(sock: SocketManager):
    while True:
        message = sock.receive_message()
        print(message.serialize())
if __name__== '__main__':
    sock_manager = SocketManager('127.0.0.1', 443)
    sock_manager.connect(arash)
    print('you are arash')
    recive_threaed = threading.Thread(target=recive, args=(sock_manager,))
    recive_threaed.daemon = True
    recive_threaed.start()
    while True:
        content = input('> ')
        sock_manager.send(content, arash, mamad)

