from __main__ import app
from flask_mde import Mde, MdeField
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask import Flask, request, redirect, json, url_for, render_template


mde = Mde(app)
class MdeForm(FlaskForm):
    editor = MdeField()
    submit = SubmitField()
@app.route("/create_post", methods=["GET","POST"])
def create_post():
    form = MdeForm()
    # if request.method == "POST":

    return render_template('create_post.html', form=form)
def feeds():
    pass

def profile():
    pass

def search():
    pass

def create():
    pass