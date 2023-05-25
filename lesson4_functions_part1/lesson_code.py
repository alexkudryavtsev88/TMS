GLOBAL_VAR = "TEST"
GLOBAL_X = [1, 2, 3]

from typing import Callable


def test1(x, y, z):
    print(x, y, z)

def test2():
    print(x)
    print("hello")


def test3(x, y):
    print(x, y, sep=', ')

def work_func(a):
    print(a)
    b = 500
    print(b)
    def inner(c):
        nonlocal b
        b += 100
        print(b)
        print(c)
    inner(b)
    print(b)

def work_func2(fn: Callable[[int, int], None], a: int, b: int):
    print(a, b)
    fn(a, b)
    return test1

result = work_func2(test3, 100, 200)
result(22, 33, 44)


