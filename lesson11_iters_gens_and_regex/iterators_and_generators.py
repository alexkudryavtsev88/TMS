import typing

"""
ИТЕРИРУЕМЫЕ ОБЪЕКТЫ (Iterable)
"""

class ListWrapper:
    """
    Данный класс:
    - создает внутри себя список из полученных на этапе инициализации аргументов
    - позволяет итерироваться по экземпляру, реализуя метод __iter__
    """
    def __init__(self, *args):
        self._list = list(args)

    def __str__(self):
        return f"MyList object: {self._list}"

    def __iter__(self):
        """
        Метод __iter__ возващает ссылку на Объект-Итератор, класс которого реализован ниже
        """
        return ListWrapperIterator(self._list)


"""
ИТЕРАТОРЫ (Iterators)
"""

class ListWrapperIterator:
    """
    Данный класс реализует интерфейс Итератора (пригоден только для работы со списками)
    """

    def __init__(self, some_list):
        self._some_list = some_list  # неизменнно с момента инициализации
        self._size = len(self._some_list)  # неизменнно с момента инициализации
        self._curr_index = 0  # увеличивается на 1 при каждом вызове __next__!

    def __iter__(self):
        """
        Для совместимости объектов-итераторов с iterable-объектами,
        класс итератора должен реализовывать метод __iter__, который
        лишь возвращает ссылку на свой же экземпляр
        """
        return self

    def __next__(self):
        """
        Метод __next__ объекта-итератора реализует логику получения следующего элемента из последовательности
        В данном случае, атрибут экземпляра '_curr_index' хранит текущее значение индекса и увеличивается на 1
        при каждом вызове метода __next__, пока не будет достигнут лимит
        """
        if self._curr_index < self._size:
            # 1. Получить элемент из внутреннего списка по индексу 'self._curr_index'
            result = self._some_list[self._curr_index]
            # 2. Увеличить значение 'self._curr_index' на 1
            self._curr_index += 1
            # 3. Вернуть полученный элемент
            return result
        else:
            # необходимо выбросить StopIteration исключение, если значение 'self_curr_index'
            # достигло значеня 'self._size' value - это значит, что внутренний список "закончился"
            # и дальнейшие вызовы __next__ попросту не имеют смысла
            raise StopIteration


my_list = ListWrapper(1, 2, 3, 4, 5)
print(my_list)

"""
Так как my_list это ссылка на экземпляр класса ListWrapper, который реализует 
метод __iter__ - значит экземпляр класса ListWrapper является Iterable-объектом
и по нему можно итерироваться с помощью цикла for
"""
for element in my_list:
    # Цикл for не знает точное количество раз, сколько раз ему нужно повторяться -
    # он повторяется до тех пор, пока не встретит StopIteration - обработает это исключение
    # и завершится без ошибок
    print(element)

"""
Реазилация цикла for под капотом:
"""


def for_loop(some_iterable: typing.Iterable):
    iterator = iter(some_iterable)  # получает Итератор у Итерэйбл-объекта
    while True:                     # бесконечный цикл while
        try:
            return next(iterator)   # возвращает результат вызова iterator.__next__
        except StopIteration:       # ловит StopIteration, если это исключение произошло
            break                   # прерывает цикл while


"""
ГЕНЕРАТОРЫ (Generators)
"""

"""
1. Объект-генератор реализуют интерфейс Итератора: в самом общем смысле, Генератор это и есть Итератор. 
Причем, чтобы написать свой Итератор, используя Генератор, не нужно описывать отдельный класс с методами 
__iter__ и __next__ 
"""


# my_gen - функция-генератор, так как содержит оператор yield
def my_gen(some_list):
    for i in some_list:
        yield i


my_list = [1, 2, 3, 4, 5]
my_iterator = my_gen(my_list)  # вызов функции-генератора НЕ выполняет код внутри функции - он лишь
# возвращает объект-генератор, который мы можем потом использовать

# в данном примере мы используем генератор как итератор для списка
for i in my_iterator:
    print(i)

# Код внутри функции-генератора начинает выполняться, когда к созданному ей
# объекту-генератору "обратятся" через вызов next()

"""
2. Генераторы - ленивые. Они отдают один элемент по очереди "по запросу" 
и не хранят все данные в памяти одновременно
"""
import sys

from_one_to_million_list = [i for i in range(1000001)]  # list comprehension возвращает список
print(sys.getsizeof(from_one_to_million_list))

from_one_to_million_gen = (i for i in range(1000001))
# а это - генераторное выражение: еще один способ создать объект-генератор из последовательности элементов
print(sys.getsizeof(from_one_to_million_gen))

# sys.getsizeof() возращает размер переданного его объекта в байтах.
# from_one_to_million_gen будет занимать гораздо меньше места в памяти, чем from_one_to_million_list
# так как список хранит все инты от 1 до миллиона в памяти (+ доп. память для новых элементов)

"""
3. Генераторы работают таким образом, что позволяют выполняющемуся внутри коду "засыпать", 
сохраняя при этом текущее состояние объекта, а после - "просыпаться" и продолжать выполнение
с того места, на котором генератор "заснул" 
"""


def generator_function(some_list: typing.List):
    func_name = generator_function.__qualname__

    print(f"'{func_name}': Generator started")

    for idx, elem in enumerate(some_list):
        print(f"'{func_name}': Returning name '{elem}' and then suspending...")
        yield elem
        print(f"'{func_name}': Awaking!")

        if idx < len(some_list) - 1:
            print(f"'{func_name}': Continue working...")
        else:
            print(f"'{func_name}': Exit")


def iterate_over_names(names: typing.List):
    func_name = iterate_over_names.__qualname__
    gen = generator_function(names)

    for name in gen:
        print(f"'{func_name}': Current name is '{name}'")


iterate_over_names(
    ['Ann', 'Alex', 'John', 'Olga', 'Mary']
)













