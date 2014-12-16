from Tkinter import *

import sys

class App():

	def __init__(self, master):
		frame = Frame(master)
		frame.pack()

		self.frame_rows = 6
		self.frame_columns = 12
		self.frames = []
		self.frame_num = 0
		
		self.current_frame = []

		self.quit_button = Button(frame, text="QUIT", fg="red", command=frame.quit)
		self.quit_button.grid(row=0, column=0)

		self.selected_color = "#000000"	
		self.current_color_lbl = Label(frame, text="Current Color")
		self.current_color_lbl.grid(row=1, column=0)

		self.current_color_entry = Entry(frame)
		self.current_color_entry.insert(0, self.selected_color)
		self.current_color_entry.grid(row=1, column=1)	
		self.current_color_btn = Button(frame, text="Update Color", command=self.update_selected_color)	
		self.current_color_btn.grid(row=1, column=2)			
		self.frame_section = Frame(master)
		self.frame_section.pack()

		self.create_first_frame()
		self.display_current_frame()
	
	def copy_frame_to_array(self):
		self.current

	def update_selected_color(self):
		old = self.selected_color
		self.selected_color = self.current_color_entry.get()
		print("Updated selected color. Was: ", old, " Now: ", self.selected_color)

	def update_color(self, event):
		grid_info = event.widget.grid_info()
		x = grid_info["row"]
		y = grid_info["column"]
		event.widget.config(background=self.selected_color)
		print("Updated to: ", self.selected_color)
		print(x, y)
		self.current_frame[int(x)][int(y)] = self.selected_color
		
	def create_first_frame(self):
		for y in range(self.frame_rows):
			row = []
			for x in range(self.frame_columns):
				row.append(self.selected_color)
				
			self.current_frame.append(row)
		

	def display_current_frame(self):
		for y in range(self.frame_rows):
			for x in range(self.frame_columns):
				canvas = Canvas(self.frame_section,background=self.selected_color, name="displayCanvas"+str(y)+str(x),width=100, height=100)
				canvas.grid(column=y, row=x)
				
				canvas.bind("<Button-1>", self.update_color)
				l = Label(self.frame_section, text=str(self.current_frame[y][x]))
				l.grid(column=y, row=x)
				sys.stdout.write(str(x))
			print()

root = Tk()

app = App(root)
root.mainloop()
root.destroy()
