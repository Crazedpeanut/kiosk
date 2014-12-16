import kiosk_client_network as kiosk_network
import lightscript_v2 as ls
import time

def print_data(self, data):
    print(data)

def update_lights(self, data):
    print("-------------------------------")
    for led in data['leds']:
        ls.set_color_grid_pixel_hex(led["x"], led["y"], led["color"])
        time.sleep(0.002)

def load_sequence(self, data):
    print("received sequence")

    while(True):

        for frame in data['frames']:
            for led in frame['leds']:
                ls.set_color_grid_pixel_hex(led["x"], led["y"], led["color"])
                time.sleep(0.001)
            time.sleep(1/int(data["fps"]))
            
def blank_lightbars(self, data):
    ls.reset_leds()

command_list = {'loadsequence': load_sequence,'printdata' : print_data, "updateleds": update_lights, "blanklightbars":blank_lightbars}
serv = kiosk_network.start_client( command_list)
serv.run()
