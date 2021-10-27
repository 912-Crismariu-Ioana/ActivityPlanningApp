import json
from repository.custom_DT_arepo import CustomActivityRepo
from entities.activity_ import Activity


class ActivityJsonRepo(CustomActivityRepo):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load()

    def _load(self):
        f = open(self._file_name, )
        activity_dict = json.load(f)
        for activity in activity_dict['activities']:
            self._ds.append(Activity(activity['id'], activity['date'], activity['start time'], activity['end time'],
                                     activity['description'], activity['person list']))
        f.close()

    def add_activity(self, activity):
        super().add_activity(activity)
        self._save()

    def remove_activity(self, activity):
        super().remove_activity(activity)
        self._save()

    def update_activity(self, activity, date, starttime, endtime, description, pers_list):
        super().update_activity(activity, date, starttime, endtime, description, pers_list)
        self._save()

    def get_all(self):
        super().get_all()
        self._save()
        return self._ds[:]

    def _save(self):
        with open(self._file_name) as json_file:
            people_dict = json.load(json_file)
            temp = people_dict['activities']
            del temp[:]
            for activity in self._ds:
                new_activity = {
                    "id": str(activity.id),
                    "date": str(activity.date),
                    "start time": str(activity.starttime),
                    "end time": str(activity.endtime),
                    "description": str(activity.description),
                    "person list": activity.perslist
                }
                temp.append(new_activity)
        with open(self._file_name, 'w') as f:
            json.dump(people_dict, f, indent=4)
