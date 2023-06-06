""" 1 """
import time

my_func = lambda x: "even" if x % 2 == 0 else "odd"
source = range(11)
result = dict(
    zip(
        source,
        list(map(lambda x: my_func(x), source))
    )
)
print(result)

""" 2 """
result = list(map(lambda x: str(x), range(11)))
print(result)

""" 3 """
palindromes = [
    "Молебен о Коне Белом",
    "Я не Палиндром",
    "Искать такси",
    "Любая строка",
    "Аргентина манит Негра"
]
result = list(
    filter(
        lambda phrase: (
            phrase.lower().replace(" ", "")
            == phrase.lower().replace(" ", "")[::-1]
        ),
        palindromes
    )
)
print(result)
assert result == ["Молебен о Коне Белом", "Искать такси", "Аргентина манит Негра"]

""" 4 """


def show_time_decorator(func):
    def inner(*args, **kwargs):
        print("Hello from decorator!")
        start = time.perf_counter()
        func_result = func(*args, **kwargs)
        print(f"'{func.__qualname__}' execution time: {time.perf_counter() - start}")

        return func_result

    return inner


@show_time_decorator
def some_func(value: int):
    print("Hello from some_func!")
    time.sleep(value)
    value *= 10
    return value


val = int(input("Enter the integer number:\n"))
print(f"Result of 'some_func' with value {val}: {some_func(val)}")



