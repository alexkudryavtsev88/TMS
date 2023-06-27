from dataclasses import dataclass


@dataclass(frozen=True)
class MyDataClass:
    a: str
    b: int
    c: list

    def __str__(self):
        return f'{self.a}, {self.b}: {self.c}'

    @classmethod
    def build(cls, a, b, c):
        values = locals()
        expected_values = cls.__annotations__  # returns dict with attributes names mapped with their types
        print(expected_values)
        for attr_name, attr_type in expected_values.items():
            actual = values.get(attr_name)
            if not isinstance(actual, attr_type):
                raise TypeError(
                    f"Attribute '{attr_name}' should have "
                    f"type {attr_type}, got: {type(actual)}"
                )

        return cls(a=a, b=b, c=c)


# Тесты для задания 1: должны отработать без ошибок!
person1 = MyDataClass.build("TEST", 34, [1, 2, 3])  # valid parameters
print(person1)
try:
    person2 = MyDataClass.build(100, 33, [1, 2, 3])  # invalid parameters
except Exception as exc:
    print(exc)

try:
    person3 = MyDataClass.build("TEST", "33", [1, 2, 3])  # invalid parameters
except Exception as exc:
    print(exc)

try:
    person3 = MyDataClass.build("TEST", 33, (1, 2, 3))  # invalid parameters
except Exception as exc:
    print(exc)
