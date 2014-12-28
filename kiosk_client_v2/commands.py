'''
Author: John Kendall
Date: 18/12/14

Description: Assorted functions to be called by the http_result_handler
'''

import lightscript_v2 as ls
import time
import simplejson as json
import os
import debug as dbug

saving_sequence = False
playing_sequence = False

def test_command(data):
    ls.mode_3(255, 0, 0)

def update_lights(data):
    for led in data['leds']:
        ls.set_color_grid_pixel_hex(led["x"], led["y"], led["color"])
        time.sleep(0.002)

def load_sequence(data):
    global saving_sequence

    while(saving_sequence == True):
        time.sleep(0.5)

    try:
        saving_sequence = True
        sequence_num = data["sequence_num"]
        dbug.debug("Saving data")
        os.remove("sequence"+sequence_num+".sequence")
        f = open("sequence"+sequence_num+".sequence", "w")
        f.write(str(data))
    except Exception as e:
        dbug.debug(str(e))
    finally:
        saving_sequence = False

    

def play_sequence(data):
    global playing_sequence

    while(playing_sequence == True):
        time.sleep(0.5)

    try:
        playing_sequence = True
        f = open("sequence" + data["sequence_num"] + ".sequence", "r")
        data = f.read()
        dbug.debug("playing sequence...\n: " + data)
        data = data.replace("\'", "\"")
        data = json.loads(data) 
        for x in range(int(data["loop"])):
            for frame in data['frames']:
                for led in frame['leds']:
                    ls.set_color_grid_pixel_hex(led["x"], led["y"], led["color"])
                    time.sleep(0.002)
                time.sleep(1/int(data["fps"]))

        ls.reset_leds()
    except Exception as e:
        dbug.debug(str(e))
    finally:
        playing_sequence = False

def blank_lightbars(data):
    global playing_sequence

    while(playing_sequence == True):
        time.sleep(0.5)
    try:
        playing_sequence = True
        ls.reset_leds()
    except Exception as e:
        dbug.debug(str(e))
    finally:
        playing_sequence = False

def print_data(data):
    print(data)
