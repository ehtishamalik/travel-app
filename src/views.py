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
from urllib.parse import urlparse
from os import path
from src.models import Destination, Messages
from src.constants import SUCCESS, ERROR
from src.models import db
from src.helpers import (
    generate_unique_key,
    save_compressed_image,
    sqlalchemy_to_tuple,
    valid_image,
)


views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
def home():
    return render_template("home.html", view="home", user=current_user)


@views.route("/about", methods=["GET"])
def about():
    return render_template("about.html", view="about", user=current_user)


@views.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        new_message = Messages(name, email, message)
        try:
            db.session.add(new_message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Something went wrong, please try again.", category=ERROR)
            current_app.logger.error(f"[ERROR]\n{e}\n\n")
        else:
            flash("Thank you for your feedback.", category=SUCCESS)

    return render_template("contact.html", view="contact", user=current_user)


@views.route("/share", methods=["GET", "POST"])
@login_required
def share():
    if request.method == "POST":
        name = request.form.get("desname", "").strip()
        description = request.form.get("description", "").strip()
        link = request.form.get("link", "").strip()
        image = request.files.get("image", None)
        is_valid = urlparse(link)

        if not name or not description or not image or not link:
            flash(
                "Destination Name, Description and Image are all required.",
                category=ERROR,
            )
        elif not image.content_type.startswith("image") or not valid_image(
            image.filename
        ):
            flash(
                "Invalid file extension, please upload 'png', 'jpg', 'jpeg'",
                category=ERROR,
            )
        elif not is_valid.scheme or not is_valid.netloc:
            flash("Invalid URL, please add a valid URL.", category=ERROR)
        else:
            unique_key = generate_unique_key()
            image_name = f"{unique_key}.jpeg"
            try:
                destination = Destination(
                    name, description, link, image_name, current_user.uid
                )
                db.session.add(destination)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(
                    "Could not add your destination, please try again", category=ERROR
                )
                current_app.logger.error(f"[ERROR]\n{e}\n\n")
            else:
                save_compressed_image(path.join(image_name), image)
                flash("Destination added successfully.", category=SUCCESS)
                return redirect(url_for("views.explore"))
    return render_template("share.html", view="share", user=current_user)


@views.route("/explore", methods=["GET"])
@login_required
def explore():
    try:
        destinations = db.session.query(Destination).all()
        to_tuple = [sqlalchemy_to_tuple(destination) for destination in destinations]
    except Exception as e:
        flash(
            "Something went wrong, we could not load all the places. Please reload the page",
            category="error",
        )
        current_app.logger.error(f"[ERROR]\n{e}\n\n")
        to_tuple = []
    return render_template(
        "explore.html", destinations=to_tuple, view="explore", user=current_user
    )


@views.route("/admin", methods=["GET"])
@login_required
def admin():
    if current_user.is_admin:
        return render_template(
        "admin.html", view="admin", user=current_user
    )
    else:
        flash("You are unauthorized to view this resource.", category=ERROR)
        return redirect(url_for("views.home"))
