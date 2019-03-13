DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Article;
DROP TABLE IF EXISTS Tag;
DROP TABLE IF EXISTS Comment;

CREATE TABLE User (
  userId INTEGER PRIMARY KEY AUTOINCREMENT,
  userName TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE Article (
  artId INTEGER PRIMARY KEY AUTOINCREMENT,
  userName TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (userName) REFERENCES User(userName)
);

CREATE TABLE Tag (
  tagId INTEGER PRIMARY KEY AUTOINCREMENT,
  tag TEXT NOT NULL,
  artId INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (artId) REFERENCES Article(artId)
);

CREATE TABLE Comment (
  commentId INTEGER PRIMARY KEY AUTOINCREMENT,
  comment TEXT NOT NULL,
  artId INTEGER NOT NULL,
  author, TEXT NOT NULL DEFAULT 'Anonymous Coward',
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (artId) REFERENCES Article(artId)
);

INSERT INTO User (username, password)
VALUES ('Tandrus', 'password'),
('Macgrey', 'password1'),
('London', 'password2');

INSERT INTO Article (userName, title, body)
VALUES ('Tandrus', 'Allo About Me', 'I love me, myself and I so much....'),
('Macgrey', 'Title 2', 'This article tells the story of nothing on a cold summers night in October...'),
('London', 'Title 3', 'It all began the day after yesterday...');

INSERT INTO Tag (tag, artId)
VALUES ('me', (SELECT artId FROM Article WHERE title = 'Allo About Me')),
('story', (SELECT artId FROM Article WHERE title = 'Title 2')),
('random', (SELECT artId FROM Article WHERE title = 'Title 2'));

INSERT INTO Comment (comment, artId, author)
VALUES ('This article is so annoying SMHHHHH', (SELECT artId FROM Article WHERE title = 'Allo About Me'), 'Tandrus'),
('Wow I feel enlightened', (SELECT artId FROM Article WHERE title = 'Title 2'), 'Tandrus'),
('Worst article EVERRRR', (SELECT artId FROM Article WHERE title = 'Title 2'), 'London');
