import socket 
import os
import datetime
import threading
import re
import time

server = socket.socket()
port = 6743
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('',port))
server.listen(5)

users = []
userRequests = {}

startTime = time.time()

refreshTime = 60
limit = 10

def Header(length,setCookie):
	if setCookie != 0:
		header = {
			'Date' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
			'Content-Length' : length,
			'Keep-Alive' : 'timeout=%d,max=%d' % (10,100),
			'Connection': 'Keep-Alive',
			'Content-Type': 'text/html',
			'Set-Cookie': setCookie
		}
	elif setCookie == 0:
		header = {
			'Date' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
			'Content-Length' : length,
			'Keep-Alive' : 'timeout=%d,max=%d' % (10,100),
			'Connection': 'Keep-Alive',
			'Content-Type': 'text/html'
		}		
	# print header
	return header

def createHeaders(length,setCookie):
	header = Header(length,setCookie)
	formattedHeader  = '\r\n'.join("%s:%s" % (field,header[field]) for field in header)
	successHeader = "HTTP/1.1 200 OK"
	jointHeader  = successHeader + '\r\n' + formattedHeader + '\r\n\r\n'
	return jointHeader

def checkCookie(cookie,addr):
	print users
	for i in users:
		print i['addr'],addr[0]
		if i['addr'] == addr[0]:
			print "True"
			return True
	return False 

def createCookie():
	pass

def sendFile(conn,fileName,cookie):
	try:
		file = open(fileName)
		fileData = file.read()
		conn.send(createHeaders(len(fileData),cookie))
		for i in range(0,len(fileData)):
			conn.send(fileData[i])
	except:
		conn.send('HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!doctype html><html><body><h1>File Not Found!<h1></body></html>')					

def sendAuthFile(conn):
	authFile = open('auth.html')
	authFileData = authFile.read()
	conn.send(createHeaders(len(authFileData),0))	
	for i in range(0,len(authFileData)):
		conn.send(authFileData[i])

def handleGET(conn,received,addr):
	fileName = received.split()[1][1:]
	# print fileName
	email, password = extractDetails(fileName)
	# print email,password
	if email != False:
		fileName = re.search('^(.*)\?',fileName)
		fileName = fileName.group(1)
		cookie = 'cookie'
		temp = {'email':email, 'password':password, 'addr':addr[0], 'cookie':cookie}
		users.append(temp)
		# print users
		sendFile(conn,fileName,cookie)
		return
	try:
		searchResults = re.search('Cookie.*\S',received)
		searchResults = searchResults.group()
		cookieValue = searchResults.split(':')[0].split()[0]
		print cookieValue
		if checkCookie(cookieValue,addr):	
			print "lolol"
			sendFile(conn,fileName,0)	
		else:
			conn.send('HTTP/1.1 401 Unauthorized\r\n\r\n')
	except:
		print users
		for i in users:
			if i['addr'] == addr[0]:
				conn.send('HTTP/1.1 401 Unauthorized\r\nContent-Type: text/html\r\n\r\n<!doctype html><html><body><h1>User Not Authorized!<h1></body></html>')
				return				
		sendAuthFile(conn)


def extractDetails(postParams):
	try:
		p = re.compile('Email=(.*)&p')
		p = p.search(postParams)
		email = p.group(1)

		s = re.compile('pass=(.*)&')
		s = s.search(postParams)
		password = s.group(1)

		return (email,password)

	except:
		return (False,False)

def handlePOST(conn,received,addr):

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
				# print "get"
				handleGET(conn,received,addr)
			elif method == "POST":
				conn.send('HTTP/1.1 200 OK\r\n\r\n')
				# handlePOST(conn,received,addr)
			conn.close()
			break

while 1:
	conn, addr = server.accept()
	# if userRequests[addr[0]] == 0:
	try:
		userRequests[addr[0]]+=1
		print userRequests[addr[0]]
	except:
		userRequests[addr[0]] = 0
	# print conn,addr
	currentTime = time.time()
	if currentTime - startTime > refreshTime:
		for i in userRequests:
			userRequests[i] = 0
	if userRequests[addr[0]] > limit:
		print "Limit Reached"
		conn.close()
		continue

	clientThread = CreateThread(conn,addr)
	clientThread.start()
	# clientThread.setDaemon(True)

#	threads.append(clientThread)
server.close()