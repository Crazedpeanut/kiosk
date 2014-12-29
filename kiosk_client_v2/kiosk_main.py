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
import queue 

HOST = settings.WEB_SERVER_HOST
PORT = settings.WEB_SERVER_PORT
METHOD = "POST"
RESOURCE = "/barcode/test.php"
PAUSE_BETWEEN_HEARBEAT = 60
DATA_FILE = settings.STORED_REQUESTS_FILE
MAINLOOP_PAUSE = 0.001

data_file_operation_queue = queue.Queue()
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
    return {"checkin":{"barcode": barcode, "kiosk": kiosk}}

def file_operation_queue_add(delegate, params):
    queue_node = {"delegate" : delegate, "params":params}
    data_file_operation_queue.put(queue_node)
    dbug.debug("Added file operation to queue")

def file_operation_queue_perform_operations():
    while(True):
        if(data_file_operation_queue.qsize()):
            node = data_file_operation_queue.get()
            operation = node["delegate"]
            params = node["params"]
            operation(params)
            time.sleep(0.2)

def http_failed_connection_handler(request):
    request = str(request)
    params = {"request": request}
    file_operation_queue_add(record_request, params) 

def record_request(params):
    request = params["request"]
    try:
        request = str(request)
        dbug.debug("Recording request for retransmission at a later time..")
        file_read = open(DATA_FILE, 'r')
        data = file_read.read()
        data_len = len(data)

        file_append = open(DATA_FILE, 'a')
        request.replace("\'", "\"")
        if(data_len > 1):
            file_append.write(","+request)
        else:
            file_append.write(request)
    except Exception as e:
        print("Recording request failed: " + str(e))
    finally:
        file_append.close()
        file_read.close()

def create_heartbeat():
    timestamp = datetime.datetime.now()
    kiosk = socket.gethostname()
    ip = socket.gethostbyname(kiosk)
    heartbeat = '{"heartbeat":{"timestamp": "%s", "kiosk": "%s", "ip": "%s"}}' % (timestamp, kiosk, ip)
    f = open(DATA_FILE, "r")	
    stored_requests = f.read().replace("\'", "\"")
    if(len(stored_requests) > 1):
        dbug.debug("Len: " + str(len(stored_requests)))
        heartbeat += "," + stored_requests
        heartbeat = '{"messages":[' + heartbeat + "]}"
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
    #check_in_json = json.loads(check_in)
    params = {"host":HOST, "port":PORT, "method":METHOD, "resource":RESOURCE, "data":check_in, "result_callback":http_result_handler, "connection_failed_callback":http_failed_connection_handler}  
    f = open(DATA_FILE, "r")
    file_size = len(f.read())
    if(file_size > 1):
        record_request({"request": params})
    else:
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
    dbug.debug(data)
    data_json = json.loads(data)
    params = {"host":HOST, "port":PORT, "method":METHOD, "resource":RESOURCE, "data":data_json, "result_callback":http_result_handler, "connection_failed_callback":http_failed_connection_handler}
		
    ticker_params = {"time":PAUSE_BETWEEN_HEARBEAT, "delegate": http.http_request, "delegate_params": params}
    create_thread_worker(ticker, ticker_params)	

    create_thread_worker(file_operation_queue_perform_operations, None)

    while(True):    	
        time.sleep(MAINLOOP_PAUSE)

if __name__ == "__main__":
	main()	

	

