import json

from flask_restful import Resource


class API(Resource):
    def get(self):
        return json.load(open('openapi3_0.json')), 200
