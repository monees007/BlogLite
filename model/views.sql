CREATE VIEW users as
select backdrop,
       profile_pic,
       name,
       email,
       username,
       bio,
       (select count(following) from follow where following = email) as follower,
       (select count(id) from posts where posts.email = user.email)  as posts,
       (select count(follower) from follow where follower = email)   as following
from user;

CREATE VIEW commentr as
select cid,
       user as email,
       post as pid,
        timestamp as sort,
        substr('JanFebMarAprMayJunJulAugSepOctNovDec', 1 + 3 * strftime('%m', timestamp), -3) ||
        strftime(' %d, %Y', timestamp) as timestamp,
        content,
        (select profile_pic from users where users.email = comments.user) as profile_pic,
        (select username from users where users.email = comments.user) as username
        from comments
        ORDER BY timestamp;

CREATE VIEW posts as
select id,
       (select profile_pic from user where user.email = post.user) as profile_pic,
       (select email from user where user.email = post.user)       as email,
       (select name from user where user.email = post.user)        as name,
       (select username from user where user.email = post.user)    as username,
        date as timestamp,
        content as content,
        substr('JanFebMarAprMayJunJulAugSepOctNovDec', 1 + 3*strftime('%m', date), -3) || strftime(' %d, %Y', date) as date,
        (select count (post) from likes where post=id) as likes,
        (select count (post) from shares where post=id and user =post.user) as shared,
        (select count (post) from comments where post=id) as comments,
        (select count (post) from shares where post=id) as shares
        from post where status='visible';

CREATE VIEW posts_all as
select id,
       (select profile_pic from user where user.email = post.user) as profile_pic,
       (select email from user where user.email = post.user)       as email,
       (select name from user where user.email = post.user)        as name,
       (select username from user where user.email = post.user)    as username,
        date as timestamp,
        content as content,
        status as status,
        substr('JanFebMarAprMayJunJulAugSepOctNovDec', 1 + 3*strftime('%m', date), -3) || strftime(' %d, %Y', date) as date,
        (select count (post) from likes where post=id) as likes,
        (select count (post) from likes where post=id and user =post.user) as liked,
        (select count (post) from shares where post=id and user =post.user) as shared,
        (select count (post) from comments where post=id) as comments,
        (select count (post) from shares where post=id) as shares
        from post;


