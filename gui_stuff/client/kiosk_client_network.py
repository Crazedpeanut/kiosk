import socket
import time
import threading 
import errno
import simplejson as json
import debug as dbug

HOST = "10.10.10.117"
PORT = 39998    
BUFFER_SIZE = 1024
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
                                time.sleep(CONNECT_WAIT)

	def run(self):
				
		while(self.keep_connected is True):
			
			if(self.connected is False):
				self.connect_to_server()

			try:
                                
                            data = self.sock.recv(BUFFER_SIZE).decode(ENCODING)
                            
                            while(len(data)):
                                data += self.sock.recv(BUFFER_SIZE).decode(ENCODING)
                                if("||" in data):
                                    break;
                            self.callback(self, data) 
                            
			except socket.error as socket_e:
				if(socket_e.errno == None):
					dbug.debug(str(socket_e))
			    
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
	
	def send_message(self,command):
		print(str(command))
		message = str(command) + "\n"
		self.sock.sendall(message.encode())

def command_handler(self, raw_command):
                #dbug.debug(raw_command)
                processed_command = parse_raw_command(raw_command)
                dbug.debug(processed_command)
                try:
                    json_load = json.loads(processed_command)

                    json_command = json_load['command']
                except Exception as e:
                    dbug.debug("Gibberish sent, not json format..")
                    json_command = "notjson"
                    json_data = raw_command
                    dbug.debug(str(e))

                if(json_command in self.command_list):
                    self.command_list[json_command](self, json_load)

def parse_raw_command(raw_command):
        processed_command = ""

        if('\n' in raw_command):
                pipe_index = raw_command.find('\n')
                processed_command = raw_command[:pipe_index]
        return processed_command

def start_client(comm_list):
        client_thrd = network_client_thread(command_handler, comm_list)
        client_thrd.start()
        return client_thrd
