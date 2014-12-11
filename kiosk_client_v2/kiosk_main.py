import kiosk_http as http
import time, datetime
import simplejson as json
import read_from_hidraw as bcode_listen

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
	timestamp = datetime.datetime.now()
	kiosk = get_kiosk_id()
	return '{"barcode": %s, "timestamp": %s, "kiosk": %s}\n' % (barcode, timestamp, kiosk)

def record_check_in(check_in):
	try:
		f = open(DATA_FILE, 'a')
		f.write(check_in)
	except Exception as e:
		print(str(e))

def create_heartbeat():
	


#TODO
def http_result_handler(result):
	print(result)
		
def bcode_handler(bcode):
	check_in = create_check_in(bcode)
	record_check_in(check_in)

def main():
	kiosk_id = str(get_kiosk_id())
	timestamp = str(datetime.datetime.now())
	barcode = "900"

	data = '{"time": "' +  timestamp + '", "station": "' +  kiosk_id + '", "barcode": "' + barcode + '"}'
	print(data)
	while(True):
		http_result = http.http_request(HOST, PORT, METHOD, RESOURCE, json.loads(data))	
		time.sleep(PAUSE_BETWEEN_REQUESTS)
		http_result_handler(http_result)
if __name__ == "__main__":
	#main()	

	bcode_listen.start_listening(bcode_handler)

	i = 1
	while(True):	
		i = i + 1
