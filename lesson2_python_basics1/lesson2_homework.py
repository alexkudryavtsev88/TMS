''' LESSON 2 '''

'''1. 2 переменные с одинаковыми данными и одинаковыми идентификаторами в памяти'''

str1, str2, str3 = "TEST", "TEST", "TEST"

assert str1 is str2 is str3

'''2. 2 переменные с одинаковыми данными, но разными идентификаторами в памяти'''


list1 = [1, 2, 3]  # создаете список целых чисел, ссылка на который хранится в переменной l1
list2 = [1, 2, 3]  # создаете список целых чисел, равный списку l1, ссылка на который хранится в переменной l2
list3 = list2  # создаете ссылку l3 на УЖЕ существующий объект l2

assert list2 == list1
assert list2 is not list1
assert list3 is list2

print(f"""
1 task:
  content: l1 = {list1}, l2 = {list2}, l3 = {list3}
  mem location: l1 = {id(list1)}, l2 = {id(list2)}, l3 = {id(list3)}
""")

x, y = 1, 1.0  # x равен y по ЗНАЧЕНИЮ, но у них разные адреса в памяти, т.к. это разные типы
assert x == y
assert x is not y

s1 = {1, 2, 3}
s2 = {1, 2, 3}

'''*3 '''

a, b, c = list(str1), list(str2), list(str3)
assert a is not b is not c

d, e = bool(list1), bool(list3)
assert d is e


'''
4
'''
input_str = input("Введите строку: ")
odd = input_str[::2]
even = input_str[1::2]
print(odd, even, sep=", ")
# print("введенная строка:", input_str.strip(), end="\n" * 2)
# print(odd, even, sep=' ' * 5, end="\n!!!")