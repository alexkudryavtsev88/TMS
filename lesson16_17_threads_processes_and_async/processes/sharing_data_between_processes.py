import logging
import multiprocessing as mp
import threading
import threading as th
import time
from collections import deque

from lesson16_17_threads_processes_and_async.helpers.custom_logger import setup_logging

logger = setup_logging(__name__)

QUEUE = deque()


def add_value(val):
    logger.debug('start')
    logger.debug(f'adding value {repr(val)}')

    QUEUE.append(val)

    logger.debug(f"QUEUE after update: {QUEUE}")


def get_value():
    logger.warning('start')
    logger.warning('getting value...')

    time.sleep(0.5)

    try:
        val = QUEUE.pop()
        logger.warning(f"Value from Queue: {repr(val)}")
    except Exception as exc:
        logger.error(f'Error is occurred! {exc}')


def run_concurrently(using_processes: bool = False):
    logger.info('start')
    logger.info(f"QUEUE before the Processes have started: {QUEUE}")

    exec_unit = mp.Process if using_processes else threading.Thread
    p1 = exec_unit(target=add_value, args=('test',))
    p2 = exec_unit(target=get_value)

    for p in p1, p2:
        p.start()

    for p in p1, p2:
        p.join()

    logger.info(f"QUEUE after All Processes have finished: {QUEUE}")


run_concurrently(using_processes=False)