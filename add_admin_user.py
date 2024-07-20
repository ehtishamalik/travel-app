from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
from src.models import User

# Database connection URI
SQLALCHEMY_DATABASE_URI = "sqlite:///instance/database.db"  # Adjust as needed

# SQLAlchemy setup
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# Function to add admin user
def add_admin_user():
    admin_user = User(
        username='admin',
        email='admin@tt.com',
        password=generate_password_hash('Eht!sham'),
        is_admin=True
    )
    
    session.add(admin_user)
    session.commit()
    print("Admin user added successfully.")

if __name__ == "__main__":
    try:
        # Create tables if they do not exist
        Base.metadata.create_all(bind=engine)
    except exc.OperationalError:
        print("cannot")
    else:
        # Add admin user
        add_admin_user()

        # Close session
        session.close()
