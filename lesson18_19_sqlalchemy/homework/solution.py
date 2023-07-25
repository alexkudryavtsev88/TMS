import asyncio
import datetime

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from lesson18_19_sqlalchemy.models import Post, User, Comment, Like
from lesson18_19_sqlalchemy import config


DTTM_FMT = '%Y-%m-%dT%H:%M:%SZ'


"""
1. Написать асинк функцию, которая:
- первый аргумент: post_id,
- второй: new_comment
- тело функции:
Получить объект Post по post_id и связанные с ним комменты, 
- обновить поле title у первого комментария: добавить к значению title строку "(updated at {current_datetime})",
- добавить новый комментарий (new_comment) в список комментариев поста 
- В самом конце функции сделать проверку, что первые две операции зафиксировались в базе 
(селект в отдельной сессии)
"""


async def update_post_comments(post_id: int, new_comment: Comment):
    first_post_comment_updated_text = f"(updated at {datetime.datetime.now().strftime(DTTM_FMT)})"
    post_has_no_comments = False

    async def get_post_by_id(session_):
        """
        Get Post object from DB
        """
        return (
            await session_.execute(
                select(Post).where(Post.id == post_id)
            )
        ).unique().scalar_one_or_none()

    engine = create_async_engine(config.DB_URL, echo=True)
    async with AsyncSession(engine) as session:
        async with session.begin():
            post = await get_post_by_id(session)
            comments = post.comments

            if not comments:  # check the case when Post doesn't have comments!
                print(f"WARNING: Post {post_id} has NO comments at all!")
                post_has_no_comments = True
            else:
                first_comment = comments[0]
                # check that first comment's title may already contains '(updated at ...) substring'
                # in this case we need to just replace the datetime value inside '(updated at ...) substring!'
                if 'updated' in first_comment.title:
                    title_temp = first_comment.title

                    # Pay Attention, that for applying updates the ASSIGN of new
                    # 'title' value should be made on 'first_comment.title', NOT
                    # on the temporary variable 'title_temp'!
                    first_comment.title = title_temp.replace(
                        title_temp[
                            title_temp.index('(updated'): len(title_temp)
                        ],
                        first_post_comment_updated_text
                    )
                else:
                    first_comment.title += first_post_comment_updated_text

            # Here we need to check the 'new_comment' object
            # contains correct post_id and user_id
            # to avoid the "data inconsistency"
            if new_comment.user_id != post.user_id:
                new_comment.user_id = post.user_id

            if new_comment.post_id != post.id:
                new_comment.post_id = post.id

            # adding new_comment to Post.comments
            comments.append(new_comment)

        # here we get Post object by id again to check that updates were applied,
        # but we should make it OUT of 'async with session.begin()' body (started at line 44)
        # Because this should be another Transaction in which we check that updates
        # made in previous Transaction were really applied to DB state
        comments = (await get_post_by_id(session)).comments

        assert len(comments) >= 1

        if post_has_no_comments:
            # added comment is only one comment related to our Post
            added_comment = comments[0]
        else:
            assert comments[0].title.endswith(first_post_comment_updated_text)
            added_comment = comments[-1]

        assert added_comment.title == new_comment.title
        assert added_comment.post_id == new_comment.post_id
        assert added_comment.user_id == new_comment.user_id


"""
2. Написать асинк функцию, которая:
- не принимает аргументов
- получает всех юзеров у которых нет лайков на постах
- добавляет по одному лайку на каждый пост

(В конце также проверка на то, что обновления зафиксировались)
"""


async def add_one_like_to_posts_with_no_likes():

    async def get_all_users(session_):
        """
        Get Users objects from DB
        """
        return (
            await session_.execute(
                select(User)
            )
        ).unique().scalars().all()

    async def get_likes_stats(session_, user_ids, post_ids):
        """
        Get likes statistics
        """
        query = (
            select(
                User.id,
                Post.id,
                func.count(Like.id).label("likes_cnt"),
            )
            .join_from(Post, Like, isouter=True)
            .join_from(Post, User, User.id == Post.user_id)
            .where(
                User.id.in_(user_ids),
                Post.id.in_(post_ids),
            )
            .group_by(User.id, Post.id)
        )
        return (await session_.execute(query)).all()

    user_with_no_likes = []
    posts_with_no_likes = []

    engine = create_async_engine(config.DB_URL, echo=True)
    async with AsyncSession(engine) as session:
        async with session.begin():
            for user in await get_all_users(session):
                print(f"User: {user}")
                for post in user.posts:
                    print(f"User Post: {post}")
                    print(f"Post Likes: {post.likes}")

                    if not post.likes:
                        # Just save the ids of Users/Posts where NO likes found
                        user_with_no_likes.append(user.id)
                        posts_with_no_likes.append(post.id)
                        # Add new Like to Post's Likes
                        post.likes.append(
                            Like(
                                user_id=user.id,
                                post_id=post.id
                            )
                        )

        if user_with_no_likes and posts_with_no_likes:
            records_after_update = await get_likes_stats(
                session, user_with_no_likes, posts_with_no_likes
            )

            for record in records_after_update:
                u_id, p_id, likes_cnt = record
                print(f"User id: {u_id}, Post id: {p_id}, Likes count: {likes_cnt}")
                assert likes_cnt == 1


if __name__ == '__main__':

    # first Task
    POST_ID = 2

    # asyncio.run(
    #     update_post_comments(
    #         post_id=POST_ID,
    #         new_comment=Comment(
    #             title=f"I'm New Comment(created at {datetime.datetime.now().strftime(DTTM_FMT)})",
    #             user_id=None,
    #             post_id=POST_ID
    #         )
    #     )
    # )

    # asyncio.run(add_one_like_to_posts_with_no_likes())