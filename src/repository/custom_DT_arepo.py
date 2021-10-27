from entities.activity_ import Activity, ActivityException, ActivityValidator
from custom_iterable_collection.iterable import IterableDS


class RepoException(ActivityException):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class CustomActivityRepo:
    """
    Stores activity instances
    """

    def __init__(self):
        self._ds = IterableDS()

    def add_activity(self, activity):
        """
        Checks if an activity instance has the same ID or takes place at the same time as
        the activities already stored in the repo.
        If not, it is added to the repo.
        :param activity: A new activity instance
        :return:
        """
        if activity in self._ds:
            raise RepoException("Activity with given ID already exists!")
        for act in self._ds:
            if act.concomitent(activity):
                raise RepoException("Activity in the given time and date and with the same people already exists!")
        self._ds.append(activity)

    def update_activity(self, activity, date, starttime, endtime, description, pers_list):
        if activity in self._ds:
            activity.date = date
            activity.starttime = starttime
            activity.endtime = endtime
            activity.description = description
            activity.perslist = pers_list
            return activity
        else:
            raise RepoException('Person with the given id not found')

    def remove_activity(self, activity):
        for i in range(0, len(self._ds)):
            if self._ds[i] == activity:
                del self._ds[i]
                break

    def __len__(self):
        return len(self._ds)

    def get_all(self):
        return self._ds.__copy__()

    def get_activity_by_id(self, id):
        for act in self._ds:
            if act.id == id:
                return act
