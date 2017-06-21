from flask import Flask
from flask_restful import Api
from res.login import *
import mlab
from res.user_res import UserRes

app = Flask(__name__)
api = Api(app)
jwt = jwt_init(app)

mlab.connect()
api.add_resource(RegisterRes, '/register')
api.add_resource(UserRes, '/user')

if __name__ == '__main__':
    app.run()
