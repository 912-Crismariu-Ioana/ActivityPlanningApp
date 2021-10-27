class PersonException(Exception):
    def __init__(self, msg):
        super().__init__(self, msg)


class PersonValidatorException(PersonException):
    """
    Receives the errors from the PersonValidator class and prints them nicely
    """

    def __init__(self, error_list):
        self._errors = error_list

    def __str__(self):
        result = ''
        for er in self._errors:
            result += er
            result += '\n'
        return result


class PersonValidator:
    """
    Checks the params of a new person instance, creates list of errors
    """

    @staticmethod
    def validate(person):
        errors = []
        if person.id == '' or len(person.id) == 0:
            errors.append('ID should contain at least one integer!')
        if not person.id.isdigit():
            errors.append('ID should contain only integers!')
        if person.name == '' or len(person.name) == 0:
            errors.append('Name should have at least a letter!')
        if len(person.number) != 10:
            errors.append('Phone number should have 10 integers!')
        if not person.number.isdigit():
            errors.append('Phone number should have only integers!')
        if len(errors) > 0:
            raise PersonValidatorException(errors)


class Person:
    """
    Creates a new person instance with an unchangeable ID, a name and phone number
    """

    def __init__(self, id, name, number):
        if not isinstance(id, str):
            raise PersonException('Invalid value for id!')
        if not isinstance(name, str):
            raise PersonException('Invalid value for name!')
        if not isinstance(number, str):
            raise PersonException('Invalid value for number!')
        self._id = id
        self._name = name
        self._number = number

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number

    @name.setter
    def name(self, value):
        self._name = value

    @number.setter
    def number(self, value):
        self._number = value

    def __str__(self):
        return "ID: " + str(self._id) + " NAME: " + str(self._name) + " NUMBER: " + str(self._number)

    def __eq__(self, other):
        return self._id == other._id

    def eq_ph(self, other):
        return self._number == other._number
