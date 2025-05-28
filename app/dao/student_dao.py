import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.extensions import db
from app.models import Student

def add_student(student: Student) -> Student:
    """
    Persist a new Student instance to the database.

    Args:
        student (Student): A Student model instance to be saved.

    Returns:
        Student: The saved Student instance, now with a database ID.
    """
    db.session.add(student)
    db.session.commit()
    return student

def get_student_by_id(student_id: int) -> Student:
    """
    Retrieve a student record by its primary key ID.

    Args:
        student_id (int): The unique identifier of the student.

    Returns:
        Student: The Student object if found; otherwise None.
    """
    return Student.query.get(student_id)

def get_student_by_email(email: str) -> Student:
    """
    Retrieve a student by their unique email address.

    Args:
        email (str): Email address to query by.

    Returns:
        Student: The matching Student object if found; otherwise None.
    """
    return Student.query.filter_by(email=email).first()

def list_all_students() -> list:
    """
    Fetch all student records from the database, ordered by creation date descending.

    Returns:
        list: A list of Student objects sorted by newest first.
    """
    return Student.query.order_by(Student.created_at.desc()).all()

def update_student(student_id: int, first_name: str, last_name: str, class_name: str, section: str) -> Student:
    """
    Update basic profile information for a student.

    Args:
        student_id (int): The ID of the student to update.
        first_name (str): New first name.
        last_name (str): New last name.
        class_name (str): New class name.
        section (str): New section.

    Returns:
        Student: The updated Student object, or None if not found.
    """
    student = get_student_by_id(student_id)
    if not student:
        return None

    student.first_name = first_name
    student.last_name = last_name
    student.class_name = class_name
    student.section = section

    db.session.commit()
    return student

def update_student_password(student_id: int, new_password_hash: str) -> Student:
    """
    Update the password hash for a student.

    Args:
        student_id (int): The ID of the student whose password to update.
        new_password_hash (str): The hashed new password.

    Returns:
        Student: The updated Student object, or None if not found.
    """
    student = get_student_by_id(student_id)
    if not student:
        return None

    student.password_hash = new_password_hash

    db.session.commit()
    return student

def delete_student_by_id(student_id: int) -> bool:
    """
    Delete a student record by ID if it exists.

    Args:
        student_id (int): The ID of the student to delete.

    Returns:
        bool: True if the student was found and deleted; False if no such student exists.
    """
    student = get_student_by_id(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return True
    return False
