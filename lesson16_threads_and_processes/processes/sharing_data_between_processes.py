import logging
import multiprocessing as mp
import threading as th
import time

from lesson16_threads_and_processes.helpers.custom_logger import setup_logging

# logger = logging.getLogger('processes-share-data')
# setup_logging(logger)

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


logger.info('start')
logger.info(f"DATA before the Processes have started: {DATA}")

p1 = mp.Process(target=add_value, args=('test',))
p2 = mp.Process(target=get_value, args=(0,))

for p in p1, p2:
    p.start()

for p in p1, p2:
    p.join()

logger.info(f"DATA after All Processes have finished: {DATA}")
