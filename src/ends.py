from flask import Response, jsonify, request
from flask_restful import Resource
from flask_login   import login_required
from src.controller import *
from src.user import get_uname
from src.login import api_login
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
    403:{
        "errorCode": "403",
        "error": "Not Authorized. Are you authenticated?"}

}

class Login(Resource):
    def get(self):
        api_key = request.args.get("api_key")
        api_secret = request.args.get("api_secret")
        api_login(api_key, api_secret)
        print("Success")
        return "Success",200


class Like(Resource):
    @staticmethod
    def post():
        pid = request.args.get('pid')
        po = like(pid)
        return po, po


# def post(pid=None):
#     if request.method == 'GET':
#         pass
#     elif request.method == 'POST':
#
#     elif request.method == 'UPDATE':
#         form = MdeForm()
#         content = form.editor.data
#         controller.update_post(pid, content)
#     elif request.method == 'DELETE':
#         controller.delete_post(pid)


class Entry(Resource):
    @staticmethod
    def get():
        pid = request.args.get('pid')
        try:
            req = retrive_a_post(int(pid))
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

    def patch(self):
        func = request.args.get('func')
        pid = request.args.get('pid')
        if func == "archive":
            return jsonify(archive(pid))
        elif func == "delete":
            return jsonify(delete_post(pid))
        elif func == "share":
            return jsonify(share(pid))
        return Response(func)

class User(Resource):
    def get(self):
        uid = request.args.get('username')
        try:
            user =  get_uname(uid)
            return jsonify(user)
        except:
            return user
    def patch(self):
        bio = request.args.get('bio') or None
        email = request.args.get('email') or None
        name = request.args.get('name') or None
        username = request.args.get('username')
        user = get_uname(username)
        if user is None:
            return Response("User not found", status=404)
        if bio:
            user["bio"] = bio
        if email:
            user["email"] = email
        if name:
            user["name"] = name

        return user
            
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
        return edit_comment(pid,cid,content)
    def delete(self):
        return delete_comment(cid=request.args.get('cid'))
