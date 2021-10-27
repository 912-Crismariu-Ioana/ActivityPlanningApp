import unittest
from custom_iterable_collection.iterable import *


class TestIterable(unittest.TestCase):
    def setUp(self):
        self._ds = IterableDS()

    def test_append(self):
        self._ds.append(25)
        self._ds.append(34)
        self.assertTrue(len(self._ds) == 2)

    def test_setitem(self):
        self._ds.append(36)
        self.assertEqual(self._ds[0], 36)
        self._ds[0] = 5
        self.assertEqual(self._ds[0], 5)

    def test_delitem(self):
        self.test_append()
        del self._ds[0]
        self.assertEqual(self._ds[0], 34)
        try:
            del self._ds[1]
        except IndexError:
            assert True

    def test_copy(self):
        cop = self._ds.__copy__()
        self.assertTrue(isinstance(cop, list))

    def test_iter(self):
        self.test_append()
        iterator = iter(self._ds)
        self.assertEqual(next(iterator), 25)
        self.assertEqual(next(iterator), 34)
        try:
            next(iterator)
        except StopIteration:
            assert True


class TestGnomeandFilter(unittest.TestCase):
    def setUp(self):
        self._ds = IterableDS()
        self._lista = [90, 56, 78, 34, 1000, 19, 45, 7]

    def test_gnome(self):
        for num in self._lista:
            self._ds.append(num)
        self.assertEqual(gnome_sort(self._lista, greater_than), self._lista.sort())
        gnome_sort(self._ds, greater_than)
        sorted = self._ds.__copy__()
        for i in range(len(sorted)):
            self.assertEqual(sorted[i], self._lista[i])

    def test_filter(self):
        for num in self._lista:
            self._ds.append(num)
        self.assertEqual(filter(self._lista, even), [90, 56, 78, 34, 1000])
        filter(self._ds, even)
        sorted = self._ds.__copy__()
        for i in range(len(sorted)):
            self.assertEqual(sorted[i], self._lista[i])
