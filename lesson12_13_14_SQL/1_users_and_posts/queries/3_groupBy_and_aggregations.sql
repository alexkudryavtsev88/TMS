-----------------------
-- Агрегатные функции --
-----------------------

-- COUNT - Общее количество
-- SUM - Сумма значений
-- MIN - Минимальное значение
-- MAX - Максимальное значение
-- AVG - Среднее значение

-- Общее свойство всех агрегатных функций - любая из них возвращает одно единственное значение.
-- (COUNT всегда возвращает ЦЕЛОЕ число, AVG всегда - ЧИСЛО С ПЛАВАЮЩЕЙ ТОЧКОЙ)

-- ПРИМЕРЫ:

-- Общее кол-во всех юзеров
select count(*) from users;

-- count
---------
--     4
--(1 row)

-- Минимальный и Максимальный возраст юзеров
select min(age) as "Min age", max(age) as "Max age" from users;

-- Min age | Max age
-----------+---------
--      25 |      35
--(1 row)


-----------
-- GROUP BY
-----------

-- GROUP BY применяется вместе с агрегатными функциями, когда кроме результата агрегатной функции, мы хотим также вывести
-- еще и связанные значения из других столбцов
-- (помним, что агрегатные функции ВСЕГДА возвращают единственное значение!)

-- ПРИМЕР 1:

-- Вывести количество лайков по всем постам (если лайков на постах нет - не учитываем эти посты),
-- с сортировкой от большего количества лайков к меньшему
select p.title, p.description, count(l.id) as likes_count
    from posts p left join likes l
    on p.id = l.post_id
    group by p.title, p.description
    order by likes_count desc;

--     title     |                 description                  | likes_count
-----------------+----------------------------------------------+-------------
-- Kate 1st post | Hello! I am Kate, I am 25 years old          |           3
-- Alex 2nd post | My favourite programming language is Python! |           2
-- Ann 1st post  | Hello! I am Ann, I am 32 years old           |           2
-- Alex 1st post | Hello! I am Alex, I am 34 years old          |           1
--(4 rows)


-- Если убрать хотя бы одно условие группировки (p.title или p.description) - получим ошибку синтаксиса!
select p.title, p.description, count(l.id) as likes_count
    from posts p join likes l
    on p.id = l.post_id
    group by p.title
    order by likes_count desc;

--ERROR:  column "p.description" must appear in the GROUP BY clause or be used in an aggregate function
--LINE 1: select p.title, p.description, count(l.id) as likes_count

-- Добавим еще один пост для юзера Alex, который быть содержать НЕ уникальный title
INSERT INTO posts (title, description, user_id)
VALUES ('Alex 1st post', 'Hello from ALEX!', 1);

-- И добавим ему лайк
INSERT INTO likes (user_id, post_id)
VALUES (1, 7);

-- Теперь выведем количество лайков по всем постам с указанием ТОЛЬКО тайтлов постов:
select p.title, count(l.id) as likes_count
    from posts p join likes l
    on p.id = l.post_id
    group by p.title
    order by likes_count desc;

--     title     | likes_count
-----------------+-------------
-- Kate 1st post |           3
-- Alex 1st post |           2
-- Ann 1st post  |           2
-- Alex 2nd post |           2
--(4 rows)

-- Как видите, пост с тайтлом 'Alex 1st post' имеет 2 лайка.
-- Однако мы знаем что у нас есть 2 поста с таким тайтлом, и это, по сути, разные посты.
-- Чтобы этого избежать, мы можем изменить условие группировки:

select p.title, count(l.id) as likes_count
    from posts p join likes l
    on p.id = l.post_id
    group by p.id
    order by likes_count desc;

--     title     | likes_count
-----------------+-------------
-- Kate 1st post |           3
-- Alex 2nd post |           2
-- Ann 1st post  |           2
-- Alex 1st post |           1
-- Alex 1st post |           1
--(5 rows)

-- Теперь, мы разделили посты с одинаковым тайтлом, сделав группировку по posts.id

-- Примечание: если бы мы выводили тайтл + дескрипшен, и добавили дескрипшен в группировку,
-- то посты сгруппировались бы корректно, так как наши 2 поста с одинаковым тайтлом имеют РАЗНЫЕ дескрипшены.


-- ПРИМЕР 2:

-- Статистика лайков по юзерам (юзеры без лайков не учитываются)
select u.name, count(l.id) as likes_count
    from users u join likes l
    on u.id = l.user_id
    group by u.id
    order by likes_count desc;

-- Примечание: группируем по users.id, так как имена юзеров в теории могут быть НЕ уникальными

-- * ПРИМЕР 3:

-- Статистика лайков по юзерам И постам (юзеры без постов, посты без лайков не учитываются)
select u.name, p.title, p.description, count(l.id) as likes_count
    from users u
    join posts p on u.id = p.user_id
    join likes l on u.id = l.user_id
    group by u.id, p.id
    order by likes_count desc;


-- name |     title     |                 description                  | likes_count
--------+---------------+----------------------------------------------+-------------
-- Alex | Alex 2nd post | My favourite programming language is Python! |       4
-- Alex | Alex 1st post | Hello from ALEX!                             |       4
-- Alex | Alex 1st post | Hello! I am Alex, I am 34 years old          |       4
-- Kate | Kate 2nd post | My favourite programming language is Java!   |           3
-- Kate | Kate 1st post | Hello! I am Kate, I am 25 years old          |           3
-- Ann  | Ann 1st post  | Hello! I am Ann, I am 32 years old           |           2
-- Ann  | Ann 2nd post  | My favourite programming language is Rust!   |           2


-- Статистика, выведенная в результате запроса не совсем корректная:
-- Мы видим likes_count = 4 во всех строках, где users.name = Alex,
-- и это похоже на то, будто у КАЖДОГО поста юзера Alex по 4 лайка, но это не так!

-- Мы можем модифицировать запрос, подставив p.id перед u.name в предложении group by,
-- однако, мы получим точно такой же, некорректный результат :(

-- Все дело в том, что мы берем строки из таблицы users, присоединяя к ним связанные строки таблиц
-- posts и likes, и группировка количества лайков здесь будет именно ПО ЮЗЕРАМ!
-- Проверим это, выполнив запрос:

select count(*) from likes where user_id = 1;
-- count
---------
--     4
--(1 row)

-- РЕШЕНИЕ:
-- Чтобы исправить это, нам нужно изменить порядок JOIN'ов таблиц:
-- Берем строки из таблицы posts, объединяя их с таблицей лайков, затем - с таблицей users

select u.name, p.title, p.description, count(l.id) as likes_count
    from posts p
    join likes l on p.id = l.post_id
    join users u on u.id = p.user_id
    group by u.id, p.id
    order by likes_count desc;

-- name |     title     |                 description                  | likes_count
--------+---------------+----------------------------------------------+-------------
-- Kate | Kate 1st post | Hello! I am Kate, I am 25 years old          |           3
-- Alex | Alex 2nd post | My favourite programming language is Python! |           2
-- Ann  | Ann 1st post  | Hello! I am Ann, I am 32 years old           |           2
-- Alex | Alex 1st post | Hello! I am Alex, I am 34 years old          |           1
-- Alex | Alex 1st post | Hello from ALEX!                             |           1
--(5 rows)

----------
-- HAVING
----------

-- Вывести всех юзеров и их посты, у котороых больше 2 лайков
select u.name, p.title, p.description, count(l.id) as likes_count
    from posts p
    join likes l on p.id = l.post_id
    join users u on u.id = p.user_id
    group by u.id, p.id
    having count(l.id) > 2;

-- Когда нам нужно указать условие для фильтра, и фильтром является результат агрегатной функции, то вместо
-- WHERE нужно использовать HAVING, как в примере выше