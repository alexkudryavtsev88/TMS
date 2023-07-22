from sqlalchemy import select
from sqlalchemy.orm.strategy_options import joinedload

from lesson18_19_sqlalchemy.models import Comment, Post, User

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


"""  RELATIONSHIP LOADING TECHNIQUE  """

"""
If you use "join" Queries as described above, for example: 

  query = select(User.name, User.age, Post.title).join(Post).where(User.id == 1)
 
When you call .all() on Result of this Query, your result will be as in pure SQL:
you have a list of "rows", where: 
- each "row" is a Tuple of appropriate columns values
- User's name and age will be repeated in each "row"

  Output: 
 
  [('Alex', 34, 'Alex 1st post'), ('Alex', 34, 'Alex 2nd post')]

But there is a more real case when we want to:
 - get a SINGLE Object from DB, NOT a list of rows
 - have access to this Object's Relations via appropriate fields
 
If you will use query like this:

  query = select(User).join(Comment).where(User.id == 1)
  
and then you call .scalar_one_or_none() on the Query result and
then you tries to get access to the User comments:

  print(my_user.comments)
  
You will get *DetachedInstanceError* because the 'comments' relations 
don't work in this case!
 
To avoid this and get your result as you expect you should use the "JoinedLoad" technique:
"""

select_user_with_comments = (
    select(User).options(
        joinedload(User.comments, innerjoin=True)
    ).where(User.id == 1)
)

"""
OR you can add *lazy='joined'* in the appropriate *relationship* field of User class
and NOT use *options(joinedload(...)) directly in query 

WORKFLOW:

- When executing the Query described above the ORM JOINS the User and Comment tables implicitly:

    SELECT users.id, users.name, users.age, users.gender, users.nationality,
    comments_1.id AS id_1, comments_1.title, comments_1.user_id, comments_1.post_id
    FROM users JOIN comments AS comments_1 ON users.id = comments_1.user_id

- Then you will have access to User's comments via 'User.comments' relationship fields :)
"""


"""
NOTE: To run any query from this module - just import it in 'play_with_db.py' and then run 
using 'execute_select_with_join() module function and pass your query as argument.
"""