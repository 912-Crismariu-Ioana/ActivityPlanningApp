from repository.custom_DT_arepo import CustomActivityRepo
from entities.activity_ import Activity


class ActivityTextFileRepository(CustomActivityRepo):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load()

    def _load(self):
        f = open(self._file_name, 'rt')
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.split(';')
            if len(line) == 6:
                pers_list_unpack = line[5].replace('[', '').replace(']', '').replace('\n', '').split(',')
                pers_list = []
                i = 0
                while i < len(pers_list_unpack) - 1:
                    person = [pers_list_unpack[i].replace("'", '').strip(),
                              pers_list_unpack[i + 1].replace("'", '').strip()]
                    pers_list.append(person)
                    i = i + 2
                super().add_activity(Activity(line[0], line[1], line[2], line[3], line[4], pers_list))

    def add_activity(self, activity):
        super().add_activity(activity)
        self._save()

    def update_activity(self, activity, date, starttime, endtime, description, pers_list):
        super().update_activity(activity, date, starttime, endtime, description, pers_list)
        self._save()

    def remove_activity(self, activity):
        super().remove_activity(activity)
        self._save()

    def get_all(self):
        super().get_all()
        self._save()
        return self._ds[:]

    def _save(self):
        f = open(self._file_name, 'wt')
        for activity in self._ds:
            line = str(activity.id) + ';' + str(activity.date) + ';' + str(activity.starttime) + ';' + str(
                activity.endtime) + ';' + str(activity.description) + ';' + str(activity.perslist)
            f.write(line)
            f.write('\n')
        f.close()
