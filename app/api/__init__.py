# RESTful Api
from flask import Blueprint, make_response, jsonify
from pymongo import MongoClient
import os

username = os.getenv('DB_USERNAME') or '1'
password = os.getenv('DB_PASSWORD') or '1'
connection = MongoClient('ds133192.mlab.com', 33192)
db = connection['stomystory']
db.authenticate(username, password)
api = Blueprint('api', __name__)

from . import comment, listing, menu, order, user
from .auth import Auth
