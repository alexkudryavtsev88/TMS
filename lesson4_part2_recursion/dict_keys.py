CACHE = {}


def get_user_data(name, surname, age):
    default_message = """
    user_name={0}, user_surname={1}, user_age={2}
    """
    key = build_key(name, surname, age)
    if (value := CACHE.get(key)) is not None:
        return value

    user_message = default_message.format(
        name, surname, age
    )
    CACHE[key] = user_message
    return user_message


def build_key(name, surname, age):
    return name, surname, [age]


# TEST
user_name = "Alex"
user_surname = "Kudryavtsev"
user_age = 34

user_data = get_user_data(
    user_name,
    user_surname,
    user_age
)
print(user_data)


class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f'Name={self.name}, Age={self.age}'


