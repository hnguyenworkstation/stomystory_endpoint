from flask import current_app
from flask_jwt import JWT
from werkzeug.security import check_password_hash
from bson.objectid import ObjectId
from datetime import datetime
from . import db

Auth = JWT()


@Auth.authentication_handler
def authenticate(email, password):
    user = db.user.find_one({"email": email})
    if user and check_password_hash(user['password_hash'], password):
        return user


@Auth.identity_handler
def identity(payload):
    _id = payload['identity']
    return db.user.find_one({'_id': ObjectId(_id)})


@Auth.jwt_payload_handler
def payload(identity):
    iat = datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
    identity = identity.get('_id', None)
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': str(identity)}
