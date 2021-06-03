import socket
import json
from threading import Thread
from typing import Tuple
import time

USERS : dict = {}

COMMANDS = """
help или ? - получить список доступных комманд
q или Q - выход
users - получить список подключенных пользователей
address [имя пользователя] - получть адрес пользователя
send [имя пользователя] [сообщение] - отправить сообщение пользователю
connect [имя пользователя] - установить соединение с пользователем
"""

client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def command(command : str):
    if (command == "help" or command == "?"):
        help()
    # if (command == "register"):
    #     name = input("Как вас зовут?: ")
    #     register(name)
    if (command == "users"):
        get_users()
    if (command.find("address") != -1):
        get_address(command.split()[1])
    if (command.find("connect") != -1):
        connect(command.split()[1])
    if (command.find("send") != -1):
        send_message(command.split()[1], command.split()[2])

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
    # Thread(target=listen, kwargs={'address': address}).start()

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

def send_message(name, message):
    if(name in USERS):
        client_socket.sendto(message.encode(),USERS[name])

def connect(name):
    client_socket.sendto(f'connect {name}'.encode(),("localhost", 5000))
    address = client_socket.recvfrom(512)[0].decode()
    host = USERS[name][0]
    port = USERS[name][1]
    Thread(target=listen, kwargs={'address': (host, int(address))}).start()
    sock = socket.socket()    
    sock.settimeout(1000000)
    time.sleep(10)
    sock.connect((host, port))
    sock.send('hello, world!'.encode())

    while True:
        message = input()
        if(message == "q"):
            break
        sock.send(message.encode())

    sock.close()

    print(data)

def listen(address: Tuple):
    sock = socket.socket()
    sock.bind(address)
    sock.listen(2)
    conn, addr = sock.accept()

    print('connected:', addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode())
        # conn.send(data.upper())

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