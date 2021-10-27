from entities.person import Person, PersonValidator, Person
from repository.custom_DT_prepo import CustomPersonRepo, PersonException, RepoException
from service.undo import Undo, FunctionCall, Operation
from custom_iterable_collection.iterable import gnome_sort, greater_than


class PersonService:
    """
    Manages person repo instances, validates input
    """

    def __init__(self, person_repo, person_validator, undo):
        self._repo = person_repo
        self._validator = person_validator
        self._undo = undo

    def add_person(self, id, name, number):
        """
        Adds a new person to the person repo instance after validating the parameters
        :param id: ID of the person instance
        :param name: Name of the person instance
        :param number: Phone number of the person instance
        :return:
        """
        person = Person(id, name, number)
        self._validator.validate(person)
        self._repo.add_person(person)
        undo_fun = FunctionCall(self._repo.remove_person, person)
        redo_fun = FunctionCall(self._repo.add_person, person)
        o = Operation(undo_fun, redo_fun)
        self._undo.record(o)

    def remove_person(self, id):
        person = self._repo.get_person_by_id(id)
        self._repo.remove_person(person)
        undo_fun = FunctionCall(self._repo.add_person, person)
        redo_fun = FunctionCall(self._repo.remove_person, person)
        o = Operation(undo_fun, redo_fun)
        self._undo.record(o)

    def update_person(self, id, name, number):
        person = self._repo.get_person_by_id(id)
        if person is None:
            raise PersonException
        previous_name = person.name
        previous_number = person.number
        self._validator.validate(Person(id, name, number))
        self._repo.update_person(person, name, number)
        undo_fun = FunctionCall(self._repo.update_person, person, previous_name, previous_number)
        redo_fun = FunctionCall(self._repo.update_person, person, name, number)
        o = Operation(undo_fun, redo_fun)
        self._undo.record(o)

    def search_by_name(self, name):
        wanted = []
        for person in self._repo.get_all():
            if name in person.name.lower():
                wanted.append(person)
            # else:
            #     continue
        if len(wanted) == 0:
            raise PersonException("Person with that name not found")
        return wanted

    def search_by_number(self, number):
        wanted_nrs = []
        for person in self._repo.get_all():
            if number in person.number.lower():
                wanted_nrs.append(person)
            # else:
            #     continue
        if len(wanted_nrs) == 0:
            raise PersonException("Person with that number not found")
        return wanted_nrs

    def __len__(self):
        return len(self._repo)

    def get_all(self):
        return self._repo.get_all()

    def sort_in_alphabetical_order(self):
        sorted = self._repo.get_all()
        gnome_sort(sorted, lambda person1, person2: greater_than(person1.name, person2.name))
        return sorted
