import os

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_mde import Mde
from flask_restful import Api
from flaskext.markdown import Markdown

from api.Comments import Comment as COMMENT
from api.Entry import Entry as ENTRY
from api.User import User as USER
from api.main import API as API
from src import routes, login
from src.user import User

basedir = os.path.abspath(os.path.dirname(__file__))
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
api = Api(app)
mde = Mde(app)
CORS(app)
Markdown(app)

login_manager = LoginManager()
login_manager.init_app(app)

# API ENDPOINTS
api.add_resource(API, "/api/", )
api.add_resource(ENTRY, "/api/entry", "/api/entry/<func>")
api.add_resource(USER, "/api/user", "/api/user/<func>")
api.add_resource(COMMENT, "/api/comment", "/api/comment/<func>")

# APP AUTHENTICATION
app.add_url_rule('/cred', view_func=login.credentials)
app.add_url_rule('/export', view_func=routes.export)
app.add_url_rule('/login', view_func=login.login)
app.add_url_rule('/logout', view_func=login.logout)
app.add_url_rule('/login/callback', view_func=login.callback)

# APP FUNCTIONS
app.add_url_rule('/', view_func=routes.index)
app.add_url_rule('/feed', view_func=routes.feed)
app.add_url_rule('/discover', view_func=routes.search)
app.add_url_rule('/user/<username>', view_func=routes.profile)
app.add_url_rule('/user', view_func=routes.current_profile)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    mde.init_app(app)
    app.config.from_object(__name__)
    app.run(debug=False, ssl_context="adhoc")
