from flask import Flask
from flask_login import LoginManager
import os
from .views import views
from .auth import auth
from .models import database, User


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(24).hex()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    @app.template_filter("include")
    def include(view):
        return view in ["home", "about", "contact"]

    @login_manager.user_loader
    def load_user(id):
        return database.query(User).filter_by(uid=int(id)).first()

    return app
