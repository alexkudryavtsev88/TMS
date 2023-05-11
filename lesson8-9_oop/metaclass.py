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