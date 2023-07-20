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


class DatabaseWorker:

    def __init__(self, db_url):
        self._url = db_url
        self._engine = None
        self._session = None

    def connect(self):
        self._engine = create_async_engine(self._url, echo=True)
        self._session = AsyncSession(self._engine)

    async def check_db(self):
        async with self._session as s:
            await s.execute(text("SELECT 1"))

    async def get_user_by_id(self, user_id: int):
        async with self._session as s:
            return await self._get_user_by_id(s, user_id)

    async def get_users_by_ids(self, users_ids: list[int]):
        async with self._session as s:
            return self._get_users_by_ids(s, users_ids)

    @staticmethod
    async def _get_user_by_id(session_, user_id: int):
        query = select(User).where(User.id == user_id)

        results = await session_.execute(query)
        result = results.unique().scalar_one_or_none()

        return result

    @staticmethod
    async def _get_users_by_ids(session_, users_ids: list[int]):
        query = select(User).where(User.id.in_(users_ids))

        results = await session_.execute(query)
        result = results.unique().scalars().all()

        return result

    async def update_user_by_id(self, user_id: int, **data):
        if not data:
            print(f"No data to update user with Id {user_id}")
            return

        async with self._session as s:
            async with s.begin():
                user = await self._get_user_by_id(s, user_id=user_id)

                if user is None:
                    print(f"No user with Id: {user_id}")
                    return

                if (name := data.get("name")) is not None:
                    user.name = name
                if (age := data.get("age")) is not None:
                    user.age = age
                if (gender := data.get("gender")) is not None:
                    user.gender = gender
                if (nationality := data.get("nationality")) is not None:
                    user.nationality = nationality

                return "Ok"


async def update_user_nationality_and_check_updates(user_id):
    db_worker = DatabaseWorker(config.DB_URL)
    db_worker.connect()
    await db_worker.check_db()

    update_result = await db_worker.update_user_by_id(user_id=user_id, nationality='Canada')
    assert update_result.lower() == 'ok'
    real_user = await db_worker.get_user_by_id(user_id=user_id)
    print(real_user)
    assert real_user.nationality == 'Canada'


asyncio.run(
    update_user_nationality_and_check_updates(user_id=1)
)
