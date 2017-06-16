from flask import jsonify, request
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from flask_jwt import jwt_required, current_identity
from . import api, db
from .errors import bad_request

User = db.user


@api.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    '''
    GET method use for retrieving user from his id
    '''
    user = dict(current_identity)
    del user['_id']
    del user['password_hash']
    return jsonify(user)


@api.route('/user', methods=['POST'])
def post_user():
    '''
    POST method for create new user in the system with basic infomation
    '''
    content = request.get_json(silent=True)
    if content is None:
        return jsonify({"error": "data are not provided"})
    email = content.get('email', None)
    password = content.get('password', None)
    if email is None or password is None:
        return jsonify({"error": "email or password is Null"})
    if User.find_one({'email': email}):
        id = User.find_one({'email': email})['_id']
        return jsonify({"error": "user already exist", "id": str(id)})
    user = {
        "email": email,
        "password_hash": generate_password_hash(
            password, method='pbkdf2:sha1:5000')
    }
    id = str(User.insert_one(user).inserted_id)
    return jsonify({'acknowledgement': True, 'id': id})


@api.route('/user', methods=['PUT'])
@jwt_required()
def put_user():
    '''
    update user
    '''
    user = dict(current_identity)
    ObjectId(user['_id'])
    return jsonify({'acknowledgement': True})


@api.route('/user', methods=['DELETE'])
@jwt_required()
def del_user():
    user = dict(current_identity)
    id = user['_id']
    User.delete_one({'_id': ObjectId(id)})
    if User.find_one({'_id': ObjectId(id)}) is None:
        return jsonify({'acknowledgement': True})
    else:
        return bad_request("Can't delete user. Please try again")
