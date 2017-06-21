from collections import OrderedDict
import datetime
from flask import jsonify, redirect
from flask_jwt import JWT, JWTError
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from models.user import *

parser = reqparse.RequestParser()
parser.add_argument("username", type=str, help="Username")
parser.add_argument("password", type=str, help="Password")


class LoginCredentials:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def create(cls, user):
        return LoginCredentials(id=str(user.id), username=user.username, password=user.password)

    def user(self):
        return User.objects().with_id(self.id)


class RegisterRes(Resource):
    def post(self):
        body = parser.parse_args()
        try:
            username = body.username
            password = body.password
            username = str(username).lower()
            if username is None or len(username) == 0 or password is None or len(password) == 0:
                return {
                           "message": "username and password requite"
                       }, 401

            user = User(username=username, password=password)
            user.save()
        except Exception as e:
            return {"message": str(e)}, 401
        return redirect('/login', 307)


def authenticate(username, password):
    username = username.lower()
    user = User.objects(username=username).first()
    if user is not None and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return LoginCredentials.create(user)


def identity(payload):
    user_id = payload['identity']
    user = User.objects.with_id(user_id)
    if user is not None:
        return LoginCredentials.create(user)


def handle_user_exception_again(e):
    if isinstance(e, JWTError):
        return jsonify(OrderedDict([
            ('status_code', e.status_code),
            ('error', e.error),
            ('description', e.description),
        ])), e.status_code, e.headers
    return e


def jwt_init(app):
    app.config['SECRET_KEY'] = '^%^(*&(^&^`~GYUdsjfksadas2141!~'
    app.config["JWT_EXPIRATION_DELTA"] =datetime.timedelta(hours=24)

    app.config["JWT_AUTH_URL_RULE"] = "/login"
    # Catch exception and return it to users
    # https://github.com/mattupstate/flask-jwt/issues/32
    app.handle_user_exception = handle_user_exception_again
    jwt = JWT(app=app,
              authentication_handler=authenticate,
              identity_handler=identity)
    return jwt
