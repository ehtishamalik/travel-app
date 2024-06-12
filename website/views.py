from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from os import path
from .models import database
from .helpers import generate_unique_key, save_compressed_image

views = Blueprint("views", __name__)
IMAGES_FOLDER = path.join("website", "static", "images")


@views.route("/")
def home():
    destinations = database.get_all_destination()
    return render_template(
        "home.html", destinations=destinations, image_folder=IMAGES_FOLDER
    )


@views.route("/about")
def about():
    return render_template("about.html")


@views.route("/contact")
def contact():
    return render_template("contact.html")


@views.route("/upload")
def upload():
    return render_template("upload.html")


@views.route("/destination", methods=["POST"])
def destination():
    image = request.files.get("image")
    name = request.form.get("desname")
    description = request.form.get("description")
    unique_key = generate_unique_key()
    unique_key = f"{unique_key}.jpeg"
    try:
        save_compressed_image(path.join(IMAGES_FOLDER, unique_key), image)
        database.add_destination(name, description, unique_key)
    except Exception as e:
        print("[ ERROR ]", e)

    return redirect(url_for("views.home"))


@views.route("/submit", methods=["POST"])
def submit_info():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    message = request.form.get("message")
    database.add_message(email, name, phone, message)
    return redirect(url_for("views.contact"))


@views.route("/database")
def show_database():
    return jsonify(database.get_all_messages())
