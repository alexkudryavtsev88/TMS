"""
Пример реализации РЕКУРСИВНОЙ ФУНКЦИИ, которая ищет слово в словаре,
в котором значения ключей могут быть ТОЛЬКО строками или вложенными словарями
"""


def recursive_simple(src: dict, lookup_value: str):
    for key, current_value in src.items():
        if isinstance(current_value, dict):
            return recursive_simple(current_value, lookup_value)
            # функция вызывает сама себя, используя в качестве аргумента
            # 'src' переменную v, которая имеет тип dict
        else:
            if current_value == lookup_value:
                return current_value


source_dict = {
    'key1': 'John',
    'key2': {
        'key3': 'Bob',
        'key4': {
            'key5': 'Alex',
            'key6': {
                'key7': {
                    'key8': 'Robert'
                }
            },
        },
    }
}
print(recursive_simple(source_dict, 'Alex'))  # напечатает 'Alex is found!'
print(recursive_simple(source_dict, 'Bob'))   # напечатает 'Alex is found!'
print(recursive_simple(source_dict, 'Jessica'))  # напечатает None, так как слова 'Jessica' нет ни на одном уровне вложенности


