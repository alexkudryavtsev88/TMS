# import os
# import asyncio
#
# from sqlalchemy import text
# from sqlalchemy.ext.asyncio import async_session, create_async_engine
# from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from lesson18_aiohttp_and_sqlalchemy.alchemy.models.user_models import User

db_user = "admin"
db_pass = "cp12345"
db_host = "127.0.0.1"
db_port = 5432
db_name = "tms"

DB_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
print(DB_URL)

# PREFIX = "db_"
# DB_CONFIG = {
#     f"{PREFIX}url": DB_URL,
#     f"{PREFIX}pool_size": int(os.getenv("DATABASE_POOL_SIZE", "1")),
#     f"{PREFIX}pool_pre_ping": True,
#     f"{PREFIX}pool_recycle": -1,
#     f"{PREFIX}future": True,
#     f"{PREFIX}echo": True,
# }


# engine = create_async_engine(DB_URL)
# session = AsyncSession(engine)


# async def check_db():
#     async with session:
#         await session.execute(text("SELECT 1"))
#
#
# async def get_users_by_ids(users_ids: list[int]):
#     query = select(User)\
#         .where(User.id.in_(users_ids))
#     async with session:
#         results = await session.execute(query)
#         results = results.scalars().all()
#         print([type(i) for i in results])
#         names = [item.name for item in results]
#         print(f"names: {names}")
#
#
# async def get_user_by_id(user_id: int):
#     query = select(User) \
#         .where(User.id == user_id)
#
#     async with session:
#         async with session.begin():
#             results = await session.execute(query)
#             result = results.unique().scalar_one_or_none()
#             print(f"Result: {result}")
#             if result:
#                 print(
#                     f"User name: {result.name}, "
#                     f"user age: {result.age}"
#                 )

# asyncio.run(check_db())
# asyncio.run(get_user_by_id(user_id=1))


