import json

"""
Функция высшего порядка – это функция, которая может принимать в качестве аргумента другую функцию 
и/или возвращать функцию как результат работы. 

Примеры встроенных (build-in) HOD-функций: map, filter, reduce, рассмотренные ранеe


ДЕКОРАТОРЫ

- Являются Функциями высшего порядка, так как всегда принимают на вход объект функции и возвращают объект функции.
- Нужны, чтобы тем или иным образом расширить функциональные возможности функции, не меняя при этом ее внутренней логики 
- Декоратор без параметров выглядит как функция внутрь которой вложена другая функция
- Чтобы сделать декоратор с параметрами нужно добавить еще 1 уровень вложенности функций.


Декоратор без параметров - классический пример.
'Декорирует' переданную ему функцию, преобразуя ее результат в JSON объект.
"""

def to_json(func):
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        if not isinstance(result, dict):
            raise TypeError(f'Instance should be a dict, got {type(result)}')
        return json.dumps(result)
    return wrapped


"""
Декоратор to_json позволяет преобразовать результат выполнения функции (словарь) в JSON-объект
"""
def create_dict_from_list(lst):
    return {element: idx for idx, element in enumerate(lst)}


@to_json
def create_json_from_dict(lst):
    result = create_dict_from_list(lst)
    return result

"""
Декоратор с параметрами:
Например, мы захотели расширить возможности нашего декоратора to_json,
чтобы он мог принимать параметр sort_keys = True/False, и в зависимости
от это параметра применять сортировку по ключам в JSON или не применять
"""
def to_json_with_keys_sorting(sort_keys):
    def wrapper(func):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if not isinstance(result, dict):
                raise TypeError(f'Instance should be a dict, got {type(result)}')
            return json.dumps(result, sort_keys=sort_keys)
        return inner
    return wrapper


# Оборачивание в декоратор с параметрами
@to_json_with_keys_sorting(sort_keys=True)
def create_json_with_keys_sorted(lst):
    result = create_dict_from_list(lst)
    return result


@to_json_with_keys_sorting(sort_keys=False)
def create_json_with_keys_unsorted(lst):
    result = create_dict_from_list(lst)
    return result


my_list = ['Y', 'B', 'Z', 'H', 'J', 'C', 'A']
json_from_dict = create_json_from_dict(my_list)
assert isinstance(json_from_dict, str)
print(f"Json from Dict:             {json_from_dict}")

json_from_dict_unsorted_keys = create_json_with_keys_unsorted(my_list)
json_from_dict_sorted_keys = create_json_with_keys_sorted(my_list)

assert all(
    [
        isinstance(var, str) for var in (json_from_dict_unsorted_keys, json_from_dict_sorted_keys)
    ]
)
print(f'Json with unsorted keys:    {json_from_dict_unsorted_keys}')
print(f'Json with sorted keys:      {json_from_dict_sorted_keys}')


# Другой способ декорирования:

