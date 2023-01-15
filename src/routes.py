import json
from io import BytesIO

from flask import request, render_template, jsonify
from flask import url_for, redirect, Response
from werkzeug.wsgi import FileWrapper

from controller.comments import *
from controller.entries import *
from controller.users import *
from src import views
from src.controller import MdeForm


def user(uid=None):
    if request.method == 'GET':
        form = MdeForm()
        ship = views.profile(uid)
        follower = False
        rw = False
        if current_user.is_authenticated and current_user.username == uid:
            rwv = True

        elif current_user.is_authenticated and follows(uid):
            rw = False
            follower = True
        else:
            rw = False
            follower = False
        return {
            'info': ship[0], 'data': ship[1], 'follower': follower, 'rw': rw
        }


def index():
    # return render_template('index.html', form=MdeForm())
    if not current_user.is_authenticated:
        return search()
    else:
        return redirect(url_for("feed"))


def add_post():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    form = MdeForm()
    if request.method == "POST":
        content = form.editor.data
        user_ = current_user.email
        code = create_post(user_, content)

    return current_profile()


def post_delete(mid):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return redirect(request.url, delete_post(mid))


def post_update(mid, content):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if request.method == "PUT":
        return redirect(request.url, update_post(mid, content))
    else:
        return redirect(request.url, 400)


def search():
    form = MdeForm()
    data = views.top_posts()
    cu = current_user.email if current_user.is_authenticated else False
    if not current_user.is_authenticated:
        return render_template('discover.html', data=data, cu=cu, form=form, show_login=True)
    elif request.method == "GET" and data != 406:

        return render_template('discover.html', data=data, cu=cu, form=form)
    else:
        return redirect(request.url, 400)


def feed():
    form = MdeForm()
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template('feed.html', data=views.feeds(), form=form, cu=current_user.email)


def archive(pid):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return redirect(request.url, archive(pid))


def current_profile():
    if current_user.is_authenticated:
        return profile(username=None, email=current_user.email)
    else:
        return redirect(url_for("login"))


def follow(user_):
    if current_user.is_authenticated:
        if follow(user_) != 406:
            return "", 203
    else:
        return redirect(url_for("login"))


def profile(username=None, email=None):
    form = MdeForm()
    if username:
        ship = views.profile(username=username)
    else:
        ship = views.profile(email=email)
    follower = False

    if current_user.is_authenticated and (current_user.username == username or current_user.email == email):
        rw = True

    elif username and current_user.is_authenticated and follows(username):
        rw = False
        follower = True
    else:
        rw = False
        follower = False
    return render_template('user.html', info=ship[0], data=ship[1], follower=follower, rw=rw, form=form,
                           cu=current_user.email)


def edit_profile():
    if request.method == "POST":
        name = request.form['name']
        bio = request.form['bio']
        email = request.form['email']
        username = request.form['username']
        code = edit_profile(name, email, username, bio)
        return redirect(url_for("user"), code)


def like(mid):
    if current_user.is_authenticated:
        if like(mid) != 406:
            return redirect(request.url)
    else:
        return redirect(url_for("login"), 406)


def comment(pid):
    if request.method == "GET":
        req = get_comments(pid).fetchall()
        if req != 406:
            return jsonify(req)
    elif request.method == "POST":
        content = request.form['content']
        if current_user.is_authenticated:
            if comment(pid, content=content) != 406:
                return redirect(request.url)
        else:
            return redirect(url_for("login"), 406)


def share(mid):
    if current_user.is_authenticated:
        if share(mid) != 406:
            return redirect(request.url)
    else:
        return redirect(url_for("login"), 406)


def export():
    if current_user.is_authenticated:
        b = FileWrapper(BytesIO(json.dumps(views.export(), indent=4).encode('utf-8')))
        header = {f'Content-Disposition': f'attachment; filename="{current_user.email}-export.json"'}
        return Response(b, mimetype="text/plain", direct_passthrough=True, headers=header)
    return redirect(url_for('login'))
