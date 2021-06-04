import socket
import json

USERS = {}

def register(name, address):
    USERS[name] = address

def get_user(address):
    for user in USERS:
        if(USERS[user] == address):
            return user
    return 0
         
def get_address(name):
    if name in USERS:
        return USERS[name]

def logout(address):
    user = get_user(address)
    if(user != 0):
        USERS.pop(user)

server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.bind(('localhost',5000))
print ("UDP -Echo Server listening on port 5000:")
while True:
    data,address=server_socket.recvfrom(512)
    message = data.decode("utf-8")

    if(message.find("add") != -1):
        register(message.split()[1], address)
        server_socket.sendto("success".encode(),address)
        print("User registered: ", message.split()[1])

    if(message == "users"):        
        server_socket.sendto(json.dumps(USERS).encode(),address)
        print("User list sended on ", address)

    if(message.find("connect") != -1):
        name = message.split()[1]
        server_socket.sendto(str(address[1]).encode(), address)

    if(message == "logout"):
        logout(address)