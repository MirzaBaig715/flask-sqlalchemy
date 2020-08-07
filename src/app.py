from flask import Flask
from application.models.database import db, bcrypt
from config import config as app_config
from application.views.user_view import api as user_resource


def create_app(env_name):

    """
    Create app and initialize it.
    """

    app = Flask(__name__)
    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)
    db.init_app(app)
    app.register_blueprint(user_resource, url_prefix=f"/api")

    @app.before_first_request
    def init_database():
        db.create_all()
    return app
