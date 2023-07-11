import time
from threading import Thread, current_thread
from LessonN_threads_and_processes.custom_logger import setup_logging


logger = setup_logging(__name__)


TIME_SLEEP = 3


def work(arg: int):
    logger.debug(f'Start')
    logger.debug(f"Sleeping for {arg} seconds")

    time.sleep(arg)

    logger.debug(f'End')


def raise_exc_with_delay(delay: int):
    logger.debug('Start')
    logger.debug(f"Sleeping for {delay} seconds")

    time.sleep(delay)
    raise RuntimeError('fail!')


logger.info(f'Start')

# Create child Thread
t1 = Thread(
    target=work,
    args=(TIME_SLEEP, ),
    name="ChildThread1"
)

# 'target' is a function/method which code will be executed in created Child thread
# 'args' is a tuple of arguments for 'target' function
# Note: all another code except the code in 'target' functions is executed in the Main thread!
logger.info(f'Thread {t1.name} is created')

# start executing of the Child thread
t1.start()

# Case 1. Join the Child thread:
# when joining the Child thread, the Main thread will wait until the Child ia completed
t1.join()

# this code line will be executed AFTER the ChildThread1 thread will be completed
logger.info(f'Waits for the {t1.name} thread!')

# Case 2. without joining the Child thread
t2 = Thread(
    target=work,
    args=(TIME_SLEEP, ),
    name="ChildThread2"
)
logger.info(f'Thread {t2.name} is created')

t2.start()

# this code line will be executed BEFORE the ChildThread2 will be completed
logger.info(f"Doesn't wait for the {t2.name} thread!")


# 3. using 'daemon' flag
t3 = Thread(
    target=raise_exc_with_delay,
    name="ChildThreadDaemon",
    args=(TIME_SLEEP, ),
    daemon=True,
)
logger.info(f'DAEMON thread {t3.name} is created')

t3.start()

# when Thread is marked as Daemon, then NOT only the Main thread doesn't for it,
# but the whole Process doesn't wait:
# In our case the Process will exit when ChildTread2 will be completed,
# and we don't see RuntimeError which raises in ChildThreadDaemon!
logger.info(f'Thread {current_thread().name} END')


def my_func(arg: int):
    cur_thread_name = current_thread().name
    print(f"Thread {cur_thread_name} start with sleep: {arg}")
    time.sleep(arg)
    print(f"Thread {cur_thread_name} end")


def run_in_one_thread(data: tuple[int, ...]):
    print(f"run_in_one_thread: start program!")

    start_time = time.perf_counter()
    for i in data:
        my_func(i)

    print(f"run_in_many_threads: common exec time is {time.perf_counter() - start_time}")


def run_in_many_threads(data: tuple[int, ...]):
    print(f"run_in_many_threads: start program ({len(data)} threads)")
    running_threads = []

    start_time = time.perf_counter()
    for i in data:
        thread = Thread(target=my_func, args=(i, ))
        thread.start()
        running_threads.append(thread)

    for t in running_threads:
        t.join()

    print(f"run_in_many_threads: common exec time is {time.perf_counter() - start_time}")


# my_data = (3, 7, 4, 1, 0, 6, 2, 5, 8)
# run_in_one_thread(my_data)
# print("*" * 50)
# run_in_many_threads(my_data)