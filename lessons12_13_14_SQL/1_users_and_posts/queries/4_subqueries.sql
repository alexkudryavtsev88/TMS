--------------
-- SUB-QUERIES
--------------

-- Возьмем запрос из предыдущей темы, который вывод статистику по юзерам/постам и кол-ву лайков
select u.name, p.title, p.description, count(l.id) as likes_count
    from posts p
    join likes l on p.id = l.post_id
    join users u on u.id = p.user_id
    group by u.name, p.id
    order by likes_count desc;

-- name |     title     |                 description                  | likes_count
--------+---------------+----------------------------------------------+-------------
-- Kate | Kate 1st post | Hello! I am Kate, I am 25 years old          |           3
-- Alex | Alex 2nd post | My favourite programming language is Python! |           2
-- Ann  | Ann 1st post  | Hello! I am Ann, I am 32 years old           |           2
-- Alex | Alex 1st post | Hello! I am Alex, I am 34 years old          |           1
-- Alex | Alex 1st post | Hello from ALEX!                             |           1
--(5 rows)

-- Теперь, с помощью такой синтаксической конструкции как подзапрос, мы можем проверить корректность данных
-- из запроса выше:

-- 1. Проверим, действительно ли пост с тайтлом 'Kate 1st post' юзера 'Kate' имеет 3 лайка:
select count(*) from likes where post_id = (select id from posts where title = 'Kate 1st post');
-- count
---------
--     3
--(1 row)

-- 2. Проверим, действительно ли пост с тайтлом 'Alex 2nd post' юзера 'Alex' имеет 2 лайка:
select count(*) from likes where post_id = (select id from posts where title = 'Alex 2nd post');
-- count
---------
--     2
--(1 row)

-- вывести все данные о юзерах, у которых возраст равен максимальному возрасту среди всех существующих юзеров
select * from users where age = (select max(age) from users);
-- вывести все данные о юзерах, у которых возраст равен максимальному возрасту среди всех существующих юзеров с возрастом < 35 лет
select * from users where age = (select max(age) from users where age < 35);
