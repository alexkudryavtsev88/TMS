import concurrent.futures as cf
import asyncio
import time

import aiohttp
import requests

from lesson16_17_threads_processes_and_async.helpers.custom_logger import setup_logging
from lesson16_17_threads_processes_and_async.homework.async_server import run_server


logger = setup_logging(__name__)


URL = "http://0.0.0.0"
PORT = 8080
HELLO_ENDPOINT = f"{URL}:{PORT}/hello"

"""
1. Дана функция отправляющая http-запрос, проверяющая статус ответа и возвращающая кортеж,
где 1 элемент - это имя текущего треда, второй элемент - данные из ответа сервера, преобразованные в dict
"""


def send_request():
    response = requests.get(url=HELLO_ENDPOINT)
    response.raise_for_status()
    data = response.json()

    return data['key'], data['value']

"""
ЗАДАНИЕ:
1. Конкурентно запустить функцию 50 раз используя Тред Пулл
2. Ожидать результата выполнения всех запущенных задач 10 секунд
4. Безопасно (то есть, с обработкой возможных ошибок) извлечь результаты только завершенных задач.
   Сформировать дикт с именем results_dict, где ключи - это имена тредов, а значения по этим ключам -
   это соответствующие им дикты (все это возвращает функция send_request).
   Если результат - это какой-либо exception, то не добавляем его в дикт, а добавляем в отдельный список errors.
5. Внутри функции 2 раза зафиксиовать время выполнения кода:
   - первый раз, когда завершили ожидания выполнения задач.
   - второй раз, после того, как обработали результаты и сформировали results_dict.
   - вывести на печать эти два времени как 'exec_time_1' и 'exec_time_2'
   - проверить, что они примерно равны друг другу и что оба времени уж точно не больше 10 секунд!
6. Вывести на печать полученный results_dict и errors.
"""


async def send_many_requests_in_threads(requests_count):
    t = time.perf_counter()

    with cf.ThreadPoolExecutor(
        max_workers=requests_count,
        thread_name_prefix='RequestorThread'
    ) as executor:
        running_futures = [
            executor.submit(send_request, i)
            for i in range(requests_count)
        ]
        print('exec time: ', time.perf_counter() - t)

        done_and_undone_futures = cf.wait(
            running_futures,
            timeout=10,
        )

        result_dict = {}
        for f in done_and_undone_futures.done:
            try:
                name, data = f.result()
                result_dict[name] = data
            except Exception as exc:
                print(f"ERROR: {exc}")

        print('exec time: ', time.perf_counter() - t)

        print(f'Results dict: {result_dict}')

        return result_dict

"""
2. Дана асинхронная функция send_request_async, делающая то же самое, что и send_request,
только использующая асинхронную библиотеку для отправки http-запросов
"""


async def send_request_async():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=HELLO_ENDPOINT) as resp:
            resp.raise_for_status()
            await asyncio.sleep(0.7)
            data = await resp.json()

            return data['key'], data['value']

"""
ЗАДАНИЕ:

Сделать асинхронную версию предыдущего задания:
- вместо Тред Пулла использовать asyncio и Корутины (async функции)
- для запуска корутин использовать asyncio.gather, Timeout в асинхронной версии не нужен!
- Вместо имени Треда в data['key'] будет возвращаться 'Async_{int}', использовать это в качестве ключей в results_dict

(Все остальные условия аналогичны предыдущему заданию)
"""


async def send_many_requests_async(requests_count):
    t = time.perf_counter()

    results_list = await asyncio.gather(
        *[
            send_request_async()
            for _ in range(requests_count)
        ],
        return_exceptions=True
    )
    print(f"exec time: {time.perf_counter() - t}")

    result_dict = {}
    errors = []
    for item in results_list:
        if isinstance(item, Exception):
            # print(f"ERROR: {item}")
            errors.append(item)
        else:
            name, data = item
            # print(name, data)
            result_dict[name] = data

    print('exec time: ', time.perf_counter() - t)

    print(f'Results dict: {result_dict}')
    print(f"Errors: {errors}")

    actual_results_count = len(result_dict.keys())
    expected_results_count = requests_count - len(errors)

    assert actual_results_count == expected_results_count, \
        f"Invalid count: exp {expected_results_count}, " \
        f"act: {actual_results_count}"

    return result_dict


REQUESTS_COUNT = 50

# Firstly you need to run Server (this is NOT blocking because Server runs in separate Process)
server = run_server(port=PORT)

# 1. Run threaded version
# ...

# 2. Run async version
# ...


# 3. Run both and check performance (don't forget to remove 'timeout' from ThreadPool! )
# ...

# Kill the server
time.sleep(3)
server.kill()
