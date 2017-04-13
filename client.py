import socket
import os
import sys

host = sys.argv[1]
port = sys.argv[2]
fileName = sys.argv[3]

def getMethod():
	client.send('GET /' + fileName + ' HTTP/1.1')
	print client.recv(4096)


def postMethod():
	f = open(fileName)
	fileData = f.read()
	client.send('POST ' + '\n\n' + fileData )
	pass

def putMethod():
	print "put"
	f = open(fileName)
	fileData = f.read()
	client.send('PUT ' + fileName + '\n\n' + fileData )
	pass

while 1:
	client = socket.socket()
	client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	client.connect((host,int(port)))
	method = raw_input('prompt>')
	if method == "GET":
		getMethod()
	elif method == "POST":
		postMethod()
	elif method == "PUT":
		putMethod()
	client.close()

