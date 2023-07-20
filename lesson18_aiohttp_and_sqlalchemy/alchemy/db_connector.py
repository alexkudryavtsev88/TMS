import asyncio
import logging

import config
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from lesson18_aiohttp_and_sqlalchemy.alchemy.models.user_models import Base, User


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DatabaseConnector:
    CHECK_QUERY = text("SELECT 1")

    def __init__(self, db_url):
        self._url = db_url
        self._engine = None
        self._session = None
        self._base = Base

    def connect(self):
        engine = create_async_engine(self._url, echo=True)
        self._engine = engine
        self._session = AsyncSession(engine)

    async def healthcheck(self):
        async with self._session as session:
            await session.execute(self.CHECK_QUERY)

    async def execute(self, query):
        async with self._session as s:
            async with s.begin():
                return await s.execute(query)

    # async def create_tables(self):
    #     # meta.create_all()
    #     Base.metadata.create_all(self._engine)


# async def run():
#     conn = DatabaseConnector(config.DB_URL)
#     conn.connect()
#
#     query = select(User).where(User.id == 1)
#     result = await conn.execute(query)
#     result_final = result.scalar_one_or_none()
#     print(result_final, type(result), sep=", ")


engine = create_async_engine(config.DB_URL)
session = AsyncSession(engine)


async def check_db():
    async with session:
        await session.execute(text("SELECT 1"))


async def get_users_by_ids(users_ids: list[int]):
    query = select(User).where(User.id.in_(users_ids))

    async with session:
        results = await session.execute(query)
        results = results.scalars().all()
        print([type(i) for i in results])
        names = [item.name for item in results]
        print(f"names: {names}")


async def get_user_by_id(user_id: int):
    query = select(User).where(User.id == user_id)

    async with session:
        results = await session.execute(query)
        result = results.unique().scalar_one_or_none()
        print(f"Result: {result}")
        if result:
            print(
                f"User name: {result.name}, "
                f"user age: {result.age}"
            )


async def update_user_by_id(user_id: int, **data):
    async with session:
        async with session.begin():



asyncio.run(get_user_by_id(user_id=1))
