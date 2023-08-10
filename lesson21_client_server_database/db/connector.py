import asyncio

import sqlalchemy.exc
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, delete
from asyncpg.exceptions import UniqueViolationError

from lesson21_client_server_database.db.models import User, Post, Comment, Like
from lesson21_client_server_database.structures import OperationStatus


class DatabaseConnector:

    def __init__(self, db_url):
        self._url = db_url
        self._engine = create_async_engine(self._url, echo=True)
        # *async_sessionmaker* call returns AsyncSession class object
        self._session = async_sessionmaker(self._engine)

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

        # here (and in all methods bellow) we use *async with self._session()*
        # instead of *async with self._session*
        # because *self._session* stores the reference to
        # the AsyncSession class, NOT AsyncSession class Instance!
        async with self._session() as session:
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

        async with self._session() as session:
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

        async with self._session() as session:
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

    # TODO: Implement methods bellow as Homework

    async def edit_post(
        self,
        user_name: str,            # for Select!
        user_age: int,             # for Select!
        post_title: str,           # for Select!
        post_description: str,     # for Select!
        new_post_title: str,       # for UPDATE!
        new_post_description: str  # for UPDATE!
    ):
        """
        To update the record from DB you need to
        SELECT this record firstly! And this is NOT
        required to build the query using *update* function
        - you just need to update the Python Object retrieved by SELECT query!
        """
        async with self._session() as session:
            async with session.begin():
                post = await self._get_post(
                    session,
                    user_name,
                    user_age,
                    post_title,
                    post_description
                )
                if not post:
                    return OperationStatus.NOT_EXIST

                post.title = new_post_title
                post.description = new_post_description

                return OperationStatus.SUCCESS

    async def edit_comment(
        self,
        user_name: str,         # for Select!
        user_age: int,          # for Select!
        post_title: str,        # for Select!
        post_description: str,  # for Select!
        comment_title: str,     # for Select!
        new_comment_title: str  # for UPDATE!
    ):
        """
        Please read *edit_post* method documentation
        """

    async def delete_post(
        self,
        user_name: str,
        user_age: int,
        post_title: str,
        post_description: str,
    ):
        """
        To DELETE the record from the DB it's NOT required to
        SELECT this record before, but in common case.
        In current case we need to SELECT the Post firstly,
        then DELETE it through the *session.delete()*.
        This is because when using just *delete().where()* Query there will
        be a problem:
        - *delete()* result CAN'T support *join* / *join_from*
        - when we just specify all our filtering criteria inside *where()*,
        this works, but there will be a Cartesian product of the appropriate rows,
        because the filtering is made by rows from 2 several Tables
        """
        async with self._session() as session:
            async with session.begin():
                if (
                        post := await self._get_post(
                            session,
                            user_name,
                            user_age,
                            post_title,
                            post_description
                        )
                ):
                    await session.delete(post)
                    return OperationStatus.SUCCESS

                return OperationStatus.NOT_EXIST

    async def delete_comment(
        self,
        user_name: str,
        user_age: int,
        post_title: str,
        post_description: str,
        comment_title: str
    ):
        """
        Please read *delete_post* method documentation
        """
        async with self._session() as session:
            async with session.begin():
                deleted_comment = await session.execute(
                    delete(Comment)
                    .join_from(Comment, User, Comment.user_id == User.id)
                    .join_from(Comment, Post, Comment.post_id == Post.id)
                    .where(
                        User.name == user_name,
                        User.age == user_age,
                        Post.title == post_title,
                        Post.description == post_description,
                        Comment.title == comment_title
                    )
                )
                print(deleted_comment)

    async def delete_like(
        self,
        user_name: str,
        user_age: int,
        post_title: str,
        post_description: str,
    ):
        """
        Please read *delete_post* method documentation
        """
        async with self._session() as session:
            async with session.begin():
                deleted_like = await session.execute(
                    delete(Like)
                    .join_from(Like, User, Like.user_id == User.id)
                    .join_from(Like, Post, Like.post_id == Post.id)
                    .where(
                        User.name == user_name,
                        User.age == user_age,
                        Post.title == post_title,
                        Post.description == post_description
                    )
                )
                print(deleted_like)
