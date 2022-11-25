import sqlite3
import sqlite3
import sys
import traceback

import json2html as json2html
from flask import render_template_string
from flask_login import current_user
from flask_mde import MdeField
from flask_wtf import FlaskForm
from wtforms import SubmitField
from src.user import User

from src.model import get_db



class MdeForm(FlaskForm):
    editor = MdeField()
    submit = SubmitField()


def error_printer(er):
    print('SQLite error: %s' % (' '.join(er.args)))
    print("Exception class is: ", er.__class__)
    print('SQLite traceback: ')
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(traceback.format_exception(exc_type, exc_value, exc_tb))


def json_render(data):
    return render_template_string(json2html.json2html.convert(json=data))


def create_post(user, content):
    db = get_db()
    try:
        db.execute(f"insert into post(user,content) values('{user}','{content}')")
        db.commit()
        return 201
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406


def delete_post(id):
    db = get_db()
    try:
        db.execute(f"delete from post where id='{id}'")
        db.commit()
        return 200
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
        data = db.cursor().execute(f"SELECT * post WHERE id='{post_id}'")

    except sqlite3.Error as err:
        error_printer(err)
        return 406
    return data


def follow(uid):
    db = get_db()
    user = User.get_email(uid)
    try:
        db.execute(f"insert into follow (follower, following) values ('{current_user.email}','{user.email}');")
        db.commit()
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406

def cred(cred):
    db = get_db()
    try:
        db.execute(f"delete from credentials where email='{current_user.email}'")
        db.execute(f"insert into credentials (email,api_key,api_secret) values ('{current_user.email}','{cred['api_key']}','{cred['api_secret']}');")
        db.commit()
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406


def archive(pid):
    db = get_db()
    try:
        db.execute(f"update main.post set status='archived' where id='{pid}' and user='{current_user.email}' ;")
        db.commit()
        return 200
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406



def edit_profile():
    return None


def like(mid):
    db = get_db()
    try:
        db.execute(f"insert into likes(doer, post) values ('{current_user.email}','{mid}');")
        db.commit()
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406


def comment(pid, content):
    db = get_db()
    try:
        db.execute(f"insert into comments(user,post,content) values ('{current_user.email}','{pid}','{content}');")
        db.commit()
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406

def get_comments(pid):
    db = get_db()
    try:
        list = db.execute(f"select * from commentr where pid ='{pid}'")
        return list
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406


def share(mid):
    db = get_db()
    try:
        db.execute(f"insert into shares(doer, post) values ('{current_user.email}','{mid}');")
        db.commit()
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406