import asyncio
import contextlib


async def my_gen():
    for i in range(10):
        yield i


async def entry():
    async for i in my_gen():
        print(i)
    print("Iterator is ended")


class MyClass:

    def __init__(self):
        self.name = "Alex"
        self.age = 34

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v

        # OR
        # return iter(self.__dict__.items())


for name, value in MyClass():
    print(f"Name: {name}, Value: {value}")


@contextlib.contextmanager
def my_context_manager(src: list[int]):
    print(f"Src before: {src}")
    src.extend(range(5, 11))
    print(f"Src after: {src}")
    yield
    src.clear()


def main():
    my_list = [1, 2, 3]
    print("My list before: ", my_list)
    with my_context_manager(my_list):
        print("Hi")

    print("My list after: ", my_list)


main()

