from datetime import date


class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def year_of_birth(self):
        return date.today().year - self.age

    def __eq__(self, other):
        return self.name.lower() == other.name.lower() and self.age == other.age

    def __ne__(self, other):
        return self.name.lower() != other.name.lower() or self.age != other.age

    def __lt__(self, other):
        return self.age < other.age

    def __le__(self, other):
        return self.age <= other.age

    def __gt__(self, other):
        return self.age > other.age

    def __ge__(self, other):
        return self.age >= other.age


person = Person('Alex', 34)
print(person.year_of_birth)