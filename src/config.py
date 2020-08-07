import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('SECRET_KEY', 'random-string')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'sqlite3.db')


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:postgres@localhost/flask-test'


config = {
    'development': DevConfig
}
