from flask import request
from flask_restful import Resource

from api.errors import *
from controller.comments import *
from src.login import auth_required


class Comment(Resource):
    def get(self):
        pid = request.args.get('pid')
        return get_comments(pid) if is_an_entry(pid) else (responses['404p'], 404)

    @auth_required
    def post(self):
        pid = request.args.get('pid')
        content = request.args.get('content')
        res = comment(pid=pid, content=content)
        return res if is_an_entry(pid) else (responses['404p'], 404)

    @auth_required
    def patch(self):
        content = request.args.get('content')
        cid = request.args.get('cid')

        if is_an_comment(cid):
            return edit_comment(cid, content)
        return responses['404c'], 404

    @auth_required
    def delete(self):
        cid = request.args.get('cid')

        return delete_comment(cid) if is_an_comment(cid) else (responses['404c'], 404)
