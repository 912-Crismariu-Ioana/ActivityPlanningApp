from repository.custom_DT_prepo import CustomPersonRepo, Person
import sqlite3


class DatabasePeopleRepo(CustomPersonRepo):
    def __init__(self, connection= "people_sample_files/people.db"):
        super().__init__()
        self._connection = sqlite3.connect(connection)
        self._cursor = self._connection.cursor()
        self._load()

    def create_table(self):
        self._cursor.execute('''CREATE TABLE PEOPLE (
        ID TEXT, NAME TEXT, NUMBER TEXT)''')

    def add_person(self, person):
        super().add_person(person)
        id = person.id
        name = person.name
        number = person.number
        with self._connection:
            self._cursor.execute("INSERT INTO PEOPLE (ID, NAME, NUMBER) VALUES (?, ?, ?)",
                             (id,name, number))

    def remove_person(self,person):
        super().remove_person(person)
        id_pers = person.id
        with self._connection:
            self._cursor.execute("DELETE from PEOPLE where ID = :aidi",{'aidi':id_pers})

    def update_person(self,person,name,number):
        super().update_person(person,name,number)
        id = person.id
        with self._connection:
            self._cursor.execute('''UPDATE PEOPLE SET NAME = :name  WHERE ID = :id''',{'name': name,'id': id})
            self._cursor.execute('''UPDATE PEOPLE SET NUMBER = :number  WHERE ID = :id''', {'number': number, 'id': id})

    def get_all(self):
        super().get_all()
        self._connection.commit()
        return self._ds.__copy__()


    def _load(self):
        self._cursor = self._connection.execute("SELECT ID, NAME, NUMBER from PEOPLE")
        for row in self._cursor:
            id = row[0]
            name = row[1]
            number = row[2]
            self._ds.append(Person(id,name,number))












