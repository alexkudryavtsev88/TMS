"""3. Дан список из 100 последовательных целых чисел"""

my_list = list(range(1, 101))

"""На основании этого списка создать новый список (используя list comprehension), по следующим условиям:
- В новый список должны войти только те элементы исходного списка, которые делятся по модулю на 10
- Оставшиеся элементы, которые НЕ делятся по модулю на 4 - должны быть умножены на 10
- Все остальные элементы должны быть умножены на 2"""


result = [x * 10 if x % 4 != 0 else x * 2 for x in my_list if x % 10 == 0]
print(f"Result: {result}")

# by steps:
first_step = [x for x in my_list if x % 10 == 0]
print(f"First Step: {first_step}")
last_step = [x * 10 if x % 4 != 0 else x * 2 for x in first_step]
print(f"Last Step: {last_step}")

assert result == last_step, f"{result} != {last_step}"