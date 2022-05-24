from os import environ
from dotenv import load_dotenv

# Initialize Environment Variables
load_dotenv()

class Config(object):
    DEBUG = False
    TESTING = False
    FLASK_APP=environ.get("FLASK_APP")
    FLASK_ENV=environ.get("FLASK_ENV")
    SECRET_KEY = environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    
