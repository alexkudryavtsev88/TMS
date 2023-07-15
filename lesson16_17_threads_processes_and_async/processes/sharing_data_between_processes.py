import multiprocessing as mp
import time
from collections import deque

from lesson16_17_threads_processes_and_async.helpers.custom_logger import setup_logging

logger = setup_logging(__name__)

QUEUE = deque()  # create a 1st Global Queue using collections.deque object
MULTIPROCESS_QUEUE = mp.Queue()  # create a 2nd Global Queue using multiprocessing.Queue object


def add_value(val):
    logger.debug('start')
    logger.debug(f'adding value {repr(val)}')

    QUEUE.append(val)
    MULTIPROCESS_QUEUE.put(val)

    logger.debug(f"QUEUE size after the value {repr(val)} was added: {len(QUEUE)}")
    logger.debug(f"MULTIPROCESS_QUEUE size after the value {repr(val)} was added: {MULTIPROCESS_QUEUE.qsize()}")


def get_value():
    logger.warning('start')
    logger.warning('getting value...')

    time.sleep(0.5)

    try:
        val_from_q1 = QUEUE.pop()  # Exception occurs here because the Process in which this function runs
        # doesn't see the updates from the another Processes
        logger.warning(f"Value from QUEUE: {repr(val_from_q1)}")
    except Exception as exc:
        logger.error(f'Error is occurred! {exc}')

    try:
        val_from_q2 = MULTIPROCESS_QUEUE.get()  # but here all is OK, because multiprocessing Queue
        # serializes the data automatically, and separate Processes may see the serialized data
        logger.warning(f"Value from MULTIPROCESS_QUEUE: {repr(val_from_q2)}")
    except Exception as exc:
        logger.error(f'Error is occurred! {exc}')


def run_concurrently():
    logger.info('start')

    logger.info(f"QUEUE size BEFORE the Processes have started: {len(QUEUE)}")
    logger.info(f"MULTIPROCESS_QUEUE size BEFORE the Processes have started: {MULTIPROCESS_QUEUE.qsize()}")

    p1 = mp.Process(target=add_value, args=('test',))
    p2 = mp.Process(target=get_value)

    for p in p1, p2:
        p.start()

    for p in p1, p2:
        p.join()

    logger.info(f"QUEUE size AFTER the Processes have ended: {len(QUEUE)}")
    logger.info(f"MULTIPROCESS_QUEUE size AFTER the Processes have ended: {MULTIPROCESS_QUEUE.qsize()}")


run_concurrently()