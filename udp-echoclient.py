#!/usr/bin/python
import socket
import commands

client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
name = input("Как вас зовут? ")
client_socket.sendto(name.encode("utf-8"),("localhost", 5000))
while True:
	command=input("Введите команду (введите help, чтобы получть список доступных команд): ")
	if command=='q' or command=='Q':
		client_socket.close()
		break
	else:
		commands.command(command)   
		# client_socket.sendto(data.encode("utf-8"),("localhost", 5000))
		# newdata=client_socket.recvfrom(512)
		# print ("Received:", newdata[0].decode("utf-8"))