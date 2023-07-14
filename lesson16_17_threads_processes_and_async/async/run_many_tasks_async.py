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

    async def coro_with_exc():
        await asyncio.sleep(1.5)
        raise RuntimeError('FAIL')

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


asyncio.run(run_many_task_fast())

