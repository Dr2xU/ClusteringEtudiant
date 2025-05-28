import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.extensions import db  # SQLAlchemy instance from extensions
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    """
    Admin model for representing administrative users in the system.
    These users have privileges to manage teachers and students.
    """

    __tablename__ = 'admins'  # Database table name

    # Primary key: unique admin ID
    id = db.Column(db.Integer, primary_key=True)

    # Admin login email (must be unique)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Hashed password for login security
    password_hash = db.Column(db.String(128), nullable=False)

    # Optional personal info
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)

    # Timestamp when the admin account was created
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        """
        Return a string representation of the admin.
        Useful for debugging and admin listings.
        """
        return f"<Admin {self.email}>"

    def set_password(self, password: str) -> None:
        """
        Hash and store the admin's password.

        Args:
            password (str): The plain-text password to be stored
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the stored password hash.

        Args:
            password (str): The plain-text password to verify

        Returns:
            bool: True if the password is correct, False otherwise
        """
        return check_password_hash(self.password_hash, password)
