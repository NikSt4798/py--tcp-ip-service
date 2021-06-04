import socket
import json
from threading import Thread
import time

USERS : dict = {}

COMMANDS = """
help или ? - получить список доступных комманд
q или Q - выход
users - получить список подключенных пользователей
address [имя пользователя] - получть адрес пользователя
connect [имя пользователя] - установить соединение с пользователем
"""

client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def command(command : str):
    if (command == "help" or command == "?"):
        help()
    if (command == "users"):
        get_users()
    if (command.find("address") != -1):
        if(len(command.split()) < 2 ):
            print("Укажите имя")
            return
        get_address(command.split()[1])
    if (command.find("connect") != -1):
        if(len(command.split()) < 2 ):
            print("Укажите имя")
            return
        connect(command.split()[1])

def help():
    print(COMMANDS)

def register(name):
    address = ("localhost", 5000)
    client_socket.sendto(f'add {name}'.encode(), address)
    newdata=client_socket.recvfrom(512)
    if(newdata[0].decode() == "success"):
        print("Регистрация прошла успешно")
    else:
        print("Ошибка сервера")

def get_users():
    client_socket.sendto('users'.encode(),("localhost", 5000))
    result = client_socket.recvfrom(512)
    jsonString = result[0].decode()
    users = json.loads(jsonString)
    USERS.update(users)
    for user in USERS.keys():
        print(user)

def get_address(name):
    if (name in USERS):
        print(USERS[name])
    else:
        print("Такого пользователя не существует")

def connect(name):
    client_socket.sendto(f'connect {name}'.encode(),("localhost", 5000))
    address = client_socket.recvfrom(512)[0].decode()
    if(not name in USERS):
        print("Такого пользователя не существует")
        return

    host = USERS[name][0]
    port = USERS[name][1]
    Thread(target=listen, kwargs={'address': (host, int(address)), "name": name}).start()

    sock = socket.socket()    
    while True:    
        try:    
            sock.connect((host, port))
            break
        except Exception:
            print(f"Waiting for {name} to connect")
            time.sleep(1)

    sock.send('Соединение установлено, отправьте q, чтобы завершить соединение'.encode())

    while True:
        message = input()
        if(message == "q"):
            break
        sock.send(message.encode())

    sock.close()

def listen(address, name):
    sock = socket.socket()
    sock.bind(address)
    sock.listen(2)
    conn, addr = sock.accept()

    print('connected:', addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(name, ": ", data.decode())

    conn.close()

def logout():
    client_socket.sendto('logout'.encode(),("localhost", 5000))

name = input("Как вас зовут?: ")
register(name)
while True:
    data=input("Введите команду (введите help, чтобы получть список доступных команд): ")
    if data=='q' or data=='Q':
        logout()
        break
    else:
        command(data)	