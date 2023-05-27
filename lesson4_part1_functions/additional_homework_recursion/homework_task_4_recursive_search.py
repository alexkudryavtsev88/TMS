"""
Изменить реализацию функции рекурсивного поиска элемента в словаре (из предыдущего задания)
следующим образом:
- функция должна находить ПЕРВОЕ соответствие имени и возвращать результат в виде словаря:

    {'val': found_value, 'parent': found_value_parent, 'deep': found_value_deep}

"""

""" Task 4: recursive search until first match occur"""
def recursive_search(src: dict, value: str, deep=-1, parent=None):
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
            return {'val': value, 'parent': parent, 'deep': deep}

    return _recursive_inner(src, value, deep, parent)


""" Source dict """
def get_source_dict():
    return {
        "key1": "John",  # deep 0
        'key2': {
            'key3': 'Alex',  # deep 1
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
                                        'key10': ['Mark']  # deep 6
                                    }
                                ]
                            }
                        }
                    ]
                },
            },
            'key8': 'Robert'  # deep 1
        }
    }

""" Test """
source_dict = get_source_dict()
values = [
    ("Alex", {'val': 'Alex', 'parent': 'key3', 'deep': 1}),
    ("Mary", {'val': 'Mary', 'parent': 'key5', 'deep': 2}),
    ('Duke', {'val': 'Duke', 'parent': 'key7', 'deep': 3}),
    ('Mark', {'val': 'Mark', 'parent': 'key10', 'deep': 6})
]

for lookup_value, expected_result in values:
    result = recursive_search(source_dict, lookup_value)
    assert result == expected_result, f"{result} != {expected_result}"
