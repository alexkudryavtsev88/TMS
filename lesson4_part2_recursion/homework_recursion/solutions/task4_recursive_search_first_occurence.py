"""
Изменить реализацию функции рекурсивного поиска элемента в словаре (из предыдущего задания)
следующим образом:
- функция должна находить ПЕРВОЕ соответствие имени и возвращать результат в виде словаря:

    {'val': found_value, 'parent': found_value_parent, 'deep': found_value_deep}
"""

from homework_recursion.source import source_dict

""" Task 4: recursive search until first match occur"""
def recursive_search_fist_match(src: dict, value: str, deep=-1, parent=None):
    result = None

    def _recursive_inner(src: dict, value: str, deep=-1, parent=None):
        nonlocal result

        if isinstance(src, dict):
            deep += 1
            for k, v in src.items():
                result = _recursive_inner(v, value, deep=deep, parent=k)
                if result:
                    return result
        elif isinstance(src, list):
            for item in src:
                result = _recursive_inner(item, value, deep=deep, parent=parent)
                if result:
                    return result
        elif isinstance(src, str) and src == value:
            # print(f'Found "{value}" on deep = {deep}, parent = {parent}')
            return {'val': value, 'parent': parent, 'deep': deep}

    return _recursive_inner(src, value, deep, parent)


""" TEST """

"""1. Find the first occurrence of lookup_name"""
# lookup_name = "Alex"
_dict = source_dict.get_source_dict_with_duplicates()

# value = recursive_search_fist_match(_dict, lookup_name)
# print(value)
# assert value == {'val': 'Alex', 'parent': 'key5', 'deep': 3}


"""2. Find all expected names"""
# _dict = source_dict.get_source_dict()
values = [
    ("Alex", {'val': 'Alex', 'parent': 'key5', 'deep': 3}),
    ("John", {'val': 'John', 'parent': 'key3', 'deep': 2}),
    ("Brad", {'val': 'Brad', 'parent': 'key3', 'deep': 2}),
    ('Kate', {'val': 'Kate', 'parent': 'key12', 'deep': 0}),
    ('Hans', {'val': 'Hans', 'parent': 'key11', 'deep': 5}),
    ('Louisa', {'val': 'Louisa', 'parent': 'key7', 'deep': 4}),

]
#
for lookup_value, expected_result in values:
    result = recursive_search_fist_match(_dict, lookup_value)
    print(result)
    assert result == expected_result, f"{result} != {expected_result}"

