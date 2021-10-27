from entities.activity_ import Activity, ActivityValidator, ActivityValidatorException, ActivityException, DayValidator
from repository.custom_DT_arepo import CustomActivityRepo, RepoException
from repository.custom_DT_prepo import CustomPersonRepo, RepoException
from service.undo import Undo, FunctionCall, Operation, CascadedOperation
from custom_iterable_collection.iterable import gnome_sort, filter
from service.person_service import *
from repository.test_inits import *


class ActivityService:
    """
    Manages ActivityRepo instances, makes the connection between the activity repo and the person repo, validates input
    """

    def __init__(self, activity_validator, activity_repo, people_repo, undo):
        self._arepo = activity_repo
        self._prepo = people_repo
        self._validator = activity_validator
        self._dvalidator = DayValidator()
        self._undo = undo

    def add_activity(self, id, date, starttime, endtime, description, id_pers_list):
        """
        Adds a new activity to the repo after checking the parameters and finding in people repo
        the people with same IDs as the ones from the input
        :param id: The ID of the activity
        :param date: The date of the activity
        :param time: The time of the activity
        :param description: The description of the activity
        :param id_pers_list: list of IDs of people that needs to be checked
        :return:
        """
        self.update_activity_repo()
        pers_list = []
        for id_pers in id_pers_list:
            try:
                pers = self._prepo.get_person_by_id(id_pers).name
            except RepoException:
                continue
            pers_list.append([pers, id_pers])
        activity = Activity(id, date, starttime, endtime, description, pers_list)
        self._validator.validate(activity)
        self._arepo.add_activity(activity)
        undo_fun = FunctionCall(self._arepo.remove_activity, activity)
        redo_fun = FunctionCall(self._arepo.add_activity, activity)
        o = Operation(undo_fun, redo_fun)
        self._undo.record(o)
        # self.update_activity_repo()

    def remove_activity(self, id):
        self.update_activity_repo()
        activity = self._arepo.get_activity_by_id(id)
        self._arepo.remove_activity(activity)
        undo_fun = FunctionCall(self._arepo.add_activity, activity)
        redo_fun = FunctionCall(self._arepo.remove_activity, activity)
        o = Operation(undo_fun, redo_fun)
        self._undo.record(o)
        # self.update_activity_repo()

    def update_activity(self, id, date, starttime, endtime, description, id_pers_list):
        self.update_activity_repo()
        activity = self._arepo.get_activity_by_id(id)
        if activity is None:
            raise ActivityException("wrong input")
        previous_date = activity.date
        previous_starttime = activity.starttime
        previous_endtime = activity.endtime
        previous_description = activity.description
        previous_perslist = activity.perslist
        pers_list = []
        for id_pers in id_pers_list:
            try:
                pers = self._prepo.get_person_by_id(id_pers).name
            except RepoException:
                continue
            pers_list.append([pers, id_pers])
        self._validator.validate(Activity(id, date, starttime, endtime, description, pers_list))
        self._arepo.update_activity(activity, date, starttime, endtime, description, pers_list)
        undo_fun = FunctionCall(self._arepo.update_activity, activity, previous_date, previous_starttime,
                                previous_endtime, previous_description, previous_perslist)
        redo_fun = FunctionCall(self._arepo.update_activity, activity, date, starttime, endtime, description, pers_list)
        o = Operation(undo_fun, redo_fun)
        self._undo.record(o)
        # self.update_activity_repo()

    def __len__(self):
        return len(self._arepo)

    def get_all(self):
        self.update_activity_repo()
        return self._arepo.get_all()

    def update_activity_repo(self):
        activitiez = self._arepo.get_all()
        active_ids = self._prepo.get_ids()
        extra_ops = []
        if not activitiez:
            return None
        for activity in activitiez:
            for lis in activity.perslist:

                if lis[1] not in active_ids:

                    activity.perslist.remove(lis)
                    undo_fun = FunctionCall(activity.perslist.append, lis)
                    redo_fun = FunctionCall(activity.perslist.remove, lis)
                    o = Operation(undo_fun, redo_fun)
                    extra_ops.append(o)
                else:
                    for id in active_ids:
                        if lis[1] == id:
                            if lis[0] != self._prepo.get_person_by_id(id).name:
                                lis[0] = self._prepo.get_person_by_id(id).name

        if self._undo.return_index() > -1:
            if self._undo.normal_op():
                first_fun, second_fun = self._undo.unpack_last_element()
                if first_fun.function_ref() == self._prepo.add_person and second_fun.function_ref() == self._prepo.remove_person:
                    # print('this works')
                    op = Operation(first_fun, second_fun)
                    co = CascadedOperation(op, *extra_ops)
                    self._undo.remove_last_element()
                    self._undo.record(co)

        return None

    """
                --SEARCH--
    """

    def get_activ_by_descr(self, description):
        self.update_activity_repo()
        wanted = []
        for activity in self._arepo.get_all():
            if description in activity.description.lower():
                wanted.append(activity)
            # else:
            #     continue
        if len(wanted) == 0:
            raise ActivityException("Activity with given description not found!")
        return wanted

    def get_activ_by_dt(self, date, starttime):
        self.update_activity_repo()
        wanted = []
        for activity in self._arepo.get_all():
            if date in activity.date.lower():
                if starttime in activity.starttime.lower():
                    wanted.append(activity)
        if len(wanted) == 0:
            raise ActivityException("Activity in the given time and date not found!")
        return wanted

    """
                      --STATISTICS TERRITORY--
    """

    def activities_per_date(self, date):
        self.update_activity_repo()
        self._dvalidator.validate(date)
        filtered = filter(self._arepo.get_all(), lambda activity: activity.date == date)
        self.arrange_dates(filtered)
        return filtered

    def upcoming_activities(self, date):
        """
        Returns a list of activities occurring at the given date and on the dates after it
        :param date:Current date
        :return:
        """
        self.update_activity_repo()
        result = filter(self._arepo.get_all(), lambda activity: activity.compare(date))
        return result

    def activities_with_person(self, id_person, date):
        """
        Returns a list of activities that take place together with a given person sorted in ascending order of their start and end time
        :param id_person: ID of the person
        :param date:
        :return:
        """
        result = self.upcoming_activities(date)
        self.arrange_dates(result)
        update_result = filter(result, lambda activity: self.is_id_in_perslist(activity, id_person))
        return update_result

    @staticmethod
    def is_id_in_perslist(act, id):
        for pers in act.perslist:
            if pers[1] != id:
                continue
            else:
                return True
        return False

    def filter_by_date(self, date, activities_list):
        # TODO: Implement this but using a deep copy of the repository object
        """
        Returns only the activities that take place at a given date  in a random list of activities(not the activity repo)
        :param date: given/current date
        :param activities_list: list of activities that needs to be filtered
        :return:
        """
        one_date_activities = filter(activities_list, lambda activity: activity.date == date)
        return self.arrange_dates(one_date_activities)

    def get_upcoming_dates(self, deit):
        """
        Returns a list of the dates (string format) that are after a given date
        :param deit: given/current date
        :return:
        """
        result = self.upcoming_activities(deit)
        dates = []
        for activity in result:
            if activity.date not in dates:
                dates.append(activity.date)
        return dates

    def calculate_lenght_and_interval(self, activities_list):
        """
        calculates the time in minutes that are occupied by activities for each date in a list of activities
        :param activities_list: list of activities
        :return:
        """
        number_of_acts = len(activities_list)
        busy_minutes = 0
        for i in range(len(activities_list)):
            busy_minutes += activities_list[i].interval()
        return busy_minutes

    def busiest_days(self, date):
        # TODO: Implement this but using gnome sort
        """
        Returns a list of activities sorted in descending order of their time which is occupied by activities after a given date
        :param date: given/current date
        :return:
        """
        upcoming = self.upcoming_activities(date)
        dates = self.get_upcoming_dates(date)
        activities_per_day = []
        for dt in dates:
            apd = self.filter_by_date(dt, upcoming)
            activities_per_day.append(apd)
        gnome_sort(activities_per_day,
                   lambda apd1, apd2: self.calculate_lenght_and_interval(apd1) <= self.calculate_lenght_and_interval(
                       apd2))
        return activities_per_day

    @staticmethod
    def arrange_dates(dates):
        # TODO: Implement this but using gnome sort
        gnome_sort(dates, lambda activity1, activity2: activity1.startminute() >= activity2.startminute())
        gnome_sort(dates, lambda activity1, activity2: activity1.starthour() >= activity2.starthour())
        return dates
