from repository.custom_DT_prepo import CustomPersonRepo
import pickle


class PersonBinaryRepo(CustomPersonRepo):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self.read_bin_file()

    def add_person(self, person):
        super().add_person(person)
        self.write_bin_file()

    def remove_person(self, person):
        super().remove_person(person)
        self.write_bin_file()

    def update_person(self, person, name, number):
        super().update_person(person, name, number)
        self.write_bin_file()

    def write_bin_file(self):
        f = open(self._file_name, 'wb')
        pickle.dump(self._ds, f)
        f.close()

    def get_all(self):
        super().get_all()
        self.write_bin_file()
        return self._ds[:]

    def read_bin_file(self):
        result = []
        try:
            f = open(self._file_name, 'rb')
            self._ds = pickle.load(f)
            f.close()
            return self._ds
        except EOFError:
            return result

        except IOError as e:
            raise e
