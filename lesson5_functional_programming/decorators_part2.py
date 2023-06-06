import json


def create_dict_from_list(lst):
    return {element: idx for idx, element in enumerate(lst)}


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
    print("I'm decorator!")
    def wrapper(func):
        print("I'm decorator wrapper!")
        def inner(*args, **kwargs):
            print("I'm decorator wrapper inner!")
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
        isinstance(var, str) for var in (
            json_from_dict_unsorted_keys,
            json_from_dict_sorted_keys
        )
    ]
)
print(f'Json with unsorted keys:    {json_from_dict_unsorted_keys}')
print(f'Json with sorted keys:      {json_from_dict_sorted_keys}')

