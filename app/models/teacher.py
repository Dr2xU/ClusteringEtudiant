import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Teacher(db.Model):
    """
    Teacher model representing instructor users who create and manage elections.
    """

    __tablename__ = 'teachers'

    # Unique identifier for the teacher
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(20), unique=True, nullable=False)

    # Unique email used for login
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Hashed password for secure authentication
    password_hash = db.Column(db.String(128), nullable=False)

    # Personal information fields
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)

    # Optional department or subject area
    department = db.Column(db.String(100), nullable=True)

    # Timestamp when the teacher account was created
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        """
        Return string representation for the Teacher instance.
        """
        return f"<Teacher {self.email}>"

    def set_password(self, password: str) -> None:
        """
        Hash and store the teacher's password.

        Args:
            password (str): Plain-text password to be hashed
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check whether the provided password matches the stored hash.

        Args:
            password (str): Plain-text password to verify

        Returns:
            bool: True if password matches, else False
        """
        return check_password_hash(self.password_hash, password)
