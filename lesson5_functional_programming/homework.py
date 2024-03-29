""" 1 """
import time

source = range(11)

result = dict(
    zip(
        source,
        list(
            map(lambda x: "even" if x % 2 == 0 else "odd", source)
        )
    )
)
print(result)

""" 2 """
result = list(map(lambda x: str(x), source))
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


# val = int(input("Enter the integer number:\n"))
val = 5
print(f"Result of 'some_func' with value {val}: {some_func(val)}")


""" 5 """


def analyze_string(string_value: str):
    message_parts = []
    try:
        num = float(string_value)
        message_parts.extend(
            (
                "положительное" if num >= 0 else "отрицательное",
                f"целое число: {int(num)}" if num.is_integer() else f"дробное число: {num}"
            )

        )
    except ValueError:
        message_parts.append(f"некорректное число: {string_value}")

    return "Вы ввели " + " ".join(message_parts)


for str_value in (
    "0",
    "1",
    "6.77",
    "-5",
    "-2.43",
    "123a",
):
    print(analyze_string(str_value))



