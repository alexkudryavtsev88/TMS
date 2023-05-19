"""Условные ветвления: if, elif, else"""

x = 10

if x == 10:
    print('1 case!')  # первая "ветка": выполнится, если 1 условие - True
else:
    print('2 case!')  # вторая "ветка": выполнится, если 1 условие – False

print("*" * 30)

# напечатает "1 case"

if x < 10:
    print("1 case!")  # первая "ветка": выполнится, если 1 условие - True
elif x > 10:
    print("2 case!")  # вторая "ветка": выполнится, если 2 условие - True
else:
    print("3 case!")  # вторая "ветка": выполнится, если условия 1 и 2 - False

# напечатает "3 case"

print("*" * 30)

"""
- Поток выполнения программы входит только в одну "ветку"
- выражений elif может быть сколь угодно много
- else выполняется тогда и только тогда, когда все условия, описанные в if/elif возвращают False
- Условные ветвления могут быть вложенными
"""

if x <= 10:
    print(f'{x} <= 10!')
    if x == 10:
        print(f'{x} == 10!')
    else:
        print(f'{x} < 10!')
else:
    print(f"{x} > 10")

print("*" * 30)

"""
Логические операторы and, or, not

Оператор and 

Если хотя бы один из операндов выражения с and равен False, то результат всего выражения будет False"""

x, y, z = True, False, False

print(f'AND result: {x and y and z}')
# False

"""
Оператор or 

Если хотя бы один из операндов выражения с or равен True, то результат всего выражения будет True"""

print(f'OR result: {x or y or z}')
# True

"""
Оператор not

оператор not инвертирует значение bool-типа, превращая False в True и наоборот"""

print(f"NOT result: {not (x and y and z)}")
# True

print("*" * 30)


def check_true_or_false(name1, age1, name2, age2):
    print(f'{name1}, {age1}, {name2}, {age2}')
    if (name1 and age1) or (name2 and age2):
        print("SUCCESS!")
    else:
        print("FAILURE!")


# TEST
data = [
    # all parameters exist
    ('Alex', 30, 'John', 40),
    # One of parameter doesn't exist
    (None, 30, 'John', 40),
    ('Alex', None, 'John', 40),
    ('Alex', 30, None, 40),
    ('Alex', 30, 'John', None),
    # 2 parameters doesn't exist
    (None, None, 'John', 40),
    ('Alex', 30, None, None),
    (None, 30, None, 40),
    ('Alex', None, 'John', None),
    (None, 30, 'John', None),
    ('Alex', None, None, 40),
    # 3 parameters doesn't exist
    ('Alex', None, None, None),
    (None, 30, None, None),
    (None, None, 'John', None),
    (None, None, None, 40),
    (None, None, None, None),
]

for a, b, c, d in data:
    check_true_or_false(a, b, c, d)

print("*" * 30)


"""
ЦИКЛЫ

1. Цикл for – используется для итерирования по какой-либо конечной последовательности (например, список или строка)"""

my_list = [1, 2, 3, 4, 5]

# итерирование по элементам самого списка my_list
for element in my_list:
    print(element)

print("*" * 30)

# итерирование по счетчику, величина которого равна длине списка – 1,
# и получение каждого элемента по индексу

for x in range(len(my_list)):
    print(my_list[x])

print("*" * 30)

# если у нас есть два списка РАВНОЙ ДЛИНЫ, и мы хотим, например,
# суммировать элементы обоих списков, стоящих на одинаковых позициях
list1 = [10, 20, 30, 40, 50]
list2 = [100, 200, 300, 400, 500]
for idx, list1_element in enumerate(my_list):
    list2_element = list2[idx]
    result = list1_element + list2_element
    print(result)

print("*" * 30)

# * функция enumerate создает пары: (индекс элемента, сам элемент)
# ПРИМЕЧАНИЕ: на самом деле функция enumerate возвращает на каждой итерации не сам индекс элемента,
# а целое число, которое соответствует индексу текущего элемента, если функция enumerate
# была вызвана БЕЗ дополнительного аргумента start (по умолчанию он равен 0)

# for цикл c else
my_list = [10, 11, 12, 13, 14]
for i in my_list:
    print(i)
    if i == 15:
        print("Break the loop!")
        break   # оператор break немедленно прерывает ВЕСЬ ЦИКЛ
        print("Hello after break!")  # эта строка кода НИКОГДА не будет выполнена
    if i == 11:
        print("Go to the next iteration!")
        continue  # оператор coninue немедленно прерывает ТЕКУЩУЮ ИТЕРАЦИЮ ЦИКЛА
        print("Hello after continue!")  # эта строка кода НИКОГДА не будет выполнена
    print('Hello at the END of iteration!')  # если в цикле случился break, эта стока кода НЕ будет выполнена
else:   # код внутри else выполнится, если в цикле не был выполнен break
    print("END")

print("*" * 30)

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

