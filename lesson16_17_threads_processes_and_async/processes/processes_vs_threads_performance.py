import time
from multiprocessing import Process
from lesson16_17_threads_processes_and_async.helpers.custom_logger import setup_logging
from lesson16_17_threads_processes_and_async.threads.creating_many_threads import (
    calculate_levenshtein_in_many_threads,
    calculate_levenshtein_in_one_thread
)
from lesson16_17_threads_processes_and_async.helpers.levenshtein_dist_calculator import LevenshteinDistanceCalculator


logger = setup_logging(__name__)


def calculate_levenshtein_in_many_processes(words: list[tuple[str, str]]):
    logger.warning(f"calculate_levenshtein_in_many_processes: start program ({len(words)} processes)")
    running = []

    # Using multiprocessing
    start_time = time.perf_counter()
    for word_a, word_b in words:
        process = Process(
            target=LevenshteinDistanceCalculator.calculate,
            args=(word_a, word_b)
        )
        process.start()
        running.append(process)

    for p in running:
        p.join()

    # using ProcessPoolExecutor
    # with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
    #     futures = [
    #         executor.submit(
    #             LevenshteinDistanceCalculator.calculate,
    #             word_a, word_b
    #         )
    #         for word_a, word_b in words
    #     ]
    # concurrent.futures.wait(futures, timeout=1)

    exec_time = (time.perf_counter() - start_time) * 1000
    logger.warning(
        f"calculate_levenshtein_in_many_processes: "
        f"common exec time is {exec_time} ms")


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
calculate_levenshtein_in_many_processes(words=WORDS)