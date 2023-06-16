"""
Домашнее Задание:

1. Описать Dataclass, который
- содержит три произвольных поля, разных типов
- имеет один-единственный classmethod, который проверяет типы этих трех полей и возвращает объект Dataclass'a
- является НЕизменяемым (у объекта этого класса нельзя изменить значения атрибута/добавить новый атрибут после его создания)

2. Написать класс, который реализует следующее:
a) содержит:
-- атрибут с именем name строкового типа
-- атрибут с именем age целочисленного типа
b) имеет property c именем year_of_birth, которое при обращении к нему возвращает год рождения (базируясь на значении атрибута age)
 (также нужно будет проверить, что после изменения значения age, результат вызова property тоже изменяется)
c) можно итерироваться по атрибутам инстанса в цикле for
d) *реализует магические методы сравнения (__eq__, __ne__, __lt__, __le__, __gt__, __ge__), благодаря которым можно будет "сравнивать"
   разные инстансы этого класса:
   - при сравнении через операторы == и != должны проверятся ОБА атрибута инстанса: name и age,
   причем, name должен сравниваться БЕЗ УЧЕТА регистра
   - при сравнении через операторы >, <, >=, <= должно сравниваться только поле age!
"""


class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # your magic methods should be defined here ...


# TESTS for Task 2
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



