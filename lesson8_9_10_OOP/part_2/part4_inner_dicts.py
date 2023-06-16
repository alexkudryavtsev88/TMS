class MyClass:

    CLASS_ATTR = "test"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __iter__(self):
        inner_dict = self.__dict__
        for attr_name, attr_value in inner_dict.items():
            yield attr_name, attr_value

    def some(self):
        print()


my_obj = MyClass('alex', 34)
print(my_obj)

for k, v in my_obj:
    print(k, v)


print(my_obj.__dict__)
for k, v in my_obj.__class__.__dict__.items():
    print(f"{k} -> {v}")


class ClassWithoutDict:

    __slots__ = ("name", "age")  # строго задаем какие атрибуты может содержать наш будущий инстанс класса

    def __init__(self):
        self.name = "Alex"
        self.age = 34

    def __str__(self):
        return f"{self.name}, {self.age}"


x = ClassWithoutDict()
print(x)
try:
    print(x.__dict__)  # инстанс, у которого объявлены __slots__ НЕ ИМЕЕТ внутреннего дикта!
except AttributeError as exc:
    print(exc)

try:
    x.test = "123"  # нельзя присвоить НОВЫЙ атрибут
except AttributeError as exc:
    print(exc)


