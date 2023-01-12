import sqlite3

from flask_login import current_user, login_required

from src.controller import error_printer
from model.model import get_db


def profile(username=None,email=None):
    db = get_db()
    try:
        if username:
            info = db.execute(f"select * from users where users.username is '{username}';").fetchone()
            data = db.execute(f"SELECT * FROM posts_all where posts_all.username is '{username}' ORDER BY timestamp DESC ").fetchall()
        elif email:
            info = db.execute(f"select * from users where users.email is '{email}';").fetchone()
            data = db.execute(f"SELECT * FROM posts_all where posts_all.email is '{email}' ORDER BY timestamp DESC ").fetchall()
        # updating liked by current user values.
        for p in range(len(data)):
            if db.cursor().execute(
                    f"select * from likes where post='{data[p]['id']}' and doer='{current_user.email}'").fetchall():
                data[p]['liked'] = True
            else:
                data[p]['liked'] = False

        return (info, data)
    except sqlite3.Error as err:
        error_printer(err)



def top_posts():
    db = get_db()
    try:
        data = db.cursor().execute(
            f"select * from posts order by (likes+comments+shares) desc ,timestamp ").fetchall()
        if current_user.is_authenticated:
            # updating liked by current user values.
            for p in range(len(data)):
                if db.cursor().execute(
                        f"select * from likes where post='{data[p]['id']}' and doer='{current_user.email}'").fetchall():
                    data[p]['liked'] = True
                else:
                    data[p]['liked'] = False

        return data
    except sqlite3.Error as err:
        error_printer(err)
        return 406

@login_required
def feeds():
    db = get_db()
    try:
        data = db.cursor().execute(
            f"select * from posts where email in(select following from follow where follower= '{current_user.email}') order by timestamp desc ").fetchall()
        # updating liked by current user values.
        for p in range(len(data)):
            if db.cursor().execute(
                    f"select * from likes where post='{data[p]['id']}' and doer='{current_user.email}'").fetchall():
                data[p]['liked'] = True
            else:
                data[p]['liked'] = False
        return data
    except sqlite3.Error as err:
        error_printer(err)
        return 406






def export():
    email=current_user.email
    db =get_db()
    return {
        'profile': profile(email=email)[0],
        'entries': profile(email=email)[1],
        'comments': db.execute(f"select content from comments where user='{email}'").fetchall()
    }
