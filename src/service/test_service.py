import unittest
from service.activity_service import ActivityException, Activity, ActivityService, ActivityValidator, CustomActivityRepo
from service.person_service import CustomPersonRepo, Person, PersonService, PersonException, PersonValidator, \
    RepoException
from service.undo import *


class TestPService(unittest.TestCase):

    def setUp(self):
        self._u = Undo()

    def test_add(self):
        pr = CustomPersonRepo()
        pv = PersonValidator()
        ps = PersonService(pr, pv, self._u)
        ps.add_person('87', 'Billy', '0766458342')
        self.assertEqual(len(pr), 1)
        try:
            ps.add_person('87', 'Phil', '0766458346')
        except PersonException:
            assert True
        try:
            ps.add_person('69', 'Ben', '0766458342')
        except PersonException:
            assert True
        try:
            ps.add_person('69', 'Ben', '0742')
        except PersonException:
            assert True

    def test_update(self):
        pr = CustomPersonRepo()
        pv = PersonValidator()
        ps = PersonService(pr, pv, self._u)
        ps.add_person('87', 'Billy', '0766458342')
        self.assertEqual(len(pr), 1)
        ps.update_person('87', 'Freddie', '9076534523')
        a = ps.search_by_name('fred')
        self.assertEqual(a[0].name, 'Freddie')
        self.assertEqual(a[0].number, '9076534523')
        ps.add_person('45', 'Kim', '0767858342')
        b = ps.search_by_number('07678')
        self.assertEqual(b[0].name, 'Kim')
        g = ps.search_by_number('42')
        try:
            b = ps.search_by_name('o')
        except PersonException:
            assert True

    def test_remove(self):
        pr = CustomPersonRepo()
        pv = PersonValidator()
        ps = PersonService(pr, pv, self._u)
        ps.add_person('87', 'Billy', '0766458342')
        self.assertEqual(len(pr), 1)
        ps.remove_person('87')
        self.assertEqual(len(ps), 0)
        self.assertEqual(len(pr), 0)
        try:
            self.assertEqual(ps.search_by_number('0766458342'), 0)
        except PersonException:
            assert True

    def test_undo(self):
        pr = CustomPersonRepo()
        pv = PersonValidator()
        ps = PersonService(pr, pv, self._u)
        person = Person('87', 'Billy', '0766458342')
        ps.add_person('87', 'Billy', '0766458342')
        self.assertEqual(len(pr), 1)
        undo_fun = FunctionCall(pr.remove_person, person)
        redo_fun = FunctionCall(pr.add_person, person)
        op = Operation(undo_fun, redo_fun)
        self._u.record(op)
        self._u.undo()
        self.assertEqual(len(pr), 0)


class TestAService(unittest.TestCase):
    def setUp(self):
        self._u = Undo()

    def test_add(self):
        pr = CustomPersonRepo()
        av = ActivityValidator()
        ar = CustomActivityRepo()
        a_s = ActivityService(av, ar, pr, self._u)
        p = Person('87', 'Billy', '0766458342')
        pr.add_person(p)
        self.assertEqual(len(pr), 1)
        a_s.add_activity('90', '15.12.2025', '16:18', '18:20', 'football', ['87'])
        self.assertEqual(len(ar), 1)
        self.assertEqual(len(a_s), 1)
        try:
            a_s.add_activity('90', '15.12.2025', '16:18', '18:20', 'football', ['87'])
        except ActivityException:
            assert True
        try:
            a_s.add_activity(45, '15.12.2025', '16:18', '18:20', 'football', ['87'])
        except ActivityException:
            assert True
        try:
            a_s.add_activity('45', '15.12.2025', '19:18', '18:20', 'football', ['23'])
        except ActivityException:
            assert True

    def test_remove(self):
        pr = CustomPersonRepo()
        av = ActivityValidator()
        ar = CustomActivityRepo()
        a_s = ActivityService(av, ar, pr, self._u)
        p = Person('87', 'Billy', '0766458342')
        pr.add_person(p)
        self.assertEqual(len(pr), 1)
        a_s.add_activity('90', '15.12.2025', '16:18', '18:20', 'football', ['87'])
        self.assertEqual(len(ar), 1)
        self.assertEqual(len(a_s), 1)
        a_s.remove_activity('90')
        self.assertEqual(len(a_s), 0)
        self.assertEqual(len(ar), 0)

    def test_update(self):
        pr = CustomPersonRepo()
        av = ActivityValidator()
        ar = CustomActivityRepo()
        a_s = ActivityService(av, ar, pr, self._u)
        p = Person('87', 'Billy', '0766458342')
        pr.add_person(p)
        self.assertEqual(len(pr), 1)
        a_s.add_activity('90', '15.12.2025', '16:18', '18:20', 'football', ['87'])
        self.assertEqual(len(ar), 1)
        self.assertEqual(len(a_s), 1)
        a_s.update_activity('90', '17.12.2002', '18:25', '18:28', 'soccer', ['87'])
        a = a_s.get_activ_by_descr('socc')
        b = a_s.get_activ_by_dt('17', '18')
        self.assertEqual(a[0].date, '17.12.2002')
        self.assertEqual(a[0].starttime, '18:25')
        self.assertEqual(a[0].endtime, '18:28')
        self.assertEqual(a[0].perslist, [['Billy', '87']])
        self.assertEqual(a, b)
        try:
            a_s.update_activity('90', '15.12.2025', '19:18', '20:20', 'football', ['23'])
        except ActivityException:
            assert True

    def test_upcoming_activities(self):
        pr = CustomPersonRepo()
        av = ActivityValidator()
        ar = CustomActivityRepo()
        a_s = ActivityService(av, ar, pr, self._u)
        p = Person('87', 'Billy', '0766458342')
        pr.add_person(p)
        a_s.add_activity('90', '15.12.2025', '16:18', '18:20', 'football', ['87'])
        a_s.add_activity('100', '17.12.2025', '16:18', '18:18', 'football', ['87'])
        upcoming = a_s.upcoming_activities('15.12.2025')
        self.assertEqual(len(upcoming), 2)
        upcoming_dates = a_s.get_upcoming_dates('15.12.2025')
        self.assertEqual(upcoming_dates, ['15.12.2025', '17.12.2025'])
        upcoming2 = a_s.upcoming_activities('17.12.2025')
        self.assertEqual(a_s.calculate_lenght_and_interval(upcoming2), 120)
        a_s.add_activity('101', '17.12.2025', '14:18', '16:18', 'football', ['87'])
        b = a_s.activities_per_date('17.12.2025')
        self.assertEqual(len(b), 2)
        a = a_s.activities_with_person('87', '15.12.2025')
        self.assertEqual(len(a), 3)
        self.assertEqual(a_s.filter_by_date('17.12.2025', a_s.get_all()), a_s.activities_per_date('17.12.2025'))

    def test_busiest_days(self):
        pr = CustomPersonRepo()
        av = ActivityValidator()
        ar = CustomActivityRepo()
        a_s = ActivityService(av, ar, pr, self._u)
        p = Person('87', 'Billy', '0766458342')
        pr.add_person(p)
        a_s.add_activity('100', '17.12.2025', '16:18', '18:18', 'football', ['87'])
        a_s.add_activity('90', '15.12.2025', '16:18', '18:20', 'football', ['87'])
        a_s.add_activity('101', '17.12.2025', '14:18', '16:18', 'football', ['87'])
        c = a_s.busiest_days('15.12.2025')
        b = a_s.upcoming_activities('15.12.2025')
        b.reverse()
        self.assertEqual(c[0][0], b[0])

    def test_undo(self):
        pr = CustomPersonRepo()
        av = ActivityValidator()
        ar = CustomActivityRepo()
        pv = PersonValidator()
        a_s = ActivityService(av, ar, pr, self._u)
        ps = PersonService(pr, pv, self._u)
        p = Person('87', 'Billy', '0766458342')
        pr.add_person(p)
        a = Activity('100', '17.12.2025', '16:18', '18:18', 'football', [['Billy', '87']])
        ar.add_activity(a)
        pr.update_person(p, 'Johnny', '0775456345')
        a_s.update_activity_repo()
        self.assertEqual(a.perslist, [['Johnny', '87']])
        ps.remove_person('87')
        a_s.update_activity_repo()
        self.assertEqual(a.perslist, [])
        self._u.undo()
        self.assertEqual(a.perslist, [['Johnny', '87']])


class TestUndo(unittest.TestCase):
    def setUp(self):
        self._pr = CustomPersonRepo()
        self._pv = PersonValidator()
        self._u = Undo()
        self._ps = PersonService(self._pr, self._pv, self._u)
        self._av = ActivityValidator()
        self._ar = CustomActivityRepo()
        self._as = ActivityService(self._av, self._ar, self._pr, self._u)
        self._ps.add_person('67', 'Jane', '0755454343')
        self._ps.add_person('76', 'Gregory', '0755489343')
        self._ps.add_person('88', 'Kyle', '0755454373')
        self._as.add_activity('56', '12.10.2002', '12:23', '18:56', 'weight lifting', ['67', '88'])
        self._as.add_activity('66', '12.11.2002', '12:23', '18:56', 'grocery shopping', ['88', '76'])

    def test_undo_redo(self):
        self.assertEqual(len(self._ar), 2)
        self._as.remove_activity('56')
        self.assertEqual(len(self._ar), 1)
        self._u.undo()
        self.assertEqual(len(self._ar), 2)
        self._u.redo()
        try:
            self._u.redo()
        except ValueError:
            assert True
        self.assertEqual(len(self._ar), 1)
        for i in range(6):
            self._u.undo()
        try:
            self._u.undo()
        except ValueError:
            assert True

    def test_cascaded_op(self):
        self._as.remove_activity('56')
        self._as.remove_activity('66')
        a = Activity('56', '12.10.2002', '12:23', '18:56', 'weight lifting', [['Jane', '67'], ['Kyle', '88']])
        a2 = Activity('66', '12.11.2002', '12:23', '18:56', 'grocery shopping', [['Kyle', '88'], ['Gregory', '76']])
        self._ar.add_activity(a)
        self._ar.add_activity(a2)
        self._ps.remove_person('88')
        self._as.update_activity_repo()
        self.assertEqual(a.perslist, [['Jane', '67']])
        self.assertEqual(a2.perslist, [['Gregory', '76']])
        self._u.undo()
        self.assertEqual(a.perslist, [['Jane', '67'], ['Kyle', '88']])
        self.assertEqual(a2.perslist, [['Gregory', '76'], ['Kyle', '88']])
        self._u.redo()
        self._as.update_activity_repo()
        self.assertEqual(a.perslist, [['Jane', '67']])
        self.assertEqual(a2.perslist, [['Gregory', '76']])
        self.assertTrue(isinstance(self._u.return_last_element(), CascadedOperation))

        sample_person = Person('27', 'Joe', '7866454384')
        sample_activity = Activity('89', '12.12.2020', '13:45', '17:27', 'test', [['Joe', '27']])
        sample_u_fun = FunctionCall(self._pr.add_person, sample_person)
        sample_r_fun = FunctionCall(self._pr.remove_person, sample_person)
        o1 = Operation(sample_u_fun, sample_r_fun)
        sample2_u_fun = FunctionCall(self._ar.add_activity, sample_activity)
        sample2_r_fun = FunctionCall(self._ar.remove_activity, sample_activity)
        o2 = Operation(sample2_u_fun, sample2_r_fun)
        co = CascadedOperation(o1, o2)
        self._u.record(co)
        self.assertEqual(self._u.unpack_last_element()[0], (sample_u_fun, sample_r_fun))
