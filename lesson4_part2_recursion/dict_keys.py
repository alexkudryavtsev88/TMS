from typing import Callable, Any

CACHE = {}


def get_user_data(
    build_key_func: Callable[[str, str, int], Any],
    name: str,
    surname: str,
    age: int,
):
    """
    Простая реализация алгоритма получения данных с использованием кэширования
    В качестве кэша мы будем использовать обычный dict
    """
    key = build_key_func(name, surname, age)
    if (value := CACHE.get(key)) is not None:
        return value

    user_data = {
        'name': name,
        'surname': surname,
        'age': age
    }
    CACHE[key] = user_data
    return user_data


def build_key_tuple_with_immutables(
    name: str,
    surname: str,
    age: int
):
    """
    Кортеж - НЕизменяемый тип данных.
    Но объект кортежа может быть КЛЮЧОМ в Словаре
    тогда и только тогда, когда он содержит
    в себе объекты НЕизменяемых типов: int, float, bool, str
    или других Кортежей, содержащих НЕизменяемые типы
    """
    return name, (surname, (age, ))


def build_key_tuple_with_mutables(
    name: str,
    surname: str,
    age: int
):
    """
    В данном примере Кортеж НЕ может быть
    КЛЮЧОМ словаря, так как он содержит внутри себя
    объект типа list, который является Изменяемым
    """
    return name, surname, [age]


def build_key_set(
    name: str,
    surname: str,
    age: int
):
    """set - Именяемый объект и НЕ может быть КЛЮЧОМ словаря"""
    return {name, surname, age}


def build_key_list(
    name: str,
    surname: str,
    age: int
):
    """list - Именяемый объект и НЕ может быть КЛЮЧОМ словаря"""
    return [name, surname, age]


def build_key_dict(
    name: str,
    surname: str,
    age: int
):
    """dict - Именяемый объект и НЕ может быть КЛЮЧОМ другого словаря"""
    return {name: name, surname: surname, age: age}


# TEST
user_name = "Alex"
user_surname = "Kudryavtsev"
user_age = 34

for func in (
    build_key_list,
    build_key_set,
    build_key_dict,
    build_key_tuple_with_mutables,
    build_key_tuple_with_immutables
):
    try:
        user_data = get_user_data(
            func,
            user_name,
            user_surname,
            user_age,
        )
    except TypeError as exc:
        print(f"ERROR in {func.__qualname__}: {exc}")
    else:
        print(f"SUCCESS in {func.__qualname__}: value = {user_data}")



