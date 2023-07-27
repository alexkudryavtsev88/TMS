import asyncio
from typing import Collection

import sqlalchemy.exc
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, delete
from asyncpg.exceptions import UniqueViolationError

from lesson21_client_server_database.db import config
from lesson21_client_server_database.db.models import User, Post, Comment, Like
from lesson21_client_server_database.structures import OperationStatus


class DatabaseConnector:

    def __init__(self, db_url):
        self._url = db_url
        self._engine = None
        self._session = None

    def connect(self):
        self._engine = create_async_engine(self._url, echo=True)
        self._session = AsyncSession(self._engine)

    def check_session(self):
        if self._session is None:
            raise RuntimeError(
                'Database session is not created,'
                'please call "connect" method first!'
            )

    async def check_db(self):
        self.check_session()
        async with self._session as s:
            await s.execute(text("SELECT 1"))

    @staticmethod
    async def _get_user(
        session: AsyncSession,
        user_name: str,
        user_age: int
    ) -> User | None:
        return (
            await session.execute(
                select(User)
                .where(
                    User.name == user_name,
                    User.age == user_age
                )
            )
        ).unique().scalar_one_or_none()

    @staticmethod
    async def _get_post(
        session: AsyncSession,
        user_name: str,
        user_age: int,
        post_title: str,
        post_description: str
    ) -> Post | None:

        return (
            await session.execute(
                select(Post)
                .join(User)
                .where(
                    User.name == user_name,
                    User.age == user_age,
                    Post.title == post_title,
                    Post.description == post_description
                )
            )
        ).unique().scalar_one_or_none()

    @staticmethod
    async def _add_post_avoid_conflict(
        session: AsyncSession,
        user: User,
        post: Post,
    ) -> OperationStatus:
        try:
            async with session.begin_nested():
                user.posts.append(post)
                return OperationStatus.SUCCESS
        except sqlalchemy.exc.IntegrityError as exc:
            match exc.orig and exc.orig.__cause__:
                case UniqueViolationError() as exc:
                    print(repr(exc))
                    return OperationStatus.NOT_UNIQUE
                case _:
                    raise exc

    async def add_post(
        self,
        user_name: str,
        user_age: int,
        post_title: str,
        post_description: str
    ) -> OperationStatus:

        self.check_session()
        async with self._session as session:
            async with session.begin():
                user = await self._get_user(
                    session, user_name, user_age
                )
                if not user:
                    return OperationStatus.NOT_EXIST

                post = Post(title=post_title, description=post_description)
                return await self._add_post_avoid_conflict(session, user, post)

    async def add_comment(
        self,
        user_name: str,
        user_age: int,
        post_title: str,
        post_description: str,
        comment_title: str
    ) -> OperationStatus:
        self.check_session()

        async with self._session as session:
            async with session.begin():
                post = await self._get_post(
                    session,
                    user_name, user_age,
                    post_title, post_description
                )
                if not post:
                    return OperationStatus.NOT_EXIST

                post.comments.append(
                    Comment(
                        title=comment_title,
                        user_id=post.user_id  # required
                    )
                )
                return OperationStatus.SUCCESS

    async def add_like(
        self,
        user_name: str,
        user_age: int,
        post_title: str,
        post_description: str,
    ) -> OperationStatus:

        self.check_session()

        async with self._session as session:
            async with session.begin():
                post = await self._get_post(
                    session,
                    user_name, user_age,
                    post_title, post_description
                )
                if not post:
                    return OperationStatus.NOT_EXIST

                post.likes.append(
                    Like(
                        user_id=post.user_id  # required
                    )
                )
                return OperationStatus.SUCCESS


# async def main():
#     conn = DatabaseConnector(config.DB_URL)
#     conn.connect()
#     await conn.check_db()
#
#     result = await conn.add_like(
#         user_name="Alex",
#         user_age=34,
#         post_title="Last Alex post",
#         post_description="I'm added by SqlAlchemy!",
#         # comment_title="Last Alex comment(2)"
#     )
#     print(result)


# if __name__ == '__main__':
#     asyncio.run(main())