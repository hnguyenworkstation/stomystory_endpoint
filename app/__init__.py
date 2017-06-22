from flask import Flask
from simplekv.db.mongo import MongoStore
# from model import ElasticDB, User
from config import config
from flask_jwt_extended import JWTManager
from model import db
# db = ElasticDB()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_STORE'] = MongoStore(db, 'token')
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = 'all'
    config[config_name].init_app(app)

    JWTManager(app)
    db.token.drop()

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
