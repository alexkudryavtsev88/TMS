import asyncio
import time
from dataclasses import dataclass
from typing import Generator


@dataclass
class TaskResult:
    value: str
    sleep_time: float
    exec_time: float

    def __str__(self):
        return f"Value {self.value}, process_time: {self.exec_time}, sleep: {self.sleep_time}"


def _gen_value(args_lst: list[int]) -> Generator[str, None, None]:
    for arg in args_lst:
        yield f"Test_{arg}"


def _create_tasks(source, sleeps):
    """
    Returns a list of 'asyncio.Task' objects
    """
    return [
        asyncio.create_task(task(batch, sleep_time=sleeps[idx]))
        for idx, batch in enumerate(_gen_value(source))
    ]


async def task(value: str, sleep_time: int) -> TaskResult:
    """
    - Measures a time when function is started
    - Sleep a specified count of seconds ('sleep_time' param)
    - Returns a dict which contains received batch, time of sleeping and measuring execution time
    """
    start = time.time()
    await asyncio.sleep(sleep_time)
    return TaskResult(value=value, sleep_time=sleep_time, exec_time=time.time() - start)


async def get_tasks_results_in_initial_order(source, sleeps):
    """
    Applies 'asyncio.gather()' to the tasks lists:
    - Returns the list of Tasks results where results order corresponds to
      the order of Tasks launch:
      first launched task's result is first, last launched task's result is last
    """
    tasks = _create_tasks(source, sleeps)
    return await asyncio.gather(*tasks)


async def get_tasks_results_in_as_completed_order(source, sleeps):
    """
    - Applies 'asyncio.as_completed()' to the tasks lists
    - Returns the list of Tasks results where results order corresponds to
      the order of Tasks completion:
      first completed task's result is first, last completed task's result is last
    """
    tasks = _create_tasks(source, sleeps)
    return [await t for t in asyncio.as_completed(tasks)]


async def main(source, sleeps):
    coroutines_map = {
        "initial": get_tasks_results_in_initial_order,
        "as completed": get_tasks_results_in_as_completed_order,
    }
    for name, coro in coroutines_map.items():
        start = time.time()
        print(f"Starting the task processing with results in {name} order:")

        response = await coro(source, sleeps)
        for item in response:
            print(item)
        print(f"common time spent: {time.time() - start}\n")


if __name__ == "__main__":
    values = [1, 2, 3, 4, 5]
    sleep_times = (2, 6, 4, 1, 3)

    args = (values, sleep_times)
    asyncio.run(main(*args))
