from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, CHAR
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = "person"

    uid = Column("uid", Integer, primary_key=True)
    username = Column("username", String)
    password = Column("password", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, uid, username, password, gender, age):
        self.uid = uid
        self.username = username
        self.password = password
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"<{self.uid}, {self.username}, {self.password}, {self.gender}, {self.age}>"

class Messages(Base):
    __tablename__ = "message"

    uid = Column("uid", Integer, primary_key=True)
    username = Column("username", String(40))
    email = Column("email", String(40))
    message = Column("message", String(400))

    def __init__(self, uid, username, email, message):
        self.uid = uid
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
    owner = Column(ForeignKey("person.uid"))

    def __init__(self, uid, name, description, image):
        self.uid = uid
        self.name = name
        self.description = description
        self.image = image

    def __repr__(self):
        return f"<<{self.uid}, {self.name}, {self.description}, {self.image}>>"

engine = create_engine("sqlite:///database/database.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
database = Session()
