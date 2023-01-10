"""1. Дан список из 50 последовательных целых чисел:"""

my_list = list(range(1, 51))
print(f"Source list: {my_list}")
print(my_list.index(50))

"""C помощью цикла for получить новый список, который будет содержать элементы списка my_list в обратном порядке"""

# variant 1
var1_list = []
# создаем последовательность в обратном порядке: от последнего индекса списка (49) до 1-го индекса (0) включительно
backward_range = range(len(my_list) - 1, -1, -1)
for i in backward_range:
    var1_list.append(my_list[i])

# variant 2
var2_list = []
counter = len(my_list)
for i in range(counter):
    counter -= 1
    var2_list.append(my_list[counter])

assert var1_list == var2_list, f"Lists are not equal: {var1_list} != {var2_list}"
print('Lists are equals!', var1_list, var2_list, sep='\n')