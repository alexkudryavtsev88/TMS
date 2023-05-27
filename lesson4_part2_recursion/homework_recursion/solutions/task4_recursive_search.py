"""
Дан входной словарь
- Ключи словаря - строки
- Значениями ключей могут быть:
-- Строки
-- Словари
-- Списки

Все элементы-словари, как и родительский словарь, могут содержать строки, списки и другие вложенные словари
Все Элементы-списки могут содержать строки, словари и другие вложенные списки

Написать рекурсивную функцию, которая:
- Принимает на вход следующие аргументы:
-- 1 аргумент: исходный словарь
-- 2 аргумент: слово, которое нужно найти в словаре (строка)
-- аргумент deep с дефолтным целочисленным значением, отображающим текущий уровень вложенности (глубину) словаря
-- аргумент parent с дефолтным значением None, который сохраняет родителя (ключ словаря) на текущем уровне вложенности

- Делает обход словаря в глубину и поиск указанного значения
- Если значение найдено: печатает строку f"Значение {val} найдено на глубине {deep}"


* будет ли ваша функция искать слово до первого совпадения или найдет все имеющиеся совпадения - не важно
* понятие "уровень вложенности" или "глубина" касается только вложенных словарей!
"""

from homework_recursion.source.source_dict import get_source_dict_with_duplicates


"""Task 4: recursive search in dict"""
def recursive_search(src: dict, value: str, deep=-1, parent=None):
    if isinstance(src, dict):
        deep += 1
        for k, v in src.items():
            recursive_search(v, value, deep=deep, parent=k)
    elif isinstance(src, list):
        for item in src:
            recursive_search(item, value, deep=deep, parent=parent)
    elif isinstance(src, str):
        if src == value:
            print(f'Found "{value}" on deep = {deep}, parent = {parent}')
            return src


""" TEST """
lookup_name = "Alex"
source_dict = get_source_dict_with_duplicates()
recursive_search(source_dict, lookup_name)


