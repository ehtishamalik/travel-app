from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Text,
)
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func


db = SQLAlchemy()


class Messages(db.Model):
    __tablename__ = "message"

    uid = Column("uid", Integer, primary_key=True)
    username = Column("username", String(40))
    email = Column("email", String(40))
    message = Column("message", String(400))

    def __init__(self, username: str, email: str, message: str):
        self.username = username
        self.email = email
        self.message = message

    def __repr__(self):
        return f"<<{self.uid}, {self.username}, {self.email}, {self.message}>>"


class Destination(db.Model):
    __tablename__ = "destination"

    uid = Column("uid", Integer, primary_key=True)
    name = Column("name", String(30))
    description = Column("description", String(400))
    image = Column("image", String(41))
    link = Column("link", Text)
    owner = Column(ForeignKey("user.uid"))

    def __init__(self, name: str, description: str, image: str, link: str, owner: int):
        self.name = name
        self.description = description
        self.image = image
        self.link = link
        self.owner = owner

    def __repr__(self):
        return f"<<{self.uid}, {self.name}, {self.description}, {self.image}, {self.link}, {self.owner}>>"


class User(db.Model, UserMixin):
    __tablename__ = "user"

    uid = Column("uid", Integer, primary_key=True)
    username = Column("username", String(40))
    email = Column("email", String(40), unique=True)
    password = Column("password", String(256))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

    def __init__(self, username: str, email: str, password: str, is_admin: bool):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def get_id(self):
        return str(self.uid)

    def is_user_authenticated(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<<{self.uid}, {self.username}, {self.email}, {self.password}, {self.created_at}>>"
