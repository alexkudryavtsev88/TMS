from executor import QueryExecutor
from models.user_models import Comment, Post, User
from sqlalchemy import select
from sqlalchemy.orm.strategy_options import joinedload

users = User
posts = Post
comments = Comment


# 1. JOIN 2 Tables
"""
SELECT users.name, posts.title
FROM users JOIN posts ON users.id = posts.user_id
"""
# we need to specify BOTH LEFT and RIGHT tables in 'join_from()'
# NOTE: the Order is important
join_2_tb_1 = select(users.name, posts.title).join_from(users, posts)

# Equivalent of previous query, but is shorter:
# in 'join()' we specify only the RIGHT table which should be JOINED to the LEFT table
join_2_tb_2 = select(users.name, posts.title).join(posts)

# 2. JOIN 3 Tables using INNER JOIN
"""
SELECT users.name, posts.title, comments.title AS title_1
FROM users
JOIN posts ON users.id = posts.user_id
JOIN comments ON posts.id = comments.post_id
"""
join_3_tb_inner_1 = (
    select(users.name, posts.title, comments.title)
    .select_from(users)
    .join(posts)
    .select_from(posts)
    .join(comments)
)

# Equivalent of previous query, but is shorter
# we can skip 'select_from(table_1)', just 'join(table_2)'
# but 'select_from(table_2)' should be, also
# we should specify 'on' condition in 'join(table_3)'
join_3_tb_inner_2 = (
    select(users.name, posts.title, comments.title)
    .join(posts)
    .select_from(posts)
    .join(comments, posts.id == comments.post_id)
)

# Equivalent of previous query, but is shorter
# we can skip both 'select_from(table)' and don't use 'on' directly
# but should use 'join_from(table_1, table_2)' and 'join_from(table_2, table_3)'
join_3_tb_inner_3 = (
    select(users.name, posts.title, comments.title)
    .join_from(users, posts)
    .join_from(posts, comments)
)

# this query doesn't work!!!
# we CAN'T JOIN 3 tables using just the chain of 'join()' calls
# join_3_tb_bad = select(users.name, posts.title, comments.title).join(posts).join(comments)


# 3. JOIN 3 Tables using LEFT OUTER JOIN

"""
SELECT users.name, posts.title, comments.title AS title_1
FROM users
LEFT OUTER JOIN posts ON users.id = posts.user_id
LEFT OUTER JOIN comments ON posts.id = comments.post_id
"""
join_3_tb_outer_1 = (
    select(users.name, posts.title, comments.title)
    .join_from(users, posts, isouter=True)
    .join_from(posts, comments, isouter=True)
)

"""
SELECT users.name, posts.title, comments.title AS title_1
FROM users
JOIN posts ON users.id = posts.user_id
LEFT OUTER JOIN comments ON posts.id = comments.post_id
"""
join_3_tb_outer_2 = (
    select(users.name, posts.title, comments.title)
    .join_from(users, posts, isouter=False)
    .join_from(posts, comments, isouter=True)
)

"""
SELECT users.name, posts.title, comments.title AS title_1
FROM users
LEFT OUTER JOIN posts ON users.id = posts.user_id
JOIN comments ON posts.id = comments.post_id
"""
join_3_tb_outer_3 = (
    select(users.name, posts.title, comments.title)
    .join_from(users, posts, isouter=True)
    .join_from(posts, comments, isouter=False)
)

# when we need to JOIN 3 tables, and BOTH 2nd and 3rd tables
# should be JOINED with the 1st by its ID column

"""
SELECT users.name, posts.title, comments.title AS title_1
FROM users
LEFT OUTER JOIN posts ON users.id = posts.user_id
JOIN comments ON users.id = comments.user_id
"""

# Equivalent of previous query, but is shorter
join_3_tb_by_one_fk_1 = (
    select(users.name, posts.title, comments.title)
    .join(posts, isouter=True)
    .select_from(users)
    .join(comments, users.id == comments.user_id)
)

join_3_tb_by_one_fk_2 = (
    select(users.name, posts.title, comments.title)
    .join_from(users, posts, isouter=True)
    .join_from(users, comments, users.id == comments.user_id)
)

# With WHERE clause
"""
SELECT users.name, posts.title, comments.title AS title_1
FROM users
LEFT OUTER JOIN posts ON users.id = posts.user_id
LEFT OUTER JOIN comments ON posts.id = comments.post_id
WHERE users.name = %s
"""
join_3_tb_outer_1_where = join_3_tb_outer_1.where(users.name == "Alex")


"""RELATIONSHIP LOADING TECHNIQUES"""

executor = QueryExecutor()

"""When we want to retrieve a single User entity and have access to the related Posts:"""

joinedload_query = (
    select(User).options(joinedload(User.comments, innerjoin=True)).where(User.id == 1)
)

"""
NOTE: we can add kwarg *lazy='joined'* in the appropriate *relationship()* field of User class
and NOT user *options(joinedload(...)) in Query directly in this case*
"""

""" WORKFLOW """


async def load_with_join():
    result = await executor.exec_query(joinedload_query)
    return result


"""
- When executing the Query described above the ORM JOINS the User and Comment tables implicitly:

SELECT users.id, users.name, users.age, users.gender, users.nationality,
comments_1.id AS id_1, comments_1.title, comments_1.user_id, comments_1.post_id
FROM users JOIN comments AS comments_1 ON users.id = comments_1.user_id
"""


async def get_scalar_one():
    result = await load_with_join()
    user = result.unique().scalar_one()
    print(f"User: {user}")
    for idx, com in enumerate(user.comments, start=1):
        print(f"Comment {idx}: {com}")


"""
- 'unique()' call on Result is required
- 'scalar_one_or_none()' call returns a single 'User' entity or None, if there are no results by search criteria. Posts
  related to the retrieved User are available through the 'User.posts' attribute.
- also retrieved User object is attached to the Session. When we update the User object attributes, ORM is automatically
  execute 'UPDATE users SET ...' query
"""


# asyncio.run(get_scalar_one())
