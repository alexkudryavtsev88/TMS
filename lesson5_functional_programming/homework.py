""" 1 """
my_func = lambda x: "even" if x % 2 == 0 else "odd"
source = range(11)
result = dict(
    zip(
        source,
        list(map(lambda x: my_func(x), source))
    )
)
print(result)

""" 2 """
result = list(map(lambda x: str(x), range(11)))
print(result)

""" 3 """
palindromes = [
    "Молебен о Коне Белом",
    "Я не Палиндром",
    "Искать такси",
    "Любая строка",
    "Аргентина манит Негра"
]
result = list(
    filter(
        lambda phrase: (
            phrase.lower().replace(" ", "")
            == phrase.lower().replace(" ", "")[::-1]
        ),
        palindromes
    )
)
print(result)
assert result == ["Молебен о Коне Белом", "Искать такси", "Аргентина манит Негра"]

""" 4 """
