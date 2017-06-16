from flask import abort, jsonify, request
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from . import api, db

Order = db.order


@api.route('/order/<id>', methods=['GET'])
def get_order(id):
    '''
    GET method use for retrieving order from his id
    '''
    try:
        order = Order.find_one({'_id': ObjectId(id)})
        del order['_id']
        return jsonify(order)
    except Exception:
        abort(404)


@api.route('/order', methods=['POST'])
def post_order():
    '''
    POST method for create new order in the system with basic infomation
    '''
    if request.json:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if email is not None and password is not None and Order.find_one({'email': email}) is None:
            order = {
                "email": email,
                "password_hash": generate_password_hash(password)
            }
            id = str(Order.insert_one(order).inserted_id)
            # send confirmation email
            return jsonify({'acknowledgement': True, 'id': id})
        else:
            abort(404)
    else:
        abort(404)


@api.route('/order/<id>', methods=['PUT'])
def put_order(id):
    '''
    update order
    '''
    return Order.findOne({'_id': id})


@api.route('/order/<id>', methods=['DELETE'])
def del_order(id):
    Order.delete_one({'_id': ObjectId(id)})
    if Order.find_one({'_id': ObjectId(id)}) is None:
        return jsonify({'acknowledgement': True})
    else:
        abort(404)
