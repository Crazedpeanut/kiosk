'''
Author: John Kendall
Date: 18/12/14

Description: Reads from the hidraw device file. As a way of binding to a barcode scanner
            (Requires either root permissions or read permission of the hidraw device file)
'''
import time
import sys
import re
import threading
import USBKey_converter as USBKey
import debug as dbug

buffersize = 16
TIME_WAIT = 0.2

class bcode(threading.Thread):
    
    def __init__(self, callback):
        self.callback = callback
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            try:
                f = open('/dev/hidraw0', 'r')
						
                while(True):
                    barcode = ""

                    b = f.read(buffersize)
                    dec = USBKey.usbkey_to_char(b[2])

                    while(dec is not None):
                        barcode = barcode + str(dec)
                        b = f.read(buffersize)
                        dec = USBKey.usbkey_to_char(b[2])
                    self.callback(barcode)
                    time.sleep(TIME_WAIT)

            except Exception as e:
                dbug.debug(str(e))

def print_barcode(barcode):
	sys.stdout.write(barcode)

def start_listening(callback):
	bcode_listen_thread = bcode(callback)
	bcode_listen_thread.start()

def main():
	thread = bcode(print_barcode)
	thread.start()

if(__name__ == "__main__"):
	main()
