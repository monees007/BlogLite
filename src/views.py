import sqlite3

from flask import render_template_string
from flask_login import current_user

from src.controller import error_printer
from src.model import get_db
from src.user import User


def profile(username=None,email=None):
    db = get_db()
    try:
        if username:
            info = db.execute(f"select * from users where users.username is '{username}';").fetchone()
            data = db.execute(f"SELECT * FROM posts_all where posts_all.username is '{username}' ORDER BY timestamp DESC ").fetchall()
        elif email:
            info = db.execute(f"select * from users where users.email is '{email}';").fetchone()
            data = db.execute(f"SELECT * FROM posts_all where posts_all.email is '{email}' ORDER BY timestamp DESC ").fetchall()

        return (info, data)
    except sqlite3.Error as err:
        error_printer(err)



def top_posts():
    db = get_db()
    try:
        data = db.cursor().execute(
            f"select * from posts order by (likes+comments+shares),timestamp  ").fetchall()
        return data
    except sqlite3.Error as err:
        error_printer(err)
        return 406


def feeds():
    db = get_db()
    try:
        data = db.cursor().execute(
            f"select * from posts where email in(select following from follow where follower= '{current_user.email}') order by timestamp  ").fetchall()
        return data
    except sqlite3.Error as err:
        error_printer(err)
        return 406




def invalid404():
    return render_template_string('<h1>This request is invalid. 404</h1>')


def follows(uid):
    db = get_db()
    user = User.get_uname(uid)
    try:
        info = db.execute(f"select * from follow where following ='{user['email']}' and follower='{current_user.email}' ;").fetchone()
        return bool(info)
    except sqlite3.Error as err:
        error_printer(err)
