import time
from threading import Thread
from lesson16_17_threads_processes_and_async.helpers.custom_logger import setup_logging
from lesson16_17_threads_processes_and_async.helpers.helper_functions import work
from lesson16_17_threads_processes_and_async.helpers.levenshtein_dist_calculator import LevenshteinDistanceCalculator


logger = setup_logging(__name__)


def run_sleeps_in_one_thread(data: tuple[int, ...]):
    logger.info(f"run_in_one_thread: start program!")

    start_time = time.perf_counter()
    for i in data:
        work(i)

    logger.info(f"run_in_one_threads: common exec time is {time.perf_counter() - start_time}")


def run_sleeps_in_many_threads(data: tuple[int, ...]):
    logger.info(f"run_in_many_threads: start program ({len(data)} threads)")
    running_threads = []

    start_time = time.perf_counter()
    for i in data:
        thread = Thread(target=work, args=(i, ))
        thread.start()
        # thread.join()  # don't use join inside the loop!
        running_threads.append(thread)

    for t in running_threads:
        t.join()

    logger.info(f"run_in_many_threads: common exec time is {time.perf_counter() - start_time}")


# MY_DATA = (3, 7, 4, 1, 9, 6, 2, 5)
# run_sleeps_in_one_thread(MY_DATA)
# run_sleeps_in_many_threads(MY_DATA)


# Running CPU-bound task in Threads
def calculate_levenshtein_in_one_thread(words: list[tuple[str, str]]):
    logger.info(f"calculate_levenshtein_in_one_thread: start program!")

    start_time = time.perf_counter()
    for word_a, word_b in words:
        _ = LevenshteinDistanceCalculator.calculate(word_a, word_b)

    exec_time = (time.perf_counter() - start_time) * 1000
    logger.info(
        f"calculate_levenshtein_in_one_thread: "
        f"common exec time is {exec_time} ms"
    )


def calculate_levenshtein_in_many_threads(words: list[tuple[str, str]]):
    logger.debug(f"calculate_levenshtein_in_many_threads: start program ({len(words)} threads)")
    running_threads = []

    start_time = time.perf_counter()
    for word_a, word_b in words:
        thread = Thread(
            target=LevenshteinDistanceCalculator.calculate,
            args=(word_a, word_b)
        )
        thread.start()
        running_threads.append(thread)

    for t in running_threads:
        t.join()

    exec_time = (time.perf_counter() - start_time) * 1000
    logger.debug(
        f"calculate_levenshtein_in_many_threads: "
        f"common exec time is {exec_time} ms")


if __name__ == '__main__':
    WORDS = [
        ("", ""),
        ("", "Test"),
        ("Levenshtein", ""),
        ("Test", "Test"),
        ("python", "Python"),
        ("Form", "Fork"),
        ("Piece", "Peace"),
        ("Kitten", "Sitting"),
    ]
    calculate_levenshtein_in_one_thread(words=WORDS)
    calculate_levenshtein_in_many_threads(words=WORDS)
