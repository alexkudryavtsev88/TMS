from LessonN_threads_and_processes.helpers.custom_logger import setup_logging
import time

logger = setup_logging(__name__)


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