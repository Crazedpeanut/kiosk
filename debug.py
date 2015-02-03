'''
Author: John Kendall
Date: 18/12/14

Description: Logging script to display debug messages on in the standard output or to record them in a file
'''

import datetime
import os
import time
import settings

DEBUGGING = settings.DEBUGGING
DEBUGGING_MODE = settings.DEBUGGING_MODE
PRINT_DATETIME = settings.PRINT_DATETIME

debugging_active = False

def debug(message):
    global debugging_active

    if(DEBUGGING == True):
        dbugmsg = "DEBUG: " + message
		
        if(PRINT_DATETIME == True):
            current_time = datetime.datetime.now()
            dbugmsg += " | " + str(current_time)
           
        
        while(debugging_active == True):
            time.sleep(0.5)
        
        dbugmsg += "\n\n\n"

        try:
            debugging_active = True

            if(DEBUGGING_MODE == 1):
                print(dbugmsg)
            elif(DEBUGGING_MODE == 2):
                if(os.path.isfile("debug.log")):
                    f = open("debug.log", "a")
                    f.write(dbugmsg)
                else:
                    f = open("debug.log", "w")
                    f.write(dbugmsg)
        except Exception as e:
            print(str(e))
        finally:
            debugging_active = False
