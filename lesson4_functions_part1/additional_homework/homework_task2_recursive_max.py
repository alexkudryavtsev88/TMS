"""
Написать рекурсивную функцию, которая принимат на вход список целых чисел
и возвращает максимальное число в списке
"""

def recursive_max(some_list, deep=-1):
    deep += 1
    rshift = '\t' * deep
    print(f"{rshift} Текущая глубина рекурсии: {deep}")
    print(f"{rshift} Проверяем длину списка: {len(some_list)} == 1 -> {len(some_list) == 1}")
    if len(some_list) == 1:  # терминальные случай: если длина списка равна 1,
        print(f"{rshift} В списке {some_list} остался ровно 1 элемент: возвращаем элемент {some_list[0]}")
        return some_list[0]  # значит просто возвращаем единственный элемент этого списка

    max_element = recursive_max(some_list[1:], deep=deep) # рекурсивно вызываем функцию с аргументом
    print(f"{rshift} Текущая глубине рекурсии {deep}, MAX элемент равен {max_element}")
    # количество рекурсивных вызовов будет равно (Длина списка - 1)
    # каждый рекурсивный вызов будет возвращать 1 элемент списка

    if some_list[0] < max_element:
        print(
            f"{rshift} Сравниваем 1-й элемент списка {some_list} с MAX элементом: {some_list[0]} < {max_element}:",
            f"{rshift} Возвращаем MAX элемент {max_element}",
            sep = '\n'
        )
        return max_element
    else:
        print(
            f"{rshift} Сравниваем 1-й элемент списка {some_list} с MAX элементом: {some_list[0]} >= {max_element}:",
            f"{rshift} Возвращаем 1-й элемент списка {some_list[0]}",
            sep='\n'
        )
        return some_list[0]
"""
Test
"""

source = [2, 1, 0, 5, 7, 6, 4, 3]
print(source)
assert recursive_max(source) == 7