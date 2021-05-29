import socket

COMMANDS = """
help или ? - получить список доступных комманд
q или Q - выход
"""

def command(command):
    if (command == "help" or command == "?"):
        help()

def help():
    print(COMMANDS)
