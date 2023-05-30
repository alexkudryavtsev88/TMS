"""
Области видимости переменных: ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ (globals)
"""


"""1. Глобальные переменные объявляются, как правило, вверху модуля (но ниже чем импорты). 
Записываются большими буквами и через _ """
GLOBAL_STRING = "GLOBAL_STRING"
GLOBAL_INT = 0

"""Плохая практика - делать изменяемые объекты (list, dict, set) Глобальными!!!"""
GLOBAL_LIST = [1, 2, 3, 4, 5]

"""2. Глобальные переменные видит весь остальной код в модуле: функции, классы и т.д."""
def func(a):
    print(f"a = {a}, GLOBAL_INT = {GLOBAL_INT}") # функция видит переменную GLOBAL_INT


class MyClass:
    class_variable = GLOBAL_STRING  # GLOBAL_STRING видна и внутри класса


"""Если Глобальная переменная - это ссылка на ИЗМЕНЯЕМЫЙ объект, 
то мы можем изменить этот объект изнутри функции через эту переменную"""
def func1():
    GLOBAL_LIST.pop()  # удалит последний элемент списка


func1()
print(GLOBAL_LIST)  # напечатает: [1, 2, 3, 4]

"""Если Глобальная переменная - это ссылка на НЕИЗМЕНЯЕМЫЙ объект, 
то мы НЕ можем просто взять и изменить значение этой переменной"""

def func2():
    GLOBAL_INT += 1  # ОШИБКА!


"""Чтобы изменить значение Глобальной переменную, которая ссылается на НЕИЗМЕНЯЕМЫЙ объект, то чтобы """
def func3():
    global GLOBAL_INT
    GLOBAL_INT += 1  # а вот здесь ошибки уже не будет


print(GLOBAL_INT)
func3()
print(GLOBAL_INT)


"""Все Глобальные переменные хранятся в дикте, чтобы получить доступ к нему, нужно вызвать функцию globals()"""
def print_globals():
    my_global_vars = globals()
    for name, value in my_global_vars.items():
        print(f"name: {name} -> value: {value}")

print_globals()


# Примечание: если вынести код из функции print_globals() на уровень модуля: то он не сработает!
# 1. Переменная my_global_vars будет являться Глобальной и одновременно хранить ссылку
# на дикт всех Глобальных переменных
# 2. Временные переменные name и value - тоже будут глобальными переменными.
# Но так как они меняют свои значения по ходу цикла, то мы получим ошибку:
#   RuntimeError: dictionary changed size during iteration