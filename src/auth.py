from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session,
    current_app,
)
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.constants import SUCCESS, ERROR
from src.models import User
from src.models import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        try:
            user = db.session.query(User).filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user, remember=True)
                next_page = session.get("next", None)
                if next_page:
                    session.pop("next")
                    return redirect(next_page)
                return redirect(url_for("views.home"))
            else:
                flash(
                    "Login Unsuccessful. Please check email and password",
                    category=ERROR,
                )
        except Exception as e:
            flash("We could not log you in, please try again", category=ERROR)
            current_app.logger.error(f"[ERROR]\n{e}")

    session["next"] = request.args.get("next")
    return render_template("login.html", view="login", user=current_user)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm-password", "").strip()
        is_admin = request.form.get("admin", False)

        if not username or not email or not password:
            flash("Username, email and password are all required.", category=ERROR)
        elif len(username) > 40:
            flash("Username must be smaller than 40 characters.", category=ERROR)
        elif len(username) < 8:
            flash("Username must be longer than 6 characters.", category=ERROR)
        elif len(password) < 8:
            flash("Username must be longer than 6 characters.", category=ERROR)
        elif password != confirm_password:
            flash("Passwords must match.", category=ERROR)
        else:
            new_user = User(
                username, email, generate_password_hash(password), bool(is_admin)
            )
            try:
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                if hasattr(e, "orig") and "UNIQUE constraint failed: user.email" in str(
                    e.orig
                ):
                    flash("Email already exists.", category=ERROR)
                else:
                    flash("Could not register, please try again.", category=ERROR)
                    current_app.logger.error(f"[ERROR]\n{e}")
            else:
                if current_user.is_authenticated and current_user.check_admin():
                    flash("Account created successfully.", category=SUCCESS)
                else:
                    flash(
                        "Account created successfully, please log in.", category=SUCCESS
                    )
                    return redirect(url_for("auth.login"))
    return render_template("register.html", view="register", user=current_user)
