from tkinter import *
from tkinter import ttk
import sqlite3
import os
import json
from datetime import datetime as dt
import sys
import re
import uuid
from student_management.view_students_dialog import MyDialog as ViewStudents
from student_management.add_students_dialog import MyDialog as AddStudents
from student_management.about_dialog import MyDialog as About
from student_management.search_students_dialog import MyDialog as Search
from tkinter import filedialog
from tkinter import messagebox
import json
import webbrowser

# Change the directory to the current directory of this file
# In case there are files missing
os.chdir(os.path.abspath(os.path.dirname(__file__)))

# Table name
TABLE = 'students'

# Connect to the database
DATABASE = 'db.sqlite3'
connection = sqlite3.connect(DATABASE)


# Create a starter class for the app
class Window(Frame):
	def __init__(self, master=None):
		"""Creates the main application window and calls a function that initialize the window components.
		"""
		Frame.__init__(self, master)
		self.master = master
		self.init_window()

	# Create the init_window function
	def init_window(self):
		"""Creates the application frame and adds the necessary components with their functionality"""
		# Clear the text in the entry field
		def clear_entry(self):
			e.set("")

		def open_file():
			try:
				file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")], initialdir = os.getcwd())
				with open(file_path, 'r') as json_file:
					data_dict = json.load(json_file)

				all_data = []
				display_data = []

				for i in range(len(data_dict)):
					all_data.append([(
					    data_dict[i]["student_id"],
					    data_dict[i]["first_name"],
					    data_dict[i]["last_name"],
					    data_dict[i]["dob"],
					    data_dict[i]["father_name"],
					    data_dict[i]["mother_name"],
					    data_dict[i]["major"],
					    data_dict[i]["years_choosen"],
					    data_dict[i]["country"],
					    data_dict[i]["state"],
					    data_dict[i]["description"]
					) if not (data_dict[i][key] in ('', None)) and key in ("student_id", "first_name", "last_name", "major", "years_choosen", "country", "state", "description") else None for key in data_dict[i].keys()][0])
					display_data.append([(
					    data_dict[i]["student_id"],
					    data_dict[i]["first_name"],
					    data_dict[i]["last_name"],
					    data_dict[i]["major"],
					    data_dict[i]["years_choosen"],
					    data_dict[i]["country"],
					    data_dict[i]["state"],
					    data_dict[i]["description"]
					) if not (data_dict[i][key] in ('', None)) and key in ("student_id", "first_name", "last_name", "major", "years_choosen", "country", "state", "description") else None for key in data_dict[i].keys()][0])
				complete_data = all_data
				minified_data = display_data
				add_students = AddStudents(self.master, complete_data, minified_data, title="Add Students")
			except json.decoder.JSONDecodeError as error:
				messagebox.showerror(title="JSON Problem", message=str(error))
			except FileNotFoundError:
				pass

		def client_exit(event):
			sys.exit(0)
		def inputs_clean():
			# Clear all inputs
			first_name.delete(0, END)
			last_name.delete(0, END)
			dob.delete(0, END)
			father_name.delete(0, END)
			mother_name.delete(0, END)
			major.delete(0, END)
			years_choosen.delete(0, END)
			country.delete(0, END)
			state.delete(0, END)
			description.delete('1.0', END)

		def search_students():
			search = Search(self.master, title="Search students")
		def view_students():
			try:
				cursor = connection.cursor()
				data = []
				for row in cursor.execute("SELECT student_id, first_name, last_name, major, years_choosen, country, state, description FROM students"):
				    data.append(row)
				view_students = ViewStudents(self.master, data, title="Students List")
			except Exception as error:
				messagebox.showerror(title='Fetching Error', message=str(error))
		def view_help():
			try:
				url = 'https://github.com/sam0132nodier/student-management-tkinter/blob/master/README.md'
				webbrowser.open(url)
			except Exception as error:
				messagebox.showerror(title='Fetching Error', message=str(error))
		def about():
			about = About(self.master, title="About Student Management")


		# Get all forms data and save them in the database
		def save():
			if(
			   	(
				    str(first_name.get()) != "" and
				   	str(last_name.get()) != "" and
				   	str(dob.get()) != "" and
				   	str(father_name.get()) != "" and
				   	str(mother_name.get()) != "" and
				   	str(major.get()) != "" and
				   	str(years_choosen.get()) != "" and
				   	str(country.get()) != "" and
				   	str(state.get()) != "" and
				   	str(description.get('1.0', END) != "")
				) and (
					years_choosen.get().isdigit() and
					int(years_choosen.get()) <= 4 and
					len(str(description.get('1.0', END))) <= 500
				) and (
					re.match(r'(0[1-9]|[12][0-9]|3[01]|[1-9])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d', dob.get())
				)
			   	):
				# Grab all the form's data

				student_first_name = first_name.get()
				student_last_name = last_name.get()
				student_dob = dob.get()
				student_father_name = father_name.get()
				student_mother_name = mother_name.get()
				student_major = major.get()
				student_years_choosen = years_choosen.get()
				student_country = country.get()
				student_state = state.get()
				student_description = description.get('1.0', END)

				# Clear all inputs
				first_name.delete(0, END)
				last_name.delete(0, END)
				dob.delete(0, END)
				father_name.delete(0, END)
				mother_name.delete(0, END)
				major.delete(0, END)
				years_choosen.delete(0, END)
				country.delete(0, END)
				state.delete(0, END)
				description.delete('1.0', END)

				# Create a student list which have tuple as data to be inserted
				student = (
					f"{str(uuid.uuid4()).replace('-', '')}",
					student_first_name,
					student_last_name,
					student_dob,
					student_father_name,
					student_mother_name,
					student_major,
					student_years_choosen,
					student_country,
					student_state,
					student_description,
				)

				try:
					# Create a cursor to use while inserting the data into the database
					cursor = connection.cursor()

					# Create student table if it doesn't exist
					cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE} (student_id TEXT PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, dob TEXT NOT NULL, father_name TEXT NOT NULL, mother_name TEXT NOT NULL, major TEXT NOT NULL, years_choosen INTEGER NOT NULL, country TEXT NOT NULL, state TEXT NOT NULL, description TEXT NOT NULL)")

					# Insert the data in the database
					cursor.execute(f'INSERT INTO {TABLE} VALUES (?,?,?,?,?,?,?,?,?,?,?)', student)

					# Commit the changes
					connection.commit()

					# Close the connection so that we can access the data base anywhere else
					connection.close()

					messagebox.showinfor(title='Data Added', message="Student Data Added Successfully!")
				except Exception as error:
					messagebox.showerror(title='Database Error', message=str(error))


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
			Edit.add_command(label="Clear", underline=0, command=inputs_clean)
			return Edit
		def makeViewCommandMenu():
			View = Menu(menuBar, tearoff=False)
			View.add_command(label="Search...", underline=0, command=search_students)
			View.add_separator()
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
		self.n = StringVar()
		years_choosen = ttk.Combobox(data_entry_frame, font=('Tahoma', 9), textvariable=self.n, width=21)
		years_choosen['values'] = (1,2,3,4)
		# Set the default value for years_choosen
		years_choosen.current(0)
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
		close_btn = Button(data_entry_frame, text='Close', width=12, height=2, relief=SOLID, borderwidth=1, default=ACTIVE)
		close_btn.grid(row=5, column=5, pady=(10, 10), sticky=W)
		close_btn.bind("<Button-1>", client_exit)

		# Save data button
		save_btn = Button(data_entry_frame, text='Save', width=12, height=2, relief=SOLID, borderwidth=1, command=save)
		save_btn.grid(row=5, column=5, pady=(10, 10), sticky=E)


def student():
	"""Create the root for application and set's its dimensions

	This function is run in the __main__.py file to run the application.
	"""
	root = Tk()
	WIDTH = 890
	HEIGHT = 550
	POS_X = int(root.winfo_screenwidth()/2-WIDTH/2)
	POS_Y = int(root.winfo_screenheight()/2-HEIGHT/2)-50
	root.geometry(f'{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}')
	root.resizable(0,0)
	app = Window(root)
	root.mainloop()
