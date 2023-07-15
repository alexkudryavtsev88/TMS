import asyncio
import time

MY_RANGE = range(1, 6)


async def coro(i: int):
    print(f"sleeping {i} seconds")
    await asyncio.sleep(i)
    # time.sleep(i)  NEVER use time.sleep() in Coroutines! Only asyncio.sleep()
    return i


async def gather1():
    start_time = time.perf_counter()
    result = await asyncio.gather(
        *[coro(i) for i in MY_RANGE],
    )
    print(f"'gather1' exec time: {time.perf_counter() - start_time}")
    return result


async def gather2():
    start_time = time.perf_counter()
    result = await asyncio.gather(
        *[coro(i) for i in MY_RANGE],
    )
    print(f"'gather2' exec time: {time.perf_counter() - start_time}")
    return result


async def main():
    start_time = time.perf_counter()
    result = await asyncio.gather(
        gather1(),
        gather2()
    )
    print(f"'main' exec time: {time.perf_counter() - start_time}\n")

    print(f"Results: {result}")


asyncio.run(main())

