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

        self.protocol("WM_DELETE_WINDOW", self.ok)

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
            Displays the hardcoded data that display information about this
            student management program.
        """

        frame = Frame(master, borderwidth=4, relief='flat')
        frame.pack(fill='x', expand=True)

        canvas = Canvas(frame, width=650, height=100)
        canvas.create_text(325, 25, text='Student Management Application', fill='#0077FF', font=('Arial', 20, 'bold'))
        canvas.create_line(20, 70, 630, 70)
        canvas.pack()

        text_frame = Frame(master, borderwidth=4, relief='flat')
        text_frame.pack(fill='both', expand=True)
        Label(text_frame, text='Student Management Version 1.0', font=('Arial', 11)).pack(side=TOP, pady=3)
        Label(text_frame, text='This application can be used for any purpose whether free or commercial', font=('Arial', 11)).pack(side=TOP, pady=3)
        Label(text_frame, text='© 2020 proprgrmmr.', font=('Arial', 11)).pack(side=TOP, pady=3)


    def buttonbox(self):
        box = Frame(self)

        ok_button = Button(box, text='OK', width=12, height=2, relief='solid', borderwidth=1, command=self.ok, default=ACTIVE)
        ok_button.pack(side=RIGHT, padx=5, pady=(10, 10))

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.ok)

        box.pack(fill=X, expand=True)

    def ok(self, event=None):
        # Put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()