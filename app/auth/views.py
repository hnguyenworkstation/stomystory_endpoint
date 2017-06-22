from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity,\
    jwt_refresh_token_required, create_refresh_token, jwt_required,\
    revoke_token, get_raw_jwt, get_all_stored_tokens
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import auth
from app.model import db
from app.utils import err, ip_2_coor, check_ip


@auth.before_request
def before():
    # check_ip from ip table to protect DDOS
    if check_ip(db.ip, request.remote_addr):
        return err("blocked_ip", "access from invalid ip address", 404)
    pass


@auth.route('/register', methods=['POST'])
def register():
    '''
    POST /auth/register
        -H 'Authorization: Basic dGVzdGNsaWVudDpzZWNyZXQ='
    '''
    if not request.authorization:
        return err("basic_auth", "use basic auth to login", 401)
    email = request.authorization.username
    password = request.authorization.password

    if email is None or password is None:
        return err("invalid_data", "email and password not found", 401)

    if db.user.find_one({'email': email}):
        return err("existed_user", "user already exist", 401)

    # get location from ip address
    location = ip_2_coor(request.remote_addr)
    user = {
        "email": email,
        "password_hash": generate_password_hash(
            password, method='pbkdf2:sha1:5000'),
        "location": [location],
        "verified": False,
        "ip": [request.remote_addr],
        "member_since": datetime.now()
    }
    db.user.insert_one(user)
    # [TODO] insert to elasticsearch
    # id = str(db.user.insert_one(user).inserted_id)
    return jsonify({'message': 'user has created'})


@auth.route('/login', methods=['POST'])
def login():
    '''
    POST /auth/login
        -H 'Authorization: Basic dGVzdGNsaWVudDpzZWNyZXQ='
    '''
    email = request.authorization.username
    password = request.authorization.password

    if email is None or password is None:
        return err(
            "invalid_data", "email and password are not provided",
            401
        )
    user = db.user.find_one({"email": email})

    # if not user['verified']:
    #     return err(
    #         "unverified_user", "user haven't verified",
    #         401
    #     )

    if not (user and check_password_hash(user['password_hash'], password)):
        return err(
            "auth_failed", "failed to login",
            401
        )

    return jsonify({
        'access_token': create_access_token(
            identity=str(user['_id']), fresh=True),
        'refresh_token': create_refresh_token(
            identity=str(user['_id']))
    })


# Helper method to revoke the current token used to access
# a protected endpoint
def _revoke_current_token():
    current_token = get_raw_jwt()
    revoke_token(current_token['jti'])


@auth.route('/logout', methods=['POST'])
@jwt_required
def logout():
    try:
        _revoke_current_token()
    except KeyError:
        return jsonify({
            'msg': 'Access token not found in the blacklist store'
        }), 500
    return jsonify({"msg": "Successfully logged out"}), 200


@auth.route('/logout2', methods=['POST'])
@jwt_refresh_token_required
def logout2():
    try:
        _revoke_current_token()
    except KeyError:
        return jsonify({
            'msg': 'Access token not found in the blacklist store'
        }), 500
    return jsonify({"msg": "Successfully logged out"}), 200


@auth.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    try:
        print "refresh"
        get_jwt_identity()
    except Exception:
        return err(
            'login_require',
            'user need to login before request a new token', 201)
    return jsonify({
        'access_token': create_access_token(
            # non-fresh token is generated when using refresh token
            identity=get_jwt_identity(), fresh=False)
    })
