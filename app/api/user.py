from flask import jsonify, current_app, request
from flask_jwt_extended import jwt_required, fresh_jwt_required,\
    get_jwt_identity
from bson.objectid import ObjectId
# from ..tasks import async
from . import api, db
from ..utils import err


@api.route('/user', methods=['GET'])
@jwt_required
def get_user():
    '''
    GET method use for retrieving user from his id
    '''
    id = get_jwt_identity()
    user = db.user.find_one({'_id': ObjectId(id)})
    not_return_keys = (
        '_id',
        'password_hash',
        'verified',
        'ip'
    )
    map(lambda x: user.pop(x, None), not_return_keys)
    return jsonify(user)


@api.route('/user', methods=['PUT'])
@jwt_required
def put_user():
    '''
    update user
    '''
    id = get_jwt_identity()
    data_bag = dict(request.get_json())
    # protected field
    protected_field = (
        '_id',
        'email',
        'password_hash',
        'verified',
        'ip',
        'member_since'
    )
    map(lambda x: data_bag.pop(x, None), protected_field)

    if not data_bag:
        err('failed_to_update', 'no update are made', 201)

    db.user.update({'_id': ObjectId(id)}, data_bag)
    return jsonify({'acknowledgement': True})


# admin only
@api.route('/user/<id>', methods=['DELETE'])
@fresh_jwt_required
def del_user(id):
    '''
    DELETE /user/9sd9288s8f
    -H Authorization: JWT token
    <Warning>: confirm before delete
    '''
    admin_id = get_jwt_identity()
    admin = db.user.find_one({'_id': ObjectId(admin_id)})

    if admin['email'] is not current_app.config['ADMIN_EMAIL']:
        return err("access_denied", "accessing protected resource denied", 401)

    db.user.delete_one({'_id': ObjectId(id)})
    if db.user.find_one({'_id': ObjectId(id)}):
        return err("database_error", "unable to delete user", 501)
