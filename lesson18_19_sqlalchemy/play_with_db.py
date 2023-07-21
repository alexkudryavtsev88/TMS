import asyncio
import random
import string
from multiprocessing import Process

from sqlalchemy import select

from lesson18_19_sqlalchemy import config
from lesson18_19_sqlalchemy.models import Post, User
from lesson18_19_sqlalchemy.db_worker import DatabaseWorker


import traceback


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


def create_two_same_users_concurrently(db_worker: DatabaseWorker):
    """
    This function creates two SAME Users and tries to add these Users
    into the "users" table

    NOTE: before running this function please execute the SQL
    from the 'CREATE_UNIQUE_INDEX_USERS.sql' file!
    """
    new_user = User(
        name="TEST",
        age=0,
        gender="male",
        nationality=random_nationality()
    )
    same_users = [new_user] * 2

    def _run_in_event_loop(user_):
        print(user_)
        """
        In accordance with the fact 
        that communication with DB 
        goes through the Coroutines
        we use 'asyncio.run' in each Process
        """
        asyncio.run(
            db_worker.add_new_user(
                user=user_
            )
        )

    running_procs = []
    for user in same_users:
        proc = Process(target=_run_in_event_loop, args=(user,))
        proc.start()
        running_procs.append(proc)

    for p in running_procs:
        p.join()


async def execute_select_with_join(db_worker: DatabaseWorker, query):
    async with db_worker._session as s:
        result = await s.execute(query)

        results = result.all()
        print(results)


if __name__ == '__main__':
    database_worker = DatabaseWorker(config.DB_URL)
    database_worker.connect()

    asyncio.run(
        execute_select_with_join(
            database_worker,
            query=select(User.name, Post.title).join(Post).where(User.id == 1)
        )
    )

    ''' update User nationality '''
    # asyncio.run(
    #     update_user_nationality_and_check_updates(database_worker, user_id=1)
    # )

    ''' add new User post '''
    # asyncio.run(
    #     update_user_post_and_check_updates(database_worker, user_id=1)
    # )

    """
    NOTE: DON'T run previous code lines simultaneously!
    """

    ''' run as standard function '''
    # create_two_same_users_concurrently(database_worker)


