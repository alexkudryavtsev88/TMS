import logging
import multiprocessing as mp
import threading
import threading as th
import time

from lesson16_threads_and_processes.helpers.custom_logger import setup_logging

logger = setup_logging(__name__)

DATA = []


def add_value(val):
    logger.debug('start')
    logger.debug(f'adding value {repr(val)}')

    DATA.append(val)

    logger.debug(f"DATA after update: {DATA}")


def get_value(idx):
    logger.warning('start')
    logger.warning(f'getting value by index {idx}')

    time.sleep(0.5)

    try:
        logger.warning(f"Element by Index {idx}: {DATA[idx]}")
    except IndexError as exc:
        logger.error(f'Error is occurred! Index {idx}, "{exc}"')


def run_concurrently(using_processes: bool = False):
    logger.info('start')
    logger.info(f"DATA before the Processes have started: {DATA}")

    exec_unit = mp.Process if using_processes else threading.Thread
    p1 = exec_unit(target=add_value, args=('test',))
    p2 = exec_unit(target=get_value, args=(0,))

    for p in p1, p2:
        p.start()

    for p in p1, p2:
        p.join()

    logger.info(f"DATA after All Processes have finished: {DATA}")


run_concurrently(using_processes=True)