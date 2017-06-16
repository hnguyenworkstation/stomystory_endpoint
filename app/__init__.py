from flask import Flask
# from model import ElasticDB, User
from config import config
from .api import Auth as auth
# db = ElasticDB()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # db.init_app(app)

    auth.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(
        api_blueprint,
        url_prefix='/api')

    return app
