from tkinter import *
from tkinter import ttk
import sqlite3
import os
import json
from datetime import datetime as dt
import sys

# Change the directory to the current directory of this file
# In case there are files missing
os.chdir(os.path.abspath(os.path.dirname(__file__)))

# Create a starter class for the app
class Window(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_window()

	# Create the init_window function
	def init_window(self):
		# Change the title of the window
		self.master.title('Student Management')
		self.master.iconname('studentmanagement')

		self.pack(expand=YES, fill=BOTH, padx=10, pady=10)

        # Create a menu instance
		menuBar = Menu(self.master)
		self.master.config(menu=menuBar)

		def makeFileCommandMenu():
			File = Menu(menuBar, tearoff=False)
			File.add_command(label="Open...", underline=0, command=self.open_file)
			File.add_separator()
			File.add_command(label="Exit", underline=0, command=self.client_exit)
			return File
		def makeEditCommandMenu():
			Edit = Menu(menuBar, tearoff=False)
			Edit.add_command(label="Undo", underline=0, command=self.undo_edit)
			Edit.add_separator()
			Edit.add_command(label="Cut", underline=0, command=self.text_cut)
			Edit.add_command(label="Copy", underline=0, command=self.text_copy)
			Edit.add_command(label="Paste", underline=0, command=self.text_paste)
			Edit.add_separator()
			Edit.add_command(label="Clear", underline=0, command=self.client_clean)
			return Edit
		def makeViewCommandMenu():
			View = Menu(menuBar, tearoff=False)
			View.add_command(label="Enter Full Screen", underline=0, command=self.full_screen)
			return View
		def makeHelpCommandMenu():
			Help = Menu(menuBar, tearoff=False)
			Help.add_command(label="View Help", underline=0, command=self.view_help)
			Help.add_separator()
			Help.add_command(label="About Student Management", underline=0, command=self.about)
			return Help

		File = makeFileCommandMenu()
		Edit = makeEditCommandMenu()
		View = makeViewCommandMenu()
		Help = makeHelpCommandMenu()

		menuBar.add_cascade(label="File", menu=File)
		menuBar.add_cascade(label="Edit", menu=Edit)
		menuBar.add_cascade(label="View", menu=View)
		menuBar.add_cascade(label="Help", menu=Help)

		# Create the app header
		Label(self.master, text="Student Management System", font=("Tahoma", 12, "bold")).pack(side=TOP, expand=True)

		data_entry_frame = Frame(self.master)
		data_entry_frame.pack(side=TOP, expand=True, fill=BOTH)

		Label(data_entry_frame, text="First Name: ", font=('Tahoma', 9)).grid(row=0, column=0, padx=(10, 2), pady=(40, 20), sticky=W)
		first_name = Entry(data_entry_frame, font=('Tahoma', 9), width=24, relief=SOLID, borderwidth=1)
		first_name.grid(row=0, column=1, ipady=4, pady=(40, 20), sticky=W)

		Label(data_entry_frame, text="Last Name: ", font=('Tahoma', 9)).grid(row=0, column=2, padx=(25, 2), pady=(40, 20), sticky=W)
		last_name = Entry(data_entry_frame, font=('Tahoma', 9), width=24, relief=SOLID, borderwidth=1)
		last_name.grid(row=0, column=3, ipady=4, pady=(40, 20), sticky=W)

		Label(data_entry_frame, text="Date Of Birth: ", font=('Tahoma', 9)).grid(row=0, column=4, padx=(25, 2), pady=(40, 20), sticky=W)
		e = StringVar()
		dob = Entry(data_entry_frame, textvariable=e, font=('Tahoma', 9), width=24, relief=SOLID, borderwidth=1)
		dob.grid(row=0, column=5, ipady=4, pady=(40, 20), sticky=W)
		e.set("DD-MM-YYYY")

		# Parents information
		Label(data_entry_frame, text="Father's Name: ", font=('Tahoma', 9)).grid(row=1, column=0, padx=(10, 2), pady=(20, 20), sticky=W)
		father_name = Entry(data_entry_frame, font=('Tahoma', 9), width=24, relief=SOLID, borderwidth=1)
		father_name.grid(row=1, column=1, ipady=4, pady=(20, 20), sticky=W)

		Label(data_entry_frame, text="Mother's Name: ", font=('Tahoma', 9)).grid(row=1, column=2, padx=(25, 2), pady=(20, 20), sticky=W)
		mother_name = Entry(data_entry_frame, font=('Tahoma', 9), width=24, relief=SOLID, borderwidth=1)
		mother_name.grid(row=1, column=3, ipady=4, pady=(20, 20), sticky=W)

		# Major information
		Label(data_entry_frame, text="Major: ", font=('Tahoma', 9)).grid(row=2, column=0, padx=(10, 2), sticky=W)
		major = Entry(data_entry_frame, font=('Tahoma', 9), width=24, relief=SOLID, borderwidth=1)
		major.grid(row=2, column=1, ipady=4, pady=(20, 20), sticky=W)

		# Year information
		Label(data_entry_frame, text="Year: ", font=('Tahoma', 9)).grid(row=2, column=2, padx=(25, 2), sticky=W)
		n = StringVar()
		years_choosen = ttk.Combobox(data_entry_frame, font=('Tahoma', 9), textvariable=n, width=21)
		years_choosen['values'] = (1,2,3,4)
		years_choosen.grid(row=2, column=3, padx=2, ipady=4, sticky=W)
		# Set the default value for years_choosen
		years_choosen.current(0)

		# Location information
		Label(data_entry_frame, text="Country: ", font=('Tahoma', 9)).grid(row=3, column=0, padx=(10, 2), sticky=W)
		country = Entry(data_entry_frame, font=('Tahoma', 9), width=24, relief=SOLID, borderwidth=1)
		country.grid(row=3, column=1, ipady=4, pady=(20, 20), sticky=W)

		Label(data_entry_frame, text="State: ", font=('Tahoma', 9)).grid(row=3, column=2, padx=(25, 2), sticky=W)
		state = Entry(data_entry_frame, font=('Tahoma', 9), width=24, relief=SOLID, borderwidth=1)
		state.grid(row=3, column=3, ipady=4, pady=(20, 20), sticky=W)

		Label(data_entry_frame, text="Description: ", font=('Tahoma', 9)).grid(row=4, column=0, padx=(10, 2), sticky=W)
		description = Entry(data_entry_frame, font=('Tahoma', 9), width=24, relief=SOLID, borderwidth=1)
		description.grid(row=4, column=4, ipady=4, pady=(20, 20), sticky=W)

	def open_file(self):
		pass
	def client_exit(self):
		sys.exit(0)
	def undo_edit(self):
		pass
	def text_cut(self):
		pass
	def text_copy(self):
		pass
	def text_paste(self):
		pass
	def client_clean(self):
		pass
	def full_screen(self):
		pass
	def view_help(self):
		pass
	def about(self):
		pass


	# Create the choose year function
	def choose_year(self, entry):
		print("you study in %s" % entry)


# Create window
root = Tk()
WIDTH = 890
HEIGHT = 500
POS_X = int(root.winfo_screenwidth()/2-WIDTH/2)
POS_Y = int(root.winfo_screenheight()/2-HEIGHT/2)-50
root.geometry(f'{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}')
root.minsize(WIDTH, HEIGHT)

app = Window(root)
root.mainloop()
