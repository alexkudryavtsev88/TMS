sqlite> select * from users;
id          name        age         gender      nationality
----------  ----------  ----------  ----------  -----------
1           Alex        34          male        belarus
2           Ann         32          female      russia
3           Kate        25          male        germany

sqlite> select name, age from users;
name        age
----------  ----------
Alex        34
Ann         32
Kate        25

sqlite> select name as MyName, age as MyAge from users;
MyName      MyAge
----------  ----------
Alex        34
Ann         32
Kate        25

sqlite> select name as 'My Name', age as 'My Age' from users;
My Name     My Age
----------  ----------
Alex        34
Ann         32
Kate        25

sqlite> select name as 'My Name', age as 'My Age' from users limit 1;
My Name     My Age
----------  ----------
Alex        34

sqlite> select name as 'My Name', age as 'My Age' from users limit 1 offset 1;
My Name     My Age
----------  ----------
Ann         32

select *  from users where age > 25;
id          name        age         gender      nationality
----------  ----------  ----------  ----------  -----------
1           Alex        34          male        belarus
2           Ann         32          female      russia


-- where gender in ('male', 'female') -> where gender = 'male' OR gender = 'female'

sqlite> select id, name, nationality from users where nationality like "%rus%";
id          name        nationality
----------  ----------  -----------
1           Alex        belarus
2           Ann         russia


select id, name, age from users order by age desc;

select users.name, posts.title from posts inner join users on posts.user_id = users.id where name = "Alex";
select u.name, p.title from posts p inner join users u on p.user_id = u.id where name = "Alex";
