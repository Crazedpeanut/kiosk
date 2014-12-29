'''
Author: John Kendall
Date: 18/12/14

Description: HTTP functions to send and recieve messages/data to and from a webserver
'''

import http.client
import urllib
import debug as dbug
import gzip
import settings

DATA_FILE = settings.STORED_REQUESTS_FILE
ENCODING = settings.ENCODING
HTTP_CONN_DEBUG_LVL = 0

def http_request(params):
    host = params["host"]
    port = params["port"]
    method = params["method"]
    resource = params["resource"]
    data = params["data"]
    callback = params["result_callback"]
    connection_failed_callback = params["connection_failed_callback"];
	
    conn = http.client.HTTPConnection(host, port)
    conn.set_debuglevel(HTTP_CONN_DEBUG_LVL)

    params = urllib.parse.urlencode(data)
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"} 
    try:	
        conn.request(method, resource, params, headers)
        response = conn.getresponse()
        result = response.read()
    #print(result)
        conn.close()

        f = open("tmp.txt.gz", "wb")
        f.write(result)
        f.close()
        f = gzip.open("tmp.txt.gz", "r")
        result = f.read()
        f.close()
    	#dbug.debug(result.decode(ENCODING))
        callback(result)
        f = open(DATA_FILE, "w")
        f.write("")
        f.close()
    except Exception as e:
        dbug.debug("Connection Failed: "+ str(e))
        connection_failed_callback(data)
        

