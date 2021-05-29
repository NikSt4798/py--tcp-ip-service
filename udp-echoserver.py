#!/usr/bin/python
#UDP echo Server
import socket
import database

server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.bind(('localhost',5000))
print ("UDP -Echo Server listening on port 5000:")
while True:
    data,address=server_socket.recvfrom(512)
    user = database.check_user(address)

    if(user != 0):
        print (user, ":said", data.decode("utf-8"))
        server_socket.sendto(data,address)
    else:
        database.register(data.decode("utf-8"), address)
        

    