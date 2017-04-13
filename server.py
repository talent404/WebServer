import socket 
import os
import datetime
import re

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
	received = conn.recv(4096)
	fileName = received.split()[1][1:]
	method = received.split()[0]
	if method == 'GET':
		try:
			file = open(fileName)
			fileData = file.read()
			conn.send(createHeaders(len(fileData)))
			for i in range(0,len(fileData)):
				conn.send(fileData[i])
		except:
			conn.send('HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!doctype html><html><body><h1>File Not Found!<h1></body></html>')		
	elif method == 'PUT':
		print 'put'
	
		# print received
		# p = received.split('\n\n')[1:]
		# print received
		# data = p.group(1)
		# print data
	   	p = re.search('PUT.*\n\n([.\S\s]*)',received)
		data = p.group(1)
		print data
		f = open(fileName+'PUT','w+')
		f.write(data)
		f.close()
		# except:
			# pass		
	conn.close()

server.close()