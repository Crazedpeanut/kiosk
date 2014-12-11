import zbar
from sys import argv

print("Hi")

proc = zbar.Processor()

proc.parse_config('enable')

device = '/dev/video0'

if len(argv) > 1:
	device = argv[1]
proc.init(device)

proc.visible = True

proc.process_one()

proc.visible = False

for symbol in proc.results:
	print('decoded', symbol.type, 'symbol', '"%s"' % symbol.data)
