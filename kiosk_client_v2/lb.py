'''
Author: Mike
Date: 18/12/14

Description: Communicate with lightbars over CANbus protocol
'''
#!/usr/bin/env python

import time
import socket
import struct
import select



s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind(('can0',))

poll = select.poll()
poll.register(s, select.POLLIN)

can_frame_fmt = "=IB3x8s"
can_frame_size = struct.calcsize(can_frame_fmt)

can_dlc = 8

def send(can_id, data):
    """send(0x400, b'\x01\x02\x03\x04\x05\x06\x07\x08')"""
    data = data.ljust(8, b'\x00')
    msg = struct.pack(can_frame_fmt, can_id, can_dlc, data)
    s.send(msg)

def recv(timeout):
    while poll.poll(timeout):
        response = s.recv(100)
        for b in response:
            print('%2.2x' % b, end=' ')
        print('\n')

def set_color(addr, led, r, g, b):
    data = struct.pack('BBBBB', 1, led, r, g, b)
    send(addr, data)

def set_state(addr, mask):
    data = struct.pack('=BH', 2, mask)
    send(addr, data)

def count(addr, rate):
    n = 0
    while 1:
        set_state(addr, n % 4096)
        n += 1
        time.sleep(rate)


def hello():
    data = struct.pack('B', 0x00)
    send(0x100, data)
    recv(500)

def set_id(sn, id):
    data = struct.pack('>BBBBI', 0x01, id, 0, 0, sn)
    send(0x100, data)


