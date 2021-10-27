import unittest
from repository.custom_DT_arepo import CustomActivityRepo, Activity, ActivityException
from repository.custom_DT_prepo import CustomPersonRepo, Person, PersonException


class TestActivityRepo(unittest.TestCase):
    def test_add(self):
        a = Activity('67', '12.03.2003', '14:13', '15:12', 'grab lunch', [['Anna', '45']])
        a_repo = CustomActivityRepo()
        a_repo.add_activity(a)
        self.assertEqual(len(a_repo), 1)
        self.assertEqual(a, a_repo.get_activity_by_id('67'))
        try:
            a_repo.add_activity(Activity('67', '01.02.2005', '07:15', '14:12', 'visiting grandpa', 'Andrew 56'))
        except ActivityException:
            assert True
        try:
            a_repo.add_activity(Activity('52', '12.03.2003', '14:13', '16:56', 'visiting grandpa', 'Andrew 56'))
        except ActivityException:
            assert True

    def test_remove(self):
        a = Activity('67', '12.03.2003', '14:13', '15:12', 'grab lunch', [['Anna', '45']])
        a_repo = CustomActivityRepo()
        a_repo.add_activity(a)
        self.assertEqual(len(a_repo), 1)
        a_repo.remove_activity(a)
        self.assertEqual(len(a_repo), 0)
        self.assertEqual(a_repo.get_all(), [])

    def test_update(self):
        a = Activity('67', '12.03.2003', '14:13', '15:12', 'grab lunch', [['Anna', '45']])
        a_repo = CustomActivityRepo()
        a_repo.add_activity(a)
        self.assertEqual(len(a_repo), 1)

        try:
            b = Activity('52', '12.03.2003', '14:13', '15:12', 'grab lunch', [['Anna', '45']])
            a_repo.update_activity(b, '12.10.2020', '16:23', '15:46', 'cinema', [[]])
        except ActivityException:
            assert True
        a_repo.update_activity(a, '16.05.2021', '14:27', '15:18', 'tyt', [[]])
        self.assertEqual(a.date, '16.05.2021')
        self.assertEqual(a.starttime, '14:27')
        self.assertEqual(a.endtime, '15:18')
        self.assertEqual(a.perslist, [[]])


class TestPersonRepo(unittest.TestCase):
    def test_add(self):
        p = Person('67', 'Anna', '0745334234')
        p_repo = CustomPersonRepo()
        p_repo.add_person(p)
        self.assertEqual(len(p_repo), 1)
        self.assertEqual(p, p_repo.get_person_by_id('67'))
        try:
            p_repo.add_person(Person('67', 'Joe', '0722354792'))
        except PersonException:
            assert True
        try:
            p_repo.add_person(Person('52', 'Joe', '0745334234'))
        except PersonException:
            assert True

    def test_remove(self):
        p = Person('67', 'Anna', '0745334234')
        p_repo = CustomPersonRepo()
        p_repo.add_person(p)
        self.assertEqual(len(p_repo), 1)
        p_repo.remove_person(p)
        self.assertEqual(len(p_repo), 0)
        self.assertEqual(p_repo.get_all(), [])

    def test_update(self):
        p = Person('67', 'Anna', '0745334234')
        p_repo = CustomPersonRepo()
        p_repo.add_person(p)
        self.assertEqual(len(p_repo), 1)
        p_repo.update_person(p, 'Diana', '0722346456')
        self.assertEqual(p.name, 'Diana')
        self.assertEqual(p.number, '0722346456')
        try:
            q = Person('52', 'Joe', '0745334234')
            p_repo.update_person(q, 'Peter', '0866787496')
        except PersonException:
            assert True
        self.assertEqual(p_repo.get_ids(), ['67'])
