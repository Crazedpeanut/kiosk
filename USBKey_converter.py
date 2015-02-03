'''
Author: John Kendall and Andrew Jones
Date: 18/12/14

Description: Convert USB keys into ASCII characters
'''
def usbkey_to_char(key):
	key = int(ord(key))
	if 4 <= key <= 29: #A-Z
		return chr(key + (65-4))
	elif 30 <= key <= 38: #1-9
		return chr(key + (48-29))
	elif key is 39:
		return '0'
	elif key is 44:
		return ' '
	elif key is 45:
		return '-'
	else:
		return None

if(__name__ == "__main__"):
	while 1:
		key = input("Enter a number: ")
		converted = usbkey_to_char(int(key))
		print(converted)
