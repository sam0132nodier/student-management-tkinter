import sqlite3

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

# Table name
TABLE = 'students'

# Database info
DATABASE = 'db.sqlite3'
connection = sqlite3.connect(DATABASE)

class MyDialog(simpledialog.Dialog):
    """The Custom dialog box that is used to display student's data"""
    def __init__(self, parent, complete_data, minified_data, title = None):
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
        self.complete_data = complete_data
        self.minified_data = minified_data

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

        frame = Frame(master, borderwidth=4, relief='flat')
        frame.pack(fill='both', expand=True)

        data_list = self.minified_data

        total_rows = len(data_list)
        total_columns = len(data_list[0])

        header_cols = ["Student ID", "First Name", "Last Name", "Major", "Year", "Country", "State", "Description"]
        for header_col in range(len(header_cols)):
            header_label = Label(frame, text=header_cols[header_col][:20], width=15, font=('Tahoma', 9, 'bold'), bg="#FFFFFF", relief="solid", borderwidth=1)
            header_label.grid(row=0, column=header_col, ipady=4, sticky=W)
        for row in range(total_rows):
            for col in range(total_columns):
                label = Label(frame, text=str(data_list[row][col])[:20], width=17, font=('Tahoma', 9), bg="#FFFFFF", relief="solid", borderwidth=1)
                label.grid(row=row+1, column=col, ipadx=0.5, ipady=4, sticky=W)


    def buttonbox(self):
        box = Frame(self)

        add_button = Button(box, text='Add', width=12, height=2, relief='solid', borderwidth=1, command=self.add, default=ACTIVE)
        add_button.pack(side=RIGHT, padx=5, pady=(10, 10))

        cancel_button = Button(box, text='Cancel', width=12, height=2, relief='solid', borderwidth=1, command=self.cancel)
        cancel_button.pack(side=RIGHT, padx=5, pady=(10, 10))

        self.bind("<Return>", self.add)
        self.bind("<Escape>", self.cancel)

        box.pack(fill=X, expand=True)


    def add(self, event=None):
        try:
            for tuple in self.complete_data:
                # Create a cursor to use while inserting the data into the database
                cursor = connection.cursor()

                # Create student table if it doesn't exist
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE} (student_id TEXT PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, dob TEXT NOT NULL, father_name TEXT NOT NULL, mother_name TEXT NOT NULL, major TEXT NOT NULL, years_choosen INTEGER NOT NULL, country TEXT NOT NULL, state TEXT NOT NULL, description TEXT NOT NULL)")

                # Insert the data in the database
                cursor.execute(f'INSERT INTO {TABLE} VALUES (?,?,?,?,?,?,?,?,?,?,?)', tuple)

                # Commit the changes
                connection.commit()

            messagebox.showinfo(title="Students Data", message="Students data added successfully")
            if self.parent is not None:
                self.parent.focus_set()
            self.destroy()
        except Exception as error:
            messagebox.showerror(title='Database Problem', message=str(error))
            if self.parent is not None:
                self.parent.focus_set()
            self.destroy()

    def cancel(self, event=None):
        # Put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()