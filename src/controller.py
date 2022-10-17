from __main__ import app

from flask import request, render_template, redirect

from src.model import *

def save_post(user,date,content):
    db= get_db()
    db.execute("insert into post(user,date,content) values(user,date,content)")



