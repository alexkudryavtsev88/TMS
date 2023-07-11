import random

from lesson16_threads_and_processes.helpers.custom_logger import setup_logging
import time

logger = setup_logging(__name__)


def work(arg: int):
    name = work.__qualname__

    logger.debug(f"'{name}': Start")
    logger.debug(f"'{name}': Sleeping for {arg} seconds")

    time.sleep(arg)

    logger.debug(f'End')

    return arg


def raise_exc_with_delay(delay: int):
    name = raise_exc_with_delay.__qualname__

    logger.debug(f"'{name}': Start")
    logger.debug(f"'{name}': Sleeping for {delay} seconds")

    time.sleep(delay)
    raise RuntimeError('fail!')


def random_long_word():
    return "".join(
        [
            random.choice(("A", "B")) for _ in range(100)
        ]
    )
