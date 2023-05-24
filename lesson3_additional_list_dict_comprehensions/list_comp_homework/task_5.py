"""5. Даны 2 списка:"""

list_1 = [1, 2, 3]
list_2 = [1, 2, 3, 4, 5]

"""С помощью list comprehension, создать новый список, содержающий все значения, 
полученные путем Декартова произведения элементов списков list_1 и list_2"""

sequence_result = [i * j for i in list_1 for j in list_2]
assert sequence_result == [1, 2, 3, 4, 5, 2, 4, 6, 8, 10, 3, 6, 9, 12, 15], f"Incorrect: {sequence_result}"
print(f"Result: {sequence_result}")

groups_result = [[i * j for j in list_2] for i in list_1]
assert groups_result == [[1, 2, 3, 4, 5], [2, 4, 6, 8, 10], [3, 6, 9, 12, 15]], f"Incorrect: {groups_result}"
print(f"Groups: {groups_result}")



