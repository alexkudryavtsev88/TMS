import concurrent.futures as cf
import asyncio
import logging
import threading
import time

import aiohttp
import requests

from lesson16_17_threads_processes_and_async.helpers.custom_logger import setup_logging
from lesson16_17_threads_processes_and_async.homework.async_server import run_server


logger = setup_logging(__name__)
logging.getLogger('urllib3.connectionpool').setLevel('ERROR')
logging.getLogger('aiohttp.access').setLevel('ERROR')


URL = "http://0.0.0.0"
PORT = 8080
HELLO_ENDPOINT = f"{URL}:{PORT}/hello"


def verify_exec_time_and_results(
    t1: float,
    t2: float,
    results_dict: dict[str, dict[str, str]],
    errors_list: list[Exception],
    expected_results_count: int,
    expected_errors_count: int
):
    print(f'exec time after waiting results: {t1}')
    print(f'exec time after processing results: {t2}')
    assert (0 < (t2 - t1) < 1) and t1 < 10 and t2 < 10

    print(f'Results dict: {results_dict}')
    print(f'Errors: {errors_list}')

    success_count = len(results_dict.keys())
    assert success_count == expected_results_count

    errors_count = len(errors_list)
    assert errors_count == expected_errors_count


"""
1. Дана функция отправляющая http-запрос, проверяющая статус ответа и возвращающая кортеж,
где 1 элемент - это имя текущего треда, второй элемент - данные из ответа сервера, преобразованные в dict
"""


def send_request():
    response = requests.get(
        url=HELLO_ENDPOINT,
        params={'requestor': threading.current_thread().name}
    )
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


def send_many_requests_in_threads(requests_count):
    t = time.perf_counter()

    with cf.ThreadPoolExecutor(
        max_workers=requests_count,
        thread_name_prefix='ThreadRequestor'
    ) as executor:
        running_futures = [
            executor.submit(send_request)
            for _ in range(requests_count)
        ]
        done_and_undone_futures = cf.wait(
            running_futures,
            timeout=10,
        )
        end_t1 = time.perf_counter() - t

        result_dict, errors = {}, []
        for f in done_and_undone_futures.done:
            try:
                name, data = f.result()
                result_dict[name] = data
            except Exception as exc:
                errors.append(exc)

        end_t2 = time.perf_counter() - t
        verify_exec_time_and_results(
            t1=end_t1,
            t2=end_t2,
            results_dict=result_dict,
            errors_list=errors,
            expected_results_count=requests_count - len(errors),
            expected_errors_count=int(requests_count / 10)
        )

        return result_dict

"""
2. Дана асинхронная функция send_request_async, делающая то же самое, что и send_request,
только использующая асинхронную библиотеку для отправки http-запросов
"""


async def send_request_async(call_number: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=HELLO_ENDPOINT,
            params={'requestor': f'AsyncRequestor_{call_number}'}
        ) as resp:
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
            send_request_async(i)
            for i in range(requests_count)
        ],
        return_exceptions=True
    )
    end_t1 = time.perf_counter() - t

    result_dict, errors = {}, []
    for item in results_list:
        if isinstance(item, Exception):
            errors.append(item)
        else:
            name, data = item
            result_dict[name] = data

    end_t2 = time.perf_counter() - t
    verify_exec_time_and_results(
        t1=end_t1,
        t2=end_t2,
        results_dict=result_dict,
        errors_list=errors,
        expected_results_count=requests_count - len(errors),
        expected_errors_count=int(requests_count / 10)
    )

    return result_dict


REQUESTS_COUNT = 50

# Firstly you need to run Server (this is NOT blocking because Server runs in separate Process)
server = run_server(port=PORT)

# 1. Run threaded version
# ...
send_many_requests_in_threads(requests_count=REQUESTS_COUNT)

# 2. Run async version
# asyncio.run(send_many_requests_async(requests_count=REQUESTS_COUNT))


# 3. Run both and check performance (don't forget to remove 'timeout' from ThreadPool! )
# ...

# Kill the server
time.sleep(5)
server.kill()
