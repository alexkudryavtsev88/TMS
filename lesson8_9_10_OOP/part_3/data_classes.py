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
class MyFrozenClass:
    name: str = "John"
    age: int = 35

    def __str__(self):
        return f'{self.name}, {self.age}'

    @classmethod
    def build(cls, name, age):
        actual_values = {
            k: type(v) for k, v in locals().items() if k != 'cls'
        }
        expected_values = cls.__annotations__
        if expected_values != actual_values:
            raise TypeError(f"invalid types! (Expected: {expected_values}, Actual: {actual_values})")
        return cls(name=name, age=age)



person = MyFrozenClass.build('Alex', 34)
print(person)

try:
    person.age = 35  # will raise error "dataclasses.FrozenInstanceError: cannot assign to field 'age'"
except dataclasses.FrozenInstanceError as err:
    print(
        "Экземпляр dataclass'а, который помечен как 'frozen' - изменить НЕЛЬЗЯ! "
        f"(Ошибка в строке {err.__traceback__.tb_lineno})"
    )

try:
    person = MyFrozenClass.build('Alex', '34')
except TypeError as err:
    print(err.args[0])


print(f"Dataclass as Dict: {asdict(person)}")


"""
Описать Dataclass, который 
- содержит три произвольных поля, разных типов
- имеет один-единственный classmethod, который проверяет типы этих трех полей и возвращает объект Dataclass'a
- является НЕизменяемым (у объекта этого класса нельзя изменить значения атрибута/добавить новый атрибут после его создания)
"""