from flask import Blueprint, render_template, request, redirect, url_for
from os import path
from .models import database, Destination, Messages
from .helpers import generate_unique_key, save_compressed_image, sqlalchemy_to_tuple

views = Blueprint("views", __name__)
IMAGES_FOLDER = path.join("website", "static", "images")

@views.route("/", methods=["GET"])
def home():
    try:
        destinations = database.query(Destination).all()
    except Exception as e:
        print(f"[ERROR] {e.orig.args[0]}")
    else:
        to_tuple = []
        for destination in destinations:
            to_tuple.append(sqlalchemy_to_tuple(destination))
    
    return render_template(
        "home.html", destinations=to_tuple, image_folder=IMAGES_FOLDER
    )


@views.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@views.route("/register", methods=["GET"])
def register():
    return render_template("register.html")


@views.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@views.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")


@views.route("/upload", methods=["GET"])
def upload():
    return render_template("upload.html")


@views.route("/destination", methods=["POST"])
def destination():
    image = request.files.get("image")
    name = request.form.get("desname")
    description = request.form.get("description")
    unique_key = generate_unique_key()
    image_name = f"{unique_key}.jpeg"
    try:
        destination = Destination(None, name, description, image_name)
        database.add(destination)
        database.commit()
    except Exception as e:
        print(f"[ERROR] {e.orig.args[0]}")
    else:
        save_compressed_image(path.join(IMAGES_FOLDER, image_name), image)

    return redirect(url_for("views.home"))


@views.route("/submit", methods=["POST"])
def submit_info():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    new_messsage = Messages(None, name, email, message)
    try:
        database.add(new_messsage)
        database.commit()
    except Exception as e:
        print(f"[ERROR] {e.orig.args[0]}")

    return redirect(url_for("views.contact"))
