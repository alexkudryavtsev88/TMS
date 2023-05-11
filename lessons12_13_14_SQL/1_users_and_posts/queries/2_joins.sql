---------------
-- Оператор JOIN
---------------

-- Вывести всех юзеров (name и age) с именем 'Alex' вместе со связанными постами этих юзеров
select users.name, users.age, posts.title, posts.description
    from users inner join posts
    on posts.user_id = users.id
    where users.name = 'Alex';


-- СИНТАКСИС:
-- 1. FROM users INNER JOIN posts: объединяем таблицы users и posts через оператор INNER JOIN
--    (здесь - 'INNER' дефотлный спецификатор, его можно не указывать явно и писать просто 'JОIN')
-- 2. ON posts.user_id = users.id: после оператора ON указываем поля, по которым нужно соединить таблицы:
--      это PRIMARY KEY таблицы 'users' (id) и FOREIGN KEY таблицы 'posts' (user_id)
-- 3. Так как в выборке участвуют столбцы из нескольких таблиц, и столбцы в этих таблицах могут иметь одинаковые имена,
--    то для таких столбцов нужно ОБЯЗАТЕЛЬНО указывать, к какой конкретно таблице относится указанный столбец
--    (имя_таблицы.имя_столбца после SELECT, как в примере).
--    В данном примере, имена столбцов в таблицах users и posts НЕ повторяются, и указывать имена таблиц для столбцов НЕ обязательно,
--    однако, лучше принять это за хорошую практику - ВСЕГДА указывать имя_таблицы.имя_столбца, если используем JOIN
-- 3.1. В предложении ON после JOIN - ВСЕГДА указываем имена таблиц перед именами столбцов.
-- 3.2. Так как имена таблиц могут быть длинными, и указание имени таблицы перед имененем столбца может делать наш запрос
--      достаточно длинным, мы можем использовать alias'ы для сокращения:

-- Вывести всех юзеров (name и age) с именем 'Alex' вместе со связанными постами этих юзеров, с использованием алиасов:
select u.name, u.age, p.title, p.description
    from users as u inner join posts as p
    on p.user_id = u.id
    where u.name = 'Alex';

-- name | age |     title     |                 description
--------+-----+---------------+----------------------------------------------
-- Alex |  34 | Alex 1st post | Hello! I am Alex, I am 34 years old
-- Alex |  34 | Alex 2nd post | My favourite programming language is Python!
--(2 rows)

-- 'from users as u inner join posts as p' - as можно не указывать и писать просто: 'from users u inner join posts p'

---------------
-- ВИДЫ JOIN'ов
---------------

-- 1. INNER JOIN (или просто JOIN)

select * from users join posts;

-- id | name | age | gender | nationality | id |     title     |                 description                  | user_id
------+------+-----+--------+-------------+----+---------------+----------------------------------------------+---------
--  1 | Alex |  34 | male   | belarus     |  1 | Alex 1st post | Hello! I am Alex, I am 34 years old          |       1
--  1 | Alex |  34 | male   | belarus     |  2 | Alex 2nd post | My favourite programming language is Python! |       1
--  2 | Ann  |  32 | female | russia      |  3 | Ann 1st post  | Hello! I am Ann, I am 32 years old           |       2
--  2 | Ann  |  32 | female | russia      |  4 | Ann 2nd post  | My favourite programming language is Rust!   |       2
--  3 | Kate |  25 | male   | germany     |  5 | Kate 1st post | Hello! I am Kate, I am 25 years old          |       3
--  3 | Kate |  25 | male   | germany     |  6 | Kate 2nd post | My favourite programming language is Java!   |       3
--(6 rows)

-- Выводит строки из таблицы, указанной СЛЕВА от JOIN, а так же связанные с ними строки из таблицы, указанной СПРАВА от JOIN
-- Если в таблице, указанной СЛЕВА от JOIN, есть записи, которые НЕ имеют связей с таблицей, указанной СПРАВА от JOIN: эти строки НЕ будут выведены!


-- 2. LEFT OUTER JOIN (или просто LEFT JOIN)

select * from users left join posts on users.id = posts.user_id;

-- id | name | age | gender | nationality | id |     title     |                 description                  | user_id
------+------+-----+--------+-------------+----+---------------+----------------------------------------------+---------
--  1 | Alex |  34 | male   | belarus     |  1 | Alex 1st post | Hello! I am Alex, I am 34 years old          |       1
--  1 | Alex |  34 | male   | belarus     |  2 | Alex 2nd post | My favourite programming language is Python! |       1
--  2 | Ann  |  32 | female | russia      |  3 | Ann 1st post  | Hello! I am Ann, I am 32 years old           |       2
--  2 | Ann  |  32 | female | russia      |  4 | Ann 2nd post  | My favourite programming language is Rust!   |       2
--  3 | Kate |  25 | male   | germany     |  5 | Kate 1st post | Hello! I am Kate, I am 25 years old          |       3
--  3 | Kate |  25 | male   | germany     |  6 | Kate 2nd post | My favourite programming language is Java!   |       3
--  4 | John |  35 | male   | belarus     |    |               |                                              |
--(7 rows)

-- Как вы можете видеть, запрос с LEFT JOIN вернул юзера John, у которой нет связей на таблицу posts
--  (в результирующей таблице, в столбцах, соответствующих столбцам таблицы posts будут NULL'ы )


-- 3. RIGHT OUTER JOIN (или просто RIGHT JOIN)

select * from posts right join users on users.id = posts.user_id;
--
-- id |     title     |                 description                  | user_id | id | name | age | gender | nationality
------+---------------+----------------------------------------------+---------+----+------+-----+--------+-------------
--  1 | Alex 1st post | Hello! I am Alex, I am 34 years old          |       1 |  1 | Alex |  34 | male   | belarus
--  2 | Alex 2nd post | My favourite programming language is Python! |       1 |  1 | Alex |  34 | male   | belarus
--  3 | Ann 1st post  | Hello! I am Ann, I am 32 years old           |       2 |  2 | Ann  |  32 | female | russia
--  4 | Ann 2nd post  | My favourite programming language is Rust!   |       2 |  2 | Ann  |  32 | female | russia
--  5 | Kate 1st post | Hello! I am Kate, I am 25 years old          |       3 |  3 | Kate |  25 | male   | germany
--  6 | Kate 2nd post | My favourite programming language is Java!   |       3 |  3 | Kate |  25 | male   | germany
--    |               |                                              |         |  4 | John |  35 | male   | belarus
--(7 rows)

-- Мы поменяли местами таблицы users и posts относительно оператора JOIN в запросе и выбрали RIGHT JOIN:
--  (в результирующей таблице, в столбцах, соответствующих столбцам таблицы posts будут NULL'ы, как и в предыдущем запросе с LEFT JOIN
--   c той лишь разницей, что сейчас эти столбцы будут идти перед столбцами таблицы users)


-- ГЛАВНОЕ для понимания сути OUTER JOIN'ов:
-- Если мы хотим объединить несколько таблиц, и в результате видеть даже те строки, которые НЕ имеют связей:
-- 1. Если строки без связей могут содержаться в ЛЕВОЙ таблице (СЛЕВА от JOIN) - то объединяем через LEFT JOIN
-- 2. Если строки без связей могут содержаться в ПРАВОЙ таблице (СПРАВА от JOIN) - то объединяем через RIGHT JOIN
-- 3. Если строки без связей могут содержаться в ОБЕИХ таблицах - то объединяем через FULL JOIN
--    (в нашем случае FULL JOIN не логичен, так как даже в теории не может сществовать постов, НЕ привязанных к конкретным юзерам)