""" Task 1: recursive reverse """
def recursive_reverse(some_list):
    if not some_list:  # терминальный кейс: лист пустой, значит возвращаем пустой лист.
        return []
    last = some_list.pop()  # pop() удаляет последний элемент И ВОЗВРАЩАЕТ его

    # - оборачиваем элемент который нам вернул pop() в список
    # - складываем получившийся список с рекурсивным вызовов,
    # в котором уже на вход в качестве списка будет исходный список БЕЗ последнего элемента
    # операция сложения 2-х списков возвращает новый список с элементами 1-го и 2-го списков по порядку

    return [last] + recursive_reverse(some_list)

# ---------------------------------------------------------------

""" Task 2: recursive max element """
def recursive_max(some_list):
    if len(some_list) == 1:
        return some_list[0]

    max_element = recursive_max(some_list[1:])
    if some_list[0] < max_element:
        return max_element
    else:
        return some_list[0]

# ---------------------------------------------------------------

""" Task 3: recursive flat """
def recursive_flat(some_list):
    if not some_list:
        return some_list
    if isinstance(some_list[0], list):
        return recursive_flat(some_list[0]) + recursive_flat(some_list[1:])
    return some_list[:1] + recursive_flat(some_list[1:])


""" Task 4: recursive search until first match occur"""
def recursive_search(src: dict, value: str, deep=-1, parent=None):
    result = None

    def _recursive_inner(src: dict, value: str, deep=-1, parent=None):
        nonlocal result

        if isinstance(src, dict):
            deep += 1
            for k, v in src.items():
                result = _recursive_inner(v, value, deep=deep, parent=k)
                if result:
                    return result
        elif isinstance(src, list):
            for item in src:
                result = _recursive_inner(item, value, deep=deep, parent=parent)
                if result:
                    return result
        elif isinstance(src, str) and src == value:
            return {'val': value, 'parent': parent, 'deep': deep}

    return _recursive_inner(src, value, deep, parent)


# from lesson4_additional.source_dict import get_source_dict

# source_dict = get_source_dict()
""" Результат работы функции: поиск слова 'Alex': """
# res = recursive_search(source_dict, 'Alex')
# print(res)
# res = recursive_search(source_dict, 'Mary')
# print(res)
# res = recursive_search(source_dict, 'Duke')
# print(res)
# res = recursive_search(source_dict, 'Mark')
# print(res)


