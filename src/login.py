import json
import random
import string
from functools import wraps
from io import BytesIO

import requests
from flask import request, redirect, url_for, Response
from flask_login import login_user, logout_user, current_user
from oauthlib.oauth2 import WebApplicationClient
from passlib.apps import custom_app_context as pwd_context
from werkzeug.wsgi import FileWrapper

SESSION_PROTECTION = None
# session_protected=None

from model import model
from src.config import *
from src.user import User
from controller.users import cred as credential_provider

client = WebApplicationClient(GOOGLE_CLIENT_ID)


def login():
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(authorization_endpoint,
                                             redirect_uri=request.base_url + "/callback",
                                             scope=["openid", "email", "profile"], )
    return redirect(request_uri)


def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]

    else:
        return "User email not available or not verified by Google.", 400

    user = User(
        mid=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    db = model.get_db()

    if not User.get(unique_id) or 0:
        User.create(unique_id, users_name, users_email, picture)
        print('user created')
    else:
        print('user already exist')

    # Begin user session by logging the user in
    login_user(user, remember=True)

    # Send user back to homepage
    return redirect(url_for("current_profile"))


def credentials():
    if current_user.is_authenticated:
        cred = {'api_key': ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(22)),
            'api_secret': ''.join(
                random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(25))}
        if credential_provider(cred) != 406:
            b = FileWrapper(BytesIO(json.dumps(cred, indent=4).encode('utf-8')))
            header = {'Content-Disposition': 'attachment; filename="credentials.json"'}
            return Response(b, mimetype="text/plain", direct_passthrough=True, headers=header)
    else:
        return redirect(url_for("login"))


def api_login(api_key, api_secret):
    if api_key and api_secret:
        db = model.get_db()
        objx = db.execute(f"SELECT * FROM credentials WHERE api_key = '{api_key}'").fetchone()

        if objx is not None and pwd_context.verify(api_secret, objx["api_secret"]):
            userDB = db.execute(f"SELECT * FROM user WHERE email = '{objx['email']}'").fetchone()
            user = User(
                mid=userDB["id"], name=userDB["name"], email=userDB["email"], profile_pic=["profile_pic"]
            )
            login_user(user, remember=True)
            return True
        else:
            return False


def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("index"))


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # if current user is logged in through AUTH2.0
        if current_user.is_authenticated:
            return f(*args, **kwargs)

        # Alternate authentication method
        api_key = ''
        api_secret = ''
        if 'api_key' in request.headers:
            api_key = request.headers['api_key']
        if 'api_secret' in request.headers:
            api_secret = request.headers['api_secret']
        # return 401 if token is not passed
        if not (api_secret and api_key):
            return {'message': 'Unauthorized'}, 401
        user = ''
        try:
            db = model.get_db()
            objx = db.execute(f"SELECT * FROM credentials WHERE api_key = '{api_key}'").fetchone()
            if objx is not None and pwd_context.verify(api_secret, objx["api_secret"]):
                userDB = db.execute(f"SELECT * FROM user WHERE email = '{objx['email']}'").fetchone()
                user = User(
                    mid=userDB["id"], name=userDB["name"], email=userDB["email"], profile_pic=["profile_pic"]
                )
            else:
                return {
                    'message': 'Credentials invalid !!'
                }, 401
        except:
            return {
                'message': 'Credentials invalid !!'
            }, 401
        login_user(user, remember=False)
        # print(current_user.email)
        return f(*args, **kwargs)

    return decorated
