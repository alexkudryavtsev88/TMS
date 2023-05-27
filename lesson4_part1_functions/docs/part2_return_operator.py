"""
Оператор return
"""

"""1. Даже если функция не имеет оператора return - она все равно возвращает значение None - когда весь код внутри функции 
будет выполнен и если будет выполнен без "исключений" (Exceptions)"""


def func_with_no_return(a: int, b: int):
    a += 10
    b += 20
    print(a, b)


result = func_with_no_return(1, 2)
assert result is None

"""2. Оператор return не только возвращает значение - он ещё является точкой выхода из функции. 
Код, написанный внутри функции после return и на одном уровне с return - никогда не будет выполнен 
(аналогично как операторы break/continue) в циклах"""


def func_with_return(a: int):
    a += 10
    return a
    print("Hello!")  # Pycharm подсказывает что этот код не досягаем


func_with_return(10)

"""3. Оператор return может быть вложен в какое-то условие (if) внутри функции. 
Тогда, если это условие выполнилось, осуществится немедленный выход из функции."""


def func_with_early_return(a: int, b: int):
    if b == 0:
        print("You can't divide to zero!")
        return  # Эквивалентно записи return None

    result = a / b
    print(f'result is {result}')
    return result


func_with_early_return(10, 20)
func_with_early_return(10, 0)


"""4. Функция может возвращать несколько значений"""
def func_with_return_two_values(a: int, b: int):
    a += 10
    b += 20
    print(a, b)
    return a, b


"""На вызывающей стороне, результат функции возвращающей несколько значений - это кортеж этих значений"""
result = func_with_return_two_values(10, 20)
assert isinstance(result, tuple)

first_value, second_value = func_with_return_two_values(100, 200)  # можем распаковать кортеж в 2 переменные


