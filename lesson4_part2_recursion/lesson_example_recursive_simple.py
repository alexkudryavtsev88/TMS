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
                print(f"{lookup_value} is found!")
                return current_value

src = {
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
found_name = recursive_simple(src, 'Sam')  # напечатает 'Alex is found!'
print(found_name)
# recursive_simple(src, 'Bob')   # напечатает 'Alex is found!'
# recursive_simple(src, 'Jessica')  # ничего не напечатает, так как слова 'Jessica' нет ни на одном уровне вложенности


