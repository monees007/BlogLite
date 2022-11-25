import os

from flask import Flask
from flask_login import LoginManager
from flask_mde import Mde
from flask_misaka import Misaka

from src import routes, login
from src.user import User

if True:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
    mde = Mde(app)
    Misaka(app)
    DATABASE = 'database/sqlite.db'
    login_manager = LoginManager()
    login_manager.init_app(app)

app.add_url_rule('/', view_func=routes.index)
app.add_url_rule('/feed', view_func=routes.feed)
app.add_url_rule('/discover', view_func=routes.search)
app.add_url_rule('/user/<uid>', view_func=routes.profile)
app.add_url_rule('/user', view_func=routes.current_profile)

app.add_url_rule('/follow/<user>', view_func=routes.follow)
app.add_url_rule('/account', view_func=routes.edit_profile, methods=["GET", "POST"])

app.add_url_rule('/create_post', view_func=routes.add_post, methods=["POST"])
app.add_url_rule('/like/<mid>', view_func=routes.like)
app.add_url_rule('/comment/<pid>', view_func=routes.comment, methods=["POST","GET"])
app.add_url_rule('/share/<mid>', view_func=routes.share)
app.add_url_rule('/archive/<mid>', view_func=routes.archive)
app.add_url_rule('/edit/<mid>', view_func=routes.post_update, methods=["POST", "GET"])
app.add_url_rule('/delete/<mid>', view_func=routes.post_delete)

app.add_url_rule('/api/post/{pid}', view_func=routes.post, methods=["GET", "POST", "UPDATE", "DELETE"])
app.add_url_rule('/cred', view_func=login.credentials)
app.add_url_rule('/login', view_func=login.login)
app.add_url_rule('/logout', view_func=login.logout)
app.add_url_rule('/login/callback', view_func=login.callback)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    app.config.from_object(__name__)
    app.run(debug=True, ssl_context="adhoc")
