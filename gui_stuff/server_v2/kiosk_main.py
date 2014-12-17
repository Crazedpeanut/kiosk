import kiosk_network
#import kiosk_http

HOST = "squirtle"
PORT = 80

def print_data(self, data):
	print(data)

def check_in(self, data):
	resource = "/barcode/test.php"
	method = "POST"

	#print(kiosk_http.http_request(HOST, PORT,method,resource , data))
		
def not_json_recv(self, data):
	print(data)

command_list = {'notjson' : not_json_recv, 'checkin' : check_in}

serv = kiosk_network.start_server(command_list)
