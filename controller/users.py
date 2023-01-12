import sqlite3

from flask_login import current_user
from passlib.apps import custom_app_context as pwd_context

from model.model import get_db
from src.controller import error_printer
from src.user import User





def follow(email):
    db = get_db()
    if not db.execute(f"SELECT * FROM follow where following='{email}' and follower='{current_user.email}'").fetchone():
        try:
            db.execute(f"insert into follow (follower, following) values ('{current_user.email}','{email}');")
            db.commit()
            return 200
        except sqlite3.Error as err:
            db.rollback()
            error_printer(err)
            return 406
    else:
        try:
            db.execute(f"delete from follow where following='{email}' and follower='{current_user.email}'")
            db.commit()
            return 417
        except sqlite3.Error as err:
            db.rollback()
            error_printer(err)
            return 406


def followings(email):
    db = get_db()
    try:
        data = db.cursor().execute(
            f"SELECT profile_pic, username, name, email from user where user.email in (select following from follow where follower='{email}');").fetchall()
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406
    return data


def followers(email):
    db = get_db()
    try:
        data = db.cursor().execute(
            f"SELECT profile_pic, username, name, email from user where user.email in (select follower from follow where following='{email}');").fetchall()
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406
    return data


def search(term):
    term += '%'
    db = get_db()
    try:
        data = db.cursor().execute(
            f"select * from users where username like '{term}' or name like '{term}' or email like '{term}';").fetchall()
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406
    return data


def follows(uid):
    db = get_db()
    user = User.get_uname(uid)
    try:
        info = db.execute(
            f"select * from follow where following ='{user['email']}' and follower='{current_user.email}' ;").fetchone()
        return bool(info)
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)


def is_following(email):
    db = get_db()
    try:
        info = db.execute(
            f"select * from follow where following ='{email}' and follower='{current_user.email}' ;").fetchone()
        return bool(info)
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406
    except TypeError:
        return 401


def user_available(username):
    db = get_db()
    try:
        data = db.cursor().execute(
            f"SELECT username from user where user.username='{username}';").fetchall()
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406
    return data


def cred(cred):
    db = get_db()
    try:
        db.execute(f"delete from credentials where email='{current_user.email}'")
        db.execute(
            f"insert into credentials (email,api_key,api_secret) values ('{current_user.email}','{cred['api_key']}','{pwd_context.encrypt(cred['api_secret'])}');")
        db.commit()
    except sqlite3.Error as err:
        db.rollback()
        
        error_printer(err)
        return 406


def edit_profile(name, username, bio, profile_pic):
    db = get_db()
    try:
        db.cursor().execute(
                f"update user set name='{name}', username='{username}', bio='{bio}',profile_pic='{profile_pic}' where email='{current_user.email}'")

        db.commit()
        return 200
    except sqlite3.Error as err:
        db.rollback()
        
        error_printer(err)
        return 406

def get_profile_pic():
    db = get_db()
    try:
        return db.cursor().execute(f"select profile_pic from user where email='{current_user.email}'")
    except sqlite3.Error as err:
        error_printer(err)
        return 500

def delete_user():

    db = get_db()
    try:
        db.cursor().execute(f"delete from user where email='{current_user.email}'")
        db.cursor().execute(f"delete from likes where doer='{current_user.email}'")
        db.cursor().execute(f"delete from credentials where email='{current_user.email}'")
        db.cursor().execute(f"delete from shares where doer='{current_user.email}'")
        db.cursor().execute(f"delete from post where user='{current_user.email}'")
        db.cursor().execute(f"delete from comments where user='{current_user.email}'")
        db.cursor().execute(f"delete from follow where follower='{current_user.email}' or following='{current_user.email}'")
        db.commit()

        return True
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 500
    return False

