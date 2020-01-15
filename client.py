#!usr/bin/bash

import socket
import signal # interrupt signal for timeout

ADDR, PORT = "127.0.0.1", 4444 # loopback address, arbitrary port number
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 address family, TCP socket
sock.connect((ADDR, PORT)) 
SIZE = 4096
signal.signal(signal.SIGALRM, lambda: 0) # handler is an empty lambda function
print("USAGE: enter HTTP URL like http://www.weevil.info \nor http://info.cern.ch/hypertext/WWW/TheProject.html \nThe 'http://' and 'www.' parts can be omitted \nType 'quit' to exit \n")
while True:
	message, reply, hostname, request, path, pathIndex = "", "", "", "", "", -1
	signal.alarm(30) # send interrupt signal in 30 seconds
	try:
		message = input("Enter URL: ")
	except:
		print("\nUser took too long. Connection timed out\n")
		message = "quit"
	signal.alarm(0)
	if message == "":
		continue
	if message[0:7] == "http://":
		message = message[7:]
	if message[0:4] == "www.":
		message = message[4:]
	pathIndex = message.find('/')
	if pathIndex != -1:
		hostname = message[0:pathIndex]
		path = message[pathIndex:]
	else: 
		hostname = message
		path = '/'
	request = "GET http://" + hostname + path + " HTTP/1.0\r\nhostname:" + hostname + "\r\n\r\n"
	sock.send(request.encode("utf-8"))
	if hostname == "quit":
		break
	reply = sock.recv(SIZE)
	print("SERVER: " + reply.decode() + '\n')

sock.close() 
