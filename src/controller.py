from __main__ import app

from flask import request, render_template, redirect

from model.model import *

owner = 'shamlee@cute.com'


######## LOGIN AND SIGNUP #######################
@app.route("/login", methods=['POST', 'GET'])
def login():  # create new list
    if request.method == 'POST':
        print(1)
        # crs.execute(f"-- insert into owner(name,email) values('{request.form['email']}','{request.form['email']}'); ")
        # crs.execute("insert into owner values('Manish Chandra2','monees008@outlook.in');")
        print(2)
    return render_template('index.html')


######## LIST MANAGEMENT ########################


@app.route("/createlist", methods=['POST', 'GET'])
def createlist():  # create new list
    if request.method == 'POST':
        print(request.form['title'])
        print(request.form['clist'])
        new_list(request.form['title'], request.form['clist'], owner)
    return redirect("/")


@app.route("/deletelist/<mid>")
def deletelist(mid):
    delete_list(mid)
    return redirect("/")


######### CARD MANAGEMENT @@@@@@@@@@@@@@@@@@@@@@@@@

@app.route("/delete/c<id>")
def delete(mid):  # delete a card
    delete_card(mid)
    return redirect("/")

@app.route("/create", methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        new_card(request.form['title'],request.form["content"],request.form['status'],request.form['parent_list'])
