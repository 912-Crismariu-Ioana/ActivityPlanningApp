class ActivityException(Exception):
    def __init__(self, msg):
        super().__init__(self, msg)


class ActivityValidatorException(ActivityException):
    """
    Receives the list of errors from ActivityValidator and prints it nicely
    """

    def __init__(self, error_list):
        self._errors = error_list

    def __str__(self):
        result = ''
        for er in self._errors:
            result += er
            result += '\n'
        return result


class DayValidator:
    @staticmethod
    def validate(date):
        errors = []
        if len(date) != 10:
            errors.append('Not a valid date!')
        if not (date[0:2]).isdigit() or not (date[3:5]).isdigit() or not (date[6:11]).isdigit():
            errors.append('Not a valid date!')
        if int(date[0:2]) > 31 or int(date[3:5]) > 12:
            errors.append('Not a valid date!')
        if len(errors) > 0:
            raise ActivityValidatorException(errors)


class ActivityValidator:
    """
    Checks the params of a new activity instance and makes a list of errors
    """

    @staticmethod
    def validate(activity):
        errors = []
        if len(activity.id) == 0 or activity.id == '':
            errors.append('ID should contain at least a character!')
        if not activity.id.isdigit():
            errors.append('ID should be made up of integers!')
        if len(activity.date) != 10:
            errors.append('Not a valid date!')
        if not (activity.date[0:2]).isdigit() or not (activity.date[3:5]).isdigit() or not (
        activity.date[6:11]).isdigit():
            errors.append('Not a valid date!')
        if int(activity.date[0:2]) > 31 or int(activity.date[3:5]) > 12:
            errors.append('Not a valid date!')
        if len(activity.starttime) != 5:
            errors.append('Not a valid time!')
        if not activity.starttime[0:2].isdigit() or not activity.starttime[3:6]:
            errors.append('Not a valid time!')
        if int(activity.starttime[0:2]) > 23 or int(activity.starttime[3:5]) > 59:
            errors.append('Not a valid time!')
        if len(activity.endtime) != 5:
            errors.append('Not a valid time!')
        if not activity.endtime[0:2].isdigit() or not activity.endtime[3:6]:
            errors.append('Not a valid time!')
        if int(activity.endtime[0:2]) > 23 or int(activity.endtime[3:5]) > 59:
            errors.append('Not a valid time!')
        if int(activity.starttime[0:2]) > int(activity.endtime[0:2]):
            errors.append('Not a valid time interval!')
        if int(activity.starttime[0:2]) == int(activity.endtime[0:2]) and int(activity.starttime[3:5]) >= int(
                activity.endtime[3:5]):
            errors.append('Not a valid time interval!')
        if len(activity.description) == 0 or activity.description == '':
            errors.append('You need a more elaborate description!')
        if len(activity.perslist) == 0:
            errors.append('You need a person to do the activity with!')
        if len(errors) > 0:
            raise ActivityValidatorException(errors)


class Activity:
    """
    Creates a new Activity instance with an unchangable ID, a date, a time and a list of names coupled with IDs of people
    """

    def __init__(self, id, date, start_time, end_time, description, pers_list):
        if not isinstance(id, str):
            raise ActivityException('Invalid value for id!')
        if not isinstance(date, str):
            raise ActivityException('Invalid value for date!')
        if not isinstance(start_time, str):
            raise ActivityException('Invalid value for time!')
        if not isinstance(end_time, str):
            raise ActivityException('Invalid value for time!')
        if not isinstance(description, str):
            raise ActivityException('Invalid description!')
        """
        for pers in pers_list:
            if not isinstance(pers, str):
                raise ActivityException('Invalid person ID!')
        """
        self._id = id
        self._date = date
        self._starttime = start_time
        self._endtime = end_time
        self._description = description
        self._pers_list = pers_list

    @property
    def id(self):
        return self._id

    @property
    def date(self):
        return self._date

    @property
    def starttime(self):
        return self._starttime

    @property
    def endtime(self):
        return self._endtime

    @property
    def description(self):
        return self._description

    @property
    def perslist(self):
        return self._pers_list

    @date.setter
    def date(self, value):
        self._date = value

    @starttime.setter
    def starttime(self, value):
        self._starttime = value

    @endtime.setter
    def endtime(self, value):
        self._endtime = value

    @description.setter
    def description(self, value):
        self._description = value

    @perslist.setter
    def perslist(self, value):
        self._pers_list = value

    def string_of_pers(self):
        people = ''
        for person in self._pers_list:
            people = people + "Name: " + str(person[0]) + ' ID: ' + str(person[1]) + ";"
        return people

    def __str__(self):
        return "ID: " + str(self._id) + " DATE: " + str(self._date) + " START TIME: " + str(
            self._starttime) + " END TIME: " + str(self._endtime) + " DESCRIPTION: " + str(
            self._description) + " PERSONS: " + str(self.string_of_pers())

    def __eq__(self, other):
        return self.id == other.id

    def concomitent(self, other):
        if self.date == other.date:
            if self.starthour() < other.starthour():
                if self.endhour() > other.starthour():
                    return True
                elif self.endhour() == other.starthour():
                    if self.endminute() > other.startminute():
                        return True
            elif self.starthour() == other.starthour():
                if self.endhour() > other.starthour():
                    return True
                elif self.endhour() == other.starthour():
                    if self.endminute() > other.startminute():
                        return True
            elif self.starthour() > other.starthour():
                if other.endhour() > self.starthour():
                    return True
                elif other.endhour() == self.starthour():
                    if self.startminute() < other.endminute():
                        return True
        return False

    def starthour(self):
        return int(self.starttime[0:2])

    def startminute(self):
        return int(self.starttime[3:5])

    def endhour(self):
        return int(self.endtime[0:2])

    def endminute(self):
        return int(self.endtime[3:5])

    def year(self):
        return int(self.date[6:11])

    def month(self):
        return int(self.date[3:5])

    def day(self):
        return int(self.date[0:2])

    def compare(self, date):
        if self.year() > int(date[6:11]):
            return True
        elif self.year() == int(date[6:11]):
            if self.month() > int(date[3:5]):
                return True
            elif self.month() == int(date[3:5]):
                if self.day() >= int(date[0:2]):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def interval(self):
        return abs(60 * (self.endhour()) + self.endminute() - 60 * (self.starthour()) - int(self.startminute()))
