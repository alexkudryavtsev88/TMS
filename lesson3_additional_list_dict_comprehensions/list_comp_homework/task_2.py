"""2. Дан список кортежей"""

my_list = [(1, 2, 3), (3, 4, 5), (5, 6, 7), (7, 8, 9)]

"""
C помощью list comprehension создать новый список, где каждый элемент будет представлять собой сумму элементов кортежа, 
расположенного на соответствующей позиции в списке my_list"""


result = [sum(tup) for tup in my_list]
expected_result = [6, 12, 18, 24]
assert result == expected_result, f"Result {result} != expected result {expected_result}"
print(f"Result: {result}")
