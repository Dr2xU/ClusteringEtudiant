import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.dao.election_dao import (
    add_election,
    get_election_by_id,
    list_elections_by_teacher,
    update_election_status,
    delete_election
)
from app.extensions import db
from datetime import datetime
from typing import Optional, List
from app.models import Election

def create_election(
    title: str,
    start_date: datetime,
    end_date: datetime,
    teacher_id: int,
    max_votes_per_student: int = 3,
    students_per_group: int = 3,
    description: str = "",
    student_ids: Optional[List[int]] = None
) -> Election:
    """
    Create a new election and save it via DAO.

    Args:
        title (str): Election title
        start_date (datetime): Start datetime
        end_date (datetime): End datetime
        teacher_id (int): Teacher who created election
        max_votes_per_student (int): Max votes per student
        students_per_group (int): Group size
        description (str): Optional description
        student_ids (list[int], optional): Students to associate with election

    Returns:
        Election: Created Election object
    """
    election = Election(
        title=title,
        start_date=start_date,
        end_date=end_date,
        teacher_id=teacher_id,
        max_votes_per_student=max_votes_per_student,
        students_per_group=students_per_group,
        description=description,
        status='running'
    )

    # Save the election first
    saved_election = add_election(election)

    if student_ids:
        from app.models import Student
        students = Student.query.filter(Student.id.in_(student_ids)).all()
        saved_election.students.extend(students)  # requires relationship set up
        # Commit changes after association
        from app.extensions import db
        db.session.commit()

    return saved_election

def get_election_by_id(election_id: int) -> Election:
    """
    Fetch an election by its ID.

    Args:
        election_id (int): The election's unique identifier

    Returns:
        Election: The matching Election object or None
    """
    return Election.query.get(election_id)

def list_elections_by_teacher(teacher_id: int) -> list:
    """
    Retrieve all elections created by a specific teacher.

    Args:
        teacher_id (int): The teacher's user ID

    Returns:
        list: A list of Election objects
    """
    return Election.query.filter_by(teacher_id=teacher_id).order_by(Election.start_date.desc()).all()

def update_election_status(election_id: int, status: str) -> bool:
    """
    Change the status of an election (e.g., 'running', 'paused', 'finished').

    Args:
        election_id (int): The ID of the election to update
        status (str): New status string

    Returns:
        bool: True if the update succeeded, False otherwise
    """
    election = get_election_by_id(election_id)
    if election:
        election.status = status
        db.session.commit()
        return True
    return False

def delete_election(election_id: int) -> bool:
    """
    Delete an election by ID.

    Args:
        election_id (int): ID of the election to delete

    Returns:
        bool: True if successfully deleted, False if not found
    """
    election = get_election_by_id(election_id)
    if election:
        db.session.delete(election)
        db.session.commit()
        return True
    return False
