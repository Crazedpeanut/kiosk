#!/usr/bin/env python

import socket, threading
import simplejson as json

class ClientThread(threading.Thread):
	WELCOME_MESSAGE = "\nWelcome to the server \n\n"
	BUFFER_SIZE = 4096
	ENCODING = "utf-8"

	def __init__(self,ip,port,socket,command_list):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.socket = socket
		self.callback = command_handler
		self.command_list = command_list

		print ("[+] New thread started for "+ip+":"+str(port))


	def run(self):  
		print ("Connection from : "+self.ip+":"+str(self.port))
		self.socket.send(self.WELCOME_MESSAGE.encode())                  
		data = "dummydata"

		while len(data):
			data = self.socket.recv(self.BUFFER_SIZE).decode(self.ENCODING)
			self.callback(self,data)
			print ("Client sent : "+data) 
			response = "You sent me: " + data
			self.socket.send(response.encode())
        
		print ("Client disconnected...")
		self.socket.close()

class server():
	def __init__(self,command_list):
		self.host = "0.0.0.0"
		self.port = 39998
		self.command_list = command_list
    
	def run(self):
		tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		tcpsock.bind((self.host,self.port))
		threads = []
	
		while True:
			tcpsock.listen(4)
			print ("\nListening for incoming connections...")
			(clientsock, (ip, port)) = tcpsock.accept()
			newthread = ClientThread(ip, port, clientsock, self.command_list)
			newthread.start()
			threads.append(newthread)

			for t in threads:
				t.join()

	def send_to_all(command, data):
		message = command + "|" + data
		message = message.encode()
		for t in threads:
			t.socket.sendall(message)


def command_handler(self, raw_command):
    
	if(len(raw_command) > 50):
		response = "[+] Command to long..\n"
		self.socket.send(response.encode())

		processed_command = parse_raw_command(raw_command)
		processed_data = parse_raw_command_data(raw_command)

		if(processed_command in self.command_list):
			self.command_list[processed_command](self, json.loads(processed_data))
        
def parse_raw_command(raw_command):
	processed_command = ""

	if('\n' in raw_command):
		pipe_index = raw_command.find('|')
		processed_command = raw_command[:pipe_index]
	return processed_command

def parse_raw_command_data(raw_command):
	processed_data = ""

	if('\n' in raw_command and '|' in raw_command):
		pipe_index = raw_command.find('|')
		newline_index = raw_command.find('\n')
		processed_data = raw_command[pipe_index + 1:newline_index - 1]
	return processed_data

def quit_client(self):
	print("quitting..")
	self.socket.close()
