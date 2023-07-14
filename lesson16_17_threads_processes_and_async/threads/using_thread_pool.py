import concurrent.futures as cf
import time

from lesson16_17_threads_processes_and_async.helpers.custom_logger import setup_logging
from lesson16_17_threads_processes_and_async.helpers.helper_functions import work, raise_exc_with_delay


logger = setup_logging(__name__)


MAX_WORKERS = 3

"""
ThreadPoolExecutor initialization
"""
with cf.ThreadPoolExecutor(max_workers=MAX_WORKERS) as threads_executor:
    pass

"""
1. ThreadPoolExecutor usually used as Context Manager ("with ... as ..." syntax)
   in this case the Executor waits for the ALL Threads running within it by default
2. 'max_workers' specifies the LIMIT count of Threads which can be created at all 
   within the ThreadPoolExecutor instance. 
   The Executor manages its Threads:
   - it spawns the new Threads only when needed: if the count of Tasks for execution is MORE 
     than the count of the existing Threads, and if all existing Threads are busy by some Tasks, 
     the Executor spawns the new Threads.  
   - if some Thread finish its work - the Executor assigns some another tasks to it.
"""


DELAYS = (5, 2, 3)


# CASE 1: run 'work' func in separate threads using 'ThreadPoolExecutor.map' method
def using_executor_map():
    """
    # use 'ThreadPoolExecutor.map' method when:
    # - you need to run exact one function in separate threads
    # and this function takes exact one input argument
    # - you need to get results of threads tasks
    # - you don't need to communicate with *Future objects directly
    # - you don't need for some waiting timeouts

    """
    t1 = time.perf_counter()
    with cf.ThreadPoolExecutor(
            max_workers=MAX_WORKERS
    ) as executor:
        res = executor.map(work, DELAYS)

        # INPUT:
        # - takes some func to execute 1st argument
        # - takes iterable of arguments for the function as 2nd argument
        # - runs passed func with each argument from iterable in separate thread
        # - NOTE: the func should take only one argument!

        # OUTPUT:
        # - returns an iterator over the threads task results

        # - NOTE: the iterator returns immediately, without real waiting the tasks results
        print('exec time: ', time.perf_counter() - t1)

        # - collecting the results from iterator
        # to list/tuple will wait for the all tasks are finished
        # - results are in the same order as elements in second argument's Iterabl
        res_list = list(res)
        print(res_list)
        print('exec time: ', time.perf_counter() - t1)


# using_executor_map()
print("*" * 50)


# CASE 2: using most general 'ThreadPoolExecutor.submit' method
# NOTE: 'map' method uses 'submit' under the hood
def using_executor_submit():
    """
    # - 'submit' method returns a *Future object
    # - using 'submit' you can run any functions with any count of arguments
    # - using 'submit' you can combine a different functions for execution in threads
    # - using Future objects returning from 'submit', you have a different ways to process the results of threads tasks
    """
    t2 = time.perf_counter()
    with cf.ThreadPoolExecutor(
            max_workers=MAX_WORKERS
    ) as ex:
        futures_list = [ex.submit(work, d) for d in DELAYS]
        print(futures_list)
        print('exec time: ', time.perf_counter() - t2)

        print([f.result() for f in futures_list])
        print('exec time: ', time.perf_counter() - t2)


# using_executor_submit()
print("*" * 50)


"""
# *Future is an abstract Object which wraps some Action which can last a long time.
# The general principal of using Futures is that you can get the Future Object immediately
# (for example, right after the call of some method which returns Future), but this Future object
# itself can be in a different states at a different points of time.
and at different points of time the Future

# may be resolved: if result of wrapped Action is received
# OR not: if the wrapped Action is still in progress
# Full list of Future statuses: pending, running, done, cancelled 
"""


# don't use 'submit' like this!
def using_submit_in_loop_with_blocking():
    results = []

    t = time.perf_counter()
    with cf.ThreadPoolExecutor(
            max_workers=MAX_WORKERS
    ) as ex:
        for d in DELAYS:
            # you create a Future here
            fut = ex.submit(work, d)  # you create a Future here
            # and here you call result() which blocks the current iteration
            # of the loop until the future has been done
            r = fut.result()
            results.append(r)
        print('exec time: ', time.perf_counter() - t)


# using_submit_in_loop_with_blocking()  # the exec time of this function is 10+ seconds (sum of DELAYS)
print("*" * 50)


def handling_exceptions_in_futures():
    """
    # If some Exception was occurred in some
    # Future, the Future.result() call will raise it.
    # Therefore, it's better to wrap the 'result' call in try/except:
    """
    with cf.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures_list = [executor.submit(work, d) for d in (1, 2)]
        futures_list.append(
            executor.submit(raise_exc_with_delay, 1)
        )
        passes, fails = [], []
        for f in futures_list:
            try:
                passes.append(f.result())
            except RuntimeError as exc:
                fails.append(
                    (type(exc), str(exc))
                )

        print("results: ", passes)
        print("errors: ", fails)

        # OR you can extract the Exception object
        # from the Future without raising this Exception
        fut_with_exc = executor.submit(raise_exc_with_delay, 1)
        exc = fut_with_exc.exception()
        print(type(exc), exc, sep=", ")

        print(fut_with_exc.exception())


# handling_exceptions_in_futures()
print("*" * 50)


def using_submit_and_as_completed():
    """
    getting the results in order as they were received
    """

    with cf.ThreadPoolExecutor(
            max_workers=3
    ) as ex:
        t = time.perf_counter()
        futures_list = [ex.submit(work, d) for d in (9, 5, 1)]

        res = [f.result() for f in cf.as_completed(futures_list)]
        print('exec time: ', time.perf_counter() - t)
        print(res)


# using_submit_and_as_completed()
print("*" * 50)


def using_wait_with_timeout():
    """
    using concurrent.futures.wait function with Timeout
    """
    delays = (3, 5, 2)

    t = time.perf_counter()
    with cf.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        futures_list = [executor.submit(work, d) for d in delays]
        done_and_undone_futures = cf.wait(
            futures_list,
            timeout=max(delays) - 1
        )
        # 'exec time' is 4.00+ seconds: the Timeout value
        print('exec time: ', time.perf_counter() - t)

        done_futures, undone_futures = done_and_undone_futures.done, done_and_undone_futures.not_done
        print(f'Done futures: {done_futures}')
        print(f'Undone futures: {undone_futures}')

        # Also we can extract the Results from Done and Undone Futures
        done_results = [f.result() for f in done_futures]
        # 'exec time' is the SAME (almost) as the 'exec time' above
        print('exec time: ', time.perf_counter() - t)
        print(done_results)

        undone_results = [f.result() for f in undone_futures]
        # 'exec time' is 5.00+ seconds: the Time of execution of the SLOWEST Task (+ small Overhead).
        # This because we need to wait this additional 1 second when extract the result from the Undone Future
        print('exec time: ', time.perf_counter() - t)
        print(undone_results)

        # *If you shift the code at lines 208-221 on ONE INDENT LEFT (Out of the ThreadPoolExecutor
        # context manager body), your FIRST 'exec_time' will be the SAME as LAST 'exec_time'
        # and equals to 5.00+ seconds.
        # This is because the ThreadPoolExecutor instance automatically waits for ALL Futures have been completed!


# using_wait_with_timeout()
print("*" * 50)


def using_wait_with_first_completed():
    """
    using concurrent.futures.wait function with return_when=FIRST_COMPLETED argument
    """
    delays = (3, 5, 2)

    t = time.perf_counter()
    with cf.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        futures_list = [executor.submit(work, d) for d in delays]

        done_and_undone_futures = cf.wait(
            futures_list,
            return_when=cf.FIRST_COMPLETED  # by default 'return_when=cf.ALL_COMPLETED'
        )

        # exec time is 2.00+ seconds: the Time of execution of the FASTEST Task
        print('exec time: ', time.perf_counter() - t)

        done_futures, undone_futures = done_and_undone_futures.done, done_and_undone_futures.not_done
        print(f'Done futures: {done_futures}')
        print(f'Undone futures: {undone_futures}')

        assert len(done_futures) == 1  # sure that there is only one Future was in 'done' set
        done_future = next(iter(done_futures), None)
        print(f'Done future: {done_future}')  # print this Future

        print('Result is: ', done_future.result())
        # 'exec time' is the SAME (almost) as the 'exec time' above
        print('exec time: ', time.perf_counter() - t)

        # Here will be the same behaviour as in function 'using_wait_with_timeout':
        # if you will try to extract the Result from Undone Futures, you will have additional wait time
        # for this, and the final 'exec time' for processing will be 5.00+ seconds
        # (the Time of execution of the SLOWEST Task)


# using_wait_with_first_completed()
print("*" * 50)


def using_wait_with_first_exception():
    """
    using concurrent.futures.wait function with return_when=FIRST_COMPLETED argument
    """
    delays = (2, 5, 3)

    t = time.perf_counter()
    with cf.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        futures_list = [executor.submit(raise_exc_with_delay, 1.3)]
        futures_list.extend([executor.submit(work, d) for d in delays])

        done_and_undone_futures = cf.wait(
            futures_list,
            return_when=cf.FIRST_EXCEPTION
        )
        # exec time is 1.30+ seconds: the Time of execution of the Task which raises Exception
        print('exec time: ', time.perf_counter() - t)

        done_futures, undone_futures = done_and_undone_futures.done, done_and_undone_futures.not_done
        print(f'Done futures: {done_futures}')
        print(f'Undone futures: {undone_futures}')

        # Fist Task which was executed raises Exception, and we wait for FIRST_EXCEPTION,
        # and this Task's Future is placed to the 'done_futures' set
        assert len(done_futures) == 1  # sure that we have Only 1 Future is in DONE set
        done_future = next(iter(done_futures), None)
        print(f'Done future: {done_future}')  # print this Future
        error = done_future.exception()
        print('Exception from Future', type(error), error, sep=": ")

        # 'exec time' is the SAME (almost) as the 'exec time' above
        print('exec time: ', time.perf_counter() - t)

        # if you will try to extract the Result from the Undone Futures, you will have additional wait time
        # for this, at the last 'exec time' will be 5.00+ seconds - the Time of execution of the SLOWEST Task


# using_wait_with_first_exception()
print("*" * 50)


def futures_cancellation():

    def infinite_loop(limit_value):
        logger.debug(f"'infinite_loop' start")
        counter = 0
        t_ = time.perf_counter()
        while counter < limit_value:
            counter += 1
            _ = counter * 10
        logger.debug(f'exec time: {time.perf_counter() - t_}')

    t = time.perf_counter()
    with cf.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        futures_list = [executor.submit(work, x) for x in (5, 2, 3)]
        futures_list.append(executor.submit(raise_exc_with_delay, 1))
        futures_list.append(executor.submit(infinite_loop, 20_000_000))

        futures_list[-1].cancel()

        done_and_undone_futures = cf.wait(
            futures_list,
            return_when=cf.FIRST_EXCEPTION
        )
        print('exec time: ', time.perf_counter() - t)

        done_futures = done_and_undone_futures.done
        print('Done futures: ', done_futures)
        undone_futures = done_and_undone_futures.not_done
        print('Undone futures: ', undone_futures)

        results = []
        for f in done_futures:
            try:
                results.append(f.result())
            except Exception as exc:
                results.append((type(exc), exc))
        print(results)

        for f in undone_futures:
            if f.running():
                print(f'{f} is running')
                f.cancel()
            print(f'Task running={f.running()}, cancelled={f.cancelled()}, done={f.done()}')

        print(done_futures)
        print(undone_futures)

        # print('Done results: ', [f.result() for f in done_futures])
        # print('Undone results: ', [f.result() for f in undone_futures])


futures_cancellation()