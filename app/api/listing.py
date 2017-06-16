from flask import jsonify, request
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from flask_jwt import jwt_required, current_identity
from . import api, db
from .errors import bad_request

Listing = db.listing


def marshal_with(marshal, model):
    # return a response object
    marshal_value = map(lambda i: model.get(i, None), marshal)
    print model
    print marshal_value
    r = jsonify(dict(zip(marshal, marshal_value)))
    return r


@api.route('/listing', methods=['GET'])
@jwt_required()
def get_listing():
    '''
    GET method use for retrieving listing from his id
    '''
    listing = (
        'title',
        'description',
        'price',
        'currency',
        'time',
        'location',
        'uri',
        'posted time',
        'img')
    l = Listing.find_one({'user_id': str(dict(current_identity)['_id'])})
    r = marshal_with(listing,l)
    # r.header('Location') = '/listing'
    return r


@api.route('/listing', methods=['POST'])
@jwt_required()
def post_listing():
    '''
    POST method for create new listing in the system with basic infomation
    '''
    listing = dict(request.get_json())
    listing['user_id'] = str(dict(current_identity).get('_id'))
    id = str(Listing.insert_one(listing).inserted_id)
    return jsonify({'acknowledgement': True, 'id': id})


@api.route('/listing', methods=['PUT'])
@jwt_required()
def put_listing():
    '''
    update listing
    '''
    listing = dict(current_identity)
    ObjectId(listing['_id'])
    return jsonify({'acknowledgement': True})


@api.route('/listing', methods=['DELETE'])
@jwt_required()
def del_listing():
    listing = dict(current_identity)
    id = listing['_id']
    Listing.delete_one({'_id': ObjectId(id)})
    if Listing.find_one({'_id': ObjectId(id)}) is None:
        return jsonify({'acknowledgement': True})
    else:
        return bad_request("Can't delete listing. Please try again")
