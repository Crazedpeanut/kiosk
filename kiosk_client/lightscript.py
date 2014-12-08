import can
import time
from random import randrange

def mode_1():
    while(True):
        for led in range(12):

            r = randrange(255)
            g = randrange(255)
            b = randrange(255)

            can.set_color(0x400, led, r, g, b)

        time.sleep(0.05)

def mode_2():
    
    t = time.time()
    state = 0

    while(True):

        for led in range(12):
            r = randrange(255)
            g = randrange(255)
            b = randrange(255)
            can.set_color(0x400, led, r, g, b) 
            
            if(state == 0):
                can.set_state(0x400, 0xaaa)
            elif(state == 1):
                can.set_state(0x400, 0x555)
            time.sleep(0.2)

        if(time.time() - t > 0 and time.time() - t < 3):
            state = 1
        elif(time.time() - t > 3 and time.time() - t < 10):
            state = 0
            t = time.time()
            
        time.sleep(0.1)

def mode_3(r, g, b):
    r = r
    g = g
    b = b

    reset_leds()
    time.sleep(0.3)

    for led in range(12):
        can.set_color(0x400, led, r, g, b)

        time.sleep(0.05)

    time.sleep(1)
    reset_leds()
    
def reset_leds():
    for led in range(12):
        can.set_color(0x400, led, 0, 0, 0)
        time.sleep(0.05)   

