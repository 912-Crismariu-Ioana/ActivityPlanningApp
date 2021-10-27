from entities.person import Person, PersonException
from custom_iterable_collection.iterable import IterableDS


class RepoException(PersonException):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class CustomPersonRepo:
    def __init__(self):
        self._ds = IterableDS()

    def add_person(self, person):
        if person in self._ds:
            raise RepoException("Person with given ID already exists!")
        for pers in self._ds:
            if pers.eq_ph(person):
                raise RepoException("Person with given phone number already exists!")
        self._ds.append(person)

    def remove_person(self, person):
        for i in range(0, len(self._ds)):
            if self._ds[i] == person:
                del self._ds[i]
                break

    def update_person(self, person, name, number):
        if person in self._ds:
            person.name = name
            person.number = number
        else:
            raise RepoException('Person with the given id not found')

    def get_all(self):
        return self._ds.__copy__()

    def get_person_by_id(self, id):
        for person in self._ds:
            if person.id == id:
                return person
        else:
            raise RepoException('Person with the given id not found')

    def get_ids(self):
        id_list = []
        for person in self._ds:
            id_list.append(person.id)
        return id_list

    def __len__(self):
        return len(self._ds)
