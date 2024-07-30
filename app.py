from logging.handlers import RotatingFileHandler
from flask_login import LoginManager
from flask_migrate import Migrate
from flask import Flask
import logging
import os
from src import db, IMAGES_FOLDER


def create_app():
    if not os.path.exists(IMAGES_FOLDER):
        os.mkdir(IMAGES_FOLDER)

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(24).hex()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./database.db"

    db.init_app(app)

    # Register Blueprints
    from src.views import views
    from src.auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    Migrate(app, db)

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

    @app.template_filter("include")
    def include(view):
        return view in ["home", "about", "contact"]

    # Load current user
    from src.models import User

    @login_manager.user_loader
    def load_user(id):
        return db.session.query(User).filter_by(uid=int(id)).first()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
