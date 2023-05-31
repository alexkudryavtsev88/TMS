"""
Дан входной словарь
- Ключи словаря - строки
- Значениями ключей могут быть:
-- Строки
-- Словари
-- Списки

Все элементы-словари, как и родительский словарь, могут содержать строки, списки и другие вложенные словари
Все Элементы-списки могут содержать строки, словари и другие вложенные списки

Написать рекурсивную функцию, которая:
- Принимает на вход следующие аргументы:
-- 1 аргумент: исходный словарь
-- 2 аргумент: слово, которое нужно найти в словаре (строка)
-- аргумент deep с дефолтным целочисленным значением, отображающим текущий уровень вложенности (глубину) словаря
-- аргумент parent с дефолтным значением None, который сохраняет родителя (ключ словаря) на текущем уровне вложенности

- Делает обход словаря в глубину и поиск указанного значения
- Если значение найдено: печатает строку f"Значение {val} найдено на глубине {deep}"


* будет ли ваша функция искать слово до первого совпадения или найдет все имеющиеся совпадения - не важно
* понятие "уровень вложенности" или "глубина" касается только вложенных словарей!
"""


def get_source_dict():
    return {
        "key1": "John",  # deep 0
        'key2': {
            'key3': 'Ann',  # deep 1
            'key4': {
                'key5': ['Kate', 'Mary'],  # deep 2
                'key6': {
                    'key7': [
                        'Bob',  # deep 3
                        'Duke',
                        {
                            'key8': {  # deep 4
                                'key9': [  # deep 5
                                    'Lisa',
                                    {
                                        'key10': ['Mark', 'Alex']  # deep 6
                                    }
                                ],
                                "key11": "Louisa",  # deep 5
                            }
                        },
                        "Alex",  # deep 3
                    ]
                },
            },
            'key12': 'Robert'  # deep 1
        },
        "key13": "Ronaldo"  # deep 0
    }


def recursive_search():  # функция должна принимать указанные по заданию аргументы
    pass  # реализация алгоритма


# TEST
_dict = get_source_dict()
values = [
    ("John", {'val': 'John', 'parent': 'key1', 'deep': 0}),
    ("Ann", {'val': 'Ann', 'parent': 'key3', 'deep': 1}),
    ('Kate', {'val': 'Kate', 'parent': 'key5', 'deep': 2}),
    ('Mary', {'val': 'Mary', 'parent': 'key5', 'deep': 2}),
    ('Bob', {'val': 'Bob', 'parent': 'key7', 'deep': 3}),
    ('Duke', {'val': 'Duke', 'parent': 'key7', 'deep': 3}),
    ('Lisa', {'val': 'Lisa', 'parent': 'key9', 'deep': 5}),
    ("Mark", {'val': 'Mark', 'parent': 'key10', 'deep': 6}),
    ("Alex", {'val': 'Alex', 'parent': 'key10', 'deep': 6}),  # have Duplicate!
    ('Louisa', {'val': 'Louisa', 'parent': 'key11', 'deep': 5}),
    ('Robert', {'val': 'Robert', 'parent': 'key12', 'deep': 1}),
    ('Ronaldo', {'val': 'Ronaldo', 'parent': 'key13', 'deep': 0})
]
for lookup_value, expected_result in values:
    result = recursive_search(_dict, lookup_value)
    print(result)
    assert result == expected_result, f"{result} != {expected_result}"