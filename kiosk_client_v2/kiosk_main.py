import kiosk_http as http
import time, datetime
import simplejson as json
import read_from_hidraw as bcode_listen
import socket

HOST = "localhost"
PORT = 80
METHOD = "POST"
RESOURCE = "/barcode/test.php"

PAUSE_BETWEEN_REQUESTS = 60

DATA_FILE = "data.json"

#TODO
def get_kiosk_id():
	return 1;

def create_check_in(barcode):	
	kiosk = get_kiosk_id()
	return '{"barcode": %s, "kiosk": %s}\n' % (barcode, kiosk)

def record_check_in(check_in):
	try:
		f = open(DATA_FILE, 'a')
		f.write(check_in)
	except Exception as e:
		print(str(e))

def create_heartbeat():
	timestamp = datetime.datetime.now()
	kiosk = get_kiosk_id()
	name = socket.gethostname()
	ip = socket.gethostbyname(name)
	return '{"timestamp": %s, "kiosk": %s, "name": %s, "ip": %s}' % (timestamp, kiosk, name, ip)

#TODO
def http_result_handler(result):
	print(result)
		
def bcode_handler(bcode):
	check_in = create_check_in(bcode)
	record_check_in(check_in)

def main():
	
	bcode_listen.start_listening(bcode_handler)
	
	while(True):
		#http_result = http.http_request(HOST, PORT, METHOD, RESOURCE, json.loads(data))	
		#http_result_handler(http_result)
		print(create_heartbeat())
		time.sleep(PAUSE_BETWEEN_REQUESTS)
if __name__ == "__main__":
	main()	

	

