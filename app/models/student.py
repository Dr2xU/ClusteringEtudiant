import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.election import election_students


class Student(db.Model):
    """
    Student model representing a student user.
    Students can log in, vote in elections, and be grouped by clustering.
    """

    __tablename__ = 'students'

    # Unique identifier for the student
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(20), unique=True, nullable=False)

    # Login email for the student (must be unique)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Hashed password for login security
    password_hash = db.Column(db.String(128), nullable=False)

    # Student’s first and last name (optional on first login)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)

    # Additional profile info (e.g., class name, section)
    class_name = db.Column(db.String(50), nullable=True)
    section = db.Column(db.String(50), nullable=True)

    # Many-to-many relationship to elections
    elections = db.relationship(
        'Election',
        secondary=election_students,
        back_populates='students',
        lazy='subquery'
    )

    # Account creation timestamp
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        """
        String representation for debugging and logging.
        """
        return f"<Student {self.email}>"

    def set_password(self, password: str) -> None:
        """
        Hash and set the student's password.

        Args:
            password (str): Plain-text password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verify a plain-text password against the stored hash.

        Args:
            password (str): Plain-text password

        Returns:
            bool: True if the password matches, else False
        """
        return check_password_hash(self.password_hash, password)
