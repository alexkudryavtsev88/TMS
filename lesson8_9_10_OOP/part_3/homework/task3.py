class Parent1:
    person = "Parent1 class attr"


class Parent2:
    person = "Parent2 class attr"


class Child(Parent1, Parent2):
    person = "Child class attr"

    def __init__(self):
        self.person = "Child Instance attr"

    def get_attribute(self, item: str):
        if item in self.__dict__:
            print(f"Attribute {item} found in Instance: {self}")
            return self.__dict__[item]

        cls = self.__class__
        parents = cls.mro()[1:]

        if item in cls.__dict__:
            print(f"Attribute {item} found in Instance Class: {cls.__name__}")
            return cls.__dict__[item]

        for parent in parents:
            if item in parent.__dict__:
                print(f"Attribute {item} found in Instance Parent Class: {parent.__name__}")
                return parent.__dict__[item]

        raise AttributeError(f"{item} not FOUND!")


instance = Child()
print(f"Value: {instance.get_attribute('person')}")
del instance.person
print(f"Value: {instance.get_attribute('person')}")
del instance.__class__.person
print(f"Value: {instance.get_attribute('person')}")
del Parent1.person
print(f"Value: {instance.get_attribute('person')}")
del Parent2.person
try:
    print(f"Value: {instance.get_attribute('person')}")
except AttributeError as exc:
    print(exc)


