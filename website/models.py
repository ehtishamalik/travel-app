from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from flask_login import UserMixin
from sqlalchemy.sql import func

Base = declarative_base()

class Messages(Base):
    __tablename__ = "message"

    uid = Column("uid", Integer, primary_key=True)
    username = Column("username", String(40))
    email = Column("email", String(40))
    message = Column("message", String(400))

    def __init__(self, username, email, message):
        self.username = username
        self.email = email
        self.message = message

    def __repr__(self):
        return f"<<{self.uid}, {self.username}, {self.email}, {self.message}>>"

class Destination(Base):
    __tablename__ = "destination"

    uid = Column("uid", Integer, primary_key=True)
    name = Column("name", String(30))
    description = Column("description", String(400))
    image = Column("image", String(41))
    owner = Column(ForeignKey("user.uid"))

    def __init__(self, name, description, image, owner):
        self.name = name
        self.description = description
        self.image = image
        self.owner = owner

    def __repr__(self):
        return f"<<{self.uid}, {self.name}, {self.description}, {self.image}>>"


class User(Base, UserMixin):
    __tablename__ = "user"

    uid = Column("uid", Integer, primary_key=True)
    username = Column("username", String(40))
    email = Column("email", String(40), unique=True)
    password = Column("password", String(256))
    created_at = Column(DateTime(timezone=True), default=func.now())

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.uid)
    
    def __repr__(self):
        return f"<<{self.uid}, {self.username}, {self.email}, {self.password}, {self.created_at}>>"

engine = create_engine("sqlite:///database/database.db", echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
database = Session()
