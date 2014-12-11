import http.client
import urllib

def http_request(host, port, method, resource, data):
	print("debug", data) 	
	params = urllib.parse.urlencode(data)
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"} 
	conn = http.client.HTTPConnection(host, port)
	conn.set_debuglevel(0)
	conn.request(method, resource, params, headers)
	response = conn.getresponse()
	result = response.read()
	conn.close()

	return result


