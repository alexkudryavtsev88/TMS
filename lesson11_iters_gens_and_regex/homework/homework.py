"""
Задание:

Реализовать 2 класса:
- Класс RandomValueIterator должен описывать ITERATOR объект
- Класс RandomValue должен описывать ITERABLE объект, использующий Итератор, который описывает класс RandomValueIterator

- Реализация RandomValueIterator:
-- Итератор должен отдавать рандомное число от 1 до 100 включительно, при каждом обращении к нему.
-- Количество обращений должно быть фиксировано, скажем, 50 (или вы можете установить свой лимит).
-- Величина лимита должна передаваться через __init__
-- При достижении лимита Итератор должен напечатать сообщение "Iterator is stopped!" и завершиться

-- Проверить реализацию следующим образом:
"""
import random


class RandomValue:

    """Your implementation here"""


class RandomValueIterator:

    """Your implementation here"""


my_limit = int(input("Введите лимит: "))
my_random = RandomValue(limit=my_limit)

results = [elem for elem in my_random]
print(results)

assert len(results) == my_limit
for i in results:
    assert i is not None

