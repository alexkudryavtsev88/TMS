# ------------------------------------------------- #

class MyMetaClass(type):
    def __call__(cls, *args, **kwds):
        print("***** Here's My int *****", args)
        print("Cast str arguments to int ...")
        args = tuple(int(a) for a in args)
        return type.__call__(cls, *args, **kwds)


class Integer(metaclass=MyMetaClass):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def sum(self):
        return self.x + self.y


my_int = Integer("1", "2")
int1 = my_int.x
int2 = my_int.y

print(int1, type(int1))
print(int2, type(int2))

# ------------------------------------------------------ #

my_obj = type('MyNewClass', (Integer, ), {'x': 1, 'y': 2})
print(my_obj)
print(type(my_obj))

# ------------------------------------------------------ #


class Parent1:
    x = "some_x"


class Parent2:
    y = "some_y"


# Создание нового типа (класса) в Рантайме с использованием функции type
new_type = type("MyNewType", (Parent1, Parent2), {"attr": "some_attr"})
# где:
# - первый аргумент - имя создаваемого типа
# - второй аргумент - кортеж "родителей" для создаваемого типа
# - третий аргумент - дикт с атрибутами создаваемого типа
print(new_type)
print(new_type.attr)
print(new_type.__dict__["attr"])

instance = new_type()
print(instance)
instance.attr = "some_instance_attr"
assert instance.attr == "some_instance_attr"
assert instance.__class__.attr == "some_attr"
