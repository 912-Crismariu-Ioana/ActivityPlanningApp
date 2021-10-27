import json
from repository.custom_DT_prepo import CustomPersonRepo
from entities.person import Person


class PersonJsonRepo(CustomPersonRepo):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load()

    def _load(self):
        f = open(self._file_name, )
        people_dict = json.load(f)
        for person in people_dict['people']:
            self._ds.append(Person(person['id'], person['name'], person['number']))
        f.close()

    def add_person(self, person):
        super().add_person(person)
        self._save()

    def remove_person(self, person):
        super().remove_person(person)
        self._save()

    def update_person(self, person, name, number):
        super().remove_person(person)
        self._save()

    def get_all(self):
        super().get_all()
        self._save()
        return self._ds[:]

    def _save(self):
        with open(self._file_name) as json_file:
            people_dict = json.load(json_file)
            temp = people_dict['people']
            del temp[:]
            for person in self._ds:
                new_person = {"id": str(person.id),
                              "name": str(person.name),
                              "number": str(person.number)
                              }
                temp.append(new_person)
        with open(self._file_name, 'w') as f:
            json.dump(people_dict, f, indent=4)
