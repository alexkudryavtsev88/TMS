import asyncio
import time


async def coro(arg: int):
    await asyncio.sleep(arg)
    return arg


async def run_many_task_slow():
    """
    DON'T USE AWAIT within the FOR loop!
    Using AWAIT blocks each Iteration of
    the loop until the Task will be completed
    """
    start = time.perf_counter()
    result = [await coro(i) for i in range(1, 11)]  # SYNCHRONOUS EXECUTION!!! exec time ~ 45 sec
    print(f"Exec time: {time.perf_counter() - start}")
    return result


async def run_many_task_fast():
    """
    For running 1+ coroutines in Async manner,
    base solution is to use asyncio.gather() function
    """

    start = time.perf_counter()
    result = await asyncio.gather(
        *[coro(i) for i in range(1, 11)],  # ASYNCHRONOUS EXECUTION!!! exec time ~ 10 sec
    )

    print(f"Exec time: {time.perf_counter() - start}")
    for item in result:
        if isinstance(item, Exception):
            print(f'Error: {(type(item), item)}')
        else:
            print(f"Success: {item}")

    print(result)
    return result


async def handling_exceptions_in_gather():
    async def coro_with_exc(val):
        t = time.perf_counter()
        await asyncio.sleep(val)
        raise RuntimeError(f'FAIL after {time.perf_counter() - t} sec')

    t1 = time.perf_counter()

    sleep_times = [0.5, 1, 2, 3, 4.5]

    tasks = [
        coro_with_exc(sleep_times[0])
    ]
    tasks.extend(
        coro(i) for i in sleep_times[1: len(sleep_times) - 1]
    )
    tasks.append(
        coro_with_exc(sleep_times[-1])
    )

    results = await asyncio.gather(
        *tasks,
        return_exceptions=True
    )

    success, errors = [], []
    for item in results:
        if isinstance(item, Exception):
            errors.append(item)
        else:
            success.append(item)

    exec_time = time.perf_counter() - t1
    print(f'exec_time: {exec_time}')
    assert max(sleep_times) <= exec_time < max(sleep_times) + 0.5

    print(f"Success: {success}")
    print(f"Errors: {errors}")


async def using_create_task_and_as_completed():
    t1 = time.perf_counter()
    tasks = [
        asyncio.create_task(coro(i)) for i in (3, 1, 2)
    ]
    for idx, result in enumerate(asyncio.as_completed(tasks)):
        print(f"Result N {idx+1}: {await result}")

    print(f'exec_time: {time.perf_counter() - t1}')


asyncio.run(using_create_task_and_as_completed())

