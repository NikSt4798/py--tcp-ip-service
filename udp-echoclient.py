import socket
import json

USERS : dict = {}

COMMANDS = """
help или ? - получить список доступных комманд
q или Q - выход
users - получить список подключенных пользователей
address [имя пользователя] - получть адрес пользователя
send [имя пользователя] [сообщение] - отправить сообщение пользователю
"""

client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def command(command : str):
    if (command == "help" or command == "?"):
        help()
    if (command == "register"):
        name = input("Как вас зовут?: ")
        register(name)
    if (command == "users"):
        get_users()
    if (command.find("address") != -1):
        get_address(command.split()[1])
    if (command.find("send") != -1):
        send_message(command.split()[1], command.split()[2])

def help():
    print(COMMANDS)

def register(name):
    client_socket.sendto(f'add {name}'.encode(),("localhost", 5000))
    newdata=client_socket.recvfrom(512)
    if(newdata[0].decode() == "success"):
        print("Регистрация прошла успешно")
    else:
        print("Ошибка сервера")

def get_users():
	client_socket.sendto('users'.encode(),("localhost", 5000))	
	USERS.update(json.loads(client_socket.recvfrom(512)[0].decode()))
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

def logout():
    client_socket.sendto('logout'.encode(),("localhost", 5000))


while True:
	data=input("Введите команду (введите help, чтобы получть список доступных команд): ")
	if data=='q' or data=='Q':
		logout()
		break
	else:
		command(data)	