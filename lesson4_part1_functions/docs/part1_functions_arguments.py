"""
Функции и их аргументы
"""

"""
Функция отдельный блок кода который будет выполнен тогда и только тогда, когда функция будет явно вызвана
"""


def my_func():
    print("Hello!")


my_func()  # если закомментировать вызов функции, то Hello не напечатается!

"""
Аргументы и вызов функций
"""

"""1. Функция может принимать N аргументов или не понимать их вообще"""

def void_func():
    print("I have no arguments!")

def func_with_args(a, b, c):
    print(a, b, c, sep=', ')


"""2. Когда мы вызываем функцию и передаём в нее параметры (значения) - эти значения мапятся 
(от англ. Map - Отображение) на Aргументы этой функции."""

func_with_args(10, 20, 30)

"""Если мы передали параметров меньше/больше, чем у функции аргументов, то мы получим ошибку."""

# Примеры:
# func_with_args()
# func_with_args(1, 2)
# func_with_args(1, 2, 3, 4)

"""3. Аргументы есть позиционные и именованные. Если мы передаём параметры в функцию без указания имён аргументов, 
то мы используем позиционные аргументы - то есть соответствие "параметр -> аргумент" будет в строгом порядке."""

func_with_args(1, 2, 3)  # напечатает: 1, 2, 3
func_with_args(3, 2, 1)  # напечатает: 3, 2, 1

"""Если же мы, вызывая функцию, указываем имя аргумента перед каждым параметром - это именованные аргументы, 
тут уже порядок того, как мы их указали не важен."""
func_with_args(a=1, b=2, c=3)  # напечатает: 1, 2, 3
func_with_args(c=3, b=2, a=1)  # напечатает: 1, 2, 3

"""Но важно чтобы указанное имя аргумента было действительным, иначе ошибка."""

# func_with_args(a=3, b=2, d=1)  # ОШИБКА!

"""4. При вызове функции с позиционными и именованными аргументами, позиционные должны быть указаны перед именованными."""
func_with_args(1, 2, c=3)
# func_with_args(a=1, 2, c=3) # ОШИБКА!

"""5. В описании функции мы можем указать дефолтное значение аргумента - оно будет применено, 
если при вызове функции соответствующий параметр не был передан вовсе."""

def func_with_default(arg1, arg2, arg3=0):
    print(arg1, arg2, arg3, sep=', ')

func_with_default(10, 20, 30)  # напечатает: 10, 20, 30
func_with_default(10, 20)  # напечатает: 10, 20, 0

"""6. Самое абстрактное описание функции:"""


def func_with_abstract_args(*args, **kwargs):
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")


"""Функция с такой сигнатурой может принимать любое количество позиционных 
и именованных аргументов или не принимать ни одного из них"""

func_with_abstract_args()
func_with_abstract_args(1, 2, 3)
func_with_abstract_args("ABC", name="Alex", age=34)

"""Позиционные аргументы args хранятся в кортеже, именованные kwargs в дикте.
Оператор * "распаковывает" кортеж, ** распаковывает дикт."""

