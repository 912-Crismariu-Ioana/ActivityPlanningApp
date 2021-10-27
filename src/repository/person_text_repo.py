from entities.person import Person
from repository.custom_DT_prepo import CustomPersonRepo


class PersonTextFileRepository(CustomPersonRepo):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = str(file_name)
        self._load()

    def _load(self):
        f = open(self._file_name, 'rt')
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.split(';')
            if len(line) == 3:
                super().add_person(Person(line[0], line[1], line[2].strip('\n')))

    def add_person(self, person):
        super().add_person(person)
        self._save()

    def update_person(self, person, name, number):
        super().update_person(person, name, number)
        self._save()

    def remove_person(self, person):
        super().remove_person(person)
        self._save()

    def get_all(self):
        super().get_all()
        self._save()
        return self._ds[:]

    def _save(self):
        f = open(self._file_name, 'wt')
        for person in self._ds:
            line = str(person.id) + ';' + str(person.name) + ';' + str(person.number)
            f.write(line)
            f.write('\n')
        f.close()
