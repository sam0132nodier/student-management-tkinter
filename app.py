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

		# Clear the text in the entry field
		def clear_entry(self):
			e.set("")

		def open_file():
			pass
		def client_exit(self):
			sys.exit(0)
		def undo_edit():
			pass
		def text_cut():
			pass
		def text_copy():
			pass
		def text_paste():
			pass
		def client_clean():
			pass
		def view_students():
			pass
		def view_help():
			pass
		def about():
			pass


		# Get all forms data and save them in the database
		def save():
			student_first_name = first_name.get()
			student_last_name = last_name.get()
			student_dob = dob.get()
			student_father_name = father_name.get()
			student_mother_name = mother_name.get()
			student_major = major.get()
			student_years_choosen = years_choosen.get()
			student_country = country.get()
			student_state = state.get()
			# student_description = "Nothing"
			student_description = description.get('1.0', END)

			if(
			   	(
				    str(student_first_name) != "" and
				   	str(student_last_name) != "" and
				   	str(student_dob) != "" and
				   	str(student_father_name) != "" and
				   	str(student_mother_name) != "" and
				   	str(student_major) != "" and
				   	str(student_years_choosen) != "" and
				   	str(student_country) != "" and
				   	str(student_state) != "" and
				   	str(student_description != "")
				) and (
					student_years_choosen.isdigit() and
					int(student_years_choosen) <= 4 and
					len(str(student_description)) <= 500
				)
			   	):
				first_name["text"] = ""
				last_name["text"] = ""
				dob["text"] = ""
				father_name["text"] = ""
				mother_name["text"] = ""
				major["text"] = ""
				years_choosen["text"] = ""
				country["text"] = ""
				state["text"] = ""
				description["value"] = ""
				print('student_first_name: ', student_first_name)
				print('student_last_name: ', student_last_name)
				print('student_dob: ', student_dob)
				print('student_father_name: ', student_father_name)
				print('student_mother_name: ', student_mother_name)
				print('student_major: ', student_major)
				print('student_years_choosen: ', student_years_choosen)
				print('student_country: ', student_country)
				print('student_state: ', student_state)
				print('student_description: ', student_description)


		# Create the choose year function
		def choose_year(self, entry):
			print("you study in %s" % entry)

		# Change the title of the window
		self.master.title('Student Management')
		self.master.iconname('studentmanagement')

		self.pack(expand=YES, fill=BOTH, padx=10, pady=10)

        # Create a menu instance
		menuBar = Menu(self.master)
		self.master.config(menu=menuBar)

		def makeFileCommandMenu():
			File = Menu(menuBar, tearoff=False)
			File.add_command(label="Open...", underline=0, command=open_file)
			File.add_separator()
			File.add_command(label="Exit", underline=0, command=client_exit)
			return File
		def makeEditCommandMenu():
			Edit = Menu(menuBar, tearoff=False)
			Edit.add_command(label="Undo", underline=0, command=undo_edit)
			Edit.add_separator()
			Edit.add_command(label="Cut", underline=0, command=text_cut)
			Edit.add_command(label="Copy", underline=0, command=text_copy)
			Edit.add_command(label="Paste", underline=0, command=text_paste)
			Edit.add_separator()
			Edit.add_command(label="Clear", underline=0, command=client_clean)
			return Edit
		def makeViewCommandMenu():
			View = Menu(menuBar, tearoff=False)
			View.add_command(label="View Students", underline=0, command=view_students)
			return View
		def makeHelpCommandMenu():
			Help = Menu(menuBar, tearoff=False)
			Help.add_command(label="View Help", underline=0, command=view_help)
			Help.add_separator()
			Help.add_command(label="About Student Management", underline=0, command=about)
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
		dob.bind('<FocusIn>', clear_entry)
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
		# Set the default value for years_choosen
		years_choosen.current(1)
		years_choosen.grid(row=2, column=3, padx=2, ipady=4, sticky=W)

		# Location information
		Label(data_entry_frame, text="Country: ", font=('Tahoma', 9)).grid(row=3, column=0, padx=(10, 2), sticky=W)
		country = Entry(data_entry_frame, font=('Tahoma', 9), width=24, relief=SOLID, borderwidth=1)
		country.grid(row=3, column=1, ipady=4, pady=(20, 20), sticky=W)

		Label(data_entry_frame, text="State: ", font=('Tahoma', 9)).grid(row=3, column=2, padx=(25, 2), sticky=W)
		state = Entry(data_entry_frame, font=('Tahoma', 9), width=24, relief=SOLID, borderwidth=1)
		state.grid(row=3, column=3, ipady=4, pady=(20, 20), sticky=W)

		# General description and background
		Label(data_entry_frame, text="Description: ", font=('Tahoma', 9)).grid(row=4, column=0, padx=(10, 2), sticky=W)
		description = Text(data_entry_frame, font=('Tahoma', 9), width=109, height=5, relief=SOLID, borderwidth=1)
		description.grid(row=4, column=1, columnspan=5, ipady=4, pady=(20, 20), sticky=W)

		# Command buttons
		close_btn = Button(data_entry_frame, text='Close', width=12, height=2, relief=SOLID, borderwidth=1)
		close_btn.grid(row=5, column=5, pady=(10, 10), sticky=W)
		close_btn.bind("<Button-1>", client_exit)

		# Save data button
		save_btn = Button(data_entry_frame, text='Save', width=12, height=2, relief=SOLID, borderwidth=1, command=save)
		save_btn.grid(row=5, column=5, pady=(10, 10), sticky=E)


# Create window
root = Tk()
WIDTH = 890
HEIGHT = 550
POS_X = int(root.winfo_screenwidth()/2-WIDTH/2)
POS_Y = int(root.winfo_screenheight()/2-HEIGHT/2)-50
root.geometry(f'{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}')
# root.minsize(WIDTH, HEIGHT)
root.resizable(0,0)
app = Window(root)
root.mainloop()
