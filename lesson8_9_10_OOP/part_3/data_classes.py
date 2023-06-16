"""
DATACLASSES

- Появились с версии 3.7
- Являются аналогами NamedTuples, но NamedTuples всегда неизменяемые,
  а dataclasses могут быть как изменяемыми, так и неизменяемыми
- Указывать тип атрибутов - ОБЯЗАТЕЛЬНО
- Упрощают описание класса в сравнении с обычными классами:
"""
import dataclasses
from dataclasses import dataclass, asdict


@dataclass
class MyDataClass:
    name: str
    age: int


my_dt_obj = MyDataClass(name="Alex", age=34)

""" VS """


class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age


my_obj = MyClass(name="Alex", age=34)
my_obj.name = "John"

"""
- Могут содержать дефолтные значения атрибутов
- Атрибуты, объявленные в датаклассе, будут содержаться и в __dict__ экземпляра класса, и в __dict__ самого класса (включая методы).
  Это избавляет от необходимости создавать экземпляры датаклассов (можно использовать класс напрямую),
  ЕСЛИ в датаклассе объявлены ДЕФОЛТНЫЕ значения атрибутов, которые НЕ нужно менять в будущем.
- Экземпляры ИЗМЕНЯЕМЫХ датаклассов НЕ могут быть ключами словарей (НЕ хэшируемые объекты)
- Могут содержать методы как обычные классы
- Можно сделать иммутабельным указав в декораторе: @dataclass(frozen=True)
"""


@dataclass(frozen=True)
class MyPerson:
    my_list: list
    name: str = "John"
    age: int = 35

    def __str__(self):
        return f'{self.name}, {self.age}, {self.my_list}'

    @classmethod
    def build(cls, name, age, my_list):
        values = locals()
        expected_values = cls.__annotations__  # returns dict with attributes names mapped with their types
        print(expected_values)
        for attr_name, attr_type in expected_values.items():
            actual = values.get(attr_name)
            if not isinstance(actual, attr_type):
                raise TypeError(
                    f"Attribute '{attr_name}' should have "
                    f"type {attr_type}, got: {type(actual)}"
                )

        return cls(name=name, age=age, my_list=my_list)

    def append(self, some):
        self.my_list.append(some)


person = MyPerson(
    name="Alex",
    age=34,
    my_list=None  # PyCharm is highlighted this line because my_list attribute has type 'list[str]',
                  # and we specify None here.

    # BUT! This is ONLY the static type check from PyCharm, for the Python interpreter this code
    # is VALID and can be executed.
)

print(person)

# But if we try to call person.append method we receive the Error, because my_list value which is None
# doesn't have .append() method!

try:
    person.my_list.append(1)
except Exception as exc:
    print(exc)

# We can use method 'build' which validates the types of input parameters:
try:
    person1 = MyPerson.build("Alex", 34, [1, 2, 3])  # valid parameters
    person2 = MyPerson.build("Ann", 33, None)  # invalid parameters
except Exception as exc:
    print(exc)

# it's possible to mutate the inner list inside the frozen dataclass instance


# but it's impossible to mutate frozen dataclass instance itself
try:
    person.age = 35  # set new value to existing attribute
    person.test = "test"  # set new attribute
    del person.age  # delete attribute
except dataclasses.FrozenInstanceError as err:
    print(
        "Экземпляр dataclass'а, который помечен как 'frozen' - изменить НЕЛЬЗЯ! "
        f"(Ошибка в строке {err.__traceback__.tb_lineno})"
    )


@dataclass(init=False)
class NoInitClass:
    name: str
    age: int

    def __str__(self):
        return f"{self.name}, {self.age}"


inst = NoInitClass()  # it's possible to create instance of dataclass with 'init=False' without its parameters
print(inst.__dict__)  # dict is empty
inst.name = "Alex"
inst.age = 34
print(inst)

print(f"Dataclass as Dict: {asdict(person)}")  # convert dataclass instance to dict