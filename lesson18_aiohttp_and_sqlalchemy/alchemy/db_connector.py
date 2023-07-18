import asyncio
import logging
import time

import config
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_session, create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.ext.asyncio import async_sessionmaker


# from typing import Any


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def init_all_connections():
    logger.info("Initializing the DB connections...")

    connector = DatabaseConnector
    connector.configure_session()

    start = time.perf_counter()
    poll_size = config.DB_CONFIG[f"{config.PREFIX}pool_size"]
    await asyncio.gather(*[connector.check() for _ in range(poll_size)])
    logger.info(
        "All DB connections are initialized (%0.2f sec)", time.perf_counter() - start
    )


class DatabaseConnector:
    SESSION = None
    CHECK_QUERY = text("SELECT 1")

    @classmethod
    def configure_session(cls):
        engine = create_async_engine(config.DB_URL)
        cls.SESSION = AsyncSession(engine)

    @classmethod
    async def check(cls):
        async with cls.SESSION as session:
            await session.execute(cls.CHECK_QUERY)

    async def healthcheck(self):
        await self.check()

    async def create_tables(self, meta):
        meta.create_all()
