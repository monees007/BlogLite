import sqlite3

from flask_login import current_user

from model.model import get_db
from src.controller import error_printer


def create_post(user, content):
    db = get_db()
    try:
        db.execute(f"insert into post(user,content) values('{user}','{content}')")
        entry = db.execute(
            "select * from posts where id = (select max(id) from post)"
        ).fetchone()
        db.commit()
        return entry, 200
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406


def delete_post(id):
    db = get_db()
    try:
        db.execute(f"delete from post where id='{id}' and user='{current_user.email}' ;")
        db.commit()
        return "Entry Deleted", 200
    except sqlite3.Error as err:
        error_printer(err)
        return 406


def update_post(id, content):
    db = get_db()
    try:
        db.execute(f"update main.post set content='{content}' where id='{id}' and user='{current_user.email}' ;")
        db.commit()
        return 200
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406


def retrive_a_post(post_id):
    db = get_db()
    try:
        data = db.cursor().execute(f"SELECT * from posts WHERE id='{post_id}'").fetchall()

    except sqlite3.Error as err:
        error_printer(err)
        return 406
    return data if data else 404


def archive(pid):
    db = get_db()
    try:
        post = data = db.cursor().execute(f"SELECT * from post WHERE id='{pid}'").fetchone()

        # return post
        if post["status"] == "archived":
            db.execute(f"update main.post set status='visible' where id='{pid}' and user='{current_user.email}' ;")
        else:
            db.execute(f"update main.post set status='archived' where id='{pid}' and user='{current_user.email}' ;")

        db.commit()
        return "Entry is " + post["status"], 200
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406


def like(pid):
    db = get_db()
    if db.execute(f"SELECT * FROM likes where post='{pid}' and doer='{current_user.email}'").fetchall() == []:
        try:
            db.execute(f"insert into likes(doer, post) values ('{current_user.email}','{pid}');")
            db.commit()
            return "Entry liked", 200
        except sqlite3.Error as err:
            db.rollback()
            error_printer(err)
            return 406
    else:
        try:
            db.execute(f"delete from likes where post='{pid}' and doer='{current_user.email}'")
            db.commit()
            return "Entry unliked", 417
        except sqlite3.Error as err:
            db.rollback()
            error_printer(err)
            return 406


def share(pid):
    db = get_db()
    if db.execute(f"SELECT * FROM shares where post='{pid}' and doer='{current_user.email}'").fetchall() == []:
        try:
            db.execute(f"insert into shares(doer, post) values ('{current_user.email}','{pid}');")
            db.commit()
            return 200
        except sqlite3.Error as err:
            db.rollback()
            error_printer(err)
            return 406
    else:
        try:
            db.execute(f"delete from shares where post='{pid}' and doer='{current_user.email}'")
            db.commit()
            return 417
        except sqlite3.Error as err:
            db.rollback()
            error_printer(err)
            return 406


def get_doers(func, pid):
    db = get_db()
    if func == 'likes':
        lis = db.execute(
            f"Select name,username,email,profile_pic from user where email in (select doer from likes where post='{pid}')").fetchall()
    elif func == 'shares':
        lis = db.execute(
            f"Select name,username,email,profile_pic from user where email in (select doer from shares where post='{pid}')").fetchall()
    else:
        return 401
    return lis


def is_liked(pid):
    db = get_db()
    try:
        return db.execute(
            f"Select * from likes where doer='{current_user.email}' and post='{pid}'"
        ).fetchall()
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406
