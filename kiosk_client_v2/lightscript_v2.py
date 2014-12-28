'''
Author: John Kendall
Date: 18/12/14

Description: Assorted functions to control lightbars. Contains methods to save and play sequences, and other stuff
'''

import lb as can
import time
from random import randrange

light_bars = [0x200, 0x201, 0x202, 0x203, 0x204, 0x205]
leds_per_bar = 12
FILE = "led_image.lightbarframe"

def decode_file():
    data = []
    f = open(FILE, 'r')

    line = f.readline()
    while(len(line) > 0):
        red = ""
        blue = ""
        green = ""

        for x in range(leds_per_bar):

            point = int(line[x])
            if(point == 1):
                red += "1"
                blue += "0"
                green += "0"
            elif(point == 2):
                red += "0"
                blue += "1"
                green += "0"           
            elif(point == 3):
                red += "0"
                blue += "0"
                green += "1"  
            elif(point == 0):
                red += "0"
                blue += "0"
                green += "0"         
        
        red_hex = int(red, 2)
        blue_hex = int(blue, 2)
        green_hex = int(green, 2)

        data.append([red_hex,blue_hex,green_hex])
        line = f.readline()

    return data

def decode_file_2():
    data = []
    f = open(FILE, 'r')

    line = f.readline()
    while(len(line) > 0):
        p = []

        for x in range(leds_per_bar):
            point = int(line[x])
            p.append(point)

        data.append(p)
        line = f.readline()

    return data


def print_file():
    data = decode_file_2()

    reset_leds()

    for x in range(6):
        for i in range(leds_per_bar):
            print(data[x][i], "x: ", x, "y: ", i)
            if(data[x][i] == 0):
                can.set_color(light_bars[x], i, 0, 0, 0)
            if(data[x][i] == 1):
                 can.set_color(light_bars[x], i, 64, 0, 0)
            if(data[x][i] == 2):
                can.set_color(light_bars[x], i, 0, 64, 0)
            if(data[x][i] == 3):
                can.set_color(light_bars[x], i, 0, 0, 64)
            
            time.sleep(0.001)

def mode_1():
    while(True):
        for led in range(12):

            r = randrange(255)
            g = randrange(255)
            b = randrange(255)

            can.set_color(0x300, led, r, g, b)

        time.sleep(0.05)

def mode_2():
    
    t = time.time()
    state = 0

    while(True):

        for led in range(12):
            r = randrange(255)
            g = randrange(255)
            b = randrange(255)
            can.set_color(0x300, led, r, g, b) 
            
            if(state == 0):
                can.set_state(0x300, 0xaaa)
            elif(state == 1):
                can.set_state(0x300, 0x555)
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
        can.set_color(0x300, led, r, g, b)

        time.sleep(0.01)

    time.sleep(1)
    reset_leds()
    
def reset_leds():
    for led in range(12):
        can.set_color(0x300, led, 0, 0, 0)
        time.sleep(0.0001)   

def set_color_grid_pixel_hex(x, y, hexstr):

    r = int(hexstr[0:2], 16)
    g = int(hexstr[2:4], 16)
    b = int(hexstr[4:6], 16)

    set_color_grid_pixel(int(x),int(y), r, g, b)

def set_color_grid_pixel(x, y, r, g, b):
    can.set_color(light_bars[y], x, r, g, b)


