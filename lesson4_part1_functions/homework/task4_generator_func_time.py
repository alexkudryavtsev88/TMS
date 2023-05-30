from datetime import datetime
from time import sleep


def get_my_time(
    seconds: int = 1,
    time_format: str = '%Y-%m-%d %H:%M:%S'
) -> str:
    sleep(seconds)
    return datetime.strftime(datetime.now(), time_format)


n = int(input('Введите целое число:\n'))
time_list = [get_my_time() for _ in range(n)]
print(f'{time_list=}')