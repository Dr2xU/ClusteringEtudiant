import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.dao import (
    add_student,
    get_student_by_email,
    delete_student_by_id,
    list_all_students,
    get_student_by_id,
    update_student,          # DAO function to commit student updates
    update_student_password  # DAO function to commit password updates
)
from app.models import Student

def create_student(email: str, password: str, first_name: str = "", last_name: str = "", class_name: str = "", section: str = "", unique_id=None) -> Student:
    """
    Create a new student instance, hash password, and save via DAO.

    Args:
        email (str): Student's email address
        password (str): Plain-text password
        first_name (str): Optional first name
        last_name (str): Optional last name
        class_name (str): Optional class name
        section (str): Optional section info
        unique_id (str): Unique student ID

    Returns:
        Student: Persisted student object
    """
    student = Student(
        email=email,
        first_name=first_name,
        last_name=last_name,
        class_name=class_name,
        section=section,
        unique_id=unique_id
    )
    student.set_password(password)  # Hash password securely before saving

    return add_student(student)  # Delegate database save operation to DAO

def create_student_with_id(unique_id, email, password, first_name="", last_name="", class_name="", section=""):
    """
    Create a new student instance, hash password, and save via DAO. (Used for testing)
    
    Args:
        email (str): Student's email address
        password (str): Plain-text password
        first_name (str): Optional first name
        last_name (str): Optional last name
        class_name (str): Optional class name
        section (str): Optional section info
        
    Returns:
        Student: Persisted student object with a unique ID
    """
    unique_id = unique_id
    student = Student(
        email=email,
        first_name=first_name,
        last_name=last_name,
        class_name=class_name,
        section=section,
        unique_id=unique_id
    )
    student.set_password(password)
    return add_student(student)

def update_student_profile(student_id: int, first_name: str, last_name: str, class_name: str, section: str) -> Student:
    """
    Update the profile fields of an existing student via DAO.

    Args:
        student_id (int): ID of student to update
        first_name (str): New first name
        last_name (str): New last name
        class_name (str): New class name
        section (str): New section

    Returns:
        Student: Updated student object or None if not found
    """
    student = get_student_by_id(student_id)
    if student:
        student.first_name = first_name
        student.last_name = last_name
        student.class_name = class_name
        student.section = section
        return update_student(student)  # Delegate commit to DAO
    return None

def update_student_password(student_id: int, new_password: str) -> Student:
    """
    Update the password for a student.

    Args:
        student_id (int): Student's ID
        new_password (str): New plain-text password

    Returns:
        Student: Updated student object or None if not found
    """
    student = get_student_by_id(student_id)
    if student:
        student.set_password(new_password)  # Hash new password
        return update_student_password(student)  # Delegate commit to DAO
    return None

def delete_student(student_id: int) -> bool:
    """
    Delete a student by ID.

    Args:
        student_id (int): Student's ID to delete

    Returns:
        bool: True if deletion succeeded, False otherwise
    """
    return delete_student_by_id(student_id)  # DAO handles deletion and commit

def get_student_by_email_service(email: str) -> Student:
    """
    Fetch a student by email.

    Args:
        email (str): Email to search for

    Returns:
        Student or None
    """
    return get_student_by_email(email)  # DAO handles retrieval

def authenticate_student(email: str, password: str) -> Student:
    """
    Authenticate a student with email and password.

    Args:
        email (str): Student email
        password (str): Plain-text password

    Returns:
        Student if authenticated, else None
    """
    student = get_student_by_email(email)
    if student and student.check_password(password):
        return student
    return None

def list_all_students_service() -> list:
    """
    Retrieve all students.

    Returns:
        List[Student]: List of all student records
    """
    return list_all_students()  # Delegate to DAO