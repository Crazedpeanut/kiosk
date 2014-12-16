import http.client, urllib
import datetime
import telnetlib
import time
#import requests

blue = False
HOST = "numbat"
PORT = 39998

def handle_scan():
    barcode = input("Scan barcode: ")

    if barcode == "exit":
        exit()
        print("Exiting.")

    #this stuff works for python 2, python 3 below it
    #j = {"barcode": barcode, "time": datetime.datetime.utcnow()}
    #r = requests.post("http://squirtle/barcode/test.php", data = j)
    #print("text is: " + r.text)

    params = urllib.parse.urlencode({"barcode": barcode, "time": datetime.datetime.utcnow()})
    conn = http.client.HTTPConnection("squirtle:80")
    conn.request("POST", "/barcode/test.php", params)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    print("Received: {}", data)

def handle_coms(tn):
    global blue
    #tn.write("login\n")
    #tn.write(user + "\n")
    #tn.write(password + "\n")

    if blue:
        tn.write(b'blue\r\n')
        blue = False
    else:
        tn.write(b'red\r\n')
        blue = True

    #tn.write("logout\n")
    #tn.close()

def test(tn):
    tn.write(b'printdata|{"data": "hello"}\r\n')
    time.sleep(3)
    
    

if __name__ == "__main__":

    tn = telnetlib.Telnet(HOST, PORT)

    while 1:
        #handle_scan()
        test(tn)
        #handle_coms(tn)
