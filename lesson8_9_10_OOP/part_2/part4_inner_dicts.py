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


