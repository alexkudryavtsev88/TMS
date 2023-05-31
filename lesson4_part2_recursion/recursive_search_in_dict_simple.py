"""
Пример реализации РЕКУРСИВНОЙ ФУНКЦИИ, которая ищет слово в словаре,
в котором значения ключей могут быть ТОЛЬКО строками или вложенными словарями
"""


def recursive_simple(src: dict, lookup_value: str):
    for key, current_value in src.items():
        if isinstance(current_value, dict):
            value = recursive_simple(current_value, lookup_value)
            if value:
                return value
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
            'key7': 'John'
        },
        'key8': 'Karl'
    },
    'key9': 'Kate'
}
print(recursive_simple(source_dict, 'Alex'))
print(recursive_simple(source_dict, 'Bob'))
print(recursive_simple(source_dict, 'John'))
print(recursive_simple(source_dict, 'Karl'))
print(recursive_simple(source_dict, 'Kate'))


