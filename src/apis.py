from flask import (
    Blueprint,
    jsonify,
    current_app
)
from src.models import Destination, Messages, User
from src.models import db
from src.constants import DELETED, ERROR

apis = Blueprint("apis", __name__)


@apis.route("/users/<int:user_id>", methods=["DELETE"])
def users(user_id):
    try:
        user = db.session.query(User).filter_by(uid=int(user_id)).first()
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"[ERROR]\n{e}\n\n")
        return (
            jsonify(
                {
                    "status": ERROR,
                    "message": "An error occurred while deleting the user.",
                }
            ),
            500,
        )
    else:
        return (
            jsonify(
                {"status": DELETED, "message": f"{user.username} deleted successfully."}
            ),
            200,
        )


@apis.route("/messages/<int:message_id>", methods=["DELETE"])
def messages(message_id):
    try:
        message = db.session.query(Messages).filter_by(uid=int(message_id)).first()
        db.session.delete(message)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"[ERROR]\n{e}\n\n")
        return (
            jsonify(
                {
                    "status": ERROR,
                    "message": "An error occurred while deleting the message.",
                }
            ),
            500,
        )
    else:
        return (
            jsonify(
                {"status": DELETED, "message": f"Message from {message.username} deleted successfully."}
            ),
            200,
        )
