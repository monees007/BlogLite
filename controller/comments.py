import sqlite3

from flask_login import current_user

from model.model import get_db
from src.controller import error_printer


def comment(pid, content):
    db = get_db()
    try:
        db.execute(f"insert into comments(user,post,content) values ('{current_user.email}','{pid}','{content}');")
        db.commit()
        return "Comment created successfully", 200
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406


def get_comments(pid):
    db = get_db()
    try:
        list = db.execute(f"select * from commentr where pid ='{pid}' order by sort ").fetchall()
        return list
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406


def edit_comment(cid, content):
    db = get_db()
    try:
        db.execute(f"update comments set content='{content}' where user='{current_user.email}' and  cid='{cid}'")
        db.commit()
        return "Comment Updated Successfully", 200
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406


def delete_comment(cid):
    db = get_db()
    try:
        db.execute(f"delete from comments where cid='{cid}' and user='{current_user.email}'")
        db.commit()
        return "Comment deleted successfully", 200
    except sqlite3.Error as err:
        error_printer(err)
        return 406
