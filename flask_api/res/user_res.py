from flask_jwt import jwt_required, current_identity
from flask_restful import reqparse, Resource


class UserRes(Resource):
    @jwt_required()
    def get(self):
        user = current_identity.user()
        return user.get_json()
