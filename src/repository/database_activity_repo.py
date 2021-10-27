from repository.custom_DT_arepo import CustomActivityRepo, Activity
import sqlite3


class DatabaseActivityRepo(CustomActivityRepo):
    def __init__(self, connection="activities_sample_files/activities.db"):
        super().__init__()
        self._connection = sqlite3.connect(connection)
        self._cursor = self._connection.cursor()
        self._load()

    def create_table(self):
        self._cursor.execute('''CREATE TABLE ACTIVITIES (
        ID TEXT NOT NULL, DATE TEXT NOT NULL, STARTTIME TEXT NOT NULL, ENDTIME TEXT NOT NULL, DESCRIPTION TEXT NOT NULL, PERSLIST TEXT NOT NULL )''')

    def add_activity(self, activity):
        super().add_activity(activity)
        id = activity.id
        date = activity.date
        starttime = activity.starttime
        endtime = activity.endtime
        description = activity.description
        perslist = str(activity.perslist)
        with self._connection:
            self._cursor.execute(
                "INSERT INTO ACTIVITIES (ID, DATE, STARTTIME, ENDTIME,DESCRIPTION,PERSLIST) VALUES (?, ?, ?, ?, ?, ?)",
                (id, date, starttime, endtime, description, perslist))

    def remove_activity(self, activity):
        super().remove_activity(activity)
        id_act = activity.id
        with self._connection:
            self._cursor.execute("DELETE from ACTIVITIES where ID = :aidi", {'aidi': id_act})

    def update_activity(self, activity, date, starttime, endtime, description, pers_list):
        super().update_activity(activity, date, starttime, endtime, description, pers_list)
        id = activity.id
        with self._connection:
            self._cursor.execute('''UPDATE ACTIVITIES SET DATE = :date WHERE ID = :id''', {"id": id, "date": date})
            self._cursor.execute('''UPDATE ACTIVITIES SET STARTTIME = :starttime WHERE ID = :id''',
                                 {"id": id, "starttime": starttime})
            self._cursor.execute('''UPDATE ACTIVITIES SET ENDTIME = :endtime WHERE ID = :id''',
                                 {"id": id, "endtime": endtime})
            self._cursor.execute('''UPDATE ACTIVITIES SET DESCRIPTION = :description WHERE ID = :id''',
                                 {"id": id, "description": description})
            self._cursor.execute('''UPDATE ACTIVITIES SET PERSLIST = :perslist WHERE ID = :id''',
                                 {"id": id, "perslist": str(pers_list)})

    def get_all(self):
        super().get_all()
        self._connection.commit()
        return self._ds.__copy__()

    def _load(self):
        self._cursor = self._connection.execute(
            "SELECT ID, DATE, STARTTIME, ENDTIME, DESCRIPTION, PERSLIST from ACTIVITIES")
        for row in self._cursor:
            id = row[0]
            date = row[1]
            starttime = row[2]
            endtime = row[3]
            description = row[4]
            pers_list_unpack = row[5].replace('[', '').replace(']', '').replace('\n', '').split(',')
            pers_list = []
            i = 0
            while i < len(pers_list_unpack) - 1:
                person = [pers_list_unpack[i].replace("'", '').strip(),
                          pers_list_unpack[i + 1].replace("'", '').strip()]
                pers_list.append(person)
                i = i + 2
            self._ds.append(Activity(id, date, starttime, endtime, description, pers_list))
