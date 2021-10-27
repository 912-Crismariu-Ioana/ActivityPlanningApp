import copy
class IterableDS:
    class Iterator():
        def __init__(self,col):
            self._collection = col
            self._poz = 0

        def __next__(self):
            if self._poz == len(self._collection._list):
                raise StopIteration()
            self._poz += 1
            return self._collection._list[self._poz -1]

    def __init__(self):
        self._list = []

    def __getitem__(self, item):
        return self._list[item]

    def __delitem__(self, key):
        del self._list[key]

    def __iter__(self):
        return self.Iterator(self)

    def __setitem__(self, key, value):
        self._list[key] = value

    def __copy__(self):
        return self._list[:]


    def append(self, item):
        self._list.append(item)

    def __len__(self):
        return len(self._list)


def gnome_sort(list,fun):
    pos = 0
    while pos < len(list):
        if pos == 0 or fun(list[pos],list[pos-1]):
            pos = pos + 1
        else:
            list[pos],list[pos-1] = list[pos-1], list[pos]
            pos = pos - 1



def filter(list, fun):
    filter_result = []
    for i in range(len(list)):
        if fun(list[i]):
            filter_result.append(list[i])
    return filter_result

def greater_than(x,y):
    return x >= y

def even(x):
    return x % 2 == 0

