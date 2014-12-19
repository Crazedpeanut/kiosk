import datetime
import os
import time

DEBUGGING = True
DEBUGGING_MODE = 2
PRINT_DATETIME = True

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
