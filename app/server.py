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

def create_app(config):
    """
    Create a Flask app with a registered API and namespaces
    """
    flask_app = Flask('book_service')
    flask_app.config.from_object(config)
    blueprint = Blueprint('api', __name__, url_prefix=API_PREFIX)
    flask_api.init_app(blueprint)
    flask_api.add_namespace(request_ns)
    flask_api.add_namespace(title_ns)
    flask_app.register_blueprint(blueprint)

    log.info('Database path: %s', config.SQLALCHEMY_DATABASE_URI)
    db.init_app(flask_app)

    return flask_app

def init_db(app):
    with app.app_context():
        db.create_all()


def initialize_app(cfg):
    #flask_cfg_obj = create_flask_config_obj(cfg)
    app = create_app(cfg)
    init_db(app)

    return app