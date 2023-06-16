import traceback

"""
1. Необработанные исключения
"""
# result = 110 / 0

"""
Код выше:
- породит Исключение класса ZeroDivisionError, так как на 0 делить нельзя
- напишет в консоль стэк-трейс Исключения в "обратном порядке": это называется Traceback
-- Стэк вызовов (Call Stack) растет Вверх, а Исключение, порожденное во фрейме (Stack Frame) на
вершине Стэка вызовов, в выводе Traceback'а Исключения мы увидим в самом низу
- Питон-процесс завершится с exit code = 1
"""

"""
2. Обработка исключений
"""
def div(a: int, b: int):
    """
    Эта функция может завершится с Исключением ZeroDivisionError,
    если аргумент b будет равен 0
    """
    return a / b


def get_by_index(some_list, index_num):
    """
    Эта функция может завершится с Исключением IndexError,
    если аргумент index_num будет иметь значение > len(some_list) - 1
    """
    return some_list[index_num]

"""
2.1 Обработка нескольких Исключений по отдельности
"""

try:
    div(100, 0)
except ZeroDivisionError as err:
    traceback.print_exception(err)

try:
    get_by_index([1, 2, 3], index_num=4)
except IndexError as err:
    traceback.print_exception(err)

"""
traceback.print_exception(err) напечатает полный Traceback Исключения,
точно такой, какой мы бы увидели в случае, если бы НЕ обрабатывали Исключение.
Но, в данном случае, Питон-процесс НЕ завершается аварийно, а продолжает работать,
и мы увидим Traceback обоих Исключений.
"""

"""
2.2 Обработка нескольких исключений вместе
"""

try:
    div(100, 1)
    get_by_index([1, 2, 3], index_num=4)
except (ZeroDivisionError, IndexError) as err:
    # traceback.print_exception(err)
    print(err)

"""
В данном случае: 
- исключение случится при вызове функции div(100, 0)
- исключение обработаетя в Except блоке и мы увидим его Traceback в консоли
- get_by_index([1, 2, 3], index_num=4) даже не будет вызван, так как Исключение случилось ДО него
"""

"""
2.2 Обработка нескольких исключений вместе, но с разными действиями после того, как то или иное исключение произошло
"""

try:
    div(100, 0)
    get_by_index([1, 2, 3], index_num=4)
except ZeroDivisionError:
    print("Произошла ошибка деления на 0!")
except IndexError:
    print("Произошла ошибка обращения по несуществующему Индексу!")

"""
2.3 try/except/else
"""
import random

try:
    result = div(100, random.randint(0, 1))
except ZeroDivisionError:
    print("Произошла ошибка деления на 0!")
else:
    print(result)

"""
Код внутри блока else выполнится Только если Исключения ZeroDivisionError НЕ произошло
"""


"""
2.4 try/except/else/finally
"""

try:
    result = div(100, random.randint(0, 1))
except ZeroDivisionError:
    print("Произошла ошибка деления на 0!")
else:
    print(result)
finally:
    print("Bye!")

"""
Код внутри блока finally выполнится ВСЕГДА, независимо от того, произошло Исключение или нет
"""


"""
3. Виды Исключений
"""

"""
Популярные виды Исключений:
"""
#
value_error = ValueError
# возникает во многих случаях, например:
# - Попытка некоректно распаковать кортеж:
# a, b, c = [1, 2]
#
# - Попытка некорректного приведения типов:
# result = int("1!")
#
# - Попытка получить Индекс элемента из Списка, которого нет в Списке
# result = [1, 2, 3].index(5)
#
# index_err = IndexError
# возникает при обращении по несуществющему индексу в списке
# lst = [1, 2, 3]; res = lst[5]
#
#
# key_error = KeyError
# возникает при обращении по несуществющему ключу в словаре
# dct = {1: 1, 2: 2}; elem = dct[3]
#
# attribute_error = AttributeError
# возникает при попытке обращения к несуществующему атрибуту у Объекта или Класса
#
# lst = [1, 2, 3]; lst.add(4)
#
# type_error = TypeError
# возникает при попытке использовать Объект какого-либо типа не по назначению этого типа
# fake_func = "lambda x: x + 1"; fake_func()
#
"""
3.1 Наследование в Исключениях

- Все исключения, включая встроенные Исключения, Исключения, специфичные для каких-либо библиотек
и ваши собственные Исключения имеют самого базового родителя - класс Exception
- Вы можете обрабатывать ВСЕ возможные исключения в стиле:
"""

# try:
#     # do something
#     print("Success")
# except Exception:
#     print("Error")
#
# """ Однако, это не считается хорошим подходом, так как вы должны знать, какие конкретно Исключения
# вы собираетесь обрабатывать,
# или же, вы должны указать какого-то родителя ваших возможных исключений, менее общего, чем Exeption, например,
# """
#
from json.decoder import JSONDecodeError


def raise_json_error():
    raise JSONDecodeError('error', '{"1": "2"}', pos=1)


try:
    raise_json_error()
except ValueError as err:  # JSONDecodeError является прямым потомком ValueError
    traceback.print_exception(err)


"""
4. Создание собственных классов Исключений и порождение Исключений из них
"""


class MyCustomException(Exception):
    """
    my exception
    """

"""
Выше создания собственного класса исключения, унаслеованного от Exception
Внутри класса достаточно написать doc string с описанием Исключения
"""


dict_ = {1: "1", 2: "2", 3: "3"}
key = 4  # несуществующий ключ
try:
    result = dict_[key]
except KeyError as err:
    raise MyCustomException(f"Dict {dict_} doesnt contain key {key}") from err



