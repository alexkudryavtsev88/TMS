from models.user_models import Like, Post, User
from sqlalchemy import desc, func, select

# ======================== GROUP BY =================================== #

# 1. Get likes statistics by posts

"""
select p.title, p.description, count(l.id) as likes_count
from posts p join likes l
on p.id = l.post_id
group by p.title, p.description
order by likes_count asc;
"""


async def get_likes_count_by_posts(db_conn):
    result = await db_conn.select(
        select(Post.title, Post.description, func.count(Like.id).label("likes_cnt"))
        .join_from(Post, Like)
        .group_by(Post.title, Post.description)
        .order_by("likes_cnt")
    )
    return result


# 2. Get likes statistics by posts and users

"""
SELECT users.name, posts.title, posts.description, count(%s) AS likes_cnt
FROM posts
JOIN likes ON posts.id = likes.post_id
JOIN users ON users.id = posts.user_id
GROUP BY users.name, posts.id
ORDER BY likes_cnt DESC
"""


async def get_likes_count_by_posts_and_users(db_conn):
    query = (
        select(
            User.name,
            Post.title,
            Post.description,
            func.count(Like.id).label("likes_cnt"),
        )
        .join_from(Post, Like, isouter=True)
        .join_from(Post, User, User.id == Post.user_id)
        .group_by(User.name, Post.id)
        .order_by(desc("likes_cnt"))
    )

    result = await db_conn.select(query)

    return result


# 3. Get likes statistics by posts and users with filter by likes count

"""
SELECT users.name, posts.title, posts.description, count(%s) AS likes_cnt
FROM posts
JOIN likes ON posts.id = likes.post_id
JOIN users ON users.id = posts.user_id
GROUP BY users.name, posts.id
ORDER BY likes_cnt
"""


async def get_likes_count_by_posts_and_users_with_having(db_conn):
    result = await db_conn.select(
        select(
            User.name,
            Post.title,
            Post.description,
            func.count(Like.id).label("likes_cnt"),
        )
        .join_from(Post, Like, isouter=True)
        .join_from(Post, User, User.id == Post.user_id)
        .group_by(User.name, Post.id)
        .having(func.count(Like.id) == 0)
        .order_by(desc("likes_cnt"))
    )
    return result


# ====================== GROUP BY VS PARTITION BY ========================== #

# 1. Get max age by user's gender
"""
SELECT users.gender, max(users.age) AS max_1
FROM users GROUP BY users.gender
"""


async def get_max_age_group_by_gender(db_conn):
    result = await db_conn.select(
        select(User.gender, func.max(User.age)).select_from(User).group_by(User.gender)
    )
    return result


# 2. Get min and max user's age by gender using 'partition'
"""
SELECT users.name, users.age, users.gender, min(users.age)
OVER (PARTITION BY users.gender) AS anon_1, max(users.age)
OVER (PARTITION BY users.gender) AS anon_2
FROM users
"""


async def get_min_max_age_partition_by_gender(db_conn):
    query = select(
        User.name,
        User.age,
        User.gender,
        func.min(User.age).over(partition_by=User.gender),
        func.max(User.age).over(partition_by=User.gender),
    ).select_from(User)
    result = await db_conn.select(query)
    return result
