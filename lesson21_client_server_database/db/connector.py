from typing import Collection

import sqlalchemy.exc
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, delete
from asyncpg.exceptions import UniqueViolationError

from lesson21_client_server_database.db.models import User, Post, Comment, Like
from lesson21_client_server_database.structures import Status


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
    async def _get_user(session: AsyncSession, user_name: str, user_age: int) -> User | None:
        return (
            await session.execute(
                select(User).where(
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
                select(Post).where(
                    User.name == user_name,
                    User.age == user_age,
                    Post.title == post_title,
                    Post.description == post_description
                )
            )
        ).unique().scalar_one_or_none()

    async def add_post(
        self,
        user_name: str,
        user_age: int,
        post_title: str,
        post_description: str
    ) -> Status:

        self.check_session()

        async with self._session as session:
            async with session.begin():
                user = await self._get_user(
                    session, user_name, user_age
                )
                if not user:
                    print(
                        f"Cannot add a Post '{post_title}', '{post_description}' "
                        f"to User {user_name} {user_age} "
                        f"which doesn't exist!"
                    )
                    return Status.NOK

                user.posts.append(
                    Post(
                        title=post_title,
                        description=post_description,
                        user_id=user.id
                    )
                )
                return Status.OK

    async def add_comment(
        self,
        user_name: str,
        user_age: int,
        post_title: str,
        post_description: str,
        comment_title: str
    ) -> Status:
        self.check_session()

        async with self._session as session:
            async with session.begin():
                post = await self._get_post(
                    session,
                    user_name, user_age,
                    post_title, post_description
                )
                if not post:
                    print(
                        f"Cannot add a Comment to Post '{post_title}', '{post_description}' "
                        f"because this Post doesn't exist OR is NOT related to "
                        f"the User '{user_name}', {user_age}"
                    )
                    return Status.NOK

                post.comments.append(
                    Comment(
                        title=comment_title,
                        post_id=post.id,
                        user_id=post.user_id
                    )
                )
                return Status.OK

    async def add_like(
        self,
        user_name: str,
        user_age: int,
        post_title: str,
        post_description: str,
    ) -> Status:

        self.check_session()

        async with self._session as session:
            async with session.begin():
                post = await self._get_post(
                    session,
                    user_name, user_age,
                    post_title, post_description
                )
                if not post:
                    print(
                        f"Cannot add a Like to Post '{post_title}', '{post_description}' "
                        f"because this Post doesn't exist OR is NOT related to "
                        f"the User '{user_name}', {user_age}"
                    )
                    return Status.NOK

                post.likes.append(
                    Like(
                        post_id=post.id,
                        user_id=post.user_id
                    )
                )
                return Status.OK

    # async def delete_post(self, user_name: str, user_age: int, post_title: str, post_description: str):
    #     """
    #     Deletes row from "posts" table
    #     """
    #     async with self._session as s:
    #         async with s.begin():
    #             query = delete(Post).where(
    #                 User.name == user_name,
    #                 User.age == user_age,
    #                 Post.title == post_title,
    #                 Post.description == post_description
    #             )
    #             return await s.execute(query)



