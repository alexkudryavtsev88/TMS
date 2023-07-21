import asyncio
import logging
import random
import string

import config
# from sqlalchemy import text
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from sqlalchemy import select, delete
from lesson18_19_sqlalchemy.models import Post
from lesson18_19_sqlalchemy.db_worker import DatabaseWorker

import traceback


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def random_nationality():
    chars = list(string.ascii_uppercase)
    random.shuffle(chars)
    return "".join(chars[:10])


async def update_user_nationality_and_check_updates(db_worker: DatabaseWorker, user_id: int):
    await database_worker.check_db()

    nationality = random_nationality()
    update_result = await db_worker.update_user_by_id(user_id=user_id, nationality=nationality)
    assert update_result.lower() == 'ok'
    """
    After updates we made need to get user from the Database within new Session
    to check that updates were really applied
    """
    real_user = await db_worker.get_user_by_id(user_id=user_id)
    print(real_user)
    assert real_user.nationality == nationality


async def update_user_post_and_check_updates(db_worker: DatabaseWorker, user_id: int):
    await database_worker.check_db()

    new_post = Post(title="NEW POST", description="Added by SQLAlchemy", user_id=user_id)
    print(new_post)
    update_result = await db_worker.update_user_by_id(user_id=user_id, new_post=new_post)
    assert update_result.lower() == 'ok'
    """
    After updates we made need to get user from the Database within new Session
    to check that updates were really applied
    """
    real_user = await db_worker.get_user_by_id(user_id=user_id)
    added_post = real_user.posts[-1]
    print(added_post)

    try:
        assert added_post.title == "NEW POST"
        assert added_post.description == "Added by SQLAlchemy"
        assert added_post.user_id == user_id
    except Exception as exc:
        traceback.print_exception(exc)
    finally:
        """
        Delete created post
        """
        await db_worker.delete_post_by_id(added_post.id)


if __name__ == '__main__':
    database_worker = DatabaseWorker(config.DB_URL)
    database_worker.connect()

    asyncio.run(
        update_user_post_and_check_updates(database_worker, user_id=1)
    )


