import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.extensions import db
from app.models import Election

def add_election(election: Election) -> Election:
    """
    Save a new Election to the database.

    Args:
        election (Election): Election instance to add

    Returns:
        Election: The persisted Election object
    """
    db.session.add(election)
    db.session.commit()
    return election

def get_election_by_id(election_id: int) -> Election:
    """
    Retrieve an election by its primary key.

    Args:
        election_id (int): Election ID

    Returns:
        Election: Matching Election object or None
    """
    return Election.query.get(election_id)

def list_elections_by_teacher(teacher_id: int) -> list:
    """
    Get all elections created by a specific teacher.

    Args:
        teacher_id (int): The teacher's user ID

    Returns:
        list: List of Election objects
    """
    return Election.query.filter_by(teacher_id=teacher_id).order_by(Election.start_date.desc()).all()

def update_election_status(election_id: int, new_status: str) -> bool:
    """
    Update the status of an election.

    Args:
        election_id (int): ID of the election
        new_status (str): New status value ('running', 'paused', 'finished', etc.)

    Returns:
        bool: True if successful, False otherwise
    """
    election = get_election_by_id(election_id)
    if election:
        election.status = new_status
        db.session.commit()
        return True
    return False

def delete_election(election_id: int) -> bool:
    """
    Delete an election and all its associated data.

    Args:
        election_id (int): ID of the election to delete

    Returns:
        bool: True if deleted successfully, False otherwise
    """
    election = get_election_by_id(election_id)
    if election:
        db.session.delete(election)
        db.session.commit()
        return True
    return False
