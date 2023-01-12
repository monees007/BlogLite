import sqlite3

from model.model import get_db
from src.controller import error_printer

responses = {
    400: {
        "errorCode": "400",
        "error": "Request Malformed."
    },
    417: {
        "errorCode": "417",
        "error": "Entry has been deleted or marked private by owner"
    },
    403: {
        "errorCode": "403",
        "error": "Not Authorized. Are you authenticated?"},
    401: {
        "errorCode": "401",
        "error": "Not Authorized. Invalid Credentials"},
    '404p': {
        "errorCode": "404",
        "error": "Entry with that pid can't be accessed"
    },
    '404c': {
        "errorCode": "404",
        "error": "Comment with that cid can't be accessed"
    },
    '404u': {
        "errorCode": "404",
        "error": "Given username or email aren't leading to any user."
    },
    '404d': {
        "errorCode": "404",
        "error": "Payload is missing."
    }
}


def is_an_comment(cid):
    db = get_db()
    try:
        output = db.execute(f"Select * from comments where cid='{cid}'").fetchall()
        return bool(output)
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406


def is_an_user(email=None, username=None):
    db = get_db()
    try:
        output = db.execute(f"Select * from user where email='{email}' or username='{username}'").fetchall()
        return bool(output)
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406


def is_an_entry(pid):
    db = get_db()
    try:
        output = db.execute(f"Select * from post where id='{pid}'").fetchall()
        return bool(output)
    except sqlite3.Error as err:
        db.rollback()
        error_printer(err)
        return 406
