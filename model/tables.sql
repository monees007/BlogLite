create table main.comments
(
    content   TEXT                           not null,
    timestamp TEXT default CURRENT_TIMESTAMP not null,
    user      TEXT                           not null
        constraint userfk
            references main.user (email),
    post      TEXT                           not null
        constraint post___fk
            references main.post,
    cid       integer                        not null
        primary key autoincrement
);

create table main.credentials
(
    email      TEXT not null
        references main.user (email),
    api_key    text not null,
    api_secret TEXT not null
);

create table main.follow
(
    follower  TEXT not null
        references main.user (email),
    following TEXT not null
        references main.user (email),
    TIMESTAMP integer default CURRENT_TIMESTAMP
);

create table main.likes
(
    doer      TEXT not null
        references main.user (email),
    post      TEXT not null
        references main.post,
    timestamp TEXT default CURRENT_TIMESTAMP
);

create table main.post
(
    forwarded INTEGER default 0,
    id        INTEGER                           not null
        primary key autoincrement
        constraint post_pk
            unique,
    user      TEXT                              not null
        constraint user
            references main.user (email),
    date      TEXT    default CURRENT_TIMESTAMP not null,
    content   ANY                               not null,
    status    TEXT    default 'visible'
);

create table main.post
(
    forwarded INTEGER default 0,
    id        INTEGER                           not null
        primary key autoincrement
        constraint post_pk
            unique,
    user      TEXT                              not null
        constraint user
            references main.user (email),
    date      TEXT    default CURRENT_TIMESTAMP not null,
    content   ANY                               not null,
    status    TEXT    default 'visible'
);

create table main.user
(
    id          TEXT not null
        primary key,
    name        TEXT not null,
    email       TEXT not null
        unique,
    profile_pic TEXT not null,
    TIMESTAMP   TEXT default CURRENT_TIMESTAMP,
    backdrop    TEXT,
    bio         TEXT,
    username    TEXT not null
        unique
);

