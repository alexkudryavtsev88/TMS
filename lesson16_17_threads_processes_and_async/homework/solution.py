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
1. 
"""


def send_request():
    response = requests.get(url=HELLO_ENDPOINT)
    response.raise_for_status()
    data = response.json()

    return data['key'], data['value']


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
2. 
"""


async def send_request_async():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=HELLO_ENDPOINT) as resp:
            resp.raise_for_status()
            await asyncio.sleep(0.7)
            data = await resp.json()

            return data['key'], data['value']


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


# 2. Run async version
asyncio.run(send_many_requests_async(requests_count=REQUESTS_COUNT))


# 3. Run both and check performance (don't forget to remove 'timeout' from ThreadPool! )

# Kill the server
time.sleep(3)
server.kill()
