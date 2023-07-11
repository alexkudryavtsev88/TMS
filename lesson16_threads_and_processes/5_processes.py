from multiprocessing import Process, current_process
# from lesson16_threads_and_processes.helpers.helper_functions import work, raise_exc_with_delay
from lesson16_threads_and_processes.helpers.custom_logger import setup_logging


logger = setup_logging(__name__)

_GLOBAL_DICT = {
    "Alex": 34,
    "Ann": 33,
    "Olga": 9
}


def process_func(dict_, key_):
    result = dict_.get(key_)
    return result


