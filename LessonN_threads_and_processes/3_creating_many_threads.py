import time
from threading import Thread
from LessonN_threads_and_processes.helpers.custom_logger import setup_logging
from LessonN_threads_and_processes.helpers.helper_functions import work


logger = setup_logging(__name__)


def run_in_one_thread(data: tuple[int, ...]):
    logger.info(f"run_in_one_thread: start program!")

    start_time = time.perf_counter()
    for i in data:
        work(i)

    logger.info(f"run_in_many_threads: common exec time is {time.perf_counter() - start_time}")


def run_in_many_threads(data: tuple[int, ...]):
    logger.info(f"run_in_many_threads: start program ({len(data)} threads)")
    running_threads = []

    start_time = time.perf_counter()
    for i in data:
        thread = Thread(target=work, args=(i, ))
        thread.start()
        running_threads.append(thread)

    for t in running_threads:
        t.join()

    logger.info(f"run_in_many_threads: common exec time is {time.perf_counter() - start_time}")


my_data = (3, 7, 4, 1, 0, 6, 2, 5, 8)
run_in_one_thread(my_data)
run_in_many_threads(my_data)