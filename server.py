#!usr/bin/bash

import socket

ADDR, PORT = "127.0.0.1", 4444 # loopback address, arbitrary port number
servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 address family, TCP socket
servSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # frees port immediately after termination
servSocket.bind((ADDR, PORT))
servSocket.listen(5) # accept up to 5 connections in queue
SIZE = 4096
while True:
	sock, address = servSocket.accept()
	message, hostname, hostAddr, reply = "", "", "", ""
	print("User has connected")
	while True:
		message = sock.recv(SIZE)
		print("CLIENT: " + message.decode())
		hostname = message.decode().split(':')[-1].strip() # extract hostname from GET request
		if hostname == "quit" or not hostname: # message received was empty
			sock.close()
			break
		try: # hostname could be invalid
			hostAddr = socket.gethostbyname(hostname)
			print("HOSTADDR: " + hostAddr)
			webSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			webSock.connect((hostAddr, 80)) # well-known port for HTTP
			webSock.send(message)
			reply = webSock.recv(SIZE) # get webpage
			webSock.close()
			reply = reply.decode().split("\r\n")[-1].encode() # save only the response's body
		except(socket.gaierror):
			reply = "Could not get IP of host".encode("utf-8")
		sock.send(reply)
	print("User has disconnected\n")
	
servSocket.close()

