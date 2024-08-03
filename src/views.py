from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    send_from_directory,
    request,
    current_app,
)
from flask_login import login_required, current_user
from urllib.parse import urlparse
from src.models import Destination, Messages, User
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
    return render_template("home.html", view="home", current_user=current_user)


@views.route("/about", methods=["GET"])
def about():
    return render_template("about.html", view="about", current_user=current_user)


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

    return render_template("contact.html", view="contact", current_user=current_user)


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
                save_compressed_image(image_name, image)
            except Exception as e:
                db.session.rollback()
                flash(
                    "An error occurred while adding your destination. Please try again!",
                    category=ERROR,
                )
                current_app.logger.error(f"[ERROR]\n{e}\n\n")
            else:
                flash("Destination added successfully.", category=SUCCESS)
                return redirect(url_for("views.explore"))
    return render_template("share.html", view="share", current_user=current_user)


@views.route("/explore", methods=["GET"])
@login_required
def explore():
    try:
        destinations = db.session.query(Destination).all()
        to_tuple = [sqlalchemy_to_tuple(destination) for destination in destinations]
    except Exception as e:
        flash(
            "An error occurred while loading all the places. Please reload!",
            category="error",
        )
        current_app.logger.error(f"[ERROR]\n{e}\n\n")
        to_tuple = []
    return render_template(
        "explore.html", destinations=to_tuple, view="explore", current_user=current_user
    )


@views.route("/admin", methods=["GET"])
@login_required
def admin():
    if current_user.is_admin:
        try:
            users = db.session.query(User).all()
            users_tuple = [sqlalchemy_to_tuple(user) for user in users]
            messages = db.session.query(Messages).all()
            messages_tuple = [sqlalchemy_to_tuple(message) for message in messages]
        except Exception as e:
            flash(
                "An error occurred while fetching data from the Database. Please reload!",
                category=ERROR,
            )
            current_app.logger.error(f"[ERROR]\n{e}\n\n")
        return render_template(
            "admin.html",
            view="admin",
            current_user=current_user,
            users=users_tuple,
            messages=messages_tuple,
        )
    else:
        flash("You are unauthorized to view this resource.", category=ERROR)
        return redirect(url_for("views.home"))


# Needs to move to the apis
@views.route("/images/<path:filename>", methods=["GET"])
@login_required
def get_images(filename):
    return send_from_directory("images", filename)


@views.route("/favicon.ico", methods=["GET"])
def get_favicon():
    return send_from_directory("static", "assets/favicon.png")


@views.route("/my_profile", methods=["GET", "POST"])
@login_required
def my_profile():
    if request.method == "POST":
        old_password = request.form.get("old-password", "").strip()
        new_password = request.form.get("new-password", "").strip()
        if old_password and new_password:
            try:
                user = db.session.query(User).filter_by(uid=current_user.uid).first()
                if user.is_user_authenticated(old_password):
                    if len(new_password) >= 6:
                        user.update_password(new_password)
                        db.session.commit()
                        flash("Password Updated successfully.", category=SUCCESS)
                    else:
                        flash(
                            "New password must be longer than 6 characters.",
                            category=ERROR,
                        )
                else:
                    flash("Old password does not match.", category=ERROR)
            except Exception as e:
                flash("An error occurred while updating the password.", category=ERROR)
                current_app.logger.error(f"[ERROR]\n{e}\n\n")
        else:
            flash("Both passwords are required.", category=ERROR)
    return render_template("profile.html", view="profile", current_user=current_user)
