from dataclasses import dataclass


@dataclass(frozen=True)
class MyPerson:
    name: str = "John"
    age: int = 35

    def __str__(self):
        return f'{self.name}, {self.age}'

    @classmethod
    def build(cls, name, age, my_list):
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

        return cls(name=name, age=age)
