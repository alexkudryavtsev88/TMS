def factorial_recursive(N: int, frame_num: int = 0, tab: int = -1):
    """ Вспомогательные переемнные """
    frame_num += 1
    tab += 1
    rshift = '\t' * tab

    if frame_num == 1:
        print(f"{rshift} Начальный вызов функции: N = {N}")
    else:
        print(f"\n{rshift} {frame_num}-й вызов функции: N = {N}")

    if N <= 1:
        print(
            f"{rshift} Проверяем значение N: {N} <= 1 это True\n"
            f"{rshift} Терминальный случай: выходим из {frame_num}-го вызова функции, возвращаем 1"
        )
        return 1
    else:
        print(f"{rshift} Проверяем значение N: {N} <= 1 это False")
        print(f"{rshift} Вызываем функцию рекурсивно с параметром N - 1")

        result = factorial_recursive(N=N-1, frame_num=frame_num, tab=tab)

        print(f"\n{rshift} Вернулись в {frame_num}-й вызов функции: сохраненное значение N = {N}, полученное значение = {result} ")
        print(f"{rshift} Возвращаем произведение сохраненного N и полученного значения: {N} * {result} = {result * N}")

        return N * result


n = 5
factorial_n = factorial_recursive(n)
print(f"\nФакториал числа 5 = {factorial_n}")
