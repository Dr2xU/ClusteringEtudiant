import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from app.extensions import db
from app.models import Admin

def create_admin(email: str, password: str, first_name: str = "", last_name: str = "") -> Admin:
    """
    Creates a new admin user and saves it to the database.

    Args:
        email (str): Admin's email address (must be unique)
        password (str): Plain-text password to hash and store
        first_name (str): Optional first name of the admin
        last_name (str): Optional last name of the admin

    Returns:
        Admin: The created Admin object
    """
    admin = Admin(
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    admin.set_password(password)  # Securely hash the password

    db.session.add(admin)
    db.session.commit()  # Persist to the database

    return admin

def get_admin_by_email(email: str) -> Admin:
    """
    Fetch an admin by their email address.

    Args:
        email (str): The admin's email

    Returns:
        Admin: Admin object if found, else None
    """
    return Admin.query.filter_by(email=email).first()

def authenticate_admin(email: str, password: str) -> Admin:
    """
    Authenticate an admin by checking email and password.

    Args:
        email (str): The admin's email
        password (str): The plain-text password to check

    Returns:
        Admin: The authenticated Admin object if credentials are correct, else None
    """
    admin = get_admin_by_email(email)
    if admin and admin.check_password(password):
        return admin
    return None

def list_all_admins() -> list:
    """
    Retrieve all admin accounts in the database.

    Returns:
        list: A list of Admin objects
    """
    return Admin.query.order_by(Admin.created_at.desc()).all()
