from flask import request, redirect, render_template, url_for, jsonify
from flask_login import current_user

from src import controller, views
from src.controller import MdeForm


def post(pid=None):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        form = MdeForm()
        content = form.editor.data
        user = current_user.email
        code = controller.create_post(user, content)
    elif request.method == 'UPDATE':
        form = MdeForm()
        content = form.editor.data
        controller.update_post(pid, content)
    elif request.method == 'DELETE':
        controller.delete_post(pid)


def user(uid=None):
    if request.method == 'GET':
        form = MdeForm()
        ship = views.profile(uid)
        follower = False
        rw = False
        if current_user.is_authenticated and current_user.username == uid:
            rwv = True

        elif current_user.is_authenticated and views.follows(uid):
            rw = False
            follower = True
        else:
            rw = False
            follower = False
        return {
            'info': ship[0], 'data': ship[1], 'follower': follower, 'rw': rw
        }
    elif request.method == 'UPDATE':
        pass
    elif request.method == 'DELETE' and current_user.is_authenticated():
        pass


def comment(pid=None, cid=None):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'UPDATE':
        pass
    elif request.method == 'DELETE':
        pass


def index():
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
        user = current_user.email
        code = controller.create_post(user, content)

    return current_profile()


def post_delete(mid):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return redirect(request.url, controller.delete_post(mid))


def post_update(mid, content):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if request.method == "PUT":
        return redirect(request.url, controller.update_post(mid, content))
    else:
        return redirect(request.url, 400)


def search():
    form = MdeForm()
    data = views.top_posts()
    if not current_user.is_authenticated:
        return render_template('discover.html', data=data, form=form, show_login=True)
    elif request.method == "GET" and data != 406:

        return render_template('discover.html', data=data, form=form)
    else:
        return redirect(request.url, 400)


def feed():
    form = MdeForm()
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template('homepageB.html', data=views.feeds(), form=form)


def archive(pid):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return redirect(request.url, controller.archive(pid))


def current_profile():
    if current_user.is_authenticated:
        return profile(current_user.username)
    else:
        return redirect(url_for("login"))


def follow(user):
    if current_user.is_authenticated:
        if controller.follow(user) != 406:
            return ("", 203)
    else:
        return redirect(url_for("login"))


def profile(uid):
    form = MdeForm()
    ship = views.profile(uid)
    follower = False
    rw = False
    if current_user.is_authenticated and current_user.username == uid:
        rwv = True

    elif current_user.is_authenticated and views.follows(uid):
        rw = False
        follower = True
    else:
        rw = False
        follower = False
    return render_template('userB.html', info=ship[0], data=ship[1], follower=follower, rw=rw, form=form)


def edit_profile():
    return None


def like(mid):
    if current_user.is_authenticated:
        if controller.like(mid) != 406:
            return redirect(request.url)
    else:
        return redirect(url_for("login"), 406)


def comment(pid):
    if request.method == "GET":
        req = controller.get_comments(pid).fetchall()
        if req != 406:
            return jsonify(req)
    elif request.method == "POST":
        content = request.form['content']
        if current_user.is_authenticated:
            if controller.comment(pid, content=content) != 406:
                return redirect(request.url)
        else:
            return redirect(url_for("login"), 406)


def share(mid):
    if current_user.is_authenticated:
        if controller.share(mid) != 406:
            return redirect(request.url)
    else:
        return redirect(url_for("login"), 406)
