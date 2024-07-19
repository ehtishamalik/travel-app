from logging.handlers import RotatingFileHandler
from flask_login import LoginManager
from flask import Flask
import logging
import os
from .views import views
from .auth import auth
from .models import database, User


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(24).hex()
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/database.db"

    # Log Errors
    file_handler = RotatingFileHandler("error.log", maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    )
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    # Login functionalities
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    @app.template_filter("include")
    def include(view):
        return view in ["home", "about", "contact"]

    @login_manager.user_loader
    def load_user(id):
        return database.query(User).filter_by(uid=int(id)).first()

    return app
