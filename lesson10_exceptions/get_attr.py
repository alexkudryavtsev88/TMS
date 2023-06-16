from typing import Any


class MyClass:

    def __init__(self):
        self.name = None
        self.age = None

    def fill_data(self, data: dict[str, Any]):
        """
        setattr - добавляет атрибут с указанным строковым именем и соответствующим значением
        """
        for k, v in data.items():
            setattr(self, k, v)

    def get_attr_value(self, attr_name: str):
        """
        getattr - нужен для того, чтобы получить атрибут объекта (класса или инстанса),
        если мы получаем имя этого атрибута в виде строки
        """
        return getattr(self, attr_name, None)

    def __str__(self):
        return f"{self.name}, {self.age}"


obj = MyClass()

dict_ = {'name': 'Alex', 'age': 34}
obj.fill_data(data=dict_)
print(obj)

assert obj.get_attr_value(attr_name='name') == 'Alex'
assert obj.get_attr_value(attr_name='city') is None


""" hasattr - проверяет, есть у объекта атрибут с указанным именем """
assert hasattr(obj, "name") is True
assert hasattr(obj, "city") is False

""" delattr - удаляет, есть у объекта атрибут с указанным именем """
delattr(obj, 'name')
assert obj.__dict__ == {'age': 34}



