# import asyncio
# import logging
# import random
# import string
#
# import config
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, delete
from lesson18_19_sqlalchemy.models import User, Post


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

    async def execute_any_query(self, query):
        async with self._session as s:
            async with s.begin():
                result = await s.execute(query)

                return result

    @staticmethod
    async def _get_user_by_id_from_session(session_, user_id: int):
        """
        This method builds query, executes it through *session* which it got as argument
        and returns result as single User object or None if there is no such id in the
        "users" table in Database
        """
        query = select(User).where(User.id == user_id)

        results = await session_.execute(query)
        result = results.unique().scalar_one_or_none()

        return result

    @staticmethod
    async def _get_users_by_ids_from_session(session_, users_ids: list[int]):
        """
        This method builds query, executes it through *session*
        and returns result
        """
        query = select(User).where(User.id.in_(users_ids))

        results = await session_.execute(query)
        result = results.unique().scalars().all()

        return result

    async def get_user_by_id(self, user_id: int):
        """
        This method just calls the *self._get_user_by_id_from_session*
        within the opened Session.
        At moment when the result has been returned, the Session
        begun in this function will be closed
        """
        async with self._session as s:
            return await self._get_user_by_id_from_session(s, user_id)

    async def get_users_by_ids(self, users_ids: list[int]):
        """
        This method just calls the *self._get_users_by_ids_from_session*
        within the opened Session.
        At moment when the result has been returned, the Session
        begun in this function will be closed
        """
        async with self._session as s:
            return await self._get_users_by_ids_from_session(s, users_ids)

    async def delete_post_by_id(self, post_id: int):
        """
        Deletes row from "posts" table
        """
        async with self._session as s:
            """
            Using *session.begin()* context manager
            you don't need to call *session.commit()* OR *session.rollback()*
            at the end of *async with self._session as s* block
            """
            async with s.begin():
                query = delete(Post).where(Post.id == post_id)
                return await s.execute(query)

    async def update_user_by_id(self, user_id: int, **data):
        if not data:
            print(f"No data to update user with Id {user_id}")
            return

        async with self._session as s:
            async with s.begin():
                user = await self._get_user_by_id_from_session(s, user_id=user_id)
                """
                NOTE: if we would use *self.get_user_by_id(user_id=user_id)* here,
                the updates we will make bellow will not be applied to real Database state!
                Because in this case the User object was got within the another Session
                """
                if user is None:
                    print(f"No user with Id: {user_id}")
                    return

                if (name := data.get("name")) is not None:
                    user.name = name  # update user's name
                if (age := data.get("age")) is not None:
                    user.age = age  # update user's age
                if (gender := data.get("gender")) is not None:
                    user.gender = gender  # update user's gender
                if (nationality := data.get("nationality")) is not None:
                    user.nationality = nationality  # update user's nationality

                """
                add new post to User: this requires to use
                *lazy="joined"* on "posts" attribute in User class.
                This makes automatic JOIN of "users" and "posts" tables
                when you just SELECT a User, and also it binds the "posts"
                to the User object within the Session
                """
                if (new_post := data.get("new_post")) is not None:
                    user.posts.append(new_post)

                """
                At the end of context manager body the updates we made above
                are applied to the Database
                """

                return "Ok"