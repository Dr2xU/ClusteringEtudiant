import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.extensions import db
from app.models import Teacher

def add_teacher(teacher: Teacher) -> Teacher:
    """
    Persist a new Teacher instance to the database.

    Args:
        teacher (Teacher): A Teacher model instance to be saved.

    Returns:
        Teacher: The saved Teacher instance, now with a database ID.
    """
    db.session.add(teacher)
    db.session.commit()
    return teacher

def get_teacher_by_id(teacher_id: int) -> Teacher:
    """
    Retrieve a teacher record by its primary key ID.

    Args:
        teacher_id (int): The unique identifier of the teacher.

    Returns:
        Teacher: The Teacher object if found; otherwise None.
    """
    return Teacher.query.get(teacher_id)

def get_teacher_by_email(email: str) -> Teacher:
    """
    Retrieve a teacher by their unique email address.

    Args:
        email (str): Email address to query by.

    Returns:
        Teacher: The matching Teacher object if found; otherwise None.
    """
    return Teacher.query.filter_by(email=email).first()

def list_all_teachers() -> list:
    """
    Fetch all teacher records from the database, ordered by creation date descending.

    Returns:
        list: A list of Teacher objects sorted by newest first.
    """
    return Teacher.query.order_by(Teacher.created_at.desc()).all()

def update_teacher(teacher_id: int, first_name: str, last_name: str, department: str) -> Teacher:
    """
    Update basic profile information for a teacher.

    Args:
        teacher_id (int): The ID of the teacher to update.
        first_name (str): New first name.
        last_name (str): New last name.
        department (str): New department.

    Returns:
        Teacher: The updated Teacher object, or None if not found.
    """
    teacher = get_teacher_by_id(teacher_id)
    if not teacher:
        return None

    teacher.first_name = first_name
    teacher.last_name = last_name
    teacher.department = department

    db.session.commit()
    return teacher

def update_teacher_password(teacher_id: int, new_password_hash: str) -> Teacher:
    """
    Update the password hash for a teacher.

    Args:
        teacher_id (int): The ID of the teacher whose password to update.
        new_password_hash (str): The hashed new password.

    Returns:
        Teacher: The updated Teacher object, or None if not found.
    """
    teacher = get_teacher_by_id(teacher_id)
    if not teacher:
        return None

    teacher.password_hash = new_password_hash

    db.session.commit()
    return teacher

def delete_teacher_by_id(teacher_id: int) -> bool:
    """
    Delete a teacher record by ID if it exists.

    Args:
        teacher_id (int): The ID of the teacher to delete.

    Returns:
        bool: True if the teacher was found and deleted; False if no such teacher exists.
    """
    teacher = get_teacher_by_id(teacher_id)
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return True
    return False
