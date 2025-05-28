import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.dao import (
    add_teacher,
    get_teacher_by_email,
    delete_teacher_by_id,
    list_all_teachers,
    get_teacher_by_id,
    update_teacher as dao_update_teacher_profile,
    update_teacher_password as dao_update_teacher_password,
    list_all_elections
)
from app.models import Teacher

def create_teacher(email: str, password: str, first_name: str = "", last_name: str = "", department: str = "", unique_id=None) -> Teacher:
    """
    Creates a new teacher and saves it to the database via DAO.

    Args:
        email (str): Teacher's email
        password (str): Plain-text password
        first_name (str): Optional first name
        last_name (str): Optional last name
        department (str): Optional department info
        unique_id (str): Unique id

    Returns:
        Teacher: The saved Teacher object
    """
    teacher = Teacher(
        email=email,
        first_name=first_name,
        last_name=last_name,
        department=department,
        unique_id=unique_id
    )
    teacher.set_password(password)

    # Delegate DB save to DAO
    return add_teacher(teacher)


def delete_teacher(teacher_id: int) -> bool:
    """
    Delete a teacher by id via DAO.

    Args:
        teacher_id (int): Teacher ID

    Returns:
        bool: True if deleted, False otherwise
    """
    return delete_teacher_by_id(teacher_id)

def update_teacher_profile(teacher_id: int, first_name: str, last_name: str, department: str) -> Teacher:
    """
    Update a teacher's profile details via DAO.

    Args:
        teacher_id (int): The teacher's ID
        first_name (str): New first name
        last_name (str): New last name
        department (str): New department name

    Returns:
        Teacher: Updated Teacher object or None if not found
    """
    return dao_update_teacher_profile(teacher_id, first_name, last_name, department)

def update_teacher_password(teacher_id: int, new_password: str) -> Teacher:
    """
    Update a teacher's password securely via DAO.

    Args:
        teacher_id (int): The teacher's ID
        new_password (str): The new plain-text password to hash and store

    Returns:
        Teacher: Updated Teacher object or None if not found
    """
    teacher = get_teacher_by_id(teacher_id)
    if not teacher:
        return None
    teacher.set_password(new_password)
    return dao_update_teacher_password(teacher_id, teacher.password_hash)

def get_teacher_by_email_service(email: str) -> Teacher:
    """
    Retrieve a teacher by email via DAO.

    Args:
        email (str): Teacher's email

    Returns:
        Teacher or None
    """
    return get_teacher_by_email(email)

def authenticate_teacher(email: str, password: str) -> Teacher:
    """
    Authenticate teacher by email and password.

    Args:
        email (str): Teacher's email
        password (str): Plain-text password

    Returns:
        Teacher or None
    """
    teacher = get_teacher_by_email(email)
    if teacher and teacher.check_password(password):
        return teacher
    return None

def list_all_teachers_service() -> list:
    """
    List all teachers via DAO.

    Returns:
        list of Teacher
    """
    return list_all_teachers()

def list_all_elections_service(teacher_id: int) -> list:
    """
    List all elections created by a specific teacher via DAO.

    Args:
        teacher_id (int): The ID of the teacher

    Returns:
        list of Election objects associated with the teacher
    """
    return list_all_elections(teacher_id)