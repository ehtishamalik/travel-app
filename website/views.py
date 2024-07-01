from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from os import path
from werkzeug.security import generate_password_hash, check_password_hash
from .models import database, Destination, Messages, User
from .helpers import generate_unique_key, save_compressed_image, sqlalchemy_to_tuple
from .constants import SUCCESS, ERROR

views = Blueprint("views", __name__)
IMAGES_FOLDER = path.join("website", "static", "images")

@views.route("/", methods=["GET"])
@login_required
def home():
    try:
        destinations = database.query(Destination).all()
    except Exception as e:
        flash(f"Something went wrong, please reload the page", category=ERROR)
    else:
        to_tuple = []
        for destination in destinations:
            to_tuple.append(sqlalchemy_to_tuple(destination))
    
    return render_template(
        "home.html", destinations=to_tuple, image_folder=IMAGES_FOLDER, view='home'
    )


@views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user = database.query(User).filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect Email or Password", category=ERROR)
        except Exception as e:
            flash(f"We could not log you in, please try again", category=ERROR)
    return render_template("login.html")


@views.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.login"))


@views.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if len(username) > 40:
            flash("Username must be smaller than 40 characters.", category=ERROR)
        elif len(username) < 8:
            flash("Username must be longer than 6 characters.", category=ERROR)
        elif len(password) < 8:
            flash("Username must be longer than 6 characters.", category=ERROR)
        else:
            new_user = User(username, email, generate_password_hash(password))
            try:
                database.add(new_user)
                database.commit()
            except Exception as e:
                if "UNIQUE constraint failed: user.email" == e.orig.args[0]:
                    flash("Email already exists.", category=ERROR)
                else:
                    flash("Could not register, please try again.", category=ERROR)
                current_app.logger.error(f"[ERROR]\n{e}")
            else:
                flash("Account created successfully, please log in.", category=SUCCESS)
                return redirect(url_for("views.login"))
    return render_template("register.html")


@views.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@views.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        new_messsage = Messages(name, email, message)
        try:
            database.add(new_messsage)
            database.commit()
        except Exception as e:
            flash("Something went wrong, please try again.", category=ERROR)
            current_app.logger.error(f"[ERROR]\n{e}")
        else:
            flash("Thank you for your feedback.", category=SUCCESS)

    return render_template("contact.html")


@views.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        image = request.files.get("image")
        name = request.form.get("desname")
        description = request.form.get("description")
        unique_key = generate_unique_key()
        image_name = f"{unique_key}.jpeg"
        try:
            destination = Destination(name, description, image_name, current_user.uid)
            database.add(destination)
            database.commit()
        except Exception as e:
            flash("Could not add you destination, please try again", category=ERROR)
            current_app.logger.error(f"[ERROR]\n{e}")
        else:
            save_compressed_image(path.join(IMAGES_FOLDER, image_name), image)
    return render_template("upload.html")

