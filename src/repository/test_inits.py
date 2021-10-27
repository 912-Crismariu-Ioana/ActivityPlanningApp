import random
from repository.custom_DT_arepo import *
from repository.custom_DT_prepo import *


class PopulatedPeopleRepo(CustomPersonRepo):
    def __init__(self):
        super().__init__()

    def test_init_person(self):
        fname_list = ['Alice', 'Mary', 'Robert', 'John', 'Katherine', 'Stanley', 'Martha', 'Claire', 'Peter', 'Flynn']
        lname_list = ['Smith', 'Johnson', 'Brown', 'Hyde', 'Keller', 'Miller', 'Hill', 'Green', 'Jenkins', 'Andersen']
        names = []
        while len(names) < 10:
            name = ' '.join([random.choice(fname_list), random.choice(lname_list)])
            if name in names:
                continue
            names.append(name)
        ids = []
        while len(ids) < 10:
            id = str(random.randint(0,999))
            if id in ids:
                continue
            ids.append(id)
        numbers = []
        while len(numbers) < 10:
            number = str(random.randint(1000000000, 9999999999))
            if number in numbers:
                continue
            numbers.append(number)
        names_already_used = []
        while len(self) < 10:
            try:
                aidi = random.choice(ids)
                neim = random.choice(names)
                namba = random.choice(numbers)
                pers = Person(aidi, neim, namba)
                names_already_used.append(neim)
                self.add_person(pers)
            except PersonException:
                continue

        return self

class PopulatedActivityRepo(CustomActivityRepo):

    def __init__(self, people_repo):
        super().__init__()
        self._people_repo = people_repo

    def test_init_activity(self):
        activity_description = ['running', 'going to the library', 'going for a walk', 'going swimming', 'cooking', 'listening to music', 'attending lectures', 'going shopping', 'gardening', 'doing chores']
        times = []
        while len(times) < 10:
            hour = str(random.randint(0,23))
            if len(hour) == 1:
                hour = hour.zfill(2)
            minute = str(random.randint(0,59))
            if len(minute) == 1:
                minute = minute.zfill(2)
            time=':'.join([hour, minute])
            if time in times:
                continue
            times.append(time)
        dates = []
        for z in range(10):
            year = str(random.randint(2021, 2022))
            month = str(random.randint(1,12))
            if month == 2:
                day = str(random.randint(1,28))
            elif month in [4,6,9,11]:
                day = str(random.randint(1,30))
            else:
                day = str(random.randint(1,31))
            if len(day) == 1:
                day = day.zfill(2)
            if len(month) == 1:
                month = month.zfill(2)
            date = '.'.join([day,month,year])
            dates.append(date)
        activity_ids = []
        while len(activity_ids) < 10:
            id = str(random.randint(0,999))
            if id in activity_ids:
                continue
            activity_ids.append(id)
        ppl = self._people_repo.get_all()
        ppl_names = []
        for pers in ppl:
            ppl_names.append([pers.name, pers.id])
        while len(self) < 10:
            try:
                activity_id = random.choice(activity_ids)
                activity_date = random.choice(dates)
                activity_starttime = random.choice(times)
                activity_endtime = random.choice(times)
                act_des= random.choice(activity_description)
                people = [random.choice(ppl_names)]
                a = Activity(activity_id, activity_date, activity_starttime, activity_endtime, act_des, people)
                av = ActivityValidator()
                av.validate(a)
                self.add_activity(a)
            except ActivityException:
                continue

        assert len(self) == 10
        return self

