import lightscript_v2 as ls
import time
import simplejson as json
import os

def test_command(data):
    ls.mode_3(255, 0, 0)

def update_lights(data):
    for led in data['leds']:
        ls.set_color_grid_pixel_hex(led["x"], led["y"], led["color"])
        time.sleep(0.002)

def load_sequence(data):
    os.remove("sequence"+sequence_num+".sequence")
    sequence_num = data["sequence_num"]
    f = open("sequence"+sequence_num+".sequence", "w")
    f.write(str(data))
    

def play_sequence(data):
    
    f = open("sequence" + data["sequence_num"] + ".sequence", "r")
    data = f.read()
    print(data)
    data = data.replace("\'", "\"")
    data = json.loads(data) 
    for x in range(int(data["loop"])):
        for frame in data['frames']:
            for led in frame['leds']:
                ls.set_color_grid_pixel_hex(led["x"], led["y"], led["color"])
                time.sleep(0.001)
            time.sleep(1/int(data["fps"]))
                                                                                                                              
def blank_lightbars(data):
    ls.reset_leds()

def print_data(data):
    print(data)
