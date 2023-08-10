"""
Async cache
"""

import asyncio.locks
import logging
import sys
import time
from typing import Callable, Coroutine, Any, ParamSpec, Type

from cachetools import TTLCache

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s "
           "[%(name)s:%(funcName)s:%(lineno)s] -> %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
    stream=sys.stdout,
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


P = ParamSpec('P')
TMethod = Callable[
    [P.args, P.kwargs],
    Coroutine[None, None, Any]
]


class AsyncCache:
    _CACHE = TTLCache(maxsize=10_000, ttl=86_400)
    _LOCKS_MAP = {}
    _LOCKS_MAP_MAX_SIZE = 10_000

    @classmethod
    async def get(
        cls,
        cache_key: int | str | tuple[Any, ...],
        data_retrieve_method: TMethod,
        *args,
        **kwargs,
    ) -> Any:
        """
        Uses separate Lock for each passed Cache key.
        This approach provides a correct Cache read/write operations
        and concurrent non-blocking execution in 2 general use-cases:
        - several Tasks try to get Value from Cache by the SAME Key
        - several Tasks try to get Value from Cache by the DIFFERENT Keys
        """
        if not (lock := cls._LOCKS_MAP.get(cache_key)):
            lock = asyncio.Lock()
            cls._LOCKS_MAP[cache_key] = lock

        if (
            not lock.locked() or (await lock.acquire()) and lock.release() is None
        ) and (cached := cls._CACHE.get(cache_key)) is not None:
            logger.debug(f"get data from cache by key: {cache_key}")
            return cached

        async with lock:
            logger.debug(f"key {cache_key} is NOT in Cache, request for data")
            data = await data_retrieve_method(
                *args, **kwargs
            )
            cls._CACHE[cache_key] = data

        cls._check_locks_limit()

        return data

    @classmethod
    def _check_locks_limit(cls):
        """
        Need to clear *_LOCKS_MAP* when its size reached
        *_LOCKS_MAP_MAX_SIZE* limit to avoid the endless growing
        of *_LOCKS_MAP* size
        """
        if len(cls._LOCKS_MAP) >= cls._LOCKS_MAP_MAX_SIZE:
            logger.debug("remove all existing locks")
            cls._LOCKS_MAP.clear()


# ===== TESTS ===== #
class DataSource:

    def __init__(self):
        self._ds = {i: f"TEST_{i}" for i in range(100)}

    async def get_data(self, key):
        if key == 0:
            sleep_time = 5
        else:
            sleep_time = 3

        await asyncio.sleep(sleep_time)
        logger.debug(f"Get value by key {key} from DATA SOURCE")
        return self._ds.get(key)


async def get_cache_keys_concurrently(
    cache_obj: Type[AsyncCache],
    data_source: DataSource,
    tasks_count: int = 10,
    use_same_key: bool = False
):
    tasks = []
    same_key = 0

    t_start = time.perf_counter()
    for item in range(tasks_count):
        if use_same_key:
            key = same_key
        else:
            key = item

        tasks.append(
            cache_obj.get(
                key,
                data_source.get_data,
                key
            )
        )

    results = await asyncio.gather(
        *tasks
    )
    t_end = time.perf_counter() - t_start

    print(f"Results: {results}")
    print(f"Exec time: {t_end}")


async def verify_cache_work():
    cache = AsyncCache
    ds = DataSource()
    await get_cache_keys_concurrently(cache, ds, tasks_count=5, )
    cache._CACHE.clear()
    await get_cache_keys_concurrently(cache, ds, tasks_count=5, use_same_key=True)


asyncio.run(verify_cache_work())