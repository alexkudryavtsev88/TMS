from sqlalchemy import desc, func, select
from lesson18_19_sqlalchemy.models import Like, Post, User

# ======================== GROUP BY =================================== #


# 1. Get likes statistics by posts
def get_likes_count_by_posts():
    """
    SQL:

    SELECT p.title, p.description, count(l.id) AS likes_cnt
    FROM posts JOIN likes
    ON posts.id = likes.post_id
    GROUP BY p.title, p.description
    ORDER BY likes_cnt;
    """
    query = select(
        Post.title,
        Post.description,
        func.count(Like.id).label("likes_cnt")
    ) \
        .join_from(Post, Like) \
        .group_by(Post.title, Post.description) \
        .order_by("likes_cnt")

    return query


# 2. Get likes statistics by posts and users

def get_likes_count_by_posts_and_users():
    """
    SQL:

    SELECT users.name, posts.title, posts.description, count(%s) AS likes_cnt
    FROM posts
    JOIN likes ON posts.id = likes.post_id
    JOIN users ON users.id = posts.user_id
    GROUP BY users.name, posts.id
    ORDER BY likes_cnt DESC;
    """

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

    return query


# 3. Get likes statistics by posts and users with filter by likes count

def get_likes_count_by_posts_and_users_with_having(likes_count: int):
    f"""
    SQL:
    
    SELECT users.name, posts.title, posts.description, count(likes.id) AS likes_cnt
    FROM posts
    LEFT JOIN likes ON posts.id = likes.post_id
    JOIN users ON users.id = posts.user_id
    GROUP BY users.name, posts.id
    HAVING count(likes.id) = {likes_count}
    ORDER BY likes_cnt;
    """
    query = select(
                User.name,
                Post.title,
                Post.description,
                func.count(Like.id).label("likes_cnt"),
        ) \
        .join_from(Post, Like, isouter=True) \
        .join_from(Post, User, User.id == Post.user_id) \
        .group_by(User.name, Post.id) \
        .having(func.count(Like.id) == likes_count) \
        .order_by(desc("likes_cnt"))

    return query


# ====================== GROUP BY VS PARTITION BY ========================== #

# 1. Get max age by user's gender

def get_max_age_group_by_gender():
    """
    SQL:

    SELECT users.gender, max(users.age) AS max_1
    FROM users GROUP BY users.gender;
    """
    query = select(
        User.gender,
        func.max(User.age)
    ).select_from(User).group_by(User.gender)

    return query


# 2. Get min and max user's age by gender using 'partition'

def get_min_max_age_partition_by_gender():
    """
    SQL:

    SELECT users.name, users.age, users.gender,
    min(users.age)
        OVER (PARTITION BY users.gender) AS anon_1,
    max(users.age)
        OVER (PARTITION BY users.gender) AS anon_2
    FROM users;
    """
    query = select(
        User.name,
        User.age,
        User.gender,
        func.min(User.age).over(partition_by=User.gender),
        func.max(User.age).over(partition_by=User.gender),
    ).select_from(User)

    return query
