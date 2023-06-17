"""OOP (parts 2-3) Homework"""

from dataclasses import dataclass

"""
Домашнее Задание:

1. Описать Dataclass, который
- содержит три произвольных поля, разных типов
- имеет один-единственный classmethod, который:
  - проверяет типы этих трех полей и возвращает объект Dataclass'a, если типы верны 
  - порождает исключение TypeError если хотя бы один из атрибутов имеет НЕВЕРНЫЙ тип
- является НЕИЗМЕНЯЕМЫМ (у инстанса этого класса нельзя изменить значения атрибута/добавить новый атрибут/удалить атрибут)
"""


# TASK 1: Шаблон класса
@dataclass
class MyDataClass:
    a: str
    b: int
    c: list

    @classmethod
    def build(cls, *args):
        """
        Your implementation here
        """


# Тесты для задания 1: должны отработать без ошибок!
person1 = MyDataClass.build("TEST", 34, [1, 2, 3])  # valid parameters
print(person1)
try:
    person2 = MyDataClass.build(100, 33, [1, 2, 3])  # invalid parameters
except Exception as exc:
    print(exc)

try:
    person3 = MyDataClass.build("TEST", "33", [1, 2, 3])  # invalid parameters
except Exception as exc:
    print(exc)

try:
    person3 = MyDataClass.build("TEST", 33, (1, 2, 3))  # invalid parameters
except Exception as exc:
    print(exc)

# -------------------------------------------------------------------------------------------------------#

"""
2. Написать класс, который реализует следующее:
a) в __init__ определяется 2 атрибута:
-- атрибут name строкового типа
-- атрибут age целочисленного типа
(неважно, передадите вы их аргументами или же строго зададите им значения в __init__)
b) можно итерироваться по атрибутам инстанса в цикле for
c) имеет property c именем year_of_birth, которое при обращении к нему возвращает год рождения
   ("год рождения" должен вычисляться по-простому, как "текущий год - age", без учета того, 
    что у человека, которому на данный момент 34 года, день рождения может быть в этом году, но оно еще не наступило :)
   (нужно будет проверить, что после изменения значения age, результат вызова property тоже изменяется)
d) *реализует магические методы сравнения (__eq__, __ne__, __lt__, __le__, __gt__, __ge__), благодаря которым можно будет "сравнивать"
   разные инстансы этого класса:
   - при сравнении через операторы == и != должны проверятся ОБА атрибута инстанса: name и age,
     причем, name должен сравниваться БЕЗ УЧЕТА регистра
   - при сравнении через операторы >, <, >=, <= должно сравниваться только поле age!

"""

# TASK 2: Шаблон класса
class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # your magic methods should be defined here ...


# Тесты для задания 2: должны отработать без ошибок!
person1 = Person('Alex', 34)
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
# <
assert person1 < Person('Alex', 35)
assert person1 < Person('Ann', 35)
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

# -------------------------------------------------------------------------------------------------------#

"""
3. Написать класс, который реализует следующее:
a) содержит атрибут person строкового типа
b) в __init__ определяется 1 атрибут с тем же именем - person
c) имеет 3 родителя (множественное наследование), у каждого из родительских классов тоже есть атрибут person
d) содержит магические методы __getitem__ и __setitem__, чтобы у инстанса можно было получить/установить значение атрибута через instance["name"]
e) *cодержит метод get_attribute (НЕ магический), который принимает 1 аргумент - строковое имя атрибута и реализует поиск атрибута cледующим образом:
-- если атрибут найден в инстансе класса:
   - печатаем f"Attribute {attr_name} found in Instance: " + инстанс
   - возвращаем значение атрибута
-- если атрибут НЕ найден в инстансе класса, но найден в самом классе:
   - печатаем f"Attribute {attr_name} found in Instance Class: " + имя класса
   - возвращаем значение атрибута
-- если атрибут НЕ найден в инстансе класса и в самом классе, но найден в каком-либо из родительских классов:
   - печатаем f"Attribute {attr_name} found in Instance Parent Class: " + имя родительского класса
   - возвращаем значение атрибута
-- атрибут не найден вообще - порождаем исключение AttributeError с соответствующим текстом ошибки

  (ПРИМЕЧАНИЕ: для поиска атрибутов использовать __dict__)
  
   
"""

# ПРИМЕЧАНИЕ: нужно будет проверить работу вашего метода get_attribute через динамическое удаление атрибутов
# (как было показано в материале одного из уроков)
# Для удаления можно использовать delattr(object_, "attribute_name") или del object_.attribute_name)

# -------------------------------------------------------------------------------------------------------#

"""
4. Используя встроенную функцию type динамически создать следующие типы (классы)
- класс Parent1 c классовым атрибутом a (любое значение)
- класс Parent2 с классовым атрибутом b (любое значение)
- класс Child, который наследуется от Parent1 и Parent2 и имеет классовый атрибут c (любое значение)
"""

# -------------------------------------------------------------------------------------------------------#

"""
*5. Описать класс MyStack, который реализует функциональность абстрактной структуры данных Stack и имеет следующие методы:
a) __init__: 
   - принимает 1 НЕОБЯЗАТЕЛЬНЫЙ аргумент, который есть какая-либо упорядоченная коллекция (лист, кортеж) или строка; 
   - добавляет элементы из входной коллециии во внутреннюю коллекцию в том же порядке 
     (в случае, если аргумент - это строка, то во внутреннюю коллекцию добавляем символы этой строки в том же порядке)
b) push (добавление нового элемента в "вершину" стэка)
c) pop (удаление элемента из "вершины" стэка и возврат удаленного элемента)
d) is_empty (возвращает True, если есть хотя бы 1 элемент, и False, если нет элементов)

ПРИМЕЧЕНИЕ: какой тип использовать для внутренней коллекции - оставляю выбор за вами :) 
Главное, чтобы соблюдались следующие условия: 
- внутренняя коллекция должна быть упорядоченной
- методы добавления и удаления элемента, реализованные в классе, должны работать за константное время 
  (не зависеть от размера внутренней коллекции)
"""
