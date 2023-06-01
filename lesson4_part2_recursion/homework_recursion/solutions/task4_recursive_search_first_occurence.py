"""
Изменить реализацию функции рекурсивного поиска элемента в словаре (из предыдущего задания)
следующим образом:
- функция должна находить ПЕРВОЕ соответствие имени и возвращать результат в виде словаря:

    {'val': found_value, 'parent': found_value_parent, 'deep': found_value_deep}
"""

from homework_recursion.source import source_dict

""" Task 4: recursive search"""
def recursive_search(source: dict, lookup_value: str, deep=-1, parent=None):
    result = None

    def _recursive_inner(src: dict, lookup: str, deep_=-1, parent_=None):
        nonlocal result

        if isinstance(src, dict):
            deep_ += 1
            for key, val in src.items():
                if result := _recursive_inner(
                    val, lookup, deep_, key
                ):
                    return result
        elif isinstance(src, list):
            for item in src:
                if result := _recursive_inner(
                    item, lookup, deep_, parent_
                ):
                    return result
        elif isinstance(src, str) and src == lookup:
            return {'val': lookup, 'parent': parent_, 'deep': deep_}

    return _recursive_inner(source, lookup_value, deep, parent)


""" TEST """

"""1. Find all expected names"""
_dict = source_dict.get_source_dict()
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




