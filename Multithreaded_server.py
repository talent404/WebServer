import socket 
import os
import datetime
import threading

server = socket.socket()
port = 6743
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('',port))
server.listen(5)

users = {}

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

def handleGET(conn,received):
	fileName = received.split()[1][1:]
	try:
		file = open(fileName)
		fileData = file.read()
		conn.send(createHeaders(len(fileData)))
		for i in range(0,len(fileData)):
			conn.send(fileData[i])
	except:
		conn.send('HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!doctype html><html><body><h1>File Not Found!<h1></body></html>')					

def handlePOST(conn,received):
	print "POST"
	pass

class CreateThread(threading.Thread):
	def __init__(self,conn,addr):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr

	def run(self):
		while 1:
			received = conn.recv(2048)
			print received
			method = received.split()[0]
			if method == "GET":
				print "get"
				handleGET(conn,received)
			elif method == "POST":
				handlePOST(conn,received)
			conn.close()
			break

while 1:
	conn, addr = server.accept()
	print "conn enter"
	clientThread = CreateThread(conn,addr)
	clientThread.start()
	# clientThread.setDaemon(True)

#	threads.append(clientThread)
server.close()