# import concurrent.futures
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import requests

from lesson16_threads_and_processes.helpers.helper_functions import work, raise_exc_with_delay

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
        # with session.get(url) as resp:
            # resp.raise_for_status()

        message = SUCCESS

        with LOCK:
            print(f"{current_thread_name}: {message}")

        # print(f"{current_thread_name}: {message}")

    except requests.RequestException:
        message = ERROR
        print(f"{current_thread_name}: {message}")

    return current_thread_name, message


max_workers = 100

# CASE 1: using ThreadPoolExecutor.map
start_time = time.perf_counter()
with ThreadPoolExecutor(
        max_workers=max_workers,
        thread_name_prefix="DownloadSitesThreadPool"
) as thread_pool_ex:
    results = thread_pool_ex.map(download_site, SITES)

duration = time.perf_counter() - start_time

print(results)
print(f"Downloaded {len(SITES)} sites THREADED in {duration} seconds")


# CASE 1: using ThreadPoolExecutor.submit
time_to_wait = [2, 5, 0, 3, 1]


# without automatic waiting for the all running threads
# start_t = time.perf_counter()
# thread_pool_ex = ThreadPoolExecutor(
#         max_workers=3,
#         thread_name_prefix="SubmitThreadPool"
# )

"""
The call of 'ThreadPoolExecutor.submit' method returns the 'concurrent.futures.Future' object:
# The Future is an abstract Object which wraps some Action which can last a long time.
# The general principal of using Futures is that you can get the Future Object immediately
# (for example, right after the call of some method which returns Future), but this Future object
# itself can be in a different states at a different points of time.
and at different points of time the Future

# may be resolved: if result of wrapped Action is received
# OR not: if the wrapped Action is still in progress
# Full list of Future statuses: pending, running, done, cancelled 
"""
# futures = [thread_pool_ex.submit(work, t) for t in time_to_wait]
# futures.append(
#     thread_pool_ex.submit(raise_exc_with_delay, 1)
# )

#print(futures)  # futures list created and printed immediately, without waiting the results

# We don't see the Exception which raised in 'raise_exc_with_delay' func
# print(f'Exec time: {time.perf_counter() - start_t}')


# future_with_exc = futures.pop()
# If we call '.result()' on Future with Exception - this Exception will be raised!
# But here we delete the Future with Exception from futures list
# results = [future.result() for future in futures]
# print(results)
#
# raised_exc = future_with_exc.exception()
# print(type(raised_exc))
# print(raised_exc.args)

# with automatic waiting for the all running threads

# longest_time = max(time_to_wait)
# expected_time_check = lambda t: longest_time <= t < longest_time + 1
#
# start_t = time.perf_counter()
# with ThreadPoolExecutor(
#     max_workers=3,
#     thread_name_prefix="SubmitThreadPool"
# ) as thread_pool_ex:
#     futures = [thread_pool_ex.submit(work, t) for t in time_to_wait]
#     print(futures)
#
# futures_results = [future.result() for future in futures]
# print(futures_results)
#
# end_t = time.perf_counter() - start_t
# print(f'Exec time: {end_t}')
# assert expected_time_check(end_t)
#
# assert futures_results == time_to_wait




