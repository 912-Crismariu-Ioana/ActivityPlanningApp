from entities.activity_ import ActivityException
from entities.person import PersonException


class Console:
    def __init__(self, person_service, activity_service, undo):
        self._pservice = person_service
        self._aservice = activity_service
        self._undo = undo



    @staticmethod
    def menu():
        print("Choose an action:")
        print("1.List all people")
        print("2.List all activities")
        print("3.Add a person")
        print("4.Add an activity")
        print("5.Update a person")
        print("6.Update an activity")
        print("7.Remove a person")
        print("8.Remove an activity")
        print("9.Search for a person")
        print("10.Search for an activity")
        print("11.Activities per date")
        print("12.Activities with person")
        print("13.Busiest days")
        print("14.Undo")
        print("15.Redo")
        print("16.Exit")

    def console(self):
        ppldict = {'3': self.add_person_ui, '5':self.update_person_ui, '7': self.remove_person_ui, '1': self.list_person_ui, '9':self.search_person_ui}
        actdict = {'4': self.add_activity_ui, '6': self.update_activity_ui, '8': self.remove_activity_ui,'2': self.list_activities_ui, '10':self.search_activity_ui, '11': self.activities_per_day_ui, '12': self.activities_with_person_ui, '13':self.busiest_days_ui, '14': self.undo, '15':self.redo}
        done = False
        while not done:
            try:
                self.menu()
                command = str(input("Enter a number:")).strip()
                if command in ppldict:
                    ppldict[command]()
                elif command in actdict:
                    actdict[command]()
                elif command == '16':
                    print("Have a nice day! :)")
                    done = True
                else:
                    print("Bad input! :(")
                print(len(self._pservice))
            except PersonException as pe:
                print(str(pe))
                print(len(self._pservice))
            except ActivityException as ae:
                print(str(ae))
            except ValueError as ve:
                print(str(ve))

    def add_person_ui(self):
        id = str(input("Enter an id: "))
        name = str(input("Enter a name: "))
        number = str(input("Enter a phone number: "))
        self._pservice.add_person(id,name,number)

    def remove_person_ui(self):
        id = str(input("Enter the id of the person you want to remove: "))
        self._pservice.remove_person(id)

    def update_person_ui(self):
        id = str(input("Enter the id of the person you want to update: "))
        name = str(input("Update name: "))
        number = str(input("Update number: "))
        self._pservice.update_person(id, name, number)


    def list_person_ui(self):
        people = self._pservice.get_all()
        if len(people) == 0:
            raise ValueError("No people here! Are you that lonely?")
        for peep in people:
            print(peep)

    def add_activity_ui(self):
        id = str(input("Enter id: "))
        date = str(input("Enter a date: "))
        starttime = str(input("Enter a start time: "))
        endtime = str(input("Enter an end time: "))
        description = str(input("Enter a description: "))
        id_pers_list = []
        done = False
        while not done:
            id_pers = str(input("Enter the ids of the people you want to do the activity with: "))
            if id_pers in id_pers_list:
                raise ValueError("Duplicate ID!")
            if id_pers == 'done':
                done = True
            id_pers_list.append(id_pers)
        self._aservice.add_activity(id,date, starttime, endtime, description,id_pers_list)

    def remove_activity_ui(self):
        id = str(input("Enter the id of the activity you want to remove: "))
        self._aservice.remove_activity(id)

    def update_activity_ui(self):
        id = str(input("Enter the id of the person you want to update: ")).strip()
        date = str(input("Update date: ")).strip()
        starttime = str(input("Update start time: ")).strip()
        endtime = str(input("Update start time: ")).strip()
        description = str(input("Update description: ")).strip()
        id_pers_list = []
        done = False
        while not done:
            id_pers = str(input("ID of the person you want to do the activity with: ")).strip()
            if id_pers == 'done':
                done = True
            if id_pers in id_pers_list:
                raise ValueError("Duplicate ID!")
            else:
                id_pers_list.append(id_pers)
        self._aservice.update_activity(id, date, starttime, endtime, description,id_pers_list)


    def list_activities_ui(self):
        activities = self._aservice.get_all()
        if len(activities) == 0:
            raise ValueError("No activities here!")
        for activity in activities:
            print(activity)

    def search_person_ui(self):
        name_or_number = input("Search by name or number? ").strip().lower()
        if name_or_number == 'name':
            name = input("Enter name: ").strip().lower()
            for person in self._pservice.search_by_name(name):
                print(person)
        elif name_or_number == 'number':
            number = input("Enter phone number: ").strip().lower()
            for person in self._pservice.search_by_number(number):
                print(person)
        else:
            print("Bad input! :(")

    def search_activity_ui(self):
        date_time_descr = input("Search by date and time or description? ").strip().lower()
        if date_time_descr == 'date and time':
            date = input("Enter date: ").strip().lower()
            time = input("Enter start time: ").strip().lower()
            for activity in self._aservice.get_activ_by_dt(date,time):
                print(activity)

        elif date_time_descr == 'description':
            description = input("Enter description: ").strip().lower()
            for activity in self._aservice.get_activ_by_descr(description):
                print(activity)

    def activities_per_day_ui(self):
        date = input("Enter a date: ").strip().lower()
        for activity in self._aservice.activities_per_date(date):
            print(activity)

    def activities_with_person_ui(self):
        date = input("Enter today's date: ").strip().lower()
        person_id = input("Enter the ID of the person: ").strip().lower()
        for activity in self._aservice.activities_with_person(person_id, date):
            print(activity)

    def busiest_days_ui(self):
        date = input("Enter today's date: ").strip().lower()
        for activity_list in self._aservice.busiest_days(date):
            for activity in activity_list:
                print(activity)

    def undo(self):
        try:
            self._undo.undo()
        except ValueError as ve:
            print(str(ve))



    def redo(self):
        try:
            self._undo.redo()
        except ValueError as ve:
            print(str(ve))






