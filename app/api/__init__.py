# RESTful Api
from flask import Blueprint, make_response, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['stoma_db']
api = Blueprint('api', __name__)

from . import comment, listing, menu, order, token, user
from .auth import Auth
