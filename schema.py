DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS article;

CREATE TABLE user (
  userID INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE article (
  artID INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL, #userID of author
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, #time published
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  tags TEXT,
  comments TEXT
  FOREIGN KEY (author_id) REFERENCES user (userID)
);