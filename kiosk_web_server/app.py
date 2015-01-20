from flask import Flask, url_for, render_template, request
import pymysql
#import simplejson as json

app = Flask(__name__)
template = 'default/'

db_config = {
	'user':'dev_kiosk',
	'password':'',
	'host':'localhost',
	'database':'dev_kiosk',
	'autocommit':True
}

def create_host(host_name):
	query = "INSERT INTO kiosks (host) VALUES ('%s')" % (host_name)
	query_db(query)
	print(query)

def insert_heartbeat(host, ip, kiosk_timestamp):
	check_host_exists(host)

	query = "INSERT INTO heartbeats (host, ip, kiosk_timestamp) VALUES ('%s', '%s', '%s')" % (host, ip, kiosk_timestamp)
	query_db(query)

def insert_checkin(barcode, host):
	query = "INSERT INTO check_ins (barcode, host) VALUES (%d, '%s')" % (int(barcode), host)
	query_db(query);

def check_host_exists(host):
	query = "SELECT count(host) from kiosks WHERE host='%s'" % (host)
	result = query_db(query)
	result = result.fetchall()
	count = int(result[0][0])

	if(count == 0):
		print("Host count: " + str(count))
		return False
	else:
		return True

def query_db(query):
	try:
		print(query)
		conn = pymysql.connect(**db_config)
		cursor = conn.cursor()
		result = cursor.execute(query)
		print(result)
		conn.close()
		return cursor

	except Exception as err:
		print(str(err))

@app.route("/")
def index():
	stylesheet = url_for('static', filename='style/style.css')
	
	title = "Home"
	header = render_template(template+'header.html', title=title)
	
	query = ('SELECT * FROM check_ins;')
	result = query_db(query)
	grid_checkins = render_template(template+'table.html', table=result)	
	
	query = ('SELECT * FROM heartbeats;')
	result = query_db(query)
	grid_heartbeats = render_template(template+'table.html', table=result)	
	
	footer = render_template(template+'footer.html')
	
	return header+grid_checkins+grid_heartbeats+footer

@app.route("/checkin/add",methods=['POST'])
def checkin():
	print(request.headers)
	if (request.method == 'POST'):
		data = request.get_json()['checkin']
		barcode = data['barcode'] 
		host = data['host']		

		insert_checkin(barcode, host)	

		if(check_host_exists(host) is False):
			create_host(host)
		return ""

@app.route("/heartbeat/add",  methods=['POST'])
def add_heartbeat():
	if(request.method == "POST"):
		data = request.get_json()['heartbeat']	
		client_timestamp = data['timestamp']
		host = data['host']	
		ip = data['ip']

		insert_heartbeat(host, ip, client_timestamp)

		if(check_host_exists(host) is False):
			create_host(host)
		return ""

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')


