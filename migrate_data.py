from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker, declarative_base
from src.models import User

# Database connection URI
SQLALCHEMY_DATABASE_URI = "sqlite:///instance/database.db"  # Adjust as needed

# SQLAlchemy setup
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# List of admin users to be added, emails must be different
admin_user = [
    User(
        username="admin",
        email="admin@tt.com",
        password="TravelTales",
        is_admin=True,
    ),
]


if __name__ == "__main__":
    try:
        # Create tables if they do not exist
        Base.metadata.create_all(bind=engine)

        # Add admin user
        for admin in admin_user:
            session.add(admin)
        session.commit()
    except exc.OperationalError:
        session.rollback()
        print("Could not make a connection with database.")
    except exc.IntegrityError as error:
        session.rollback()
        print(f"**UNIQUE constraint failed**\n{error}")
    except Exception as error:
        session.rollback()
        print(f"**Something wend wrong**\n{error}")
    else:
        print("Admin user added successfully.")
    finally:
        # Close session
        session.close()
