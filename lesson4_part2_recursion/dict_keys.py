from typing import Callable, Any

CACHE = {}


def get_user_data(
    build_key_func: Callable[[str, str, int], Any],
    name: str,
    surname: str,
    age: int,
):
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
) -> tuple[str, str, tuple[int]]:
    return name, surname, (age, )


def build_key_tuple_with_mutables(
    name: str,
    surname: str,
    age: int
) -> tuple[str, str, list[int]]:
    return name, surname, [age]

def build_key_set(
    name: str,
    surname: str,
    age: int
) -> set[str, str, int]:
    return {name, surname, age}

def build_key_list(
    name: str,
    surname: str,
    age: int
) -> list[str, str, int]:
    return [name, surname, age]


# TEST
user_name = "Alex"
user_surname = "Kudryavtsev"
user_age = 34

for func in (
    build_key_list,
    build_key_set,
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
        print(exc)
    else:
        print(user_data)



class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f'Name={self.name}, Age={self.age}'


