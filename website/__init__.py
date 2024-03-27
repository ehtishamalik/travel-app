from flask import Flask
from .views import views


def main():
    app = Flask(__name__)
    app.register_blueprint(views, url_prefix="/")
    return app
