from flask import Flask
from flask_login import LoginManager
import os
from .views import views
from .models import database, User


def main():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24).hex()
    app.register_blueprint(views, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "views.login"
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return database.query(User).filter_by(uid=int(id)).first()
    
    return app
