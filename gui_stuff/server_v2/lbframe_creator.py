from Tkinter import *
import kiosk_main as kiosk
import sys
from copy import deepcopy

#color must be hex string without prefixes. e.g must be aaaaaa or ffffff
def send_frame_to_lightbars():
	message = app.frame_to_json()
	kiosk.serv.send_to_all(message)	
	
def send_sequence_to_lightbars():
	message = app.sequence_to_json(5, 5, 0)
	#f = open("file.txt", "w")
	f.write(message)
	kiosk.serv.send_to_all(message)
	print("-------------")
	print(message)
	print("------------")

def blank_lightbars():
	message = '{"command": "blanklightbars"}'
	kiosk.serv.send_to_all(message)

class App():

	def __init__(self, master):
		self.frame = Frame(master)
		self.frame.pack()

		self.frame_rows = 6
		self.frame_columns = 12
		self.frames = []
		self.current_frame_index = 0
		
		self.current_frame = []
		self.current_frame_canvases = []

		self.quit_button = Button(self.frame, text="QUIT", fg="red", command=self.quit)
		self.quit_button.grid(row=0, column=0)

		self.frame_json_btn = Button(self.frame, text="To Lightbars", command=send_frame_to_lightbars)		
		self.frame_json_btn.grid(row=0, column=1)
		
		self.blank_lightbars_btn = Button(self.frame, text="Blank lightbars", command=blank_lightbars)
		self.blank_lightbars_btn.grid(row=0, column=2)

		self.change_current_frame_entry = Entry(self.frame)
		self.change_current_frame_entry.insert(0, "0")
		self.change_current_frame_entry.grid(row=0, column=3)
		self.change_current_frame_btn = Button(self.frame, text="Change Frame", command=self.change_frame)
		self.change_current_frame_btn.grid(row=0, column=4)
		
		self.new_frame_btn = Button(self.frame, text="Create new frame", command=self.create_new_frame)
		self.new_frame_btn.grid(row=0, column=5)

		self.print_all_btn = Button(self.frame, text="Print All", command=self.print_all)		
		self.print_all_btn.grid(row=0, column=6)	
		
		self.send_sequence_btn = Button(self.frame, text="Send Sequence", command=send_sequence_to_lightbars)
		self.send_sequence_btn.grid(row=0, column=7)	
		
		self.default_color = "#000000"	
		self.selected_color = self.default_color

		self.current_color_lbl = Label(self.frame, text="Current Color")
		self.current_color_lbl.grid(row=1, column=0)

		self.current_color_entry = Entry(self.frame)
		self.current_color_entry.insert(0, self.selected_color)
		self.current_color_entry.grid(row=1, column=1)	
		self.current_color_btn = Button(self.frame, text="Update Color", command=self.update_selected_color)	
		self.current_color_btn.grid(row=1, column=2)			
		self.frame_section = Frame(master)
		self.frame_section.pack()
		#scrollbar = Scrollbar(self.frame_section)
		
		self.set_up_grid()		
		self.create_first_frame()
		self.display_current_frame()
	
	def quit(self):
		kiosk.serv.quit()
		self.frame.quit()

	def copy_frame_to_array(self):
		print("Copying Frame: ", self.change_current_frame_entry.get())
		print("To: ", str(self.current_frame_index))
		self.frames[self.current_frame_index] = deepcopy(self.current_frame)

	def copy_from_array_to_current_frame(self):
		self.current_frame = deepcopy(self.frames[self.current_frame_index])


	def print_frame(self, frame_index):
		frame = self.frames[frame_index]

		for y in range(self.frame_rows):
			for x in range(self.frame_columns):
				#print(frame[y][x])
				print()
	
	def print_all(self):
		for y in range(self.frame_rows):
			for x in range(self.frame_columns):
				for f in self.frames:
					sys.stdout.write(f[y][x] + " ")
				print()
				
				

	def update_selected_color(self):
		old = self.selected_color
		self.selected_color = self.current_color_entry.get()
		print("Updated selected color. Was: ", old, " Now: ", self.selected_color)
		
	def change_frame(self):
		selected_frame = int(self.change_current_frame_entry.get())
		self.copy_frame_to_array()
		
		print("Current Frame: ", self.current_frame_index)
		print("Selected Frame: ", selected_frame)
		print("frames in array: ", len(self.frames))

		if(selected_frame > len(self.frames) - 1):
			print("Frame does not exist")
			return
		elif(selected_frame < 0):
			print("frame does not exist")
			return
		
		self.current_frame_index = selected_frame
		self.copy_from_array_to_current_frame()
		
		self.change_current_frame_entry.delete(0, END)
		self.change_current_frame_entry.insert(0, str(self.current_frame_index))
		
		self.display_current_frame()
		self.copy_frame_to_array()

	def create_new_frame(self):
		self.copy_frame_to_array()
		self.create_first_frame()
		self.current_frame_index = len(self.frames) - 1

		self.change_current_frame_entry.delete(0, END)
		self.change_current_frame_entry.insert(0,str(self.current_frame_index))
		self.change_frame()

	#fps = frames per second, loop = T/F, sequence_num = reference_number on client
	def sequence_to_json(self, fps, loop, sequence_num):
		json = '{"command":"loadsequence", "fps": "'+str(fps)+'", "loop":"'+str(loop)+'",'
		json += '"frames":['
		for f_index in range(len(self.frames)):
			frame = self.frames[f_index]
			
			json += '{"leds": ['
			for y in range(self.frame_rows):
				for x in range(self.frame_columns):
					json += '{"x":"'+str(x)+'", "y":"'+str(y)+'", "color": "'+frame[y][x][1:]+'"}'
					if(y == self.frame_rows - 1 and x == self.frame_columns -1):
						print()
					else:
						json += ", "
			json += ']}'
			if(f_index != len(self.frames) -1):
				json += ", "
		json += ']}'
		return(json)

	def frame_to_json(self):
		frame = self.frames[self.current_frame_index]

		json = '{"command":"updateleds", "leds":['
		for y in range(self.frame_rows):
			for x in range(self.frame_columns):
				json += '{"x":"'+str(x)+'", "y":"'+str(y)+'", "color": "'+frame[y][x][1:]+'"}'
				if(y == self.frame_rows - 1 and x == self.frame_columns -1):
					print()
				else:
					json += ", "
		json += ']}'
		return json
				

	def update_color(self, event):
		grid_info = event.widget.grid_info()
		x = grid_info["row"]
		y = grid_info["column"]
		event.widget.config(background=self.selected_color)
		print("Updated to: ", self.selected_color)
		print(x, y)
		self.copy_frame_to_array()
		self.current_frame[int(y)][int(x)] = self.selected_color
		
	def create_first_frame(self):
		self.current_frame = []
		for y in range(self.frame_rows):
			row = []
			for x in range(self.frame_columns):
				row.append(self.default_color)
				
			self.current_frame.append(row)
		self.frames.append(self.current_frame)
	
	def set_up_grid(self):
		for y in range(self.frame_rows):
			row = []
			for x in range(self.frame_columns):
				canvas = Canvas(self.frame_section,background=self.default_color, name="displayCanvas"+str(y)+str(x),width=100, height=50)
				canvas.grid(column=y, row=x)
				canvas.bind("<Button-1>", self.update_color)
				row.append(canvas)
			self.current_frame_canvases.append(row)

	def display_current_frame(self):
		for y in range(self.frame_rows):
			for x in range(self.frame_columns):
				print(self.current_frame[y][x])	
				self.current_frame_canvases[y][x].config(background=self.current_frame[y][x])

root = Tk()

app = App(root)
root.mainloop()
root.destroy()

