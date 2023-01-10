--users table:
CREATE TABLE users(
 id serial PRIMARY KEY,
 name VARCHAR(20) NOT NULL,
 age INTEGER NOT NULL,
 gender VARCHAR(6) NOT NULL,
 nationality TEXT
);

--posts table:
CREATE TABLE posts(
 id serial PRIMARY KEY,
 title VARCHAR(20) NOT NULL,
 description VARCHAR(100) NOT NULL,
 user_id INTEGER,
 FOREIGN KEY (user_id)
  REFERENCES users (id)
   ON DELETE CASCADE ON UPDATE NO ACTION
);

--comments table:
CREATE TABLE IF NOT EXISTS comments(
 id serial PRIMARY KEY,
 title TEXT NOT NULL,
 user_id INTEGER,
 post_id INTEGER,
 FOREIGN KEY (user_id)
  REFERENCES users (id)
   ON DELETE CASCADE ON UPDATE NO ACTION,
 FOREIGN KEY (post_id)
  REFERENCES posts (id)
   ON DELETE CASCADE ON UPDATE NO ACTION
);

--likes table:
CREATE TABLE likes(
 id serial PRIMARY KEY,
 user_id INTEGER,
 post_id INTEGER,
 FOREIGN KEY (user_id)
  REFERENCES users (id)
   ON DELETE CASCADE ON UPDATE NO ACTION,
 FOREIGN KEY (post_id)
  REFERENCES posts (id)
   ON DELETE CASCADE ON UPDATE NO ACTION
);

--Посмотреть структуру таблицы:
--.header on
--.mode column
--pragma table_info('comments');