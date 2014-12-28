'''
Author: John Kendall
Date: 18/12/14

Description: Main script for the kiosk application. Functions called from the main loop are ran in separate threads
'''
#TODO - Include saved data from failed connection attempts to HTTP requests (heartbeats)

import kiosk_http as http
import time, datetime
import simplejson as json
import read_from_hidraw as bcode_listen
import socket
import commands
import threading
import debug as dbug
import settings

HOST = settings.WEB_SERVER_HOST
PORT = settings.WEB_SERVER_PORT
METHOD = "POST"
RESOURCE = "/barcode/test.php"
PAUSE_BETWEEN_HEARBEAT = 60
DATA_FILE = settings.STORED_REQUESTS_FILE
MAINLOOP_PAUSE = 0.001

threads = []

class thread_worker(threading.Thread):
    def __init__(self, delegate, delegate_params):
        threading.Thread.__init__(self)
        self.delegate = delegate
        self.delegate_params = delegate_params

    def run(self):
        if(self.delegate_params != None):
            self.delegate(self.delegate_params)
        else:
            self.delegate()

        refresh_thread_array()

def create_check_in(barcode):	
	kiosk = socket.gethostname()
	return '{"barcode": "%s", "kiosk": "%s"}' % (barcode, kiosk)

def record_check_in(check_in):
	try:
		f = open(DATA_FILE, 'a')
		f.write(check_in)
	except Exception as e:
		print(str(e))

def create_heartbeat():
	timestamp = datetime.datetime.now()
	kiosk = socket.gethostname()
	ip = socket.gethostbyname(kiosk)
	heartbeat = '{"timestamp": "%s", "kiosk": "%s", "ip": "%s"}' % (timestamp, kiosk, ip)
	f = open(DATA_FILE, "r")	
	stored_requests = f.read()
	if(len(stored_requests) > 0):
		heartbeat += stored_requests
	return heartbeat

def http_result_handler(result):
    command_list = {"play_sequence":commands.play_sequence,"test": commands.test_command, "loadsequence":commands.load_sequence, "printdata":commands.print_data, "updateleds":commands.update_lights, "blanklightars":commands.blank_lightbars}

    try:
    	json_data = json.loads(result)
    
        serv_commands = json_data['commands']

        for comm in serv_commands:
            if(comm['command'] in command_list):
        	    command_list[comm['command']](comm)
    except Exception as e:
        dbug.debug("response from webserver probably isn't JSON format.. " + str(e))
		
def bcode_handler(bcode):
    check_in = create_check_in(bcode)
    #record_check_in(check_in)
    params = {"host":HOST, "port":PORT, "method":METHOD, "resource":RESOURCE, "data":json.loads(check_in), "result_callback":http_result_handler, "connection_failed_callback":record_check_in}  
    create_thread_worker(http.http_request, params)

def create_thread_worker(delegate, delegate_params):
    new_thread = thread_worker(delegate, delegate_params)
    new_thread.start()
    threads.append(new_thread)
    return new_thread

def refresh_thread_array():
    global threads

    for t in threading.enumerate():
        threads.append(t)

def ticker(params):
    time_in_seconds = params["time"]
    delegate = params["delegate"]
    delegate_params = params["delegate_params"]

    while(True):
        time.sleep(time_in_seconds)
        delegate(delegate_params)

def main():
    bcode_listen.start_listening(bcode_handler)

    data = create_heartbeat() 
    params = {"host":HOST, "port":PORT, "method":METHOD, "resource":RESOURCE, "data":json.loads(data), "callback":http_result_handler}
		
    ticker_params = {"time":PAUSE_BETWEEN_HEARBEAT, "delegate": http.http_request, "delegate_params": params}
    create_thread_worker(ticker, ticker_params)	

    while(True):    	
        time.sleep(MAINLOOP_PAUSE)

if __name__ == "__main__":
	main()	

	

