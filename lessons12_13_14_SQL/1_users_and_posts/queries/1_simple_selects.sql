
-- Выбрать все записи из таблицы Юзеров
select * from users;

-- id | name | age | gender | nationality
------+------+-----+--------+-------------
--  1 | Alex |  34 | male   | belarus
--  2 | Ann  |  32 | female | russia
--  3 | Kate |  25 | male   | germany
--  4 | John |  35 | male   | belarus
-- (4 rows)


-- Выбрать все name и age из всех записей в таблице Юзеров
select name, age from users;

-- name | age
--------+-----
-- Alex |  34
-- Ann  |  32
-- Kate |  25
-- John |  35
--(4 rows)


-- Выбрать все name и age из всех записей в таблице Юзеров, используя кастомные имена стобцов в выводе
select name as My_Name, age as My_Age from users;

-- myname | myage
----------+-------
-- Alex   |    34
-- Ann    |    32
-- Kate   |    25
-- John   |    35
--(4 rows)


-- Если хотите использовать пробелы в кастомных именах, то эти имена должны быть взяты в двойные кавычки
select name as "My Name", age as "My Age" from users;

-- My Name | My Age
-----------+--------
-- Alex    |     34
-- Ann     |     32
-- Kate    |     25
-- John    |     35
--(4 rows)


-- Ограничение строк вывода ДО 1 строки с помощью limit:
select name as "My Name", age as "My Age" from users limit 1;

-- My Name | My Age
-----------+--------
-- Alex    |     34
--(1 row)


-- Вывести все строки таблицы Юзеров, начиная со 2-й строки:
select name as "My Name", age as "My Age" from users offset 1;

-- My Name | My Age
-----------+--------
-- Ann     |     32
-- Kate    |     25
-- John    |     35
--(3 rows)

-- WHERE: позволяет фильтровать данные для вывода по условию:

-- Все юзеры, у которых возраст больше 25 лет
select * from users where age > 25;

-- id | name | age | gender | nationality
------+------+-----+--------+-------------
--  1 | Alex |  34 | male   | belarus
--  2 | Ann  |  32 | female | russia
--  4 | John |  35 | male   | belarus
--(3 rows)

-- Все юзеры, у которых возраст равен 25 ИЛИ равен 35
select * from users where age in (25, 35);

-- id | name | age | gender | nationality
------+------+-----+--------+-------------
--  3 | Kate |  25 | male   | germany
--  4 | John |  35 | male   | belarus
--(2 rows)

-- Все юзеры, у которых возраст в ДИАПАЗОНЕ от 30 до 34 лет
select *  from users where age between 30 and 34;

-- id | name | age | gender | nationality
------+------+-----+--------+-------------
--  1 | Alex |  34 | male   | belarus
--  2 | Ann  |  32 | female | russia
--(2 rows)


-- Все юзеры, у которых nationality содержит подстроку 'rus' (в ЛЮБОЙ части значения) И имя начинается с буквы 'A'
select id, name, nationality from users where nationality like '%rus%' and name like 'A%';

--id          name        nationality
------------  ----------  -----------
--1           Alex        belarus
--2           Ann         russia
--(2 rows)

-- СОРТИРОВКА результатов: ORDER BY

-- Все юзеры, c сортировкой по полю age по УБЫВАНИЮ
select * from users order by age desc;

-- id | name | age | gender | nationality
------+------+-----+--------+-------------
--  4 | John |  35 | male   | belarus
--  1 | Alex |  34 | male   | belarus
--  2 | Ann  |  32 | female | russia
--  3 | Kate |  25 | male   | germany
--(4 rows)

-- Все юзеры, c сортировкой по полю nationality по ВОЗРАСТАНИЮ (ASC в выражении ORDER BY можно не указывать, оно дефолтное)
select * from users order by nationality;

-- id | name | age | gender | nationality
------+------+-----+--------+-------------
--  1 | Alex |  34 | male   | belarus
--  4 | John |  35 | male   | belarus
--  3 | Kate |  25 | male   | germany
--  2 | Ann  |  32 | female | russia
--(4 rows)


