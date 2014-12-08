import socket
import time
import threading 
import errno
import simplejson as json
import debug as dbug

HOST = "localhost"
PORT = 39998    
BUFFER_SIZE = 4096
ENCODING = "utf-8"
CONNECT_WAIT = 5
SOCKET_TIMEOUT = 5

class network_client_thread(threading.Thread):
    
	def __init__(self, callback, command_list):
		threading.Thread.__init__(self)
		self.sock = self.socket_init()
		self.callback = callback
		self.command_list = command_list
		self.connected = False
		self.failed_to_connect = False
		self.keep_connected = True
	
	def socket_init(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(SOCKET_TIMEOUT)
		return sock

	def connect_to_server(self):
		while(self.connected is False):
			try:
				if(self.failed_to_connect is True):
					dbug.debug("Reattempting connection..")
					self.sock.connect((HOST, PORT))
					self.connected = True
					self.failed_to_connect = False
				else:
					dbug.debug("Connecting to server..")
					self.sock.connect((HOST, PORT))
					self.connected = True
					
			except socket.error as socket_e:
				dbug.debug(str(socket_e));
				if (socket_e.errno == errno.ECONNREFUSED):
					dbug.debug("Failed to connect to server..")
					dbug.debug("Will try again every " + str(CONNECT_WAIT) + " seconds.")
					self.failed_to_connect = True
					self.connected = False
					time.sleep(CONNECT_WAIT)
				if (socket_e.errno == errno.EISCONN):
					if(self.test_connection(self.sock) is True):
						self.connected = True
						dbug.debug("Ignoring open socket exception..")
					else:
						dbug.debug("Closing socket..")
						try:
							self.sock.close()
							self.sock = self.socket_init()
						except Exception as e:
							exit()
						self.connected = False
						self.failed_to_connect = True
			except Exception as exception:
				print (exception)	

	def run(self):
				
		while(self.keep_connected is True):
			
			if(self.connected is False):
				self.connect_to_server()

			try:
				data = self.sock.recv(BUFFER_SIZE)
				while len(data):
					self.callback(self, data.decode(ENCODING))
					data = self.sock.recv(BUFFER_SIZE)
				#self.keep_connected = False
				self.connected = False
				#self.sock.close()
			except socket.error as socket_e:
				if(socket_e.errno == None):
					dbug.debug(str(socket_e))
				#	self.send_message("check", "")
				else:
					self.connected = False
					dbug.debug(str(socket_e) + str(socket_e.errno))				
		dbug.debug("Connection Closed.")

	def test_connection(self, socket):
		result = True
		try:
			socket.sendall("test")
		except Exception as e:
			result = False

		return result
	
	def send_message(self,command, data):
		message = command + "|" + data
		self.sock.sendall(message.encode())

def command_handler(self, raw_command):

#       if(len(raw_command) > 50):
#               response = "[+] Command to long..\n"
#               self.socket.send(response.encode())
#		dbug.debug(raw_command)
		processed_command = parse_raw_command(raw_command)
#		dbug.debug(processed_command)
		processed_data = parse_raw_command_data(raw_command)
		dbug.debug(processed_data)

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


def test_function(data):
	dbug.debug(data)
	dbug.debug("yo yo yo yo")

clist = {"test" : test_function}
client_thrd = network_client_thread(command_handler, clist)
client_thrd.start()
	

