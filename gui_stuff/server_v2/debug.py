DEBUGGING_MODE = True
PRINT_DATETIME = True
import datetime

def debug(message):
	if(DEBUGGING_MODE == True):
		dbugmsg = "DEBUG: " + message
		
		if(PRINT_DATETIME == True):
			current_time = datetime.datetime.now()
			dbugmsg += " | " + str(current_time)
		print(dbugmsg)
