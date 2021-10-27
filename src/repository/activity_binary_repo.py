from repository.custom_DT_arepo import CustomActivityRepo
import pickle


class ActivityBinaryRepo(CustomActivityRepo):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self.read_bin_file()

    def add_activity(self, activity):
        super().add_activity(activity)
        self.write_bin_file()

    def remove_activity(self, activity):
        super().remove_activity(activity)
        self.write_bin_file()

    def update_activity(self, activity, date, starttime, endtime, description, pers_list):
        super().update_activity(activity,date,starttime,endtime,description,pers_list)
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
