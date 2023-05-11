"""Условные ветвления: if, elif, else"""

x = 10

if x == 10:
    print('1 case!')  # первая "ветка": выполнится, если 1 условие - True
else:
    print('2 case!')  # вторая "ветка": выполнится, если 1 условие – False

# напечатает "1 case"


if x < 10:
    print("1 case!")  # первая "ветка": выполнится, если 1 условие - True
elif x > 10:
    print("2 case!")  # вторая "ветка": выполнится, если 2 условие - True
else:
    print("3 case!")  # вторая "ветка": выполнится, если условия 1 и 2 - False

# напечатает"3 case" 

"""
- Поток выполнения программы входит только в одну "ветку"
- выражений elif может быть сколь угодно много
- else выполняется тогда и только тогда, когда все условия, описанные в if/elif возвращают False
- Условные ветвления могут быть вложенными
"""

if x <= 10:
    print(x)
    if x == 10:
        ...

"""
Логические операторы and, or, not

Оператор and 

Если хотя бы один из операндов выражения с and равен False, то результат всего выражения будет False"""

x = True
y = False
z = False

print(x and y and z)
# False

"""
Оператор or 

Если хотя бы один из операндов выражения с or равен True, то результат всего выражения будет True"""

print(x or y or z)
# True

"""
Оператор not

оператор not инвертирует значение bool-типа, превращая False в True и наоборот"""

print(not (x and y and z))
# True

"""
ЦИКЛЫ

1. Цикл for – используется для итерирования по какой-либо конечной последовательности (например, список или строка)"""

my_list = [1, 2, 3, 4, 5]

# итерирование по элементам самого списка my_list
for element in my_list:
    print(element)

# итерирование по счетчику, величина которого равна длине списка – 1,
# и получение каждого элемента по индексу

for x in range(len(my_list)):
    print(my_list[x])

# если у нас есть два списка равной длины, и мы хотим, например, суммировать элементы обоих списков, стоящих на одинаковых позициях
my_list2 = [10, 11, 12, 13, 14]
for idx, element in enumerate(my_list):
    print(element + my_list2[idx])
# * функция enumerate создает пары индекс элемента – сам элемент

# for цикл c else
my_list = [10, 11, 12, 13, 14]
for i in my_list:
    print(i)
    if i == 15:
        break
else:   # else выполнится, если не был выполнен break внутри цикла
    print("END")

"""
2. Цикл while

Позволяет реализовать бесконечный цикл, который может прерваться в случае наступления определенного события"""

# Обход списка в цикле while 

my_list = [1, 2, 3, 4, 5]
counter = -1
condition = True

while condition:
    counter += 1
    if counter >= len(my_list) - 1:
        condition = False
    print(my_list[counter])

# ИЛИ проще 
counter = -1
while True:
    counter += 1
    if counter > len(my_list) - 1:
        break  # оператор break немедленно прерывает цикл
    print(my_list[counter])


# ** цикл for под капотом реализован примерно так:
def custom_for_loop(collection):
    iterator = iter(collection)
    while True:
        try:
            yield next(iterator)
        except StopIteration:
            break


# пример использования
my_list = ['A', 'B', 'C']
for element in custom_for_loop(my_list):
    print(element)

