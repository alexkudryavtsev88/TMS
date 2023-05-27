"""
Пример реализации РЕКУРСИВНОЙ ФУНКЦИИ, которая ищет слово в словаре,
в котором значения ключей могут быть ТОЛЬКО строками или вложенными словарями
"""

def recursive_simple(src: dict, value: str):
    for k, v in src.items():
        if isinstance(v, dict):
            recursive_simple(v, value)
            # функция вызывает сама себя, используя в качестве аргумета 'src' переменную v, которая имеет тип dict
        else:
            if v == value:
                print(f"{value} is found!")
                return


src = {
    'key1': 'John',
    'key2': {
        'key3': 'Bob', 'key4': {
            'key5': 'Alex'
        }
    }
}
recursive_simple(src, 'Alex')  # напечатает 'Alex is found!'
recursive_simple(src, 'Bob')   # напечатает 'Alex is found!'
recursive_simple(src, 'Jessica')  # ничего не напечатает, так как слова 'Jessica' нет ни на одном уровне вложенности


