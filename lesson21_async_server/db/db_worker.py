from typing import Collection

import sqlalchemy.exc
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, delete
from asyncpg.exceptions import UniqueViolationError

from lesson18_19_20_sqlalchemy.models import User, Post


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

    @staticmethod
    async def _get_all_users(session: AsyncSession):
        return (
            await session.execute(
                select(User)
            )
        ).unique().scalar_one_or_none()

    @staticmethod
    async def _get_user_by_name_and_age(session: AsyncSession, user_name: str, user_age: int):
        return (
            await session.execute(
                select(User).where(
                    User.name == user_name,
                    User.age == user_age
                )
            )
        ).unique().scalar_one_or_none()

    # @staticmethod
    # async def _get_users_by_names_and_ages(session: AsyncSession, users_names_ages: dict[str, int]):
    #     return (
    #         await session.execute(
    #             select(User).where(
    #                 User.name.in_(users_names_ages.keys()),
    #                 User.age.in_(users_names_ages.values())
    #             )
    #         )
    #     ).unique().scalars().all()

    @staticmethod
    async def _get_user_posts_by_title(session: AsyncSession, user_name: str, user_age: int, post_title: str):
        return (
            await session.execute(
                select(User).where(
                    User.name == user_name,
                    User.age == user_age,
                    Post.title == post_title
                )
            )
        ).unique().scalar_one_or_none()

    @staticmethod
    async def _get_user_by_id(session: AsyncSession, user_id: int):
        query = select(User).where(User.id == user_id)

        result = await session.execute(query)
        return result.unique().scalar_one_or_none()

    @staticmethod
    async def _get_users_by_ids_from_session(session: AsyncSession, users_ids: list[int]):
        """
        This method builds query, executes it through *session*
        and returns result
        """
        query = select(User).where(User.id.in_(users_ids))

        results = await session.execute(query)
        users_list = results.unique().scalars().all()

        """
        - 'unique()' call on result is required 
          (because we have lazy="joined" flag specified in User class)
        - Call of chain '.scalars().all()' returns a list of User entities
           Posts related to the retrieved Users are available through the 'User.posts' attribute 
           (because we have lazy="joined" flag specified in User class)
        - Please note, that retrieved User objects are attached to the *session*. 
          When we update some of them latter within the SAME session, the ORM is automatically
          executes 'UPDATE users SET ...' query
        """

        return users_list

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
            """
            starting the new Transaction using 'begin()' context manager
            to avoid making 'commit / rollback' directly later
            """
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

    async def add_new_user(self, user: User):
        async with self._session as s:
            async with s.begin():
                result = await self._add_user(s, user=user)

                return result

    @staticmethod
    async def _add_user(session: AsyncSession, user: User):
        try:
            """
            create SAVEPOINT for started Transaction
            """
            async with session.begin_nested():
                session.add(user)  # attach User object to the session
                return "Ok"

        except sqlalchemy.exc.IntegrityError as exc:
            """
            Here we check that underlying Exception is
            the UniqueViolationError which occurs when
            the UNIQUE constraint was Violated: in this specific case,
            it may occur upon adding the 2 SAME Users
            """
            match exc.orig and exc.orig.__cause__:
                case UniqueViolationError() as exc:
                    """
                    Please NOTE that here we only print the 
                    Exception's traceback without raising 
                    the Exception itself!
                    """
                    print(repr(exc))
                case _:
                    raise exc

            # Transaction state will be RELEASED OR ROLLED BACK to the SAVEPOINT


