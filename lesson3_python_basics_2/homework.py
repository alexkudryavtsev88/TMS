''' LESSON 3 '''

# 1


# 2 + 3
def task2_3():
    a = input("Как вас зовут? ")
    # изначальный ввод должен быть ЗА пределами бесконечного цикла
    b = input("Сколько вам лет? ")
    while True:
        try:
            b = int(b)
            if b <= 0:
                b = input("Ошибка, повторите ввод: ")
            elif b < 10:
                print("Привет, шкет", a)
                break  # при каждом УСПЕШНОМ вводе, вы должны напечатать сообщение и оборвать бесконечный цикл

            elif 10 <= b <= 18:
                # print("Как жизнь? ", a)
                print(f"Как жизнь {a}?")
                break

            elif 18 < b < 100:
                print(f"Что желаете {a}?")
                break
            else:
                print(a, "Вы лжете - в наше время столько не живут")
                break
        except ValueError:
            b = input("Ошибка, повторите ввод: ")
            # если словили ValueError - просим юзера ввести повторить ввод, и возвращаемся в начало цикла.


# 4:
def task3():
    n = int(input("Введите целое число: "))

    # using FOR loop
    sum_for_loop = 0
    for i in range(1, n + 1):
        sum_for_loop += i ** 3

    # using WHILE loop
    sum_while_loop = 0
    start = 1
    while True:
        if start >= n + 1:
            break
        sum_while_loop += start ** 3
        start += 1

    # using built-in *sum* function
    sum_with_func = sum([i ** 3 for i in range(1, n + 1)])

    assert sum_for_loop == sum_while_loop == sum_with_func
    print(f"""
    Sum of kubes for N = {n}:
    Using FOR loop: {sum_for_loop}
    Using WHILE loop: {sum_while_loop}
    Using built-in *sum* function: {sum_with_func}"""
    )


task3()


# 5
def task5():
    z = 60
    x = int(input('Enter Введите число: '))
    while x != z:
        print('Вы не угадали число')
        x = int(input('Enter Введите другое число: '))
    else:
        print('Вы угадали число')
