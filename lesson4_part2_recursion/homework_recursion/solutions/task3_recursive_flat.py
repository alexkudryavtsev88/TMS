"""
Написать рекурсивную функцию, которая принимает на вход Список со следующей структурой:

-- Список может содержать числа и/или вложенные списки
-- вложенные списки повторяют структуру родительского списка (содержат числа и/или вложенные списки)
-- уровень вложенности не определен

Функция должна возвращать новый список, который будет содержать все элементы из входного списка и вложенных в него списков (на одном уровне)

Примеры входных списков:
"""

""" Task 3: recursive flat """

def recursive_flat(some_list):
    if not some_list:
        return some_list
    if isinstance(some_list[0], list):
        return recursive_flat(some_list[0]) + recursive_flat(some_list[1:])
    return some_list[:1] + recursive_flat(some_list[1:])

"""
Пример
"""
source_list_1 = [[1, 2], [3, 4], [5, 6]]
print(source_list_1)
assert recursive_flat(source_list_1) == [1, 2, 3, 4, 5, 6]

source_list_2 = [1, [2, 3], [4, 5, [6]], [7, 8], 9, 10]
print(source_list_2)
assert recursive_flat(source_list_2) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

source_list_3 = [[1, 2], [3, 4, [5, 6]], [7, 8, [9, 10, [11, 12]]]]
print(source_list_3)
assert recursive_flat(source_list_3) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

"""
ПРИМЕЧАНИЕ:
Помните, что списки поддерживают слияние через метаметический оператор +

merged = [1, 2, 3] + [3, 4, 5]
>> [1, 2, 3, 3, 4, 5,]
"""

