import socket
import json
import database as db

server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.bind(('localhost',5000))
print ("UDP -Echo Server listening on port 5000:")
while True:
    data,address=server_socket.recvfrom(512)
    message = data.decode("utf-8")

    if(message.find("add") != -1):
        db.register(message.split()[1], address)
        server_socket.sendto("success".encode(),address)
        print("User registered: ", message.split()[1])

    if(message == "users"):        
        server_socket.sendto(json.dumps(db.USERS).encode(),address)
        print("User list sended on ", address)

    if(message == "logout"):
        db.logout(address)