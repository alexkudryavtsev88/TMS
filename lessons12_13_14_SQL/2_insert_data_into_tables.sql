-- fill users table
INSERT INTO users (name, age, gender, nationality)
VALUES
  ('Alex', 34, 'male', 'belarus'),
  ('Ann', 32, 'female', 'russia'),
  ('Kate', 25, 'male', 'germany');

-- fill posts table
INSERT INTO posts (title, description, user_id)
VALUES
  ('Alex 1st post', 'Hello! I am Alex, I am 34 years old', 1),
  ('Alex 2nd post', 'My favourite programming language is Python!', 1),
  ('Ann 1st post', 'Hello! I am Ann, I am 32 years old', 2),
  ('Ann 2nd post', 'My favourite programming language is Rust!', 2),
  ('Kate 1st post', 'Hello! I am Kate, I am 25 years old', 3),
  ('Kate 2nd post', 'My favourite programming language is Java!', 3);

-- fill comments table
INSERT INTO comments (title, user_id, post_id)
VALUES
  ('Wow, It is great!', 1, 2),
  ('I am 32 years old too!', 2, 3),
  ('I like Java too!', 3, 6);

-- fill likes table
INSERT INTO likes (user_id, post_id)
VALUES
  (1, 1),
  (1, 2),
  (1, 2),
  (2, 3),
  (2, 3),
  (3, 5),
  (3, 5),
  (3, 5);

-- Добавлаяем нового юзера, у которого нет постов, комментов и лайков
INSERT INTO users (name, age, gender, nationality)
VALUES
  ('John', 35, 'male', 'belarus');