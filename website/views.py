from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    request,
    current_app,
)
from flask_login import login_required, current_user
from os import path
from .models import database, Destination, Messages
from .helpers import generate_unique_key, save_compressed_image, sqlalchemy_to_tuple
from .constants import SUCCESS, ERROR

views = Blueprint("views", __name__)
IMAGES_FOLDER = path.join("website", "static", "images")


@views.route("/", methods=["GET"])
def home():
    return render_template("home.html", view="home", user=current_user)


@views.route("/about", methods=["GET"])
def about():
    return render_template("about.html", view="about", user=current_user)


@views.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        new_message = Messages(name, email, message)
        try:
            database.add(new_message)
            database.commit()
        except Exception as e:
            database.rollback()  # Rollback the session in case of error
            flash("Something went wrong, please try again.", category=ERROR)
            current_app.logger.error(f"[ERROR]\n{e}\n\n")
        else:
            flash("Thank you for your feedback.", category=SUCCESS)

    return render_template("contact.html", view="contact", user=current_user)


@views.route("/share", methods=["GET", "POST"])
@login_required
def share():
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
            database.rollback()  # Rollback the session in case of error
            flash("Could not add your destination, please try again", category=ERROR)
            current_app.logger.error(f"[ERROR]\n{e}\n\n")
        else:
            save_compressed_image(path.join(IMAGES_FOLDER, image_name), image)
            flash("Destination added successfully.", category=SUCCESS)
            return redirect(url_for("views.explore"))
    return render_template("share.html", view="share", user=current_user)


@views.route("/explore", methods=["GET"])
@login_required
def explore():
    try:
        destinations = database.query(Destination).all()
        to_tuple = [sqlalchemy_to_tuple(destination) for destination in destinations]
    except Exception as e:
        flash("Something went wrong, please reload the page", category="error")
        current_app.logger.error(f"[ERROR]\n{e}\n\n")
        to_tuple = []
    return render_template("explore.html", destinations=to_tuple, view="explore", user=current_user)
