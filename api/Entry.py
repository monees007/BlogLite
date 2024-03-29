import os

from flask import Response, request, jsonify
from flask_restful import Resource
from werkzeug.utils import secure_filename

from api.errors import *
from controller.entries import *
from src.login import auth_required
from src.views import *


class Entry(Resource):

    @auth_required
    def get(self, func=None):
        pid = request.args.get('pid') or None
        username = request.args.get('username') or None

        if pid and not is_an_entry(pid):
            return responses['404p'], 404
        if username and not is_an_user(username=username):
            return responses['404u'], 404

        if pid:
            try:
                req = retrive_a_post(int(pid))
            except IndexError:
                req = responses[417]
            return jsonify(req) if req != 404 else Response(status=req)
        elif func == 'username':
            try:
                req = profile(username)[1]
            except IndexError:
                req = responses[417]
            return jsonify(req) if req != 406 else Response(status=req)
        elif func == 'feed':
            try:
                req = feeds()
            except IndexError:
                req = responses[417]
            return jsonify(req) if req != 406 else Response(status=req)
        elif func == 'trending':
            try:
                req = top_posts()
            except IndexError:
                req = responses[417]
            return jsonify(req) if req != 406 else Response(status=req)

    @auth_required
    def post(self, func=None):
        content = request.args.get('content')
        if content:
            try:
                user = current_user.email
                code = create_post(user, content)
            except Exception:
                code = responses[403]
            return code
        # print(request.files.getlist('fileName'))
        # print(request.files.getlist('file')[0].filename)
        print(request.files['file'].filename)
        if func == 'upload' and 'file' in request.files:

            file = request.files['file']
            print(file)
            if file:
                payload = os.path.join('static/img/upload', secure_filename(file.filename))
                file.save(payload)
                return jsonify(payload)

        else:
            return responses['404d'], 404

    @auth_required
    def delete(self, func=None):
        pid = request.args.get('pid')
        return delete_post(pid) if is_an_entry(pid) else (responses['404p'], 404)

    @auth_required
    def put(self, func=None):
        pid = request.args.get('pid')
        if not is_an_entry(pid):
            return responses['404p'], 404
        content = request.args.get('content')
        try:
            code = update_post(pid, content)
        except Exception:
            code = responses[403]
        return jsonify(code) if code == 201 else Response(status=code)

    @auth_required
    def patch(self, func=None):

        pid = request.args.get('pid')
        if not is_an_entry(pid):
            return responses['404p'], 404
        if func == "archive":
            return archive(pid)
        elif func == "share":
            return Response(status=share(pid))
        elif func == "like":
            return like(pid)
        elif func == "likes":
            return jsonify(get_doers('likes', pid))
        elif func == "shares":
            return jsonify(get_doers('shares', pid))
        elif func == 'is_liked':
            return ('True', 200) if is_liked(pid) else ('False', 417)
        return Response(func, 123)
