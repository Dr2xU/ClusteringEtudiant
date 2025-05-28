import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.extensions import db
from app.models import Admin

def add_admin(admin: Admin) -> Admin:
    """
    Persist a new Admin instance to the database.

    Args:
        admin (Admin): The Admin object to save

    Returns:
        Admin: The saved Admin object
    """
    db.session.add(admin)
    db.session.commit()
    return admin

def get_admin_by_id(admin_id: int) -> Admin:
    """
    Fetch an Admin by their unique ID.

    Args:
        admin_id (int): The admin's primary key

    Returns:
        Admin: The matching Admin object or None
    """
    return Admin.query.get(admin_id)

def get_admin_by_email(email: str) -> Admin:
    """
    Fetch an Admin by email address.

    Args:
        email (str): Email address of the admin

    Returns:
        Admin: The matching Admin object or None
    """
    return Admin.query.filter_by(email=email).first()

def list_all_admins() -> list:
    """
    Retrieve all Admin users in the system.

    Returns:
        list: List of Admin objects
    """
    return Admin.query.order_by(Admin.created_at.desc()).all()

def delete_admin(admin_id: int) -> bool:
    """
    Delete an Admin by their ID.

    Args:
        admin_id (int): Admin's primary key

    Returns:
        bool: True if deleted successfully, False otherwise
    """
    admin = get_admin_by_id(admin_id)
    if admin:
        db.session.delete(admin)
        db.session.commit()
        return True
    return False
