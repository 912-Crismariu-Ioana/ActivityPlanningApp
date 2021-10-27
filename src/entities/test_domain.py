import unittest
from entities.activity_ import ActivityValidator, Activity, ActivityException, DayValidator
from entities.person import Person, PersonValidator, PersonException, PersonValidatorException

class TestActivity(unittest.TestCase):
    def test_activity(self):
        activity = ActivityValidator()
        activity.validate(Activity('56', '23.07.2001', '14:23','15:12', 'reading', [['Alina']]))
        active = Activity('56', '23.07.2001', '14:23', '15:12', 'reading', [['Alina']])
        active2 = Activity('56', '23.07.2001', '14:23', '15:12', 'chilling', [['Alina']])
        self.assertEqual(active, active2)
        self.assertEqual(active.id,'56')
        self.assertEqual(active.date,'23.07.2001')
        self.assertEqual(active.starttime, '14:23')
        self.assertEqual(active.endtime, '15:12')
        self.assertEqual(active.description, 'reading')
        self.assertEqual(active.perslist,[['Alina']])
        active.date = '17.08.2001'
        active.starttime = '12:34'
        active.endtime = '13:23'
        active.description = 'studying'
        active.perslist= [['Maria', '56']]
        self.assertEqual(active.date, '17.08.2001')
        self.assertEqual(active.starttime, '12:34')
        self.assertEqual(active.endtime, '13:23')
        self.assertEqual(active.description, 'studying')
        self.assertEqual(active.perslist, [['Maria', '56']])
        self.assertEqual(active.starthour(), 12)
        self.assertEqual(active.endhour(), 13)
        self.assertEqual(active.startminute(), 34)
        self.assertEqual(active.endminute(), 23)
        self.assertEqual(active.year(), 2001)
        try:
            activ = Activity(12, '14.05.2002', '15:16', '16:17', 'cleaning', ['Elena'])
        except ActivityException:
            assert True
        try:
            activv = ActivityValidator.validate(Activity('', '14.05.2002', '15:16', '16:17', '', ''))
        except ActivityException:
            assert True
        actif = Activity('56', '17.08.2001', '12:34', '13:23', 'reading', ['Alina'])
        self.assertTrue(active.concomitent(actif))
        self.assertTrue(active.concomitent(Activity('56', '17.08.2001', '10:34', '13:23', 'reading', ['Alina'])))
        self.assertFalse(active.concomitent(Activity('56', '17.08.2001', '10:34', '12:23', 'reading', ['Alina'])))
        self.assertTrue(active.concomitent(Activity('56', '17.08.2001', '11:34', '13:20', 'reading', ['Alina'])))
        self.assertTrue(active.concomitent(Activity('56', '17.08.2001', '11:34', '12:35', 'reading', ['Alina'])))
        active.starttime = '12:34'
        active.endtime = '12:40'
        self.assertTrue(active.concomitent(Activity('56', '17.08.2001', '12:35', '12:40', 'reading', ['Alina'])))
        active.endtime = '13:40'
        self.assertTrue(active.concomitent(Activity('56', '17.08.2001', '13:34', '14:48', 'reading', ['Alina'])))
        active.endtime = '14:40'
        self.assertTrue(active.concomitent(Activity('56', '17.08.2001', '13:34', '14:39', 'reading', ['Alina'])))
        self.assertTrue(active.compare('16.08.2001'))
        self.assertTrue(active.compare('16.07.2001'))
        self.assertFalse(active.compare('18.09.2001'))
        self.assertTrue(active.compare('16.08.2000'))
        self.assertFalse(active.compare('18.08.2001'))
        self.assertFalse(active.compare('16.08.2002'))
        self.assertEqual(active.interval(), 126)
        try:
            dv = DayValidator.validate('1.8.20')
        except:
            assert True
        try:
            activv = ActivityValidator.validate(Activity('34', '14.05.202', '11:16', '10:17', 'bl', []))
        except:
            assert True

        try:
            activv = ActivityValidator.validate(Activity('', '14.05.202', '1:16', '1:17', '', ''))
        except:
            assert True
        try:
            activv = ActivityValidator.validate(Activity('34', '14.05.2002', '78:60', '89:70', 'ui', []))
        except:
            assert True
        try:
            activv = ActivityValidator.validate(Activity('34', '14.05.2002', '78:60', '9:70', 'ui', []))
        except:
            assert True
        try:
            dv = DayValidator.validate('60.28.2002')
        except:
            assert True
        try:
            active = Activity('56', 23, '14:23', '15:12', 'reading', ['Alina'])
        except ActivityException:
            assert True
        try:
            active = Activity('56', '23', 14, '15:12', 'reading', ['Alina'])
        except ActivityException:
            assert True
        try:
            active = Activity('56', '23', '14:23', '15:12', 7, ['Alina'])
        except ActivityException:
            assert True
        try:
            active = Activity('56', '23', '14:23', 12, 'reading', ['Alina'])
        except ActivityException:
            assert True
        try:
            activv = ActivityValidator.validate(Activity('34', '56.72.2002', '78:60', '9:70', 'ui', []))
        except:
            assert True
        self.assertEqual(active.string_of_pers(), 'Name: Maria ID: 56;' )

class TestPerson(unittest.TestCase):
    def test_person(self):
        person = PersonValidator()
        person.validate(Person('34', 'Joan','0755456345'))
        pers = Person('34', 'Joan','0755456345')
        self.assertEqual(pers.id, '34')
        self.assertEqual(pers.name, 'Joan')
        self.assertEqual(pers.number, '0755456345')
        pers2 = Person('34', 'U', '0755456345')
        self.assertTrue(pers.eq_ph(pers2))
        self.assertEqual(pers, pers2)
        pers.name = 'Barbara'
        pers.number = '0746554342'
        self.assertEqual(pers.name, 'Barbara')
        self.assertEqual(pers.number, '0746554342')

        try:
            self.assertFalse(person.validate(Person(34, 56, 76689)))
        except PersonException:
            assert True
        try:
            self.assertFalse(person.validate(Person('', '', '')))
        except PersonException:
            assert True
        try:
            self.assertFalse(person.validate(Person('34', 56, '76689')))
        except PersonException:
            assert True
        try:
            self.assertFalse(person.validate(Person('34', '56', 76689)))
        except PersonException:
            assert True
        try:
            self.assertFalse(person.validate(Person('', '56', '7668956789')))
        except PersonException:
            assert True

        error_list = ['Phone number should have 10 integers!']
        pve = PersonValidatorException(error_list)
        self.assertEqual(str(pve), 'Phone number should have 10 integers!\n')

