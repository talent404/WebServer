import socket 
import os
import datetime
server = socket.socket()
port = 6743
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('',port))
server.listen(5)

def Header(length):
	header = {
		'Date' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
		'Content-Length' : length,
		'Keep-Alive' : 'timeout=%d,max=%d' % (10,100),
		'Connection': 'Keep-Alive',
		'Content-Type': 'text/html'
	}
	return header

def createHeaders(length):
	header = Header(length)
	formattedHeader  = '\r\n'.join("%s:%s" % (field,header[field]) for field in header)
	successHeader = "HTTP/1.1 200 OK"
	jointHeader  = successHeader + '\r\n' + formattedHeader + '\r\n\r\n'
	return jointHeader

while 1:
	conn, addr = server.accept()
	received = conn.recv(1024)
	fileName = received.split()[1][1:]
	try:
		file = open(fileName)
		fileData = file.read()
		conn.send(createHeaders(len(fileData)))
		for i in range(0,len(fileData)):
			conn.send(fileData[i])
	except:
		conn.send('HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!doctype html><html><body><h1>File Not Found!<h1></body></html>')		
	conn.close()

server.close()