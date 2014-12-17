#!/usr/bin/env python
import gzip 
import socket, threading
import simplejson as json
import debug as dbug

SOCKET_TIMEOUT = 5
WELCOME_MESSAGE = "\nWelcome to the server \n\n"
BUFFER_SIZE = 4096
ENCODING = "utf-8"
HOST = "localhost"
PORT = 39998

class ClientThread(threading.Thread):
	
	def __init__(self,ip,port,socket,command_list, serv_reference):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.socket = socket
		self.callback = command_handler
		self.command_list = command_list
		self.connection_open = True
		self.serv_reference = serv_reference
		dbug.debug ("[+] New thread started for "+ip+":"+str(port))

	def run(self):  
		#print(self.socket.getpeername())
		dbug.debug ("Connection from : "+self.ip+":"+str(self.port))
		self.socket.send(WELCOME_MESSAGE.encode())                  
		data = "dummydata"	

		while (len(data) and self.connection_open is True):
			try:
				dbug.debug("going to receive..")
				data = self.socket.recv(BUFFER_SIZE).decode(ENCODING)
				dbug.debug("finished receiving..")
				self.callback(self,data)
				dbug.debug("Client sent : "+data) 
				response = "You sent me: " + data
				self.socket.send(response.encode())
			except socket.error as socket_e:
				if(socket_e.errno == None):
					dbug.debug(str(socket_e))
				else:
					self.connection_open = False
		dbug.debug ("Client disconnected...")
		self.socket.close()
		self.connection_open = False
		self.serv_reference.refresh_thread_array()

class ServerThread(threading.Thread):
	
	def __init__(self,command_list):
		threading.Thread.__init__(self)
		self.command_list = command_list
		self.host = HOST
		self.port = PORT
		self.threads = []	
		self.connection_open = True
		dbug.debug("Server starting..")

	def run(self):
		tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		tcpsock.bind((self.host,self.port))
		self.threads = []
	
		while (self.connection_open == True):
			tcpsock.listen(4)
			dbug.debug("\nListening for incoming connections...")
			(clientsock, (ip, port)) = tcpsock.accept()
			clientsock.settimeout(SOCKET_TIMEOUT)
			newthread = ClientThread(ip, port, clientsock, self.command_list, self)
			newthread.start()
			self.threads.append(newthread)

			for t in self.threads:
				t.join()
	def quit(self):
		for t in self.threads:
			t.connection_open = False		

		dbug.debug("Quitting Server..")
		self.connection_open = False

	def send_to_all(self, command):
		tmp_file = open("tmp.txt.gz", "wb")
		tmp_file.write(command)
		tmp_file.close()
		tmp_file = open("tmp.txt.gz", "rb")

		if(self.count_threads() == 0):
			dbug.debug("No open connections to send to..")
			return None
		message = command + "\n"
		message = message.encode()
		message = tmp_file.read()
		for t in self.threads:
			t.socket.sendall(message)
		tmp_file.close()
		print(message)

	def refresh_thread_array(self):
		new_threads = []
		
		dbug.debug("Refreshing Thread Array")
		for t in self.threads:
			if(t.connection_open):
				new_threads.append(t)

		self.threads = new_threads

	def count_threads(self):
		open_threads = len(self.threads)
		dbug.debug("Threads open: " +  str(open_threads))
		return open_threads

def command_handler(self, raw_command):
    
#	if(len(raw_command) > 50):
#		response = "[+] Command to long..\n"
#		self.socket.send(response.encode())

	processed_command = parse_raw_command(raw_command)
	try:
		json_load = json.loads(processed_command)

		json_command = json_load['command']
		json_data = json_load['data']
	except Exception as e:
		dbug.debug("Gibberish sent, not json format..")
		json_command = "notjson"
		json_data = raw_command

	if(json_command in self.command_list):
		self.command_list[json_command](self, json_data)
        
def parse_raw_command(raw_command):
	processed_command = ""

	if('\n' in raw_command):
		pipe_index = raw_command.find('\n')
		processed_command = raw_command[:pipe_index]
	return processed_command

def start_server(command_list):
	serv_thread = ServerThread(command_list)
	serv_thread.start()

	return serv_thread
