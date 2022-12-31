from flask import Response, request
from flask_restful import Resource

from src.controller import *
from src.login import api_login
from src.user import get_uname
from src.views import *

responses = {
    401: {
        "errorCode": "USRRES0001",
        "error": "Input parameter missing"
    },
    400: {},
    417: {
        "errorCode": "417",
        "error": "Entry has been deleted or marked private by owner"
    },
    403: {
        "errorCode": "403",
        "error": "Not Authorized. Are you authenticated?"},
    9: {
        "errorCode": "9",
        "error": "Token expired"
    }

}


class Login(Resource):
    pass


class Entry(Resource):
    @staticmethod
    def get():
        pid = request.args.get('pid') or None
        username = request.args.get('username') or None
        feed = request.args.get('feed') or None
        trending = request.args.get('trending') or None

        if pid != None:
            try:
                req = retrive_a_post(int(pid))
            except IndexError:
                req = responses[417]
            return jsonify(req) if req != 406 else Response(status=req)
        elif username != None:
            try:
                req = profile(username)[1]
            except IndexError:
                req = responses[417]
            return jsonify(req) if req != 406 else Response(status=req)
        elif feed:
            try:
                req = feeds()
            except IndexError:
                req = responses[417]
            return jsonify(req) if req != 406 else Response(status=req)
        elif trending:
            try:
                req = top_posts()
            except IndexError:
                req = responses[417]
            return jsonify(req) if req != 406 else Response(status=req)

    @staticmethod
    def post():
        content = request.args.get('content')
        try:
            user = current_user.email
            code = create_post(user, content)
        except Exception:
            code = responses[403]
        return jsonify(code) if code == 201 else Response(status=code)

    @staticmethod
    def delete():
        pid = request.args.get('pid')
        req = delete_post(pid)
        return jsonify(req) if req != 406 else Response(status=req)

    @staticmethod
    def put():
        pid = request.args.get('pid')
        content = request.args.get('content')
        try:
            code = update_post(pid, content)
        except Exception:
            code = responses[403]
        return jsonify(code) if code == 201 else Response(status=code)

    @staticmethod
    def patch():
        func = request.args.get('func')
        pid = request.args.get('pid')
        if func == "archive":
            return Response(status=archive(pid))
        elif func == "share":
            return Response(status=share(pid))
        elif func == "like":
            f = like(pid)
            return Response(f, status=f)
        return Response(func, 123)


class User(Resource):
    def get(self):
        uid = request.args.get('username')
        try:
            user = get_uname(uid)
            return jsonify(user)
        except:
            return user

    def put(self):
        bio = request.args.get('bio') or None
        email = request.args.get('email') or None
        name = request.args.get('name') or None
        username = request.args.get('username')
        # if user is None:
        #     return Response("User not found", status=404)
        # if bio:
        #     user["bio"] = bio
        # if email:
        #     user["email"] = email
        # if name:
        #     user["name"] = name
        user = edit_profile(name, email, username, bio)

        return user

    def post(self):
        api_key = request.args.get("api_key")
        api_secret = request.args.get("api_secret")
        api_login(api_key, api_secret)
        print("Success")
        return "Success", 200

    def patch(self):
        username = request.args.get()
        return

    @staticmethod
    def patch():
        email = request.args.get('email')
        func = request.args.get('func')
        if email and func:
            if func == 'followers':
                res = followers(email=email)
                return responses[403] if res == 406 else res
            elif func == 'followings':
                res = followings(email=email)
                return responses[403] if res == 406 else res
            elif func == "follow":
                res = follow(email)
                return responses[403] if res == 406 else res
            elif func == "search":
                pass
        return responses[401]

class Comment(Resource):
    def get(self):
        pid = request.args.get('pid')
        return get_comments(pid)

    def post(self):
        pid = request.args.get('pid')
        content = request.args.get('content')
        return comment(pid=pid, content=content)

    def patch(self):
        pid = request.args.get('pid')
        content = request.args.get('content')
        cid = request.args.get('cid')
        return edit_comment(pid, cid, content)

    def delete(self):
        return delete_comment(cid=request.args.get('cid'))


