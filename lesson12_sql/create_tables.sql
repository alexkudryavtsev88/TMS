--users table:
CREATE TABLE users(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT(20) NOT NULL,
 age INTEGER NOT NULL,
 gender TEXT(6) NOT NULL,
 nationality TEXT
);

--posts table:
CREATE TABLE posts(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 title TEXT(20) NOT NULL,
 description TEXT(100) NOT NULL,
 user_id INTEGER,
 FOREIGN KEY (user_id)
  REFERENCES users (id)
   ON DELETE CASCADE ON UPDATE NO ACTION
);

--comments table:
CREATE TABLE IF NOT EXISTS comments(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
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
 id INTEGER PRIMARY KEY AUTOINCREMENT,
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
.header on
.mode column
pragma table_info('comments');