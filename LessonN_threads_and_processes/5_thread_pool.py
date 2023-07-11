import logging
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import requests

from typing import Callable, Any
from LessonN_threads_and_processes.helpers.helper_functions import work

urllib3_logger = logging.getLogger('urllib3.connectionpool')
urllib3_logger.setLevel(logging.ERROR)


SITES = (
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
) * 20


SUCCESS = "success"
ERROR = "error"
LOCK = threading.Lock()
THREAD_LOCAL = threading.local()


def get_session():
    if not hasattr(THREAD_LOCAL, "session"):
        THREAD_LOCAL.session = requests.Session()
    return THREAD_LOCAL.session


def download_site(url):
    session = get_session()
    current_thread_name = threading.current_thread().name
    try:
        with session.get(url) as resp:
            resp.raise_for_status()
            message = SUCCESS

            # with LOCK:
            #     print(f"{current_thread_name}: {message}")

            print(f"{current_thread_name}: {message}")

    except requests.RequestException:
        message = ERROR
        print(f"{current_thread_name}: {message}")

    return current_thread_name, message


max_workers = 50

# start_time = time.perf_counter()
# with ThreadPoolExecutor(
#         max_workers=max_workers,
#         thread_name_prefix="DownloadSitesThreadPool"
# ) as thread_pool_ex:
#     results = thread_pool_ex.map(download_site, SITES)
#
# duration = time.perf_counter() - start_time
#
# print(results)
# print(f"Downloaded {len(SITES)} sites THREADED in {duration} seconds")


time_to_wait = [2, 5, 0, 3, 1]
longest_time = max(time_to_wait)
expected_time_check = lambda t: longest_time <= t < longest_time + 1


# without automatic waiting for the all running threads
# start_t = time.perf_counter()
# thread_pool_ex = ThreadPoolExecutor(
#         max_workers=3,
#         thread_name_prefix="SubmitThreadPool"
# )
# futures = [thread_pool_ex.submit(work, t) for t in time_to_wait]
# end_t = time.perf_counter() - start_t
# print(futures)
# print(f'Exec time: {end_t}')


# with automatic waiting for the all running threads
start_t = time.perf_counter()
with ThreadPoolExecutor(
        max_workers=3,
        thread_name_prefix="SubmitThreadPool"
) as thread_pool_ex:
    futures = [thread_pool_ex.submit(work, t) for t in time_to_wait]
    print(futures)
    futures_results = [future.result() for future in futures]
    print(futures_results)

end_t = time.perf_counter() - start_t
print(f'Exec time: {end_t}')
assert expected_time_check(end_t)

assert futures_results == time_to_wait

# getting results as completed



