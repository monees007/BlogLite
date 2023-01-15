import os

from flask import request, jsonify
from flask_restful import Resource
from werkzeug.utils import secure_filename

from api.errors import *
from controller.users import *
from src import views
from src.login import api_login
from src.login import auth_required
from src.user import get_uname


class User(Resource):
    @auth_required
    def get(self):
        uid = request.args.get('username')
        email = request.args.get('email')
        export = request.args.get('export')
        if uid and is_an_user(username=uid):
            user = get_uname(uid)
            return jsonify(user)
        if email and export and is_an_user(email=email):
            return jsonify(views.export())
        return responses['404u'], 404

    @auth_required
    def put(self):
        bio = request.args.get('bio') or None
        name = request.args.get('name') or None
        username = request.args.get('username')
        profile_pic = get_profile_pic()  # default profile_pic

        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file.filename == '':
                print('No selected file')
            if file:
                profile_pic = os.path.join('static/img/upload', secure_filename(file.filename))
                file.save(profile_pic)
            else:
                print('no filess')

        user = edit_profile(name, username, bio, profile_pic)
        print(profile_pic)

        return "User updated successfully.", user if user == 200 else responses['user']

    @auth_required
    def delete(self):
        return ("User deleted successfully.", 200) if delete_user() else responses[401]

    @auth_required
    def post(self):
        try:
            api_key = request.args.get("api_key")
            api_secret = request.args.get("api_secret")
            if not api_login(api_key, api_secret):
                return responses[401], 401
            print("Success")
            return "Success", 200
        except Exception:
            return responses[401]

    @staticmethod
    @auth_required
    def patch(func=None):
        email = request.args.get('email')
        username = request.args.get('username')

        if func:
            if func == "search":
                return search(request.args.get('term'))
            elif func == "is_available":
                return user_available(username)
            if not (is_an_user(username=username) or is_an_user(email=email)):
                return responses['404u']
            if func == 'followers':
                res = followers(email=email)
                return responses[403] if res == 406 else res
            elif func == 'followings':
                res = followings(email=email)
                return responses[403] if res == 406 else res
            elif func == "follow":
                return follow(email)


            elif func == "is_following":
                res = is_following(email)
                return responses[403] if res == 406 else res
        return responses[401]
