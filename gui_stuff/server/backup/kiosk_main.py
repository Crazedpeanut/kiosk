import kiosk_network
import kiosk_http

HOST = "squirtle"
PORT = 80

def print_data(self, data):
	print(data)

def check_in(self, data):
	resource = "/barcode/test.php"
	method = "POST"

	print(kiosk_http.http_request(HOST, PORT,method,resource , data))
		

command_list = {'printdata' : print_data, 'checkin' : check_in}

serv = kiosk_network.server(command_list)
serv.run()
