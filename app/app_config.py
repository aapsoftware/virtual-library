"""
Configuration settings for the application
"""
import os

listen_addr = os.getenv('LISTEN_ADDR', '127.0.0.1')
listen_port = os.getenv('LISTEN_PORT', 7777)

class Config(object):
    # Flask settings
    SERVER_HOST = listen_addr
    SERVER_PORT = listen_port

    SQLALCHEMY_DATABASE_URI = 'sqlite:///books_req.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    ERROR_404_HELP = False

    DEBUG = False
    FLASK_DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(Config):
    DEBUG = False
    FLASK_DEBUG = False
    TESTING = True
