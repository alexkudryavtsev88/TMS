"""
Пример реализации РЕКУРСИВНОЙ ФУНКЦИИ, которая ищет слово в словаре,
в котором значения ключей могут быть ТОЛЬКО строками или вложенными словарями
"""

def recursive_simple(src: dict, value: str):
    for k, v in src.items():
        if isinstance(v, dict):
            recursive_simple(v, value)
            # функция вызывает сама себя, используя в качестве аргумета 'src' переменную v, которая имеет тип dict
        else:
            if v == value:
                print(f"{value} is found!")
                return


src = {
    'key1': 'John',
    'key2': {
        'key3': 'Bob', 'key4': {
            'key5': 'Alex'
        }
    }
}
recursive_simple(src, 'Alex')  # напечатает 'Alex is found!'
recursive_simple(src, 'Bob')   # напечатает 'Alex is found!'
recursive_simple(src, 'Jessica')  # ничего не напечатает, так как слова 'Jessica' нет ни на одном уровне вложенности


"""
ВЛОЖЕННЫЕ ФУНКЦИИ И ОБЛАСТИ ВИДИМОСТИ ПЕРЕМЕННЫХ
"""

def func_with_closure():
    A = 0
    B = 0

    def inner_a(a):
        nonlocal A
        A += 1
        # nonlocal позволяет вложенной функции inner_a видеть и изменять переменную А,
        # объявленную в родительской функции

    def inner_b(b):
        b += 1
        return b
        # B += 1
        # если раскомментировать строку B += 1, то будет ошибка,
        # так как функция inner_b НЕ видит переменную B из родительской функции

    inner_a(A)
    # Здесь функция inner_a принимает значение переменной A из родительской функции как аргумент a,
    # и ничего не делает с этим своим аргументом.
    # Но inner_a изменят переменную A из родительской функции.

    C = inner_b(B)
    # функция inner_b принимает значение переменной B из родительской функции как аргумент b,
    # и увеличивает значение аргумента на 1.
    # При этом изменяется только значение аргумента b, который живет только внутри функции inner_b
    # и далее, функция возвращает значение измененного аргумента b.
    # Значение переменной B из родительской функции при этом не меняется!

    print(A)  # A будет равно 1, так как функция inner_a изменила значение A
    print(B)  # B будет равно 0, так как функция inner_b НЕ изменила значение B
    print(C)  # С будет равно 1, так как мы записали в переменную С результат функкции inner_b


func_with_closure()

