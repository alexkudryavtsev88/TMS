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


person1 = Person('Alex', 34)
print(person1.year_of_birth)

# ==
assert person1 == Person('Alex', 34)
assert person1 == Person('alex', 34)
assert person1 == Person('ALEX', 34)
# !=
assert person1 != Person('Alex!', 34)
assert person1 != Person('Alex', 35)
# >
assert person1 > Person('Alex', 33)
assert person1 > Person('Ann', 33)
assert not person1 > Person('Ann', 34)
# <
assert person1 < Person('Alex', 35)
assert person1 < Person('Ann', 35)
assert not person1 < Person('Ann', 34)
# >=
assert person1 >= Person('Alex', 34)
assert person1 >= Person('Alex', 33)
assert person1 >= Person('Ann', 34)
assert person1 >= Person('Ann', 33)
# <=
assert person1 <= Person('Alex', 34)
assert person1 <= Person('Alex', 35)
assert person1 <= Person('Ann', 34)
assert person1 <= Person('Ann', 35)
