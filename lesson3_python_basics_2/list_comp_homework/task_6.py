"""5. Дан Словарь: """

dict_1 = {
  "key1": 1,
  "key2": 2,
  "key3": 3,
  "key4": 4,
  "key5": 5
}

"""С помощью dict comprehension получить новый словарь dict_2, в котором значения dict_1 будут ключами, а ключи dict_1 будут значениями"""


var_1 = {dict_1[key]: key for key in dict_1}
var_2 = {value: key for key, value in dict_1.items()}
print(f"Variant 1 result: {var_1}\nVariant 2 result: {var_2}")
expected = {
    1: 'key1',
    2: 'key2',
    3: 'key3',
    4: 'key4',
    5: 'key5'
}

assert var_1 == var_2, f"Variant 1 {var_1} != Variant 2 {var_2}"
assert var_1 == expected, f"Result {var_1} != Expected {expected}"
