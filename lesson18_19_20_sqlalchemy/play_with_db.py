import asyncio
import random
import string
from multiprocessing import Process

from lesson18_19_20_sqlalchemy import config
from lesson18_19_20_sqlalchemy.models import Post, User
from lesson18_19_20_sqlalchemy.db_worker import DatabaseWorker
from lesson18_19_20_sqlalchemy.queries import joins
from lesson18_19_20_sqlalchemy.queries import groupings


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
        # here we only print Exception's traceback!
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


async def execute_select_with_join(db_worker: DatabaseWorker):
    """
    Test the query from 'queries/joins.py' module

    Use 'scalars=False, one_result=False' for all queries from module
    except the joinedload query!

    - when you execute some Query like 'select(User.name, User.age, Post.title)'
    and then you call the .scalars().all() on result: you will get the values from first column only!!!
    - 'one_result = True' should be used only when the query expectedly returns a single row


    Examples:
    """
    q = joins.join_3_tb_inner_1
    result = await db_worker.execute_any_select(q, scalars=True, one_result=False)
    print(result)

    q2 = joins.select_user_with_comments
    result = await db_worker.execute_any_select(q2, scalars=True, one_result=True)
    print(result)
    print(result.comments)


async def execute_select_with_grouping(db_worker: DatabaseWorker):
    """
    Test the query from 'queries/groupings.py' module

    Use 'scalars=False, one_result=False' for all queries from module!

    Examples:
    """
    q1 = groupings.get_likes_count_by_posts()
    result1 = await db_worker.execute_any_select(q1, scalars=False, one_result=False)
    print(result1)

    q2 = groupings.get_likes_count_by_posts_and_users_with_having(likes_count=2)
    result2 = await db_worker.execute_any_select(q2, scalars=False, one_result=False)
    print(result2)

    q3 = groupings.get_min_max_age_partition_by_gender()
    result3 = await db_worker.execute_any_select(q3, scalars=False, one_result=False)
    print(result3)


if __name__ == '__main__':
    database_worker = DatabaseWorker(config.DB_URL)
    database_worker.connect()

    ''' update User nationality '''
    asyncio.run(
        update_user_nationality_and_check_updates(database_worker, user_id=1)
    )

    ''' add new User post '''
    # asyncio.run(
    #     update_user_post_and_check_updates(database_worker, user_id=1)
    # )

    """
    NOTE: DON'T run previous code lines simultaneously!
    """

    ''' Try to add 2 same users '''
    # create_two_same_users_concurrently(database_worker)

    ''' Test 'join' queries '''
    # asyncio.run(
    #     execute_select_with_join(
    #         database_worker,
    #     )
    # )

    ''' Test 'grouping' queries '''
    # asyncio.run(
    #     execute_select_with_grouping(
    #         db_worker=database_worker
    #     )
    # )



