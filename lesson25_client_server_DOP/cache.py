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
TMethod = Callable[[P], Coroutine[None, None, Any]]


class DataSource:

    def __init__(self):
        self._ds = {i: f"TEST_{i}" for i in range(101)}

    async def get_data(self, key):
        sleep_time = 3
        await asyncio.sleep(sleep_time)
        logger.debug(f"Get value by key {key} from DATA SOURCE")
        return self._ds.get(key)


class AsyncCache:
    _CACHE = TTLCache(maxsize=10_000, ttl=86_400)
    _LOCK = asyncio.Lock()
    _LOCKS_MAP = {}
    _LOCKS_MAP_MAX_SIZE = 10_000

    @classmethod
    async def get_with_no_lock(
        cls,
        cache_key: int | str | tuple[Any, ...],
        data_retrieve_method: TMethod,
        *args,
        **kwargs,
    ):
        """
        This approach doesn't use any Lock at all.
        This is OK for case when several Tasks try to get
        value by the DIFFERENT keys (the Cache can not be used
        in this case at all, because ALL keys are the DIFFERENT),
        but when the several Tasks try to get value by the SAME key -
        each Task will go to the Data Source for the Value
        instead of using Cache (and we have a redundant calls to
        the Data Source)
        """
        value = cls._CACHE.get(cache_key)
        if value is not None:
            logger.debug(f"Get key {cache_key} from CACHE")
            return value

        value = await data_retrieve_method(*args, **kwargs)
        cls._CACHE[cache_key] = value

        return value

    @classmethod
    async def get_with_single_lock(
        cls,
        cache_key: int | str | tuple[Any, ...],
        data_retrieve_method: TMethod,
        *args,
        **kwargs,
    ):
        """
        This approach uses single Lock, this is good for the case
        when several Tasks try to get value by the SAME key from Cache, but it's
        very slow (sequential execution) if the several Tasks try to get
        value by the DIFFERENT keys (because each call to the Data Source
        is made under the Lock)
        """
        async with cls._LOCK:
            value = cls._CACHE.get(cache_key)
            if value is not None:
                logger.debug(f"Get key {cache_key} from CACHE")
                return value

            value = await data_retrieve_method(*args, **kwargs)
            cls._CACHE[cache_key] = value

            return value

    @classmethod
    async def get_with_locks_map(
        cls,
        cache_key: int | str | tuple[Any, ...],
        data_retrieve_method: TMethod,
        *args,
        **kwargs,
    ) -> Any:
        """
        This approach uses separate Lock for each passed Cache key
        (if the key is unique, of course)
        This provides a correct Cache read/write operations
        and concurrent non-blocking execution in 2 general use-cases:
        - several Tasks try to get Value from Cache by the SAME Key
        - several Tasks try to get Value from Cache by the DIFFERENT Keys

        NOTE: 'select for update' query in SQL works the similar way
        """
        lock = cls._LOCKS_MAP.get(cache_key)
        if lock is None:
            lock = asyncio.Lock()
            cls._LOCKS_MAP[cache_key] = lock

        if (
            not lock.locked()
            or (await lock.acquire()) and lock.release() is None
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
            cache_obj.get_using_locks_map(
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
    await get_cache_keys_concurrently(cache, ds, tasks_count=5)
    cache._CACHE.clear()
    await get_cache_keys_concurrently(cache, ds, tasks_count=5, use_same_key=True)


asyncio.run(verify_cache_work())