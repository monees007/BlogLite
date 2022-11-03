CREATE TABLE user
(
    id          TEXT PRIMARY KEY,
    name        TEXT        NOT NULL,
    email       TEXT UNIQUE NOT NULL,
    profile_pic TEXT        NOT NULL,
    backdrop TEXT,
    bio TEXT,
    followers TEXT,
    followings TEXT


);

CREATE TABLE post
(
    forwarded TEXT default 0,
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE ,
    user TEXT FOREIGN KEY REFERENCES user NOT NULL ,
    date TIMESTAMP NOT NULL ,
    content TEXT NOT NULL,
    likes TEXT default 0,
    comments TEXT default 0,
    forwords TEXT default 0

);

CREATE TABLE comment
(
    postid TEXT FOREIGN KEY REFERENCES post,
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    content TEXT NOT NULL,
    date TIMESTAMP
)

