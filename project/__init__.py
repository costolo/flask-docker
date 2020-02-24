# project/__init__.py

from flask import Flask, jsonify
from flask_restplus import Resource, Api


# initiate the app
app = Flask(__name__)
api = Api(app)

# set config
app.config.from_object('project.config.DevelopmentConfig')

class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong'
        }

api.add_resource(Ping, '/ping')