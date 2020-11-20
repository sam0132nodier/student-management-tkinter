import os
from tkinter import *
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Change the directory to the current directory of this file
# In case there are files missing
os.chdir(os.path.abspath(os.path.dirname(__file__)))

# Connect to the database
DATABASE = 'db.sqlite3'
connection = sqlite3.connect(DATABASE)

class MyDialog(simpledialog.Dialog):
	"""The Custom dialog box that is used to display student's data"""
	def __init__(self, parent, title = None):
		'''Initialize a dialog.

		Arguments:

			parent -- a parent window (the application window)

			title -- the dialog title
		'''
		Toplevel.__init__(self, parent)

		self.withdraw() # remain invisible for now
		# If the master is not viewable, don't
		# make the child transient, or else it
		# would be opened withdrawn
		if parent.winfo_viewable():
			self.transient(parent)

		if title:
			self.title(title)

		self.parent = parent

		self.result = None

		body = Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5, pady=5)

		self.buttonbox()

		if not self.initial_focus:
			self.initial_focus = self

		self.protocol("WM_DELETE_WINDOW", self.cancel)

		if self.parent is not None:
			self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
									  parent.winfo_rooty()+50))

		self.deiconify() # become visible now

		self.initial_focus.focus_set()

		# wait for window to appear on screen before calling grab_set
		self.wait_visibility()
		self.grab_set()
		self.wait_window(self)

	def body(self, master):
		"""
			data = <list> the data that we use to create the table of student's data
			dict_key = <sequence> (Dictionary, Key) to associate with user input
		"""

		# Create the search_data function to do all the work required
		# To get the students' information as we need
		def search_data(event):
			if(str(category.get()) != "" and str(category.get()) != "Search using..." and str(search_entry.get()) != ""):
				search_category = category.get()
				if search_category == 'Student ID':
					column = 'student_id'
				elif search_category == 'First Name':
					column = 'first_name'
				elif search_category == 'Last Name':
					column = 'last_name'
				elif search_category == 'Major':
					column = 'major'
				elif search_category == 'Year':
					column = 'years_choosen'
				elif search_category == 'Country':
					column = 'country'
				elif search_category == 'State':
					column = 'state'

				search_term = search_entry.get()

				try:
					data = []
					cursor = connection.cursor()
					for row in cursor.execute(f"SELECT student_id, first_name, last_name, major, years_choosen, country, state, description FROM students WHERE {column} = '{search_term}'"):
						data.append(row)

					for widget in results_frame.winfo_children():
						print(widget)
						widget.destroy()

					data_list = data

					total_rows = len(data_list)
					total_columns = len(data_list[0])


					header_cols = ["Student ID", "First Name", "Last Name", "Major", "Year", "Country", "State", "Description"]
					for header_col in range(len(header_cols)):
						header_label = Label(results_frame, text=header_cols[header_col][:20], width=15, font=('Tahoma', 9, 'bold'), bg="#FFFFFF", relief="solid", borderwidth=1)
						header_label.grid(row=0, column=header_col, ipady=4, sticky=W)
					for row in range(total_rows):
						for col in range(total_columns):
							data_label = Label(results_frame, text=str(data_list[row][col])[:20], width=17, font=('Tahoma', 9), bg="#FFFFFF", relief="solid", borderwidth=1)
							data_label.grid(row=row+1, column=col, ipadx=0.5, ipady=4, sticky=W)

				except Exception as error:
					messagebox.showerror(title='Fetching Error', message=str(error))

		frame = Frame(master, borderwidth=4, relief='flat')
		frame.pack(fill='x', expand=True)

		# Create a frame to display results on
		results_frame = Frame(master, borderwidth=4, relief='flat')
		results_frame.pack(fill='both', expand=True)

		# Create the window header
		Label(frame, text="Search students", font=('Tahoma', 12, 'bold')).grid(row=0, column=0, columnspan=4, pady=(5, 20))

		# Create search label, combobox, entry and button

		Label(frame, text="Search: ", font=('Tahoma', 12)).grid(row=1, column=0, padx=(10,2), sticky=W)
		self.n = StringVar()
		category = ttk.Combobox(frame, font=('Tahoma', 9), textvariable=self.n, width=15)
		category['values'] = ('Search using...', 'Student ID', 'First Name', 'Last Name', 'Major', 'Year', 'Country', 'State')
		# Set the default value for the categories
		category.current(0)
		category.grid(row=1, column=1, padx=(2, 20), ipady=4, sticky=W)

		search_entry = Entry(frame, font=('Tahoma', 9), width=27, relief=SOLID, borderwidth=1)
		search_entry.grid(row=1, column=2, padx=(2, 20), ipady=5, sticky=W)

		search_btn = Button(frame, text='Search', width=12, height=2, relief=SOLID, borderwidth=1, default=ACTIVE)
		search_btn.grid(row=1, column=3, padx=(20, 0), sticky=W)
		search_btn.bind("<Button-1>", search_data)
		search_btn.bind("<Return>", search_data)

	def buttonbox(self):
		box = Frame(self)

		ok_button = Button(box, text='OK', width=12, height=2, relief=SOLID, borderwidth=1, command=self.ok)
		ok_button.pack(side=RIGHT, padx=5, pady=(10, 10))


		box.pack(fill=X, expand=True)

	def ok(self, event=None):
		# Put focus back to the parent window
		if self.parent is not None:
			self.parent.focus_set()
		self.destroy()
