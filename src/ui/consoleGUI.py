from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

from ui.console import Console, PersonException, ActivityException


class ConsoleGUI(Console):
    def __init__(self, p_service, a_service, undo, win):
        super().__init__(p_service, a_service, undo)

        self._mainwin = win
        self._mainwin.title("Activity Planner")
        self._mainwin.geometry('700x700')
        self._frame = Frame(cursor='heart', width='500', height='200')

    def butttons(self):
        button1 = Button(self._mainwin, text="List all people", fg='red', command=self.list_ppl_gui)
        button1a = Button(self._mainwin, text="List people alphabetical", fg='red',
                          command=self.list_ppl_alphabetical_gui)
        button2 = Button(self._mainwin, text="List all activities", fg='blue', command=self.list_activities_gui)
        button3 = Button(self._mainwin, text="Add a person", fg='red', command=self.add_person)
        button4 = Button(self._mainwin, text="Add an activity", fg='blue', command=self.add_activity)
        button5 = Button(self._mainwin, text="Update a person", fg='red', command=self.update_person)
        button6 = Button(self._mainwin, text="Update an activity", fg='blue', command=self.update_activity)
        button7 = Button(self._mainwin, text="Remove a person", fg='red', command=self.remove_person)
        button8 = Button(self._mainwin, text="Remove an activity", fg='blue', command=self.remove_activity)
        button9 = Button(self._mainwin, text="Search for a person", fg='red', command=self.search_person)
        button10 = Button(self._mainwin, text="Search for an activity", fg='blue', command=self.search_activity)
        button11 = Button(self._mainwin, text="Activities per date", fg='purple', command=self.activs_per_day)
        button12 = Button(self._mainwin, text="Activities with person", fg='purple', command=self.activs_with_person)
        button13 = Button(self._mainwin, text="Busiest days", fg='purple', command=self.busiest_dayz)
        button14 = Button(self._mainwin, text="Clear", fg='orange', command=self.clear)
        button15 = Button(self._mainwin, text="Undo", fg='green', command=self.undo)
        button16 = Button(self._mainwin, text="Redo", fg='green', command=self.redo)
        button1.pack()
        button1a.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        button5.pack()
        button6.pack()
        button7.pack()
        button8.pack()
        button9.pack()
        button10.pack()
        button11.pack()
        button12.pack()
        button13.pack()
        button14.pack()
        button15.pack()
        button16.pack()

    def list_ppl_gui(self):
        self._frame.pack()
        self.clear()
        scroll_bar = Scrollbar(self._frame)
        scroll_bar.pack(side=RIGHT, fill=Y)
        scroll_barx = Scrollbar(self._frame, orient='horizontal')
        scroll_barx.pack(side=BOTTOM, fill=X)
        mylist = Listbox(self._frame, width='500', height='200', yscrollcommand=scroll_bar.set,
                         xscrollcommand=scroll_barx.set)
        for person in self._pservice.get_all():
            mylist.insert(END, str(person))
        mylist.pack()
        scroll_bar.config(command=mylist.yview)
        scroll_barx.config(command=mylist.xview)

    def list_ppl_alphabetical_gui(self):
        self._frame.pack()
        self.clear()
        scroll_bar = Scrollbar(self._frame)
        scroll_bar.pack(side=RIGHT, fill=Y)
        scroll_barx = Scrollbar(self._frame, orient='horizontal')
        scroll_barx.pack(side=BOTTOM, fill=X)
        mylist = Listbox(self._frame, width='500', height='200', yscrollcommand=scroll_bar.set,
                         xscrollcommand=scroll_barx.set)
        for person in self._pservice.sort_in_alphabetical_order():
            mylist.insert(END, str(person))
        mylist.pack()
        scroll_bar.config(command=mylist.yview)
        scroll_barx.config(command=mylist.xview)

    def list_activities_gui(self):
        self._frame.pack()
        self.clear()
        scroll_bar = Scrollbar(self._frame)
        scroll_bar.pack(side=RIGHT, fill=Y)
        scroll_barx = Scrollbar(self._frame, orient='horizontal')
        scroll_barx.pack(side=BOTTOM, fill=X)
        mylist = Listbox(self._frame, width='500', height='200', yscrollcommand=scroll_bar.set,
                         xscrollcommand=scroll_barx.set)
        try:
            for activity in self._aservice.get_all():
                mylist.insert(END, str(activity))
        except ValueError:
            mylist.insert(END, "List is empty!")
        mylist.pack()
        scroll_bar.config(command=mylist.yview)
        scroll_barx.config(command=mylist.xview)

    def clear(self):
        for child in self._frame.winfo_children():
            child.destroy()

    def add_person(self):
        self._frame.pack()
        id = simpledialog.askstring(title='ID', prompt="Enter ID:")
        name = simpledialog.askstring(title='Name', prompt="Enter Name:")
        number = simpledialog.askstring(title='Number', prompt="Enter Number:")
        try:
            self._pservice.add_person(id, name, number)
        except PersonException as pe:
            messagebox.showerror(str(pe))

    def add_activity(self):
        self._frame.pack()
        id = simpledialog.askstring(title='ID', prompt="Enter ID:")
        date = simpledialog.askstring(title='Date', prompt="Enter Date:")
        starttime = simpledialog.askstring(title='Start Time', prompt="Enter start time:")
        endtime = simpledialog.askstring(title='End Time', prompt="Enter end time:")
        description = simpledialog.askstring(title='End Description', prompt="Enter description:")
        done = False
        person_list = []
        while not done:
            person = simpledialog.askstring(title='Add person', prompt="Enter ID of person to do the activity with:")
            if person == 'done':
                done = True
            if person in person_list:
                messagebox.showerror('Duplicate ID!')
            person_list.append(person)

        try:
            self._aservice.add_activity(id, date, starttime, endtime, description, person_list)
        except ActivityException as ae:
            messagebox.showerror(str(ae))
        except ValueError as ve:
            messagebox.showerror(str(ve))

    def remove_person(self):
        self._frame.pack()
        id = simpledialog.askstring(title='ID', prompt="Enter ID:")
        try:
            self._pservice.remove_person(id)
        except PersonException as pe:
            messagebox.showerror(str(pe))

    def remove_activity(self):
        self._frame.pack()
        id = simpledialog.askstring(title='ID', prompt="Enter ID:")
        try:
            self._aservice.remove_activity(id)
        except ActivityException as ae:
            messagebox.showerror(str(ae))

    def update_person(self):
        self._frame.pack()
        id = simpledialog.askstring(title='ID', prompt="Enter ID:")
        name = simpledialog.askstring(title='Name', prompt="Update Name:")
        number = simpledialog.askstring(title='Number', prompt="Update Number:")
        try:
            self._pservice.update_person(id, name, number)
        except PersonException as pe:
            messagebox.showerror(str(pe))

    def update_activity(self):
        self._frame.pack()
        id = simpledialog.askstring(title='ID', prompt="Enter ID:")
        date = simpledialog.askstring(title='Date', prompt="Update Date:")
        starttime = simpledialog.askstring(title='Start Time', prompt="Update start time:")
        endtime = simpledialog.askstring(title='End Time', prompt="Update end time:")
        description = simpledialog.askstring(title='End Description', prompt="Update description:")
        done = False
        person_list = []
        while not done:
            person = simpledialog.askstring(title='Add person', prompt="Update ID of person to do the activity with:")
            if person == 'done':
                done = True
            if person in person_list:
                messagebox.showerror('Duplicate ID!')
            person_list.append(person)

        try:
            self._aservice.update_activity(id, date, starttime, endtime, description, person_list)
        except ActivityException as ae:
            messagebox.showerror(str(ae))
        except ValueError as ve:
            messagebox.showerror(str(ve))
        except AttributeError as ae:
            messagebox.showerror(str(ae))

    def search_person(self):
        self._frame.pack()
        scroll_bar = Scrollbar(self._frame)
        scroll_bar.pack(side=RIGHT, fill=Y)
        scroll_barx = Scrollbar(self._frame, orient='horizontal')
        scroll_barx.pack(side=BOTTOM, fill=X)
        mylist = Listbox(self._frame, width='500', height='200', yscrollcommand=scroll_bar.set,
                         xscrollcommand=scroll_barx.set)
        mylist.pack()
        scroll_bar.config(command=mylist.yview)
        scroll_barx.config(command=mylist.xview)
        name_or_nr = simpledialog.askstring(title='Search', prompt="Search by name or number?")
        if name_or_nr == 'name':
            try:
                name = simpledialog.askstring(title='Search', prompt="Enter name: ").strip().lower()
                for person in self._pservice.search_by_name(name):
                    mylist.insert(END, str(person))
            except PersonException as pe:
                messagebox.showerror(str(pe))
        elif name_or_nr == 'number':
            try:
                number = simpledialog.askstring(title='Search', prompt="Enter number: ").strip().lower()
                for person in self._pservice.search_by_number(number):
                    mylist.insert(END, str(person))
            except PersonException as pe:
                messagebox.showerror(str(pe))
        else:
            messagebox.showerror('Bad input! :(')

    def search_activity(self):
        self._frame.pack()
        scroll_bar = Scrollbar(self._frame)
        scroll_bar.pack(side=RIGHT, fill=Y)
        scroll_barx = Scrollbar(self._frame, orient='horizontal')
        scroll_barx.pack(side=BOTTOM, fill=X)
        mylist = Listbox(self._frame, width='500', height='200', yscrollcommand=scroll_bar.set,
                         xscrollcommand=scroll_barx.set)
        mylist.pack()
        scroll_bar.config(command=mylist.yview)
        scroll_barx.config(command=mylist.xview)
        dt_or_dscr = simpledialog.askstring(title='Search', prompt="Search by date and time or description?")
        if dt_or_dscr == 'date and time':
            try:
                date = simpledialog.askstring(title='Search', prompt="Enter date: ").strip().lower()
                starttime = simpledialog.askstring(title='Search', prompt="Enter start time: ").strip().lower()
                for activity in self._aservice.get_activ_by_dt(date, starttime):
                    mylist.insert(END, str(activity))
            except ActivityException as ae:
                messagebox.showerror(str(ae))
        elif dt_or_dscr == 'description':
            try:
                descr = simpledialog.askstring(title='Search', prompt="Enter description: ").strip().lower()
                for activity in self._aservice.get_activ_by_descr(descr):
                    mylist.insert(END, str(activity))
            except ActivityException as ae:
                messagebox.showerror(str(ae))

        else:
            messagebox.showerror('Bad input! :(')

    def activs_per_day(self):
        scroll_bar = Scrollbar(self._frame)
        scroll_bar.pack(side=RIGHT, fill=Y)
        scroll_barx = Scrollbar(self._frame, orient='horizontal')
        scroll_barx.pack(side=BOTTOM, fill=X)
        mylist = Listbox(self._frame, width='500', height='200', yscrollcommand=scroll_bar.set,
                         xscrollcommand=scroll_barx.set)
        mylist.pack()
        scroll_bar.config(command=mylist.yview)
        scroll_barx.config(command=mylist.xview)
        self._frame.pack()
        date = simpledialog.askstring(title='Statistics', prompt="Enter date: ").strip().lower()
        for activity in self._aservice.activities_per_date(date):
            mylist.insert(END, str(activity))

    def activs_with_person(self):
        scroll_bar = Scrollbar(self._frame)
        scroll_bar.pack(side=RIGHT, fill=Y)
        scroll_barx = Scrollbar(self._frame, orient='horizontal')
        scroll_barx.pack(side=BOTTOM, fill=X)
        mylist = Listbox(self._frame, width='500', height='200', yscrollcommand=scroll_bar.set,
                         xscrollcommand=scroll_barx.set)
        mylist.pack()
        scroll_bar.config(command=mylist.yview)
        scroll_barx.config(command=mylist.xview)
        self._frame.pack()
        date = simpledialog.askstring(title='Statistics', prompt="Enter date: ").strip().lower()
        id = simpledialog.askstring(title='Statistics', prompt="Enter ID of the person: ").strip().lower()
        for activity in self._aservice.activities_with_person(id, date):
            mylist.insert(END, str(activity))

    def busiest_dayz(self):
        scroll_bar = Scrollbar(self._frame)
        scroll_bar.pack(side=RIGHT, fill=Y)
        scroll_barx = Scrollbar(self._frame, orient='horizontal')
        scroll_barx.pack(side=BOTTOM, fill=X)
        mylist = Listbox(self._frame, width='500', height='200', yscrollcommand=scroll_bar.set,
                         xscrollcommand=scroll_barx.set)
        mylist.pack()
        scroll_bar.config(command=mylist.yview)
        scroll_barx.config(command=mylist.xview)
        self._frame.pack()
        date = simpledialog.askstring(title='Statistics', prompt="Enter date: ").strip().lower()
        for activity_list in self._aservice.busiest_days(date):
            for activity in activity_list:
                mylist.insert(END, str(activity))

    def undo(self):
        try:
            self._undo.undo()
        except ValueError:
            messagebox.showerror("No more undos")

    def redo(self):
        try:
            self._undo.redo()
        except ValueError:
            messagebox.showerror("No more redos")
