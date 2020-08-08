#!/usr/bin/python

import usb.core
import usb.util
import time
import thread

# find our device
dev = usb.core.find(idVendor=0x04b4, idProduct=0x00f0 )

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()

#intf = cfg[(0,1)]

#dev.set_interface_altsetting(interface = 0, alternate_setting = 0)
intf = cfg[(0,0)]

#print intf

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        e.bEndpointAddress == 1)

ep2 = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        e.bEndpointAddress == 0x81)

assert ep is not None
assert ep2 is not None

print 'ep:',ep
print 'ep2:',ep2

chunkr = 2**16
chunkw = 2**22

print "Starting CYUSB3014 python loopback test"

def read_loop():
    start = time.time()
    trans = 0
    while True:
        data = dev.read(0x81, chunkw, 1000)
        trans = trans + len(data)
        if time.time() > start + 1:
            bps = trans/(time.time() - start)
            print ("Transfered %d kB/s" % (bps/(1024)) )
            trans = 0
            start = time.time()

def write_loop():
    dat = "A"*chunkw
    while True:
        try:
            ep.write(dat)
        except:
            pass

thread.start_new_thread( write_loop, () )

read_loop()

