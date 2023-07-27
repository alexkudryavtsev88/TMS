import asyncio
from lesson18_19_20_sqlalchemy import config
from lesson18_19_20_sqlalchemy.models import Post, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


# async def _get_post(
#     session: AsyncSession,
#     user_name: str,
#     user_age: int,
#     post_title: str,
#     post_description: str
# ) -> Post | None:
#     return (
#         await session.execute(
#             select(Post).join(User).where(
#                 User.name == user_name,
#                 User.age == user_age,
#                 Post.title == post_title,
#                 Post.description == post_description
#             )
#         )
#     ).unique().scalar_one_or_none()


# async def main():
#     engine = create_async_engine(config.DB_URL, echo=True)
#     async with AsyncSession(engine) as session:
#         async with session.begin():
#             post = await _get_post(
#                 session,
#                 user_name="Alex",
#                 user_age=34,
#                 post_title="Alex 1st post",
#                 post_description="Hello! I am Alex, I am 34 years old"
#             )
#             print(post)
#
#
# asyncio.run(main())



