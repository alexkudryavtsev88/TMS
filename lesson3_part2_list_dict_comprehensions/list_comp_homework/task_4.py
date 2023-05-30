"""4. Даны три списка равной длины:"""

list_1 = [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
list_2 = [(3, 3, 3), (2, 2, 2), (1, 1, 1)]
list_3 = [(2, 2, 2), (3, 3, 3), (4, 4, 4)]

"""Каждый элемент Каждого списка представляет собой кортеж из 3-х элементов.

Задание:

Получить новый список, длиной равной длинам списков x, y и z, где элемент i будет представлять собой произведение типа: 

  1-й элемент кортежа i списка x * 2-й элемент кортежа i списка y * 3-й элемент кортежа i списка z"""


result = [element[0] * list_2[idx][1] * list_3[idx][2] for idx, element in enumerate(list_1)]
expected_result = [6, 12, 12]
print(result)
assert result == expected_result, f"Result {result} != expected result {expected_result}"