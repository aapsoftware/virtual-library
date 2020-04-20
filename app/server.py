"""
Flask RESTPlus API with 2 namespaces
1. Request API for dealing with requests - the main purpose of the exercise
2. Book API to help with populating the db with titles and/or testing
"""
import logging

from flask import Flask, Blueprint
from app.rest import flask_api
from app.request_api import ns as request_ns
from app.book_title_api import ns as title_ns
from app.storage.db import db

API_PREFIX = '/api/v1'

log = logging.getLogger(__name__)

class FlaskCfgObject(object):
    def __init__(self, server_cfg):

        # Flask does not work well with 0.0.0.0 being used as domain in SERVER_NAME
        if server_cfg.SERVER_HOST != '0.0.0.0':
            self.SERVER_NAME = '{0}:{1}'.format(server_cfg.SERVER_HOST, server_cfg.SERVER_PORT)
        self.SERVER_HOST_AND_PORT = '{0}:{1}'.format(server_cfg.SERVER_HOST, server_cfg.SERVER_PORT)

        self.RESTPLUS_VALIDATE = server_cfg.RESTPLUS_VALIDATE
        self.RESTPLUS_MASK_SWAGGER = server_cfg.RESTPLUS_MASK_SWAGGER
        self.ERROR_404_HELP = server_cfg.RESTPLUS_ERROR_404_HELP
        self.ERROR_INCLUDE_MESSAGE = server_cfg.RESTPLUS_ERROR_INCLUDE_MESSAGE

        # database location can be overridden in server_cfg
        self.SQLALCHEMY_DATABASE_URI = server_cfg.SQLALCHEMY_DATABASE_URI
        self.SQLALCHEMY_COMMIT_ON_TEARDOWN = True

        # these 2 settings useful for debugging
        self.SQLALCHEMY_ECHO = server_cfg.SQLALCHEMY_ECHO
        self.SQLALCHEMY_TRACK_MODIFICATIONS = server_cfg.SQLALCHEMY_TRACK_MODIFICATIONS

        self.TESTING = server_cfg.TESTING

        # flask uses ENV
        if server_cfg.FLASK_DEBUG:
            self.ENV = 'development'

def create_app(config):
    """
    Create a Flask app with a registered API and namespaces
    """
    flask_app = Flask('book_service')
    flask_app.config.from_object(FlaskCfgObject(config))
    blueprint = Blueprint('api', __name__, url_prefix=API_PREFIX)
    flask_api.init_app(blueprint)
    flask_api.add_namespace(request_ns)
    flask_api.add_namespace(title_ns)

    if 'api' not in flask_app.blueprints:
        flask_app.register_blueprint(blueprint)

    log.info('Database path: %s', config.SQLALCHEMY_DATABASE_URI)
    db.init_app(flask_app)

    return flask_app

def init_db(app):
    with app.app_context():
        db.create_all()


def initialize_app(cfg):
    app = create_app(cfg)
    init_db(app)

    return app