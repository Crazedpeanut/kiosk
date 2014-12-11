import usb.core
import usb.util

DEFAULT_VENDOR_ID = 0x0483
DEFAULT_PRODUCT_ID = 0x5800
interface = 0

dev = usb.core.find(idVendor=DEFAULT_VENDOR_ID, idProduct=DEFAULT_PRODUCT_ID)

if (dev is None):
	raise ValueError('Device not found')

if(dev.is_kernel_driver_active(interface) is True):
	print ("but we need to detach kernel driver")
	dev.detach_kernel_driver(interface)
	print ("claiming device")
	dev.set_configuration()
	usb.util.claim_interface(dev, interface)
	#print ("release claimed interface")
	#usb.util.release_interface(dev, interface)
	#print ("now attaching the kernel driver again")
	#dev.attach_kernel_driver(interface)
	#print ("all done")

cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN)

assert ep is not None

while(True):
	data = dev.read(ep, 2048)
	if(len(data)):
		print(data)
